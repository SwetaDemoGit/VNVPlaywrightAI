
from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool


# Sample product catalogue (fictional prices)
PRODUCTS = [
    {"name": "Dell Inspiron", "category": "laptop", "price": 55000},
    {"name": "HP Pavilion", "category": "laptop", "price": 58000},
    {"name": "Lenovo IdeaPad", "category": "laptop", "price": 49000},
    {"name": "Samsung Galaxy A", "category": "phone", "price": 22000},
    {"name": "Pixel A Series", "category": "phone", "price": 25000},
]


# Tool 1: Search products within a budget
@tool
def search_products(category: str, budget: float) -> str:
    """Find products in a category that cost no more
    than the specified budget."""

    matches = [
        p for p in PRODUCTS
        if p["category"] == category.lower()
        and p["price"] <= budget
    ]

    if not matches:
        return "No matching products found."

    return "\n".join(
        f"{p['name']}: Rs. {p['price']}"
        for p in matches
    )


# Tool 2: Compare two products
@tool
def compare_products(product1: str, product2: str) -> str:
    """Compare two products by name and price."""

    p1 = next(
        (p for p in PRODUCTS
         if p["name"].lower() == product1.lower()),
        None
    )
    p2 = next(
        (p for p in PRODUCTS
         if p["name"].lower() == product2.lower()),
        None
    )

    if not p1 or not p2:
        return "One or both products were not found."

    difference = abs(p1["price"] - p2["price"])

    return (
        f"{p1['name']}: Rs. {p1['price']}\n"
        f"{p2['name']}: Rs. {p2['price']}\n"
        f"Price difference: Rs. {difference}"
    )


# Create the agent
agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[search_products, compare_products],
    system_prompt=(
        "You are a shopping assistant. "
        "Use search_products to find products within "
        "a budget. Use compare_products to compare "
        "two named products. Use only tool results "
        "for product prices. Explain recommendations "
        "clearly and never invent product information."
    )
)


# Run the agent
if __name__ == "__main__":
    while True:
        question = input("\nCustomer: ")

        if question.lower().strip() == "exit":
            break

        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })

        print("\nShopping Assistant:")
        print(result["messages"][-1].content)
