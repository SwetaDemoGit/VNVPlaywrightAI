# QA Test Execution Report Analyzer Agent

This is a beginner-friendly LangChain agent demo using a local Ollama model. It requires no OpenAI API key.

## Files
- `test_execution_report.json`: 25 fictional test results.
- `test_execution_report.csv`: same report in spreadsheet-friendly format.
- `failure_logs.json`: logs for the five failed tests.
- `qa_report_agent.py`: LangChain agent with two tools to read the report and failure logs.
- `requirements.txt`: Python dependencies.

## Sample report totals
- Total: 25
- Passed: 18
- Failed: 5
- Skipped: 2
- Pass rate: 72% (18 / 25; skipped tests are included in the denominator).

## Setup
1. Install Ollama from https://ollama.com/download
2. Download a local model:
   `ollama pull llama3.2:3b`
3. From this folder, create/activate a virtual environment if desired.
4. Install dependencies:
   `python -m pip install -r requirements.txt`
5. Ensure Ollama is running, then start:
   `python qa_report_agent.py`
6. Ask:
   `Analyze the report, review the failure logs, and flag critical bugs.`

## Teaching notes
- Tools: `get_execution_summary()` and `get_failure_logs()`.
- The LLM selects the tools and summarizes their results.
- Counts are calculated in Python from the report; the LLM should not be trusted to do arithmetic unaided.
- All test data is fictional and for training only.
- A flagged critical issue is a recommendation based on test evidence, not a confirmed production incident.
