import re

class TruncateThinking:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Text": ("STRING", {"forceInput": True}),
                "Start Token": ("STRING", {"default": "<think>", "multiline": False}),
                "End Token": ("STRING", {"default": "</think>", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Cleaned Text", "Thinking Content")
    FUNCTION = "truncate"
    CATEGORY = "ThatAIGod/Text Utils"

    def truncate(self, **kwargs):
        text = kwargs.get("Text", "")
        start_token = kwargs.get("Start Token", "<think>")
        end_token = kwargs.get("End Token", "</think>")

        if not text:
            return ("", "")

        # 1. Construct Regex
        # re.escape ensures that if user uses special chars like '[', it doesn't break regex
        # (.*?) matches any character (non-greedy) until the end token
        # flags=re.DOTALL ensures that '.' matches newlines, allowing multi-line thoughts
        pattern = re.compile(
            re.escape(start_token) + r"(.*?)" + re.escape(end_token),
            flags=re.DOTALL
        )

        # 2. Extract Thinking Content
        # findall returns a list of all matches (in case model hallucinated multiple think blocks)
        thoughts_found = pattern.findall(text)
        thinking_content = "\n\n".join(thoughts_found).strip()

        # 3. Remove Thinking Content to get Clean Text
        cleaned_text = pattern.sub("", text).strip()

        return (cleaned_text, thinking_content)

NODE_CLASS_MAPPINGS = {
    "TruncateThinking": TruncateThinking
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TruncateThinking": "Truncate LLM Thinking"
}