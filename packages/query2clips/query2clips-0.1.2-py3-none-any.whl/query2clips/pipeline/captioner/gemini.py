import time
import re
from typing import Optional
from query2clips.pipeline.captioner.abc import Captioner
import google.generativeai as genai
import os

DEFAULT_PROMPT = """Please give me a description and a matching score for this video.

1. Video description:
Please give me a detailed description of what is happening in this video
The description should be compact and comprehensive, and should not exceed 50 words.

2. Matching score:
Please give me a score between 0 and 100 that represents how well the video matches the description.
If the video is containing too many different things, the score should be low.

Please answer in the following format.
Video description: <description>
Matching score: <score>
"""


class GeminiCaptioner(Captioner):
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        self.prompt = prompt or DEFAULT_PROMPT
        self.model_name = model_name or "gemini-1.5-flash"
        gemini_api_key = api_key or os.getenv("GEMINI_API_KEY")
        if gemini_api_key is None:
            raise ValueError("GEMINI_API_KEY is not set")
        genai.configure(api_key=gemini_api_key)

    def caption(self, video_path: str) -> tuple[str, float]:
        model = genai.GenerativeModel(self.model_name)

        video_file = genai.upload_file(path=video_path)
        while video_file.state.name == "PROCESSING":
            time.sleep(0.5)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(f"Video file processing failed: {video_file.state.name}")

        response = model.generate_content(
            [video_file, self.prompt], request_options={"timeout": 600}
        )
        generated_text = response.text
        video_description = re.search(r"Video description: (.+)", generated_text).group(
            1
        )
        matching_score = (
            int(re.search(r"Matching score: (\d+)", generated_text).group(1)) / 100
        )
        return video_description, matching_score
