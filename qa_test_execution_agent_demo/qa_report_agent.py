import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

load_dotenv()

REPORT_PATH = Path("test_execution_report.json")
LOGS_PATH = Path("failure_logs.json")


@tool
def get_execution_summary() -> str:
    """Read the test execution report and return verified counts and test results."""
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    cases = report["test_cases"]
    counts = {
        "total": len(cases),
        "passed": sum(t["status"] == "PASS" for t in cases),
        "failed": sum(t["status"] == "FAIL" for t in cases),
        "skipped": sum(t["status"] == "SKIPPED" for t in cases),
    }
    return json.dumps({
        "report_title": report["report_title"],
        "environment": report["environment"],
        "build": report["build"],
        "summary_from_file": report["summary"],
        "verified_counts": counts,
        "test_cases": cases,
    }, indent=2)


@tool
def get_failure_logs() -> str:
    """Read detailed failure logs for failed test cases."""
    logs = json.loads(LOGS_PATH.read_text(encoding="utf-8"))
    return json.dumps(logs, indent=2)


llm = ChatOllama(model="gemma4:12b", temperature=0)

agent = create_agent(
    model=llm,
    tools=[get_execution_summary, get_failure_logs],
    system_prompt="""
You are a careful QA test execution analyst.
When asked to analyze the report:
1. Call get_execution_summary to read the report and verify counts.
2. Call get_failure_logs to inspect each failed test's evidence.
3. Report total, passed, failed, skipped, and pass rate (passed / total * 100).
4. For each failure, summarize observed behavior versus expected behavior.
5. Flag a bug as CRITICAL only when evidence suggests a serious security/access-control issue,
   authentication bypass, expired reset token accepted, or material payment/order integrity risk.
6. Do not claim a root cause is confirmed unless the logs prove it. Use "potential" or
   "investigate" where evidence is incomplete.
7. For each flagged issue, include test ID, evidence, impact, severity recommendation,
   and next investigation step.
8. Distinguish a failed test from a confirmed production bug. These are fictional QA/staging
   test results; do not imply they are real incidents.
9. Do not invent data. Base conclusions only on the tool results.
"""
)


def main():
    print("QA Test Execution Analysis Agent (local Ollama)")
    print("Type 'exit' to quit.")
    print("Example: Analyze the report, review failure logs, and flag critical bugs.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        result = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })
        print("\nAgent:")
        print(result["messages"][-1].content)
        print()


if __name__ == "__main__":
    main()
