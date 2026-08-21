# Customer Feedback Analyzer

## Group Project

**Tool Name:** Customer Feedback Analyzer  
**Repository:** wca-ai-s11-Tech-Titans-Tech-Titans

## Group Members

- Gill Omondi Ochieng
- Alfred Otieno Owuor
- Stewart Murandi

## Problem

Businesses receive customer feedback that can be difficult and time-consuming to process manually. Customer Feedback Analyzer uses AI to analyse customer feedback, identify the main issue, and produce a professional response and recommended action.

## What the Tool Does

The Customer Feedback Analyzer processes customer feedback in two connected AI stages.

### Stage 1 — Feedback Analysis

The first Gemini API call analyses the customer's feedback and returns structured JSON containing:

- Sentiment
- Sentiment score
- Category
- Summary
- Tags
- Urgency

### Stage 2 — Professional Response

The second Gemini API call uses the Stage 1 analysis to generate:

- A professional response to the customer
- A recommended next step for the business

The final result is displayed to the user and saved as a Markdown file in the `outputs` folder.

### Stage 3 - Menu

The tool displays a simple input validation menu whose options are:

 - Option 1 - Analyse feedback
 - Option 2 - To exit

### Stage 4 - Save the Report

This final stage assembles everything into a markdown report and writes it to, ('outputs/feedback_analysis_<timestamp>.md').

## How the Tool Works

```text
Customer Feedback
        |
        v
      Menu
        |
        v
  Gemini API - Stage 1
  Feedback Analysis
        |
        v
   Structured JSON
        |
        v
  Gemini API - Stage 2
  Response Generation
        |
        v
 Professional Response
        +
 Recommended Next Step
        |
        v
Markdown File - Stage 4
