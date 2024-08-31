import google.generativeai as genai

class ContentAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_content(self, topic, duration):
        prompt = f"""
        Create a script for a {duration}-minute video about {topic}.
        The script should include:
        1. An engaging introduction
        2. 3-5 main points or facts about the topic
        3. A brief conclusion

        Also, provide a short description for an image that could be used in the video.

        Format the response as follows:
        Script:
        [Your generated script here]

        Image Description:
        [Your image description here]
        """

        try:
            response = self.model.generate_content(prompt)
            content = response.text
            script, image_description = self._parse_response(content)
            return script, image_description
        except Exception as e:
            print(f"An error occurred while generating content: {str(e)}")
            return None, None

    def _parse_response(self, content):
        parts = content.split("Image Description:")
        script = parts[0].replace("Script:", "").strip()
        image_description = parts[1].strip() if len(parts) > 1 else ""
        return script, image_description