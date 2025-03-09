from .SummaryFromContentServiceBase import SummaryFromContentServiceBase
from django.conf import settings
from google import genai


class SummaryFromContentGeminiAPI(SummaryFromContentServiceBase):

    def generate_summary(self, content):
        prompt = f"""
        you are given a document content
        you need to summarize the content in less tha 20 word
        Document Format:
        {content}
        Output Format:
        Return the summarized content
        """
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=prompt
        )
        print("Summary from content: ", response.text)
        return response.text
