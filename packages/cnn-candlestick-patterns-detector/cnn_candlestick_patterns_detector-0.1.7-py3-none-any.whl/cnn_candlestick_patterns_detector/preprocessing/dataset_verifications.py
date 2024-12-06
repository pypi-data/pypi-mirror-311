import os


def check_consistency(directory):
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            _check_files(subdir_path)


def _check_files(directory):
    all_files = os.listdir(directory)
    file_pairs = {}

    for filename in all_files:
        if filename.endswith("_config.json"):
            key = filename.replace("_config.json", "")
            file_pairs.setdefault(key, {})['conf'] = filename

    errors = []
    print(f'{directory}')
    for key, files in file_pairs.items():
        conf_exists = 'conf' in files
        if not conf_exists:
            errors.append(f"Error: Object '{key}' is missing " +
                          ("'.conf.json'" if not conf_exists else ""))

    if errors:
        for error in errors:
            print(error)
    else:
        print("All objects have complete file pairs.")
