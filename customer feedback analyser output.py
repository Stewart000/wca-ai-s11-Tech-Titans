"""
Customer Feedback Analyzer

Uses Gemini + Pydantic structured output to analyze feedback,
then saves a JSON file and a Markdown report.
"""

import json
from datetime import datetime
from pathlib import Path

from r import FeedbackAnalysisSchema, analyze_customer_feedback

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def build_report(feedback: str, analysis: FeedbackAnalysisSchema) -> str:
    """Build a Markdown report from the feedback and its analysis."""
    lines = [
        "# Customer Feedback Analysis Report",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Original Feedback",
        feedback,
        "",
        "## Analysis",
        "```json",
        json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False),
        "```",
    ]
    return "\n".join(lines)

# Output directory for saving JSON and Markdown reports

def save_outputs(analysis: FeedbackAnalysisSchema, report_md: str) -> tuple[Path, Path]:
    """Save the JSON analysis and Markdown report to timestamped files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = OUTPUT_DIR / f"feedback_analysis_{timestamp}.json"
    md_path = OUTPUT_DIR / f"feedback_report_{timestamp}.md"

    json_path.write_text(
        json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    md_path.write_text(report_md, encoding="utf-8")

    return json_path, md_path

# Function to get feedback input from the user, either pasted directly or loaded from a file.

def get_feedback_input() -> str | None:
    """Prompt the user for feedback text, pasted directly or from a file. Returns None to quit."""
    choice = input("\nPaste feedback (p), load from file (f), or quit (q)? ").strip().lower()

    if choice == "q":
        return None
    if choice == "f":
        path = input("File path: ").strip()
        try:
            return Path(path).read_text(encoding="utf-8").strip()
        except OSError as e:
            print(f"Could not read file: {e}")
            return ""
    if choice == "p":
        print("Paste feedback, then press Enter on an empty line to finish:")
        lines = iter(input, "")
        return "\n".join(lines).strip()

    print("Invalid choice.")
    return ""

# Main function to run the feedback analyzer interactively.

def main() -> None:
    while True:
        feedback = get_feedback_input()
        if feedback is None:
            print("Goodbye.")
            break
        if not feedback:
            continue

        try:
            analysis = analyze_customer_feedback(feedback)
        except Exception as e:
            print(f"Analysis failed: {e}")
            continue

        report_md = build_report(feedback, analysis)
        print("\n=== Analysis ===")
        print(json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False))

        json_path, md_path = save_outputs(analysis, report_md)
        print(f"\nSaved: {json_path}")
        print(f"Saved: {md_path}")

        if input("\nAnalyze another? (y/n): ").strip().lower() != "y":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()