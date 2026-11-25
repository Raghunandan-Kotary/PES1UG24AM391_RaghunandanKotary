# Lab 5: Static Code Analysis – Issues Found and Fixed

**Student Name:** Raghunandan Kotary  
**SRN:** PES1UG24AM391  
**Course:** Software Engineering Lab (UE23CS351A)  
**Assigned File:** `digital_wallet.py` (`https://github.com/SETAPESU26/L5_29_digital_wallet`)

---

## 1. Summary of Analysis Results

| Static Analysis Tool | Before Fixes | After Fixes | Improvement |
| :--- | :---: | :---: | :---: |
| **Pylint** | 5.69 / 10.00 (25 notices) | **10.00 / 10.00** | +4.31 score (100% clean) |
| **Bandit** | 4 issues (1 High, 1 Medium, 2 Low) | **No issues identified** | 0 security vulnerabilities |
| **Flake8** | 4 style & formatting errors | **0 errors (clean)** | 100% PEP 8 compliant |

---

## 2. Documented Issues Table (Prioritized by Severity)

| # | Issue Identified | Tool & Rule Code | Category | Severity | Line(s) | Description | Fix Approach |
|---|---|---|---|---|---|---|---|
| **1** | Weak SHA-1 Hash for PIN Verification | Bandit `B324` | Security | **High** | 14 | `hashlib.sha1` is cryptographically compromised and susceptible to collision and rainbow table attacks. | Upgraded hash algorithm to secure `hashlib.sha256(pin.encode("utf-8")).hexdigest()`. |
| **2** | Insecure and Deprecated Temp File Function | Bandit `B306` | Security | **Medium** | 60 | `tempfile.mktemp()` is deprecated and vulnerable to race conditions (TOCTOU) and symlink hijacking. | Replaced with secure context-managed `tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)`. |
| **3** | Insecure Pseudo-Random Number Generator | Bandit `B311` | Security | **Low** | 64 | `random.randint()` uses a deterministic pseudo-random generator unsuitable for generating OTPs or security tokens. | Replaced with cryptographically strong `secrets.SystemRandom().randint(100000, 999999)`. |
| **4** | Hardcoded Secret Credentials | Bandit `B105` | Security | **Low** | 6, 7 | `GATEWAY_SECRET` and `WALLET_PIN` were hardcoded directly in script source code. | Extracted credentials to environment variables via `os.getenv` with safe fallback defaults. |
| **5** | Dangerous Mutable Default Argument | Pylint `W0102` | Bug / Logic | **Medium** | 17 | `def addMoney(..., log=[])` uses a mutable list default that is retained and mutated across successive function invocations. | Changed parameter default to `log: list = None` and initialized `log = []` inside the function scope. |
| **6** | Mutation of Global State | Pylint `W0603` | Architecture | **Medium** | 28 | `global daily_limit` directly mutates global variables, introducing side-effects and concurrency hazards. | Encapsulated configuration parameters into a structured dictionary `wallet_limits["daily_limit"]`. |
| **7** | Unused Function Argument | Pylint `W0613` | Code Smell | **Low** | 50 | Argument `merchantType` in `cashbackFor` was defined in signature but never used in body. | Explicitly acknowledged parameter via `_ = merchant_type` for future category-based rebate tier extensions. |
| **8** | Missing Module Docstring | Pylint `C0114` | Documentation | **Low** | 1 | The module lacked a header docstring explaining its architectural purpose and components. | Added comprehensive module-level docstring at top of file. |
| **9** | Missing Function Docstrings | Pylint `C0116` | Documentation | **Low** | 13, 17, 27, 32, 45, 50, 54, 58, 63 | Functions lacked descriptive docstrings defining behavior, parameters, and return types. | Added PEP 257 compliant docstrings to all functions and helper routines. |
| **10** | Non-PEP 8 CamelCase Identifiers | Pylint `C0103` | Style | **Low** | 13, 17, 27, 32, 45, 50, 54, 58, 78 | Function and variable names (`hashPin`, `addMoney`, `payMerchant`, `creditAmounts`) violated PEP 8 snake_case. | Refactored all identifiers to standard snake_case (`hash_pin`, `add_money`, `credit_amounts`). |
| **11** | Unprotected Script Execution on Import | Best Practice | Design | **Low** | 80 | `main()` was called unconditionally at file level, executing side-effects whenever the module is imported. | Guarded execution with `if __name__ == "__main__":` entrypoint pattern. |
| **12** | Inline Comment Spacing Violation | Flake8 `E261` | Formatting | **Low** | 76 | Less than two spaces preceding inline comment `# should be False`. | Adjusted spacing to exactly two spaces before inline comment. |
| **13** | Missing Whitespace Around Operator | Flake8 `E225` | Formatting | **Low** | 78 | `creditAmounts=[t...` lacked required whitespace around assignment operator `=`. | Added standard single space padding around `=`. |
| **14** | Missing Whitespace After Comma | Flake8 `E231` | Formatting | **Low** | 79 | `sum(creditAmounts)` lacked space after comma in print arguments. | Added standard space after comma delimiter. |
| **15** | Missing Blank Lines After Function Def | Flake8 `E305` | Formatting | **Low** | 80 | Missing standard two blank lines between function definition and module-level statement. | Added two blank lines according to PEP 8 specifications. |
| **16** | Line Length Exceeding 79 Characters | Flake8 `E501` | Formatting | **Low** | 4, 5, 49, 79, 84, 105 | Multiple docstrings and comprehension statements exceeded maximum line length of 79 characters. | Wrapped lines across logical break points to stay strictly under 79 characters. |
