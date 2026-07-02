# src/ai_handler.py
import os
from google import genai
from dotenv import load_dotenv 

# لود کردن فایل .env
load_dotenv()

class AIReviewer:
    @staticmethod
    def get_suggestions(issues: list):
        if not issues:
            return "AI Review: Everything looks amazing! No code optimizations needed."

        # خواندن کلید از متغیرهای محیطی سیستم
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "[AI INFO] To get smart code suggestions, please set the GEMINI_API_KEY environment variable."

        # 🟢 اصلاح باگ: پاس دادن متغیر درست api_key
        client = genai.Client(api_key=api_key)

        prompt = (
            "You are an expert Senior Software Engineer and Code Reviewer. "
            "Below is a list of static analysis issues found in my Python project. "
            "Please analyze these issues and provide clear, concise, and professional refactoring recommendations "
            "along with clean code snippets to fix them.\n\n"
            f"Issues Found:\n{issues}\n"
        )

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"[AI ERROR] Failed to fetch suggestions from Gemini: {str(e)}"