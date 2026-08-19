# output_handler.py
# Handles formatting and saving the final customer feedback analysis.


from pathlib import Path
from datetime import datetime


def format_output(
    feedback: str,
    sentiment: str,
    sentiment_score: float,
    category: str,
    summary: str,
    tags: list[str],
    urgent_action_required: bool,
    professional_response: str,
    recommended_next_step: str
) -> str:
    """
    Format the complete Stage 1 and Stage 2 analysis
    into a readable Markdown report.
    """

    tags_text = ", ".join(tags)

    output = f"""
CUSTOMER FEEDBACK ANALYSIS
==========================

Customer Feedback:
{feedback}


STAGE 1 - AI ANALYSIS
=====================

Sentiment:
{sentiment}

Sentiment Score:
{sentiment_score}

Category:
{category}

Summary:
{summary}

Tags:
{tags_text}

Urgent Action Required:
{urgent_action_required}


STAGE 2 - PROFESSIONAL RESPONSE
================================

{professional_response}


RECOMMENDED NEXT STEP
=====================

{recommended_next_step}
"""

    return output.strip()


def save_output(content: str, output_folder: str = "outputs") -> str:
    """
    Save the formatted result as a Markdown file inside the outputs folder.
    """

    try:
        folder = Path(output_folder)

        # Create the outputs folder if it does not exist.
        folder.mkdir(parents=True, exist_ok=True)

        # Create a timestamp so every report has a unique filename.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = folder / f"feedback_analysis_{timestamp}.md"

        # Save the formatted report.
        filename.write_text(content, encoding="utf-8")

        return str(filename)

    except OSError as error:
        raise OSError(
            f"Could not save the output file: {error}"
        ) from error
        
if __name__ == "__main__":

    test_output = format_output(
        feedback="I was charged twice for my subscription.",
        sentiment="Negative",
        category="Billing",
        action_item="Investigate the duplicate charge.",
        professional_response=(
            "Thank you for bringing this billing issue to our attention. "
            "We apologize for the inconvenience."
        ),
        recommended_next_step=(
            "Investigate the duplicate subscription charge."
        )
    )

    try:
        saved_file = save_output(test_output)
        print(f"Output saved successfully to: {saved_file}")

    except OSError as error:
        print(f"Error saving output: {error}")