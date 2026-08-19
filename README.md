# Customer Feedback Analyzer

## Project Overview

Customer Feedback Analyzer is a Python AI tool that helps businesses understand customer feedback and decide what action to take.

The tool uses two connected Gemini API calls:

1. **Stage 1 - Feedback Analysis:** Analyzes the customer's feedback and returns structured JSON containing sentiment, category, summary, tags, sentiment score, and urgency.
2. **Stage 2 - Professional Response:** Uses the Stage 1 analysis to generate a professional customer response and recommend the next practical action.

The final analysis is saved as a Markdown (`.md`) file in the `outputs` folder.

## Features

- Two connected Gemini AI API calls
- Structured JSON responses using Pydantic
- Sentiment analysis
- Customer feedback categorization
- Keyword/tag extraction
- Urgency detection
- Professional customer response generation
- Recommended next action
- Input validation
- Error handling
- Markdown output files
- Interactive menu

## How the Tool Works

```text
Customer Feedback
        |
        v
   User Menu
        |
        v
  Stage 1: Gemini
  Feedback Analysis
        |
        v
   Structured JSON
        |
        v
  Stage 2: Gemini
 Professional Response
        |
        v
 Recommended Action
        |
        v
   Markdown File