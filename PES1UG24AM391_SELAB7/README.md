# PES1UG24AM391 — Software Engineering Lab 7: Fuzzing for Input Validation Bugs

**Student Name**: Raghunandan Kotary  
**SRN**: PES1UG24AM391  
**Course**: UE23CS351A — Software Engineering Lab  
**Module Under Test**: `processor.py` (`L6_L7_05_blood_donation_screening`)  
**Testing Tool**: Hypothesis Property-Based Fuzz Testing + Pytest

---

## Deliverables Summary

| Deliverable | File Name | Description |
|-------------|-----------|-------------|
| **Final Lab Report** | `PES1UG24AM391_SELAB7.pdf` | Comprehensive 5-page report with screenshots & analysis |
| **Fixed Application** | `processor.py` | Defensively hardened module against nulls, type errors & zero-division |
| **Updated Test Suite** | `test_processor.py` | Property-based fuzz tests using `@given(st.text() \| st.none())` |
| **Step 2 Screenshot** | `step2_run_buggy.png` | Terminal execution of initial buggy `processor.py` |
| **Step 4 Screenshot** | `step4_test_failing.png` | Hypothesis test failures uncovering crashes |
| **Step 5 Screenshot** | `step5_run_fixed.png` | Execution of defensively hardened `processor.py` |
| **Step 6 Screenshot** | `step6_test_passing.png` | Re-running Hypothesis tests on fixed code (all passed) |

---

## Execution Steps

### 1. Run the initial buggy application:
```powershell
python processor.py
```

### 2. Run the property-based fuzz test suite (uncovering bugs):
```powershell
pytest test_processor.py
```

### 3. Run the fixed, hardened application:
```powershell
python processor.py
```

### 4. Re-run fuzz tests to verify robustness (all tests pass):
```powershell
pytest test_processor.py
```
