
import os
import requests

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv()


# 1. Define the structure of a test case
class TestCase(BaseModel):
    title: str = Field(description="Test case title")
    test_type: str = Field(
        description="Positive, Negative, or Boundary"
    )
    preconditions: str
    steps: list[str]
    expected_result: str


class TestCaseList(BaseModel):
    test_cases: list[TestCase]


# 2. Configure the LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

generator = llm.with_structured_output(TestCaseList)


# 3. Generate test cases from a user story
def generate_test_cases(story: str) -> TestCaseList:
    prompt = f"""
    You are an experienced QA engineer.

    Generate 5 test cases based on this user story.
    Include positive and negative cases, and boundary
    cases where justified by the requirements.

    For each case provide:
    - Title
    - Test type
    - Preconditions
    - Numbered test steps
    - Expected result

    Do not invent requirements. Identify assumptions.

    User story and acceptance criteria:
    {story}
    """

    return generator.invoke(prompt)


# 4. Create an ordinary Jira issue
def create_jira_issue(tc: TestCase) -> dict:
    base_url = os.environ["JIRA_BASE_URL"].rstrip("/")
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]

    project_key = os.environ["JIRA_PROJECT_KEY"]
    issue_type = os.getenv("JIRA_ISSUE_TYPE", "Task")

    steps = "\n".join(
        f"{i}. {step}"
        for i, step in enumerate(tc.steps, 1)
    )

    description = (
        f"Test Type: {tc.test_type}\n\n"
        f"Preconditions:\n{tc.preconditions}\n\n"
        f"Test Steps:\n{steps}\n\n"
        f"Expected Result:\n{tc.expected_result}"
    )

    # Jira Cloud REST API v3 description format
    adf_description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": description}
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": f"[AI Test Case] {tc.title}",
            "issuetype": {"name": issue_type},
            "description": adf_description,
            "labels": ["ai-generated-test"]
        }
    }

    response = requests.post(
        f"{base_url}/rest/api/3/issue",
        json=payload,
        auth=(email, token),
        headers={"Accept": "application/json"},
        timeout=30
    )

    if not response.ok:
        raise RuntimeError(
            f"Jira error {response.status_code}: {response.text}"
        )

    issue = response.json()

    return {
        "key": issue["key"],
        "url": f"{base_url}/browse/{issue['key']}"
    }


# 5. Run the application
if __name__ == "__main__":
    story = input(
        "Paste the user story and acceptance criteria:\n"
    ).strip()

    if not story:
        raise SystemExit("A user story is required.")

    generated = generate_test_cases(story)

    print("\n--- GENERATED TEST CASES ---")

    for i, tc in enumerate(generated.test_cases, 1):
        print(f"\n{i}. {tc.title} [{tc.test_type}]")
        print("Preconditions:", tc.preconditions)

        for n, step in enumerate(tc.steps, 1):
            print(f"  {n}. {step}")

        print("Expected result:", tc.expected_result)

    approval = input(
        "\nCreate these issues in Jira? Type YES: "
    )

    if approval != "YES":
        print("Cancelled. Nothing was created.")
        raise SystemExit(0)

    print("\n--- JIRA CREATION RESULTS ---")

    for tc in generated.test_cases:
        try:
            issue = create_jira_issue(tc)
            print(f"Created {issue['key']}: {issue['url']}")
        except (requests.RequestException, RuntimeError, KeyError) as exc:
            print(f"Failed to create '{tc.title}': {exc}")
