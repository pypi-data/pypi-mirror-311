import os
import random

from PIL import Image


def create_image_grid(input_dir, image_name, canvas_width=3800, canvas_height=2100, spacing=2,
                      img_scale_factor=4):
    input_dir = f'{input_dir}//{image_name}'
    results_folder = 'out/visualization_image_grid/'
    os.makedirs(results_folder, exist_ok=True)
    if os.path.exists(input_dir):
        files = [file for file in os.listdir(input_dir) if file.endswith('.png')]
        sample_img = Image.open(os.path.join(input_dir, files[0]))
        img_width, img_height = sample_img.size
        img_width //= img_scale_factor
        img_height //= img_scale_factor
        cols = (canvas_width + spacing) // (img_width + spacing)
        rows = (canvas_height + spacing) // (img_height + spacing)
        total_images_needed = cols * rows
        selected_files = random.sample(files, min(len(files), total_images_needed))
        resized_images = [Image.open(os.path.join(input_dir, file)).resize((img_width, img_height)) for file in
                          selected_files]
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'black')
        for index, img in enumerate(resized_images):
            row = index // cols
            col = index % cols
            x = col * (img_width + spacing)
            y = row * (img_height + spacing)
            canvas.paste(img, (x, y))

        output_path = os.path.join(results_folder, f'{image_name}.png')
        canvas.save(output_path)
        print(f'Saved image grid to {output_path}')
