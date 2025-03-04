from document.utils.FormatContentService.FormatContentServiceBase import (
    FormatContentServiceBase,
)
from django.conf import settings
from google import genai


class FormatContentServiceUsingGeminiAPI(FormatContentServiceBase):
    def clean_content(self, content):
        return content.replace("\n", " ").replace("  ", " ")

    def optimize_content(self, content):
        cleaned_content = self.clean_content(content)
        template = f"""
            I will provide the extracted text from an image. Your task is to format the text into a well-structured document.
            Input Format:
            Extracted Text:
            {cleaned_content}
            Output Format:
            Return the formatted text.
            """
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=template
        )
        return response.text
