from .Dynamic_Resolution_Picker import NODE_CLASS_MAPPINGS as DYN_CLASS, NODE_DISPLAY_NAME_MAPPINGS as DYN_DISPLAY
from .Wildcard_Reader import NODE_CLASS_MAPPINGS as WILD_CLASS, NODE_DISPLAY_NAME_MAPPINGS as WILD_DISPLAY
from .LLM_Node import LLM_Node
from .LLM_Fallback_Node import LLM_Fallback_Node
from .Sequential_Image_Loader import NODE_CLASS_MAPPINGS as SEQ_CLASS, NODE_DISPLAY_NAME_MAPPINGS as SEQ_DISPLAY
from .Truncate_LLM_Thinking import NODE_CLASS_MAPPINGS as TRUNC_CLASS, NODE_DISPLAY_NAME_MAPPINGS as TRUNC_DISPLAY
from .Upscale_By_Max_Side import NODE_CLASS_MAPPINGS as UP_CLASS, NODE_DISPLAY_NAME_MAPPINGS as UP_DISPLAY

# Manual mappings for LLM nodes
LLM_CLASS = {
    "LLM_Node": LLM_Node,
    "LLM_Fallback_Node": LLM_Fallback_Node
}
LLM_DISPLAY = {
    "LLM_Node": "LLM Chat (OpenRouter/Local)",
    "LLM_Fallback_Node": "LLM Fallback Switch"
}

# Combine all mappings
NODE_CLASS_MAPPINGS = {
    **DYN_CLASS, 
    **WILD_CLASS, 
    **LLM_CLASS, 
    **SEQ_CLASS, 
    **TRUNC_CLASS,
    **UP_CLASS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **DYN_DISPLAY, 
    **WILD_DISPLAY, 
    **LLM_DISPLAY, 
    **SEQ_DISPLAY, 
    **TRUNC_DISPLAY,
    **UP_DISPLAY
}

# Import the JS files automatically
WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print("------------------------------------")
print("✅ ComfyUI-Pack-Of-ThatAIGod loaded.")
print("------------------------------------")