import os
import shutil

dest_dir = r"/\s7\data_provider\data\softlabels_class_1\p_0.45"
source_dir = r"/\s7\data_preprocessing\out\dataset_checking"

png_files = [f for f in os.listdir(dest_dir) if f.endswith('.png')]

for png_file in png_files:
    base_name = os.path.splitext(png_file)[0]
    config_file = f"{base_name}_config.json"
    json_file = f"{base_name}.json"
    png_file = f"{base_name}.png"

    source_config_path = os.path.join(source_dir, config_file)
    dest_config_path = os.path.join(dest_dir, config_file)
    if os.path.exists(source_config_path):
        shutil.move(source_config_path, dest_config_path)
        print(f"Перенесен файл: {config_file}")

    source_json_path = os.path.join(source_dir, json_file)
    dest_json_path = os.path.join(dest_dir, json_file)
    if os.path.exists(source_json_path):
        shutil.move(source_json_path, dest_json_path)
        print(f"Перенесен файл: {json_file}")

    source_png_path = os.path.join(source_dir, png_file)
    dest_png_path = os.path.join(dest_dir, png_file)
    if os.path.exists(source_png_path):
        shutil.move(source_png_path, dest_png_path)
        print(f"Перенесен файл: {png_file}")
