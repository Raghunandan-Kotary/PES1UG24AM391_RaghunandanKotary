import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

# ==============================================================================
# Tests for process_donor_cohort - Code Coverage Suite
# ==============================================================================

def test_invalid_cohorts_type_raises_value_error():
    """Trigger ValueError when cohorts is not a list."""
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort("not-a-list", 450)

def test_invalid_standard_volume_raises_value_error():
    """Trigger ValueError when standard volume is zero or negative."""
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort([], 0)
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort([], -100)

def test_empty_cohorts_yields_zero():
    """Empty cohort list returns ZERO_YIELD."""
    result = process_donor_cohort([], 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"

def test_unregistered_clinic_skipped():
    """Cohorts that are not clinic registered are skipped."""
    cohorts = [
        {
            "clinic_registered": False,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 25, "weight_kg": 70, "hb": 14.5}]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"

def test_single_accepted_donor():
    """Standard cohort with a single valid donor."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"

def test_donor_underage_deferred():
    """Donor below 17 is deferred."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 16, "weight_kg": 60, "hb": 14.0}]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"

def test_donor_underweight_deferred():
    """Donor below 50 kg is deferred."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 20, "weight_kg": 48, "hb": 14.0}]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"

def test_donor_low_hemoglobin_standard_cohort():
    """Low hemoglobin in standard cohort increments deferred_count."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [
                {"age": 30, "weight_kg": 70, "hb": 11.5},
                {"age": 28, "weight_kg": 68, "hb": 14.0}
            ]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"

def test_donor_low_hemoglobin_high_altitude_resets_and_breaks():
    """Low hemoglobin in high_altitude cohort resets volume to 0 and breaks."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "high_altitude",
            "fast_track": False,
            "donors": [
                {"age": 30, "weight_kg": 75, "hb": 15.0},
                {"age": 25, "weight_kg": 60, "hb": 12.0},
                {"age": 40, "weight_kg": 80, "hb": 14.5}
            ]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"

def test_donor_high_hemoglobin_deferred():
    """Hemoglobin above 18.0 causes deferral."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 35, "weight_kg": 75, "hb": 18.5}]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"

def test_fast_track_cohort_adds_bonus_volume():
    """Fast-track adds 50ml bonus volume."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": True,
            "donors": [{"age": 22, "weight_kg": 60, "hb": 13.5}]
        }
    ]
    result = process_donor_cohort(cohorts, 400)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"

def test_high_deferral_status():
    """More than 4 deferrals marks cohort as HIGH_DEFERRAL."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [
                {"age": 15, "weight_kg": 40, "hb": 14.0}, # 1
                {"age": 16, "weight_kg": 45, "hb": 14.0}, # 2
                {"age": 25, "weight_kg": 45, "hb": 14.0}, # 3
                {"age": 30, "weight_kg": 70, "hb": 10.0}, # 4
                {"age": 40, "weight_kg": 80, "hb": 19.0}, # 5
                {"age": 25, "weight_kg": 65, "hb": 14.0}  # 1 accepted
            ]
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "HIGH_DEFERRAL"


# ==============================================================================
# Tests for verify_storage_centrifuge - Code Coverage Suite
# ==============================================================================

def test_centrifuge_no_data():
    """Empty or None runs return NO_DATA."""
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge(None) == "NO_DATA"

def test_centrifuge_stable():
    """All RPMs at or above 3000 result in STABLE status."""
    runs = [[3200, 3100, 3300, 3050]]
    assert verify_storage_centrifuge(runs) == "STABLE"

def test_centrifuge_single_drop_recovers():
    """Single RPM drop below 3000 followed by normal speed resets streak and stays STABLE."""
    runs = [[3200, 2900, 3100, 3200]]
    assert verify_storage_centrifuge(runs) == "STABLE"

def test_centrifuge_abort_spin_consecutive_drops():
    """Two consecutive RPM drops below 3000 trigger ABORT_SPIN."""
    runs = [[3200, 2800, 2700, 3200]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"
