import json
import os
import shutil

import py7zr


def unpack_archive(archive_path):
    print(f'unpack archive {archive_path}')
    archive_dir = os.path.dirname(archive_path)
    archive_name = os.path.splitext(os.path.basename(archive_path))[0]
    extract_dir = os.path.join(archive_dir, archive_name)

    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)

    os.makedirs(extract_dir)

    with py7zr.SevenZipFile(archive_path, mode='r') as z:
        z.extractall(path=extract_dir)

    return extract_dir


def repack_archive(extract_dir):
    archive_name = os.path.basename(extract_dir) + ".7z"
    archive_path = os.path.join(os.path.dirname(extract_dir), archive_name)
    print(f'Repacking archive from {extract_dir} to {archive_path}')

    if os.path.exists(archive_path):
        os.remove(archive_path)

    with py7zr.SevenZipFile(archive_path, mode='w') as z:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if not file.endswith('.png'):
                    file_path = os.path.join(root, file)
                    z.write(file_path, os.path.basename(file_path))

def group_by_probability(output_folder, conf_suffix="_config.json"):
    config_files = [f for f in os.listdir(output_folder) if f.endswith(conf_suffix)]

    for conf_filename in config_files:
        conf_file_path = os.path.join(output_folder, conf_filename)
        base_filename = conf_filename.replace(conf_suffix, '')

        probability = _get_probability(conf_file_path)
        if probability is not None:
            target_folder = f"p_{probability}"
            target_folder_path = os.path.join(output_folder, target_folder)

            os.makedirs(target_folder_path, exist_ok=True)

            shutil.move(conf_file_path, os.path.join(target_folder_path, conf_filename))
            png_file = os.path.join(output_folder, base_filename + '.png')
            if os.path.exists(png_file):
                shutil.move(os.path.join(output_folder, base_filename + '.png'),
                        os.path.join(target_folder_path, base_filename + '.png'))
            shutil.move(os.path.join(output_folder, base_filename + '.json'),
                        os.path.join(target_folder_path, base_filename + '.json'))


def _get_probability(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    if data and "probability" in data[0]:
        return "{:.2f}".format(data[0]["probability"])
    return None