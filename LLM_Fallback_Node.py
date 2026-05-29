class LLM_Fallback_Node:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # We always need the original text to fall back to
                "Original Input": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # These are optional so the node runs even if LLM is bypassed/disconnected
                "Generated Text": ("STRING", {"forceInput": True}),
                "Status (Boolean)": ("BOOLEAN", {"default": False}), 
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Final Text",)
    FUNCTION = "switch"
    CATEGORY = "ThatAIGod/LLM"

    def switch(self, **kwargs):
        # Safe extraction with defaults
        generated_text = kwargs.get("Generated Text", "")
        original_input = kwargs.get("Original Input", "")
        status = kwargs.get("Status (Boolean)", False)

        # Handle None explicitly (which can happen if a node is bypassed)
        if generated_text is None: 
            generated_text = ""
        if status is None: 
            status = False

        # Logic: Only use Generated Text if Status is True AND text is valid
        if status and generated_text and generated_text.strip():
            return (generated_text,)
        else:
            # Fallback for: Bypassed Node, Error in LLM, or Empty Result
            return (original_input,)