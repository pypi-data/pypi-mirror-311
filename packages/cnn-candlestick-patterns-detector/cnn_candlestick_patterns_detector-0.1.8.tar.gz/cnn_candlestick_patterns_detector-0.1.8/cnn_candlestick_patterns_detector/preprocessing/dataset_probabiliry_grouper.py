import shutil
from pathlib import Path


def group_by_probability(source_dir, target_dir, interval=0.05):
    target_dir = Path(target_dir)
    source_dir = Path(source_dir)

    target_dir.mkdir(parents=True, exist_ok=True)

    subdirs = [d for d in source_dir.iterdir() if d.is_dir() and d.name.startswith('p_')]

    for subdir in subdirs:
        try:
            value = float(subdir.name[2:])
            rounded_value = round(value / interval) * interval
            rounded_dir_name = f'p_{rounded_value:.2f}'

            target_subdir = target_dir / rounded_dir_name
            target_subdir.mkdir(exist_ok=True)

            for item in subdir.iterdir():
                shutil.copy(str(item), target_subdir)
        except ValueError:
            print(f"Ошибка в имени папки: {subdir.name}")


group_by_probability('//searching/out/findings_soft_multiple_model_CNN',
                     '//searching/out/GROUPED')
