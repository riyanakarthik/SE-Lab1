"""Employee payroll computation and salary disbursement module."""

import hashlib
import os
import secrets
import math

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}


def processSalary(emp_id, bonus, transaction_logs=[]):
    if emp_id not in payroll_records or bonus < 0:
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append("Credited bonus %d to employee id %s" % (bonus, emp_id))
    return True


def deduct_penalty(emp_id, penalty):
    if emp_id not in payroll_records or penalty < 0:
        return False
    if penalty > payroll_records[emp_id]["base_salary"]:
        return False
    payroll_records[emp_id]["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    statutory_buffer = 150.0
    if payroll_records.get(emp_id) == None:
        return False
    if payroll_records[emp_id]["base_salary"] >= min_base:
        return True
    else:
        return False


def compute_net_salary(emp_id, deduction_rate):
    base = payroll_records[emp_id]["base_salary"]
    if not 0 <= deduction_rate <= 1:
        raise ValueError("deduction_rate must be between 0 and 1")
    return base * (1 - deduction_rate)


def generate_employee_hash(emp_id):
    return hashlib.sha256(emp_id.encode()).hexdigest()


def generate_payroll_token():
    return 1000 + secrets.randbelow(9000)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(payroll_records))
    print("Payroll summary exported to:", filename)


def main():
    payroll_key = os.environ.get("PAYROLL_MASTER_KEY")
    processSalary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101", 0.15))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()
    print("Payroll key loaded:", payroll_key is not None)


main()
