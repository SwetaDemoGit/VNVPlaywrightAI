import json
import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

# Public demo API. JSONPlaceholder is a fake REST API intended for practice.
BASE_URL = "https://jsonplaceholder.typicode.com"


@tool
def get_post(post_id: int) -> str:
    """Call the demo API to retrieve a post by ID and return status and response data."""
    url = f"{BASE_URL}/posts/{post_id}"
    try:
        response = requests.get(url, timeout=15)
        result = {
            "method": "GET",
            "url": url,
            "status_code": response.status_code,
            "passed_status_check": response.status_code == 200,
        }
        try:
            result["response_body"] = response.json()
        except ValueError:
            result["response_body"] = response.text[:500]
        return json.dumps(result, indent=2)
    except requests.RequestException as exc:
        return json.dumps({
            "method": "GET",
            "url": url,
            "error": str(exc),
            "passed_status_check": False
        }, indent=2)


@tool
def validate_post_response(post_id: int) -> str:
    """Call the demo API and validate status code plus required JSON fields for a post."""
    url = f"{BASE_URL}/posts/{post_id}"
    try:
        response = requests.get(url, timeout=15)
        checks = {
            "status_is_200": response.status_code == 200,
            "content_type_is_json": "application/json" in response.headers.get("Content-Type", ""),
        }

        body = None
        try:
            body = response.json()
        except ValueError:
            pass

        checks["body_is_json_object"] = isinstance(body, dict)
        checks["has_userId"] = isinstance(body, dict) and "userId" in body
        checks["has_id"] = isinstance(body, dict) and "id" in body
        checks["has_title"] = isinstance(body, dict) and isinstance(body.get("title"), str)
        checks["has_body"] = isinstance(body, dict) and isinstance(body.get("body"), str)

        result = {
            "test_name": f"GET /posts/{post_id} response validation",
            "url": url,
            "status_code": response.status_code,
            "checks": checks,
            "passed": all(checks.values()),
            "response_body": body if body is not None else response.text[:500]
        }
        return json.dumps(result, indent=2)
    except requests.RequestException as exc:
        return json.dumps({
            "test_name": f"GET /posts/{post_id} response validation",
            "url": url,
            "passed": False,
            "error": str(exc)
        }, indent=2)


@tool
def check_missing_post(post_id: int) -> str:
    """Test that a non-existent post returns HTTP 404. Use an ID such as 999999."""
    url = f"{BASE_URL}/posts/{post_id}"
    try:
        response = requests.get(url, timeout=15)
        passed = response.status_code == 404
        return json.dumps({
            "test_name": f"GET /posts/{post_id} should return 404",
            "url": url,
            "expected_status": 404,
            "actual_status": response.status_code,
            "passed": passed,
            "note": "This endpoint may return 404 for an ID that does not exist."
        }, indent=2)
    except requests.RequestException as exc:
        return json.dumps({
            "test_name": f"GET /posts/{post_id} expected 404",
            "passed": False,
            "error": str(exc)
        }, indent=2)


llm = ChatOllama(model="gemma4:12b", temperature=0)

agent = create_agent(
    model=llm,
    tools=[get_post, validate_post_response, check_missing_post],
    system_prompt="""
You are a careful API testing assistant.
- Use the tools to execute actual requests against the JSONPlaceholder practice API.
- For a request to test or validate a post response, call validate_post_response.
- For a request to inspect or fetch a post, call get_post.
- For a request to test a missing/non-existent post or expected 404, call check_missing_post.
- Explain each assertion as PASS or FAIL based on the tool output.
- Never claim an API call succeeded unless a tool result confirms it.
- Do not invent status codes, response fields, or test results.
- This is a public practice API with fake data; do not send private data.
- Summarize the endpoint, checks, actual results, and any failures in simple language.
"""
)


def main():
    print("LangChain API Testing Agent")
    print("Practice API: JSONPlaceholder (read-only GET requests)")
    print("Examples:")
    print("  Test the response schema for post 1")
    print("  Fetch post 3")
    print("  Test that post 999999 returns 404")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Tester: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        result = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })
        print("\nAgent:", result["messages"][-1].content, "\n")


if __name__ == "__main__":
    main()
