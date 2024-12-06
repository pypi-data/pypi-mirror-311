import json
import os


def calculate_statistic(directory):
    results = {}
    total_count = 0

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            config_count = 0
            for file in os.listdir(subdir_path):
                if file.endswith("_config.json"):
                    config_count += 1
            results[subdir] = config_count
            total_count += config_count

    for subdir, count in sorted(results.items(), key=lambda x: x[0]):
        percentage = (count / total_count * 100) if total_count > 0 else 0
        print(f"{subdir}: {count}, {percentage:.2f}%")

    print(f"Total Count: {total_count}")

    return results

def update_probabilities(directory):
    for subdir in os.listdir(directory):
        probability = float(subdir.split('_')[-1])

        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                if file.endswith('_config.json'):
                    file_path = os.path.join(subdir_path, file)
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                    if data and isinstance(data, list):
                        for item in data:
                            item['probability'] = probability
                    with open(file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)