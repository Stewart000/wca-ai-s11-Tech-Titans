# wca-ai-s11-Tech-Titans
# agent.py 
import config
from google. genai import types
from pydantic import BaseModel, Field
from google import genai

## The client automatically discovers os.environ["GEMINI_API_KEY"]
client = genai.Client()

## Define the precise structure your team needs for the analysis output
class FeedbackAnalysis(BaseModel):
    sentiment: str = Field(..., description="Sentiment of the feedback (Positive, Neutral, Negative)")
    category: str = Field(..., description="Category of the feedback (e.g., Bug, Feature Request, Billing, Usability)")
    action_item: str = Field(..., description="Suggested action item for the team based on the feedback")

def analyze_customer_feedback(feedback_text: str) -> str:
    """ Analyzes customer feedback sentiment, category, and action items."""
    
   prompt = f"""
   You are an expert customer feedback analyzer AI agent.
   Analyze the following customer review. Provide a JSON response containing:
   1. Sentiment (Positive, Neutral, Negative)
   2. Category (e.g., Bug, Feature Request, Billing, Usability)
   3. Suggested Action Item for the team.

   Review: "{feedback_text}"
  """
  response = client.model.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
    )
    
  def analyze_customer_feedback(feedback_text: str) -> FeedbackAnalysis:
        """ Analyzes customer feedback and guarantees structured python object output."""
        
   prompt = f"Analyze this custtomer feedback and provide a JSON response with sentiment, category, and action item: {feedback_text}"
        
   ## Tell Gemini to enforce this pydantic schema
  response = client.models.generate_content(
            response_schema=FeedbackAnalysis,
            model=config.GEMINI_MODEL,
            contents=prompt,
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FeedbackAnalysis,
                temperature=0.1, # Low temperature for deterministic output
        ),
        )
        
   ## Parse the response into the FeedbackAnalysis model
   analysis = FeedbackAnalysis.parse_raw(response.text)
        return analysis
    
  response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt,
    )
    
   return response.text

## 3. parse and return the structured object
## The SDK automatically handles the conversation back to your pydantic class
return FeedbackAnalysis.model_validate_JSON(response.text)

## Local Test
if _name_== "__main__":
    sample_feedback = "I Love the new UI, but billing charged me twice for my subscription. Please fix this issue."
    
   ## Run the agent
   result = analyze_feedback(sample_feedback)
    
   ## can access the fields with dot notation and type hinting
   print(f"Sentiment: {result.sentiment}"),
    print(f"Category: {result.category}"),
    print(f"Urgency: {result.urgency_score} /5")
    print(f"Action Item: {result.action_item}")     



