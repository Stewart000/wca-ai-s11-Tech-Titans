# main.py
# Customer Feedback Analyzer
# Complete application: Stages 1, 2, 3 and 4

import os
from pathlib import Path
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


# ==================================================
# CONFIGURATION
# ==================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )

client = genai.Client(api_key=api_key)

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


# ==================================================
# STAGE 1 — CUSTOMER FEEDBACK ANALYSIS
# ==================================================

class FeedbackAnalysis(BaseModel):
    sentiment: str = Field(
        description="Must be one of: Positive, Neutral, Negative"
    )

    sentiment_score: float = Field(
        description="Confidence score from 0.0 to 1.0"
    )

    category: str = Field(
        description=(
            "Primary category: Bug, Feature Request, Pricing, "
            "Customer Support, UI/UX, Other"
        )
    )

    summary: str = Field(
        description="One sentence summarizing the customer's feedback."
    )

    tags: List[str] = Field(
        description="Important keywords extracted from the feedback."
    )

    urgent_action_required: bool = Field(
        description=(
            "True if the customer is highly frustrated, "
            "experiencing an outage, or threatening to leave."
        )
    )


def analyze_feedback(feedback: str) -> FeedbackAnalysis:
    """Analyze customer feedback using Gemini."""

    prompt = f"""
ROLE:
You are a Customer Operations Triaging Agent.

TASK:
Analyze the customer's feedback and identify its sentiment,
category, summary, important tags, and urgency.

CONTEXT:
The customer provided the following feedback:
"{feedback}"

CONSTRAINTS:
- Sentiment must be Positive, Neutral, or Negative.
- Sentiment score must be between 0.0 and 1.0.
- Category must be Bug, Feature Request, Pricing,
  Customer Support, UI/UX, or Other.
- Do not invent information.
- Mark urgent_action_required as true only when the
  situation genuinely requires immediate attention.

OUTPUT:
Return structured JSON containing:
- sentiment
- sentiment_score
- category
- summary
- tags
- urgent_action_required
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FeedbackAnalysis,
            temperature=0.1,
        ),
    )

    try:
        return FeedbackAnalysis.model_validate_json(response.text)
    except Exception as error:
        raise ValueError(
            f"Invalid JSON from stage 1: {error}"
    ) from error


# ==================================================
# STAGE 2 — PROFESSIONAL RESPONSE GENERATION
# ==================================================

class ProfessionalResponse(BaseModel):
    response: str = Field(
        description=(
            "A professional, polite response that can "
            "be sent to the customer."
        )
    )

    recommended_next_step: str = Field(
        description=(
            "The practical next step the company should "
            "take based on the feedback analysis."
        )
    )


def generate_professional_response(
    sentiment: str,
    category: str,
    action_item: str
) -> ProfessionalResponse:
    """Generate a professional response using Stage 1 results."""

    prompt = f"""
ROLE:
You are a professional customer support representative
responding on behalf of a company.

TASK:
Create a professional and helpful response to a customer
based on the customer feedback analysis provided below.

CONTEXT:
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
- The recommended next step must be practical and related
  to the action item.

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

    try:
        return ProfessionalResponse.model_validate_json(response.text)
    except ValueError as error:
        raise ValueError(
            f"Invalid JSON from stage 2: {error}"
        ) from error


# ==================================================
# STAGE 4 — OUTPUT FORMATTING AND SAVING
# ==================================================

def format_output(
    feedback: str,
    analysis: FeedbackAnalysis,
    professional_response: ProfessionalResponse
) -> str:
    """Format the complete analysis as a Markdown report."""

    tags = ", ".join(analysis.tags)

    return f"""# CUSTOMER FEEDBACK ANALYSIS

## Customer Feedback

{feedback}

## STAGE 1 - AI ANALYSIS

**Sentiment:**  
{analysis.sentiment}

**Sentiment Score:**  
{analysis.sentiment_score}

**Category:**  
{analysis.category}

**Summary:**  
{analysis.summary}

**Tags:**  
{tags}

**Urgent Action Required:**  
{analysis.urgent_action_required}

## STAGE 2 - PROFESSIONAL RESPONSE

{professional_response.response}

## RECOMMENDED NEXT STEP

{professional_response.recommended_next_step}
"""


def save_output(content: str) -> str:
    """Save the final report to the outputs directory."""

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = OUTPUT_DIR / (
            f"feedback_analysis_{timestamp}.md"
        )

        filename.write_text(
            content,
            encoding="utf-8"
        )

        return str(filename)

    except OSError as error:
        raise OSError(
            f"Could not save the output file: {error}"
        ) from error


# ==================================================
# STAGE 3 — MENU AND INPUT VALIDATION
# ==================================================

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

        choice = input(
            "Enter your choice (1 or 2): "
        ).strip()

        if choice == "1":
            return choice

        if choice == "2":
            return choice

        print(
            "\nInvalid choice. Please enter 1 or 2."
        )


def get_feedback():
    """Get and validate customer feedback."""

    while True:

        try:
            feedback = input("\nEnter customer feedback: ").strip()

            if not feedback:
                raise ValueError("Feedback cannot be empty.")

        except ValueError as error:
            print(f"Error: {error}")
            continue

        if len(feedback) < 10:
            print(
                "Error: Please provide more detailed "
                "feedback (at least 10 characters)."
            )
            continue

        return feedback


# ==================================================
# COMPLETE ANALYSIS PIPELINE
# ==================================================

def analyze_customer_feedback():
    """Run Stages 1, 2 and 4 for validated feedback."""

    feedback = get_feedback()

    try:

        # ------------------------------
        # Stage 1
        # ------------------------------

        print("\nAnalyzing customer feedback...")

        analysis = analyze_feedback(feedback)

        print("\n--- STAGE 1 ANALYSIS ---")
        print(
            analysis.model_dump_json(indent=2)
        )

        # ------------------------------
        # Stage 2
        # ------------------------------

        result = generate_professional_response(
            analysis.sentiment,
            analysis.category,
            analysis.summary
        )

        print("\n--- PROFESSIONAL RESPONSE ---")
        print(result.response)

        print("\n--- RECOMMENDED NEXT STEP ---")
        print(result.recommended_next_step)

        # ------------------------------
        # Stage 4
        # ------------------------------

        formatted_output = format_output(
            feedback=feedback,
            analysis=analysis,
            professional_response=result
        )

        saved_file = save_output(
            formatted_output
        )

        print(
            f"\nOutput saved successfully to: "
            f"{saved_file}"
        )

    except Exception as error:

        print(
            "\nAn error occurred while processing "
            "the feedback."
        )

        print(f"Error details: {error}")


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================

def main():
    """Run the Customer Feedback Analyzer."""

    while True:

        display_menu()

        choice = get_menu_choice()

        if choice == "2":

            print(
                "\nThank you for using "
                "Customer Feedback Analyzer."
            )

            print("Goodbye!")

            break

        analyze_customer_feedback()


if __name__ == "__main__":
    main()