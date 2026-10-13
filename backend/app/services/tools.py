
import logging
from app.services.vector_store import search_chunks


# Configure logging for this module.
logger = logging.getLogger(__name__)


# TOOL 1: Search the company's HR policy documents.
def search_hr_policy(question: str):
    """
    Search company HR policies for information
    relevant to the employee's question.
    """

    # Log that a policy search was requested.
    logger.info("HR policy search requested.")

    # Validate the question before searching.
    if not question or not question.strip():
        logger.warning("Policy search rejected: empty question.")

        return {
            "success": False,
            "error": "The policy question cannot be empty.",
            "results": []
        }

    try:
        # Search for the three closest policy chunks.
        results = search_chunks(
            query=question.strip(),
            top_k=3
        )

        # Log how many chunks passed the search filter.
        logger.info(
            "HR policy search returned %d relevant chunks.",
            len(results)
        )

        # Handle a search that found no relevant chunks.
        if not results:
            logger.warning(
                "No relevant policy information was found."
            )

            return {
                "success": True,
                "found": False,
                "message": "No relevant policy information was found.",
                "results": []
            }

        # Return the retrieved policy information.
        return {
            "success": True,
            "found": True,
            "results": results
        }

    except Exception:
        # Record the technical error in the server logs.
        logger.exception("HR policy search failed.")

        # Return a safe message to the calling agent.
        return {
            "success": False,
            "error": "The HR policy search failed.",
            "results": []
        }



# TOOL 2: Retrieve employee information from dummy data.
def get_employee_info(employee_id: str):
    """
    Retrieve basic employee information.
    Uses fictional data for testing.
    """

    # Log that an employee lookup was requested.
    logger.info("Employee lookup requested.")

    employees = {
        "EMP001": {
            "name": "Alex",
            "department": "Engineering",
            "job_title": "Software Developer",
            "leave_balance": 8
        },
        "EMP002": {
            "name": "Sam",
            "department": "Human Resources",
            "job_title": "HR Manager",
            "leave_balance": 12
        },
        "EMP003": {
            "name": "Jordan",
            "department": "Marketing",
            "job_title": "Marketing Associate",
            "leave_balance": 5
        }
    }

    # Reject an empty employee ID.
    if not employee_id or not employee_id.strip():
        logger.warning("employee lookup rejected: empty employee ID.")
        return {
            "success": False,
            "error": "An employee ID is required."
        }
    

    # Allow IDs such as "emp001" and " EMP001 ".
    normalized_id = employee_id.strip().upper()

    employee = employees.get(normalized_id)

    # Return a clear error for an unknown employee.
    if employee is None:
        logger.warning("Employee lookup failed: iD not found.")

        return {
            "success": False,
            "error": "Employee not found.",
            "employee_id": normalized_id
        }

    # Log successful retrieval without exposing employee details.
    logger.info("Employee record retrieved successfully")

    # Return the employee's record.
    return {
        "success": True,
        "employee_id": normalized_id,
        **employee
    }
