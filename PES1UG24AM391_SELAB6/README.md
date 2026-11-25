# PES1UG24AM391 — Software Engineering Lab 6: Code and Branch Coverage

**Student Name**: Raghunandan Kotary  
**SRN**: PES1UG24AM391  
**Course**: UE23CS351A — Software Engineering Lab  
**Module Under Test**: `blood_donation_screening.py` (`L6_L7_05_blood_donation_screening`)

---

## Deliverables Summary

| Deliverable | File Name | Metric Achieved |
|-------------|-----------|-----------------|
| **Final Lab Report** | `PES1UG24AM391_SELAB6.pdf` | Complete 5-page report with analysis, matrices, and screenshots |
| **Code Coverage Test Suite** | `CodeCoverageTest_blood_donation_screening_application.py` | **100% Statement Coverage** (45/45 stmts) |
| **Branch Coverage Test Suite** | `BranchCoverageTest_blood_donation_screening_application.py` | **100% Branch Coverage** (32/32 branches) |
| **Application Module** | `blood_donation_screening.py` | Module Under Test |
| **Starter Test Suite** | `test_blood_donation.py` | Baseline starter suite (47% line, 43% branch) |
| **Code Coverage Screenshot** | `code_coverage.png` | Terminal screenshot (>90% requirement) |
| **Branch Coverage Screenshot** | `branch_coverage.png` | Terminal screenshot (>90% requirement) |
| **Baseline Coverage Screenshot** | `initial_coverage.png` | Baseline starter screenshot |

---

## Execution Commands

### 1. Code (Line) Coverage Run:
```powershell
coverage run -m pytest CodeCoverageTest_blood_donation_screening_application.py
coverage report -m blood_donation_screening.py
```
**Output**: 100% statement coverage (45/45 executed, 16 passed in 0.06s).

### 2. Branch Coverage Run:
```powershell
coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening_application.py
coverage report -m blood_donation_screening.py
```
**Output**: 100% branch coverage (32/32 branches, 0 partial, 23 passed in 0.08s).
