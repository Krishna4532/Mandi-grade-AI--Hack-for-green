import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_mandi_grade(image_data: bytes) -> str:
    """
    Analyzes crop quality using Gemini 1.5 Flash.
    Returns a Grade: 'FAQ' (Fair Average Quality), 'Premium', or 'Under-Grade'.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Prepare the image part for the multimodal prompt
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_data
        }

        # Professional Prompt for Agricultural Grading
        prompt = (
            "You are an expert Mandi Inspector. Analyze this crop image for: "
            "1. Grain luster and color. 2. Presence of foreign matter/dust. 3. Grain breakage. "
            "Return ONLY one word as the grade: 'Premium' if it looks perfect, "
            "'FAQ' if it is standard quality, or 'Under-Grade' if there are many defects."
        )

        # Generate response
        response = model.generate_content([prompt, image_part])
        
        # Clean the output (Gemini sometimes adds spaces or dots)
        grade = response.text.strip().replace(".", "")
        
        # Validation to ensure Pathway join doesn't fail
        valid_grades = ["Premium", "FAQ", "Under-Grade"]
        if grade not in valid_grades:
            # Fallback if AI gets talkative
            return "FAQ"
            
        return grade

    except Exception as e:
        print(f"Error in Gemini Analysis: {e}")
        return "FAQ" # Default fallback so the pipeline doesn't break