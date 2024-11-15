from diffusers import StableDiffusionPipeline
import torch
import numpy

# Tải mô hình Stable Diffusion
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

pipe = pipe.to("cuda")  # Sử dụng GPU nếu có

if torch.cuda.is_available():
    print("CUDA is available!")
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("CUDA Version:", torch.version.cuda)
    print("CuDNN Version:", torch.backends.cudnn.version())
else:
    print("CUDA is not available. PyTorch is running on CPU.")

def generate_image(prompt):
        with torch.autocast("cuda"):
            image = pipe(prompt).images[0]
        return image
