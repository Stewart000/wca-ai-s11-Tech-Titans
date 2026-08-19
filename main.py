# main.py
# Stage 2: Professional Customer Response Generation

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from output_handler import format_output, save_output
from stage1 import analyze_feedback


# --------------------------------------------------
# Load the Gemini API key from the .env file
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")


# --------------------------------------------------
# Create the Gemini client
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Define the structure of Stage 2's JSON response
# --------------------------------------------------

class ProfessionalResponse(BaseModel):
    response: str = Field(
        description="A professional, polite response that can be sent to the customer."
    )

    recommended_next_step: str = Field(
        description="The practical next step the company should take based on the feedback analysis."
    )


# --------------------------------------------------
# Stage 2: Generate a professional customer response
# --------------------------------------------------

def generate_professional_response(
    sentiment: str,
    category: str,
    action_item: str
) -> ProfessionalResponse:

    prompt = f"""
ROLE:
You are a professional customer support representative
responding on behalf of a company.

TASK:
Create a professional and helpful response to a customer
based on the customer feedback analysis provided below.

CONTEXT:
The Stage 1 analysis produced:

Sentiment: {sentiment}
Category: {category}
Action Item: {action_item}

CONSTRAINTS:
- Be polite, professional, empathetic, and clear.
- Acknowledge the customer's concern when appropriate.
- Base the response only on the information provided.
- Do not invent facts, refunds, discounts, deadlines, or promises.
- Do not blame the customer.
- Keep the customer-facing response concise.
- The recommended next step must be practical and related to the action item.

OUTPUT:
Return valid JSON with exactly these two fields:
1. response
2. recommended_next_step
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProfessionalResponse,
            temperature=0.2,
        ),
    )

    # Convert Gemini's JSON response into our Pydantic model.
    result = ProfessionalResponse.model_validate_json(response.text)

    return result

# --------------------------------------------------
# Local test
# --------------------------------------------------

# --------------------------------------------------
# Stage 3: Menu and User Input Validation
# --------------------------------------------------

def display_menu():
    """Display the main application menu."""
    print("\n========================================")
    print("   CUSTOMER FEEDBACK ANALYZER")
    print("========================================")
    print("1. Analyze customer feedback")
    print("2. Exit")
    print("========================================")


def get_menu_choice():
    """Get and validate the user's menu choice."""

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            return choice

        if choice == "2":
            return choice

        print("\nInvalid choice. Please enter 1 or 2.")


def get_feedback():
    """Get and validate customer feedback."""

    while True:
        feedback = input("\nEnter customer feedback: ").strip()

        if not feedback:
            print("Error: Feedback cannot be empty.")
            continue

        if len(feedback) < 10:
            print(
                "Error: Please provide more detailed feedback "
                "(at least 10 characters)."
            )
            continue

        return feedback


def analyze_customer_feedback():
    """Run the Stage 1 → Stage 2 → output pipeline."""

    feedback = get_feedback()

    try:
        analysis = analyze_feedback(feedback)

        sentiment = analysis.sentiment
        category = analysis.category
        action_item = analysis.summary

        result = generate_professional_response(
            sentiment,
            category,
            action_item
        )

        print("\n--- PROFESSIONAL RESPONSE ---")
        print(result.response)

        print("\n--- RECOMMENDED NEXT STEP ---")
        print(result.recommended_next_step)

        formatted_output = format_output(
            feedback=feedback,
            sentiment=analysis.sentiment,
            sentiment_score=analysis.sentiment_score,
            category=analysis.category,
            summary=analysis.summary,
            tags=analysis.tags,
            urgent_action_required=analysis.urgent_action_required,
            professional_response=result.response,
            recommended_next_step=result.recommended_next_step
        )

        saved_file = save_output(formatted_output)

        print(f"\nOutput saved successfully to: {saved_file}")

    except Exception as error:
        print("\nAn error occurred while processing the feedback.")
        print(error)


# --------------------------------------------------
# Application entry point
# --------------------------------------------------

if __name__ == "__main__":

    while True:

        display_menu()

        choice = get_menu_choice()

        if choice == "2":
            print("\nThank you for using Customer Feedback Analyzer.")
            print("Goodbye!")
            break

        analyze_customer_feedback()