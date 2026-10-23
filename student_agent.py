
# TOOL: Suggest a learning plan
def suggest_learning_plan(subject):
    plans = {
        "python": "Learn variables, loops, functions, and OOP.",
        "java": "Learn syntax, OOP, collections, and exceptions.",
        "testing": "Learn test cases, Selenium, and automation."
    }

    return plans.get(
        subject.lower(),
        "Sorry, no learning plan is available."
    )


# AGENT: Decide which tool to call
def student_agent(user_input):
    print("Agent is analyzing your request...")

    return suggest_learning_plan(user_input)


# USER INPUT
subject = input("What do you want to learn? ")

# AGENT RESPONSE
print("Agent:", student_agent(subject))
