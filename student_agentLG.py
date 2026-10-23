
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# TOOL 1: Suggest a learning plan
@tool
def learning_plan(subject: str) -> str:
    """Provide a beginner learning plan for a subject."""

    plans = {
        "python": "Learn variables, conditions, loops, functions and OOP.",
        "java": "Learn syntax, OOP, collections and exceptions.",
        "testing": "Learn test cases, Selenium and automation testing."
    }

    return plans.get(
        subject.lower(),
        "Start with fundamentals, practise examples, and build a small project."
    )


# TOOL 2: Generate a simple quiz question
@tool
def practice_quiz(subject: str) -> str:
    """Return a beginner practice question for a subject."""

    quizzes = {
        "python": "What is the difference between a list and a tuple?",
        "java": "What is the difference between a class and an object?",
        "testing": "What is the difference between smoke testing and regression testing?"
    }

    return quizzes.get(
        subject.lower(),
        "Explain one important concept in " + subject + "."
    )


# CREATE THE LANGCHAIN AGENT
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[learning_plan, practice_quiz],
    system_prompt=(
        "You are a helpful student assistant. "
        "If the student asks for a learning plan, use learning_plan. "
        "If the student asks for a practice question or quiz, "
        "use practice_quiz. Explain results in simple language."
    )
)


# INTERACT WITH THE AGENT
if __name__ == "__main__":
    print("Student Assistant Agent is ready!")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("Student: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })

        print("\nAgent:", result["messages"][-1].content, "\n")
