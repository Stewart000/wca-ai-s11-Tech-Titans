# main.py
# Stage 2: Professional Customer Response Generation

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from output_handler import format_output, save_output


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

if __name__ == "__main__":

    print("========================================")
    print("   CUSTOMER FEEDBACK ANALYZER - STAGE 2")
    print("========================================")

    feedback = input("\nEnter customer feedback: ").strip()

    if not feedback:
        print("Error: Customer feedback cannot be empty.")
        exit()

    # Temporary Stage 1 result.
    # These values will later come from the real Stage 1 API call.
    sentiment = "Negative"
    category = "Billing"
    action_item = (
        "Investigate the duplicate subscription charge "
        "and resolve the billing issue."
    )

    try:

        # Generate the professional customer response.
        result = generate_professional_response(
            sentiment,
            category,
            action_item
        )

        # Display the Stage 2 result.
        print("\n--- PROFESSIONAL RESPONSE ---")
        print(result.response)

        print("\n--- RECOMMENDED NEXT STEP ---")
        print(result.recommended_next_step)

        # Format the complete result for saving.
        formatted_output = format_output(
            feedback=feedback,
            sentiment=sentiment,
            category=category,
            action_item=action_item,
            professional_response=result.response,
            recommended_next_step=result.recommended_next_step
        )

        # Save the final result to the outputs folder.
        saved_file = save_output(formatted_output)

        print(f"\nOutput saved successfully to: {saved_file}")

    except Exception as error:
        print("\nAn error occurred while processing the feedback.")
        print(error)