from unittest.mock import patch

from app.services.tools import search_hr_policy

def test_empty_policy_question():
    result = search_hr_policy("")

    assert result["success"] is False
    assert result["error"] == "The policy question cannot be empty."
    assert result["results"] == []

@patch("app.services.tools.search_chunks")
def test_policy_search_with_results(mock_search):
    mock_search.return_value = [
        {
            "text": "Paternity leave is 5 days.",
            "source": "company_policy.pdf",
            "Page": 9,
            "chunk_index": 23,
            "distance": 0.4
        }
    ]

    result = search_hr_policy("How many days of paternity leave? ")

    assert result["success"] is True
    assert result["found"] is True
    assert len(result["results"]) == 1
    assert "5 days" in result["results"][0]["text"]

    mock_search.assert_called_once_with(
        query = "How many days of paternity leave?",
        top_k=3
    )


@patch("app.services.tools.search_chunks")
def test_policy_search_with_no_result(mock_search):
    mock_search.return_value = []

    result = search_hr_policy("What is the variable pay percentage?")

    assert result["success"] is True
    assert result["found"] is False
    assert result["results"] == []

@patch("app.services.tools.search_chunks")
def test_policy_search_failure(mock_search):
    mock_search.side_effect = RuntimeError("Simulated search failure")

    result = search_hr_policy("How much annaual leave is available?")

    assert result["success"] is False
    assert result["error"] == "The HR policy search failed."
    assert result["results"] == []
