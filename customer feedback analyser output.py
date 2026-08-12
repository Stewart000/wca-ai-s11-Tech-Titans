
import os
import json
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# Load environment variables    
# -----------------------------

load_dotenv()
