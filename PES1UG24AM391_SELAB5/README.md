# Lab 5: Static Code Analysis (PES1UG24AM391)

**Student Name:** Raghunandan Kotary  
**SRN:** PES1UG24AM391  
**Course:** Software Engineering Lab (SE Lab)  
**Assigned Repository:** SETAPESU26/L5_29_digital_wallet  

---

## Overview
This laboratory applies static code analysis tools (**Bandit**, **Pylint**, and **Flake8**) to systematically detect, classify, and fix security vulnerabilities, code smells, bad practices, and PEP 8 style violations in digital_wallet.py.

## Summary of Results
| Tool | Baseline Metric | Post-Fix Metric | Status |
| :--- | :--- | :--- | :--- |
| **Bandit** | 4 issues (1 High, 1 Med, 2 Low) | **0 issues** (No issues identified) | Passed |
| **Pylint** | 5.69 / 10 (25 notices) | **10.00 / 10** (0 warnings) | Passed |
| **Flake8** | 4 errors (E261, E225, E231, E305) | **0 errors** (PEP 8 compliant) | Passed |

## Deliverables in this Directory
- digital_wallet.py: Hardened, fully documented, and PEP 8 compliant source code.
- issues.md: Detailed issue tracking table documenting 16 findings, severities, lines, and fix strategies.
- 
eflection.md: Comprehensive responses to all 4 laboratory reflection questions.
- 
eports/: Raw command line output before and after applying fixes for Bandit, Pylint, and Flake8.
- screenshots/: Terminal execution capture screenshots for each tool.
- PES1UG24AM391_SELAB5.pdf: Complete submission PDF report formatted according to laboratory rubrics.
