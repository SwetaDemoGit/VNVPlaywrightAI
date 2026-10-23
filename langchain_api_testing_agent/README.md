# LangChain API Testing Agent (No OpenAI API key)

A beginner-friendly API testing agent using LangChain, a local Ollama model, and Python `requests`.

## What it demonstrates
- `get_post(post_id)`: makes a real GET request to a public practice API.
- `validate_post_response(post_id)`: checks HTTP status, JSON content type, and required response fields.
- `check_missing_post(post_id)`: checks whether a non-existent post returns 404.
- The LLM chooses the relevant tool based on the tester's natural-language request.

## Prerequisites
1. Install Ollama: https://ollama.com/download
2. Download a model: `ollama pull llama3.2:3b`
3. Keep Ollama running.
4. Python 3.10+ recommended.

## Install and run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python api_testing_agent.py
```

If you already have a virtual environment, activate it and install the requirements without creating another one.

## Prompts to try
- `Test the response schema for post 1`
- `Fetch post 3`
- `Test that post 999999 returns 404`
- `Validate post 10 and explain any failed checks`

## Notes
- Uses JSONPlaceholder, a public practice API with fake data.
- The code only issues GET requests; it does not create, update, or delete remote data.
- Network access is required when running the agent.
- Results depend on the remote service being reachable.
- The LLM explains tool results; assertions are calculated in Python, not guessed by the model.
