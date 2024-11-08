from diffusers import StableDiffusionPipeline
# from transformers import MarianMTModel, MarianTokenizer
import torch

# model_name = 'Helsinki-NLP/opus-mt-vi-en'
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)

# Tải mô hình Stable Diffusion
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

pipe = pipe.to("cuda")  # Sử dụng GPU nếu có

def generate_image(prompt):
        with torch.autocast("cuda"):
            image = pipe(prompt).images[0]
        return image


# Kiểm tra xem CUDA có khả dụng không
# device = "cuda" if torch.cuda.is_available() else "cpu"
# pipe = pipe.to(device)

# def generate_image(prompt):
#     # Sử dụng autocast nếu chạy trên GPU
#     if device == "cuda":
#         with torch.autocast("cuda"):
#             image = pipe(prompt).images[0]
#     else:
#         image = pipe(prompt).images[0]  # Không sử dụng autocast trên CPU
#     return image