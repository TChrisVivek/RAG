from app.services.tools import get_employee_info

def test_vaild_employee():
    result = get_employee_info("EMP001")


    assert result["success"] is True
    assert result["name"] == "Alex"
    assert result["department"] == "Engineering"


def test_lowercase_employee_id():
    result = get_employee_info("emp001")

    assert result["success"] is True
    assert result["employee_id"] == "EMP001"


def test_unkown_employee():
    result = get_employee_info("EMP999")

    assert result["success"] is False
    assert result["error"] == "Employee not found."


def test_empty_employee_id():
    result = get_employee_info("")

    assert result["success"] is False
    assert result["error"] == "An employee ID is required."