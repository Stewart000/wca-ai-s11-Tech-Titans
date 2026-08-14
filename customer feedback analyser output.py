import os
import json
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# Load environment variables / JSON configuration from the local .env file.
# Do not hardcode API keys in the source code.  
# -----------------------------

load_dotenv()

MODEL_NAME = "gemini-1.5-flash"

def extract_json(raw_text):
    """Extract and parse a JSON object from Gemini output, including markdown fences."""
    if raw_text is None:
        raise ValueError("Gemini returned no content.")

    cleaned = str(raw_text).strip()

    # Remove markdown fences used by the model for readability.
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    # Try standard JSON parsing first.
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to the first JSON object in case the model adds surrounding prose.
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise ValueError("Bad JSON from Gemini response.")
        return json.loads(match.group(0))

# Prompt formatting function using the R-T-C-C-O framework: Role, Task, Context, Constraints, Output.

def build_rtcco_prompt(role, task, context, constraints, output):
    """Format a prompt using the R-T-C-C-O framework: Role, Task, Context, Constraints, Output."""
    return f"""

Role:
You are a junior online business analyst.

Task:
You are tasked with analyzing customer feedback data and providing insights to improve the business.

Context:
You have access to a dataset of customer feedback reviews across various products and services.
Customer feedback: [INSERT_CUSTOMER_FEEDBACK_HERE]

Constraints:
- Return your insights in a structured JSON format.
- Provide insights in a clear and concise manner, using plain and respectful language.
- Use data-driven analysis to support your conclusions.
- Avoid making assumptions without evidence from the data.
- Metrics to track such as customer satisfaction scores, common complaints, and recurring themes should be highlighted.
- Be transparent on what can and cannot be concluded from the data.

Output:
Return a JSON object containing the following fields:
- "summary": A brief summary of the overall customer sentiment.
- "key_issues": A list of the most common issues or complaints raised by customers.
- "recommendations": A list of actionable recommendations for improving the business based on the feedback.
- "data_insights": Any additional insights or patterns observed in the data that could be useful for decision-making.

"""
# Model configuration and API call functions.

def configure_model():
    """Load the Gemini API key from .env and create the model client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_key_here":
        raise ValueError("Missing GEMINI_API_KEY in the .env file.")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

# Model initialization and API call function

def call_gemini(model, prompt):
    """Call the Gemini API with the given prompt."""
    response = model.generate_content(prompt)
    return response.text

# First API call

# Sample feedback data (replace with actual feedback source)
feedback = ""

# Configure the model
model = configure_model()

analysis_prompt = build_rtcco_prompt(
        role="You are a junior online business analyst.",
            task="Analyse this customer feedback and determine overall sentiment, major themes, issues, and urgency.",
        context=f"Customer feedback: {feedback}",
        constraints=(
            "Return only valid JSON. Use exact keys: sentiment, sentiment_score, key_themes, "
            "main_issues, strengths, suggested_improvements, urgency_level. "
            "Keep values concise but useful."
        ),
        output="JSON object only with no markdown fences or commentary.",
    )

analysis_raw = call_gemini(model, analysis_prompt)
analysis = extract_json(analysis_raw)