import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

# ==============================================================================
# Branch Coverage Suite: process_donor_cohort
# ==============================================================================

# 1. Guard clause: not isinstance(cohorts, list) or standard_volume_ml <= 0
def test_guard_cohorts_not_list():
    """Branch: not isinstance(cohorts, list) is True"""
    with pytest.raises(ValueError):
        process_donor_cohort("invalid_string", 450)
    with pytest.raises(ValueError):
        process_donor_cohort(None, 450)
    with pytest.raises(ValueError):
        process_donor_cohort({"key": "dict"}, 450)

def test_guard_standard_volume_zero_or_negative():
    """Branch: standard_volume_ml <= 0 is True"""
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)
    with pytest.raises(ValueError):
        process_donor_cohort([], -50)

def test_guard_valid_inputs_empty_cohorts():
    """Branch: both guard checks False -> empty cohorts loop -> ZERO_YIELD"""
    result = process_donor_cohort([], 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


# 2. Clinic registration branch
def test_unregistered_cohort_branch():
    """Branch: not cohort.get('clinic_registered', False) is True -> continue"""
    cohorts = [
        {"clinic_registered": False, "donors": [{"age": 25, "weight_kg": 60, "hb": 14.0}]},
        {"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 60, "hb": 14.0}]}
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


# 3. Age and weight decision branches
def test_age_below_17_boundary():
    """Branch: age < 17 is True (age = 16) -> deferred"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 16, "weight_kg": 60, "hb": 14.0}]}]
    assert process_donor_cohort(cohort, 450)["status"] == "ZERO_YIELD"

def test_age_at_17_boundary():
    """Branch: age == 17 is False (< 17) -> eligible if weight >= 50"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 17, "weight_kg": 50, "hb": 14.0}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "ACCEPTED"

def test_weight_below_50_boundary():
    """Branch: weight < 50 is True (weight = 49.9) -> deferred"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 49.9, "hb": 14.0}]}]
    assert process_donor_cohort(cohort, 450)["status"] == "ZERO_YIELD"

def test_weight_at_50_boundary():
    """Branch: weight == 50 is False (< 50) -> eligible"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 20, "weight_kg": 50, "hb": 13.0}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "ACCEPTED"


# 4. Hemoglobin decision branches (hb < 12.5, hb > 18.0, 12.5 <= hb <= 18.0)
def test_hb_below_12_5_standard_cohort():
    """Branch: hb < 12.5 in standard cohort -> deferred, does not break loop"""
    cohort = [{
        "clinic_registered": True,
        "type": "standard",
        "donors": [
            {"age": 25, "weight_kg": 60, "hb": 12.4}, # deferred
            {"age": 25, "weight_kg": 60, "hb": 14.0}  # accepted
        ]
    }]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "ACCEPTED"

def test_hb_below_12_5_high_altitude_resets_and_breaks():
    """Branch: hb < 12.5 and cohort_type == 'high_altitude' -> total_collected_ml = 0 and break"""
    cohort = [{
        "clinic_registered": True,
        "type": "high_altitude",
        "donors": [
            {"age": 30, "weight_kg": 70, "hb": 14.0}, # +450
            {"age": 25, "weight_kg": 60, "hb": 12.0}, # triggers reset to 0 and break
            {"age": 40, "weight_kg": 80, "hb": 15.0}  # never executed due to break
        ]
    }]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 0
    assert res["status"] == "ZERO_YIELD"

def test_hb_at_12_5_boundary():
    """Branch: hb == 12.5 is False (< 12.5) -> accepted"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 60, "hb": 12.5}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "ACCEPTED"

def test_hb_at_18_0_boundary():
    """Branch: hb == 18.0 is False (> 18.0) -> accepted"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 60, "hb": 18.0}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "ACCEPTED"

def test_hb_above_18_0_deferred():
    """Branch: hb > 18.0 (18.1) is True -> deferred_count += 1, continue"""
    cohort = [{"clinic_registered": True, "donors": [{"age": 25, "weight_kg": 60, "hb": 18.1}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 0
    assert res["status"] == "ZERO_YIELD"


# 5. Fast-track bonus branch
def test_fast_track_true():
    """Branch: cohort.get('fast_track', False) is True -> +50ml bonus"""
    cohort = [{"clinic_registered": True, "fast_track": True, "donors": [{"age": 25, "weight_kg": 60, "hb": 14.0}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 500
    assert res["status"] == "ACCEPTED"

def test_fast_track_false():
    """Branch: cohort.get('fast_track', False) is False -> no bonus"""
    cohort = [{"clinic_registered": True, "fast_track": False, "donors": [{"age": 25, "weight_kg": 60, "hb": 14.0}]}]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450


# 6. Deferral count threshold branches (deferred_count > 4)
def test_exactly_4_deferrals_not_high_deferral():
    """Branch: deferred_count == 4 is False (> 4) -> ACCEPTED"""
    cohort = [{
        "clinic_registered": True,
        "donors": [
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 1
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 2
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 3
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 4
            {"age": 25, "weight_kg": 60, "hb": 14.0}  # accepted
        ]
    }]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "ACCEPTED"

def test_more_than_4_deferrals_high_deferral():
    """Branch: deferred_count > 4 is True (count = 5) -> HIGH_DEFERRAL"""
    cohort = [{
        "clinic_registered": True,
        "donors": [
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 1
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 2
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 3
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 4
            {"age": 16, "weight_kg": 60, "hb": 14.0}, # 5
            {"age": 25, "weight_kg": 60, "hb": 14.0}  # accepted
        ]
    }]
    res = process_donor_cohort(cohort, 450)
    assert res["collected_ml"] == 450
    assert res["status"] == "HIGH_DEFERRAL"


# ==============================================================================
# Branch Coverage Suite: verify_storage_centrifuge
# ==============================================================================

def test_centrifuge_empty_or_none():
    """Branch: not centrifuge_runs is True"""
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge(None) == "NO_DATA"

def test_centrifuge_all_stable():
    """Branch: all rpm >= 3000 -> STABLE"""
    runs = [[3000, 3100, 3500]]
    assert verify_storage_centrifuge(runs) == "STABLE"

def test_centrifuge_rpm_at_3000_boundary():
    """Branch: rpm == 3000 is False (< 3000) -> resets drop streak"""
    runs = [[2999, 3000, 2999]]
    # 2999 -> streak 1
    # 3000 -> streak reset to 0
    # 2999 -> streak 1
    assert verify_storage_centrifuge(runs) == "STABLE"

def test_centrifuge_abort_spin_consecutive_drops():
    """Branch: rpm_drop_streak >= 2 is True -> ABORT_SPIN"""
    runs = [[2999, 2998]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"

def test_centrifuge_multiple_runs_aborts_in_later_run():
    """Branch: first run passes, second run aborts"""
    runs = [
        [3200, 3100, 3050],
        [3200, 2800, 2700]
    ]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"

def test_centrifuge_empty_inner_run():
    """Branch: run with empty reading list completes cleanly -> STABLE"""
    runs = [[]]
    assert verify_storage_centrifuge(runs) == "STABLE"
