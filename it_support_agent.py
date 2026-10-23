# Tool 1
def troubleshoot_laptop():
    return "Close unused apps and restart your laptop."


# Tool 2
def troubleshoot_wifi():
    return "Check Wi-Fi settings and reconnect."


# Agent
def agent(user_input):

    if "laptop" in user_input.lower():
        return troubleshoot_laptop()

    elif "wifi" in user_input.lower():
        return troubleshoot_wifi()

    else:
        return "I cannot solve this issue yet."


# User input
question = input("Describe your IT problem: ")

print("Agent:", agent(question))