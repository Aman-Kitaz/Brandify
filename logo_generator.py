import torch
import uuid
import os
from diffusers import DiffusionPipeline
from PIL import Image

class LogoGenerator:
    def __init__(self):
        # Determine device (GPU or CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load Stage 1 Model
        self.stage_1 = DiffusionPipeline.from_pretrained(
            "DeepFloyd/IF-I-XL-v1.0",
            variant="fp16",
            torch_dtype=torch.float16,
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to(self.device)
        
        # Enable memory optimizations
        self.stage_1.enable_model_cpu_offload()
        self.stage_1.enable_attention_slicing()

        # Load Stage 2 Model
        self.stage_2 = DiffusionPipeline.from_pretrained(
            "DeepFloyd/IF-II-L-v1.0",
            variant="fp16",
            torch_dtype=torch.float16,
            text_encoder=None,
            use_safetensors=True,
            low_cpu_mem_usage=True
        ).to(self.device)
        
        # Enable memory optimizations
        self.stage_2.enable_model_cpu_offload()
        self.stage_2.enable_attention_slicing()

        # Ensure logos directory exists
        os.makedirs('static/logos', exist_ok=True)

    def generate(self, prompt, brand_name=None):
        try:
            # Set random seed for reproducibility
            generator = torch.Generator(self.device).manual_seed(0)
            
            # Generate unique filename
            if brand_name:
                # Use brand name in filename if provided
                safe_brand_name = "".join(x for x in brand_name if x.isalnum() or x in [' ', '_'])
                safe_brand_name = safe_brand_name.replace(' ', '_')
                logo_filename = f"static/logos/{safe_brand_name}_{uuid.uuid4()}.png"
            else:
                logo_filename = f"static/logos/{uuid.uuid4()}.png"

            # Print generation details
            print(f"Starting logo generation for prompt: {prompt}")
            print(f"Logo will be saved as: {logo_filename}")

            # Encode prompt
            prompt_embeds, negative_embeds = self.stage_1.encode_prompt(prompt)

            # Stage 1: Base Image Generation
            print("Stage 1: Generating base image...")
            stage_1_result = self.stage_1(
                prompt_embeds=prompt_embeds,
                negative_prompt_embeds=negative_embeds,
                generator=generator,
                output_type="pt"
            )

            # Stage 2: Upscaling and Refinement
            print("Stage 2: Upscaling and adding details...")
            stage_2_result = self.stage_2(
                image=stage_1_result.images,
                prompt_embeds=prompt_embeds,
                negative_prompt_embeds=negative_embeds,
                generator=generator,
                output_type="pt"
            )

            # Convert and save image
            logo_image = Image.fromarray(
                (stage_2_result.images[0].cpu().numpy().transpose(1, 2, 0) * 255).astype("uint8")
            )
            logo_image.save(logo_filename)

            print("Logo generated successfully")
            return logo_filename

        except Exception as e:
            print(f"Logo generation error: {e}")
            import traceback
            traceback.print_exc()
            return None