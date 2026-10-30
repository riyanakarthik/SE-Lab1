# Lab 5: Static Code Analysis Report

**File analysed:** `employee_payroll_system.py`
**Tools:** Pylint, Bandit, Flake8

## Results summary

| Tool | Before | After |
|---|---|---|
| Pylint | 5.53/10 (20 messages) | 10.00/10 |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 6 issues (+ W292 missing final newline) | 0 issues |

Reports are in `reports/before/` and `reports/after/`.

## Issue table

Line numbers refer to the original file. Ordered by severity, security first.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| `os.system("echo ..." + filename)` (Bandit B605) | Security, High | 58 | Shell command built from a variable allows command injection | Removed the shell call and used `print()` |
| MD5 hash (Bandit B324) | Security, High | 47 | MD5 is cryptographically broken | Switched to `hashlib.sha256` |
| `eval(deduction_expr)` (Bandit B307, Pylint W0123) | Security, Medium | 42 | Runs arbitrary code passed in as a string | `compute_net_salary` now takes a numeric `deduction_rate`, validated to 0 to 1 |
| `random.randint` for a token (Bandit B311) | Security, Low | 51 | The `random` module is predictable | Used `secrets.randbelow` |
| `except: pass` (Bandit B110, Flake8 E722, Pylint W0702) | Security / Bug, Low | 26 | Swallows every error, so unknown IDs fail silently | Explicit validation; function returns True or False |
| Hardcoded secret `payroll_key` | Security (no tool flagged it) | 62, 70 | Secret stored in source code and printed to the console | Read from the `PAYROLL_MASTER_KEY` environment variable; print only whether it is loaded |
| Mutable default `transaction_logs=[]` (Pylint W0102) | Bug | 15 | The same list is shared across every call | Default `None`, create a new list inside the function |
| Penalty can make salary negative | Logic bug (no tool flagged it) | 23 to 27 | No validation of the penalty amount | Reject negative penalties and penalties larger than salary |
| Unused import `math` (Flake8 F401, Pylint W0611) | Style | 6 | Dead import | Removed |
| Unused variables `statutory_buffer`, `base` (F841, W0612) | Style | 31, 41 | Assigned but never used | Removed `statutory_buffer`; `base` is now used in the return |
| `== None` (Flake8 E711, Pylint C0121) | Style | 32 | Should compare identity | `is None` |
| Line too long (Flake8 E501) | Style | 19 | 84 > 79 characters | Wrapped the line |
| No newline at end of file (Flake8 W292) | Style | 73 | File does not end with a newline | Added |
| `processSalary` naming (Pylint C0103) | Style | 15 | Not snake_case | Renamed `process_salary` |
| Missing docstrings (Pylint C0116) | Style | 15, 23, 30, 40, 46, 50, 54, 61 | Functions undocumented | Added docstrings |
| Redundant if/else (Pylint R1703, R1705) | Style | 34 | Could return the comparison directly | `return ... >= min_base` |
| `open()` without `with` or encoding (Pylint R1732, W1514) | Style | 55 | File may not close on error, encoding unspecified | `with open(..., encoding="utf-8")` |
| `%d` string formatting (Pylint C0209) | Style / Bug | 19 | Old-style formatting; `%d` truncates a bonus like 350.75 to 350 in the log | f-string with `:.2f` |
| `main()` runs on import | Style | 73 | Module executes when imported | Added `if __name__ == "__main__":` |

## Observations not caught by tools

- The net salary uses a hardcoded 0.15 rather than each employee's own `tax_rate` from `payroll_records`. It was left as is so the output is unchanged.
- `statutory_buffer = 150.0` in `check_bonus_eligibility` was never used, so its intended purpose is unclear.
- The handout says the program asks one question, but this script has no `input()` call.

## Reflection

*(Add answers to the handout's reflection questions here.)*
