import torch
import comfy.utils

class UpscaleByMaxSide:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Image": ("IMAGE",),
                "Max Side": ("INT", {"default": 1024, "min": 64, "max": 16384, "step": 8}),
                "Divisibility": ("INT", {"default": 8, "min": 1, "max": 128, "step": 1}),
                "Method": (["lanczos", "bicubic", "bilinear", "nearest-exact", "area"], {"default": "lanczos"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("Image", "Width", "Height")
    FUNCTION = "upscale"
    CATEGORY = "ThatAIGod/Image Utils"

    def upscale(self, **kwargs):
        image = kwargs.get("Image")
        max_side = kwargs.get("Max Side", 1024)
        divisibility = kwargs.get("Divisibility", 8)
        method = kwargs.get("Method", "lanczos")

        # Image is [Batch, Height, Width, Channels]
        _, h, w, _ = image.shape
        
        # 1. Calculate Scaling Ratio preserving aspect ratio
        ratio = w / h

        if w > h:
            scale_w = max_side
            scale_h = int(max_side / ratio)
        else:
            scale_h = max_side
            scale_w = int(max_side * ratio)

        # 2. Upscale
        # Move channels to [Batch, Channels, Height, Width] for pytorch interpolation
        samples = image.movedim(-1, 1)
        
        # crop="disabled" ensures we resize strictly by dimensions first
        s = comfy.utils.common_upscale(samples, scale_w, scale_h, method, "disabled")
        
        # Move channels back to [Batch, Height, Width, Channels]
        s = s.movedim(1, -1)

        # 3. Calculate Divisible Target Dimensions (Round Down)
        target_w = (scale_w // divisibility) * divisibility
        target_h = (scale_h // divisibility) * divisibility

        # Ensure we don't round down to 0
        target_w = max(target_w, divisibility)
        target_h = max(target_h, divisibility)

        # 4. Center Crop if dimensions differ
        if target_w != scale_w or target_h != scale_h:
            # Calculate start points for centering
            h_start = (scale_h - target_h) // 2
            w_start = (scale_w - target_w) // 2
            
            # Slice the tensor: [Batch, H, W, C]
            # We add target dimensions to start points
            s = s[:, h_start:h_start + target_h, w_start:w_start + target_w, :]

        return (s, target_w, target_h)

NODE_CLASS_MAPPINGS = {
    "UpscaleByMaxSide": UpscaleByMaxSide
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UpscaleByMaxSide": "Upscale By Max Side"
}