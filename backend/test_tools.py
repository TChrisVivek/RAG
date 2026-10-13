from app.services.tools import (
    search_hr_policy,
    get_employee_info
)


print("TEST 1: Valid employee")
print(get_employee_info("EMP001"))


print("\nTEST 2: Lowercase employee ID")
print(get_employee_info("emp001"))


print("\nTEST 3: Unknown employee ")
print(get_employee_info("EMP999"))

print("\nTEST 4: Empty employee ID")
print(get_employee_info(""))

print("\nTEST 5: HR policy search")
print(search_hr_policy(
    "how many days of paternity leave are provided?"
))

print("\nTEST 6: Empty policy question")
print(search_hr_policy(""))

