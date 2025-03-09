from .ContentToJSONServiceBase import ContentToJSONServiceBase
from django.conf import settings
from google import genai
import json


class ContentToJSONGeminiAPI(ContentToJSONServiceBase):
    def content_to_json(self, formatted_content: str) -> json:
        prompt = f"""
        you are given formatted file content
        you need to convert it to json format
        Input Format:
        Formatted Content:
        {formatted_content}
        Output Format:
        Return the json content
        """
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=prompt
        )
        print("to json: ", response.text)
        return json.loads(
            response.text[response.text.find("{") : response.text.rfind("}") + 1]
        )
