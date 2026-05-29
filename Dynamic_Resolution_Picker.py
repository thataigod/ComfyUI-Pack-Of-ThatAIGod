import torch
import math
import random

class DynamicResolution:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        ratio_options = [
            "Random (Any)", 
            "Random (Portrait)", 
            "Random (Landscape)",
            "Square 1:1",
            "Portrait 2:3 (Classic)", 
            "Portrait 3:4 (Standard)", 
            "Portrait 4:5 (Social)", 
            "Portrait 9:16 (Mobile)", 
            "Landscape 3:2 (Classic)", 
            "Landscape 4:3 (Standard)", 
            "Landscape 5:4 (Display)", 
            "Landscape 16:9 (HD)", 
            "Landscape 16:10 (Monitor)",
            "Landscape 21:9 (Ultrawide)",
            "Landscape 1.85:1 (Cinema)"
        ]
        
        return {
            "required": {
                "Max Side Pixels": ("INT", {"default": 1024, "min": 256, "max": 16384, "step": 8}),
                "Aspect Ratio": (ratio_options, {"default": "Square 1:1"}),
                "Scale Factor": ("FLOAT", {"default": 1.5, "min": 0.1, "max": 8.0, "step": 0.05}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "FLOAT", "STRING", "INT", "INT")
    RETURN_NAMES = ("Width", "Height", "Scaled Width", "Scaled Height", "Scale Factor", "Keywords", "Guide Size", "Max Size")
    FUNCTION = "calculate"
    CATEGORY = "ThatAIGod/Image Utils"

    def calculate(self, **kwargs):
        # Kwargs consistency
        max_side = kwargs.get("Max Side Pixels", 1024)
        aspect_ratio_label = kwargs.get("Aspect Ratio", "Square 1:1")
        scale_factor = kwargs.get("Scale Factor", 1.5)
        seed = kwargs.get("seed", 0) 
        
        rng = random.Random(seed)
        
        portraits = {
            "Portrait 2:3 (Classic)": 2/3, 
            "Portrait 3:4 (Standard)": 3/4, 
            "Portrait 4:5 (Social)": 4/5, 
            "Portrait 9:16 (Mobile)": 9/16
        }
        landscapes = {
            "Landscape 3:2 (Classic)": 3/2, 
            "Landscape 4:3 (Standard)": 4/3, 
            "Landscape 5:4 (Display)": 5/4, 
            "Landscape 16:9 (HD)": 16/9, 
            "Landscape 16:10 (Monitor)": 16/10,
            "Landscape 21:9 (Ultrawide)": 21/9,
            "Landscape 1.85:1 (Cinema)": 1.85
        }
        square = {"Square 1:1": 1.0}

        keyword_map = {
            "Square 1:1": "Square, 1:1 Aspect Ratio, Boxed Composition",
            "Portrait 2:3 (Classic)": "Portrait, 2:3 Aspect Ratio, Vertical Orientation",
            "Portrait 3:4 (Standard)": "Portrait, 3:4 Aspect Ratio, Vertical Format",
            "Portrait 4:5 (Social)": "Portrait, 4:5 Aspect Ratio, Vertical Composition",
            "Portrait 9:16 (Mobile)": "Portrait, 9:16 Aspect Ratio, Full Screen Vertical",
            "Landscape 3:2 (Classic)": "Landscape, 3:2 Aspect Ratio, Horizontal Orientation",
            "Landscape 4:3 (Standard)": "Landscape, 4:3 Aspect Ratio, Standard View",
            "Landscape 5:4 (Display)": "Landscape, 5:4 Aspect Ratio, Wide Format",
            "Landscape 16:9 (HD)": "Landscape, 16:9 Aspect Ratio, Widescreen Format",
            "Landscape 16:10 (Monitor)": "Landscape, 16:10 Aspect Ratio, Wide Display",
            "Landscape 21:9 (Ultrawide)": "Landscape, 21:9 Aspect Ratio, Ultra-Wide Panoramic",
            "Landscape 1.85:1 (Cinema)": "Landscape, 1.85:1 Aspect Ratio, Theatrical Format"
        }
        
        target_label = aspect_ratio_label
        ratio_float = 1.0
        
        if "Random" in aspect_ratio_label:
            if aspect_ratio_label == "Random (Portrait)":
                target_label, ratio_float = rng.choice(sorted(list(portraits.items())))
            elif aspect_ratio_label == "Random (Landscape)":
                target_label, ratio_float = rng.choice(sorted(list(landscapes.items())))
            else: 
                all_ratios = {**portraits, **landscapes, **square}
                target_label, ratio_float = rng.choice(sorted(list(all_ratios.items())))
        else:
            all_known = {**portraits, **landscapes, **square}
            if target_label in all_known:
                ratio_float = all_known[target_label]
            else:
                ratio_float = 1.0
                target_label = "Square 1:1"

        keywords = keyword_map.get(target_label, f"{target_label}, Aspect Ratio")

        if ratio_float > 1.0: 
            width = max_side
            height = max_side / ratio_float
        elif ratio_float < 1.0:
            height = max_side
            width = max_side * ratio_float
        else:
            width = max_side
            height = max_side

        width = int(round(width / 8) * 8)
        height = int(round(height / 8) * 8)
        width = max(width, 64)
        height = max(height, 64)

        guide_size = min(width, height)
        max_size_val = max(width, height)

        s_width = width * scale_factor
        s_height = height * scale_factor
        scaled_width = int(round(s_width / 8) * 8)
        scaled_height = int(round(s_height / 8) * 8)

        actual_mp = (width * height) / 1000000
        
        info_string = (
            f"Mode:   {target_label}\n"
            f"Base:   {width}x{height} ({actual_mp:.2f} MP)\n"
            f"Scaled: {scaled_width}x{scaled_height} (x{scale_factor})\n"
            f"Keywords: {keywords}"
        )

        return {
            "ui": {
                "text": [info_string],
                "width": [width],
                "height": [height],
                "scaled_width": [scaled_width],
                "scaled_height": [scaled_height],
                "scale_factor": [scale_factor],
                "guide_size": [guide_size],
                "max_size": [max_size_val]
            }, 
            "result": (width, height, scaled_width, scaled_height, scale_factor, keywords, guide_size, max_size_val)
        }

NODE_CLASS_MAPPINGS = {
    "DynamicResolution": DynamicResolution
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicResolution": "Dynamic Resolution Picker"
}