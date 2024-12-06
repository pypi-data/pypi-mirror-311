import json
import os
import random
import shutil
import string

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import shap
from PIL import Image, ImageDraw, ImageFont
from mplfinance.original_flavor import candlestick_ohlc

matplotlib.use('Agg')


def save_prediction_error_analysis(all_predictions, all_targets, folder, file_name, tolerance=0.1):
    all_predictions = all_predictions.flatten()
    all_targets = all_targets.flatten()

    errors_dict = {}
    all_cases_dict = {}

    for pred, target in zip(all_predictions, all_targets):
        target_str = f"{target:.2f}"

        if target_str not in all_cases_dict:
            all_cases_dict[target_str] = 0
        all_cases_dict[target_str] += 1

        if not (target - tolerance <= pred <= target + tolerance):
            error = abs(pred - target)
            if target_str not in errors_dict:
                errors_dict[target_str] = []
            errors_dict[target_str].append(error)

    target_values = sorted(all_cases_dict.keys(), key=float)
    error_percentages = [len(errors_dict.get(t, [])) / all_cases_dict[t] * 100 for t in target_values]
    error_medians = [np.median(errors_dict[t]) if t in errors_dict else 0 for t in target_values]
    example_counts = [all_cases_dict[t] for t in target_values]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 18), sharex=True)

    ax1.bar(target_values, error_percentages, color='blue', label='Percentage of Errors')
    ax1.set_ylabel('Percentage of Errors (%)')
    ax1.set_ylim(0, 100)
    ax1.set_title('Percentage of Errors per Target Value')
    ax1.grid(True)

    ax2.bar(target_values, error_medians, color='red', label='Median Error')
    ax2.set_ylabel('Median Error')
    ax2.set_ylim(0, max(error_medians) + 0.1)
    ax2.set_title('Median Error per Target Value')
    ax2.grid(True)

    ax3.bar(target_values, example_counts, color='green', label='Number of Examples')
    ax3.set_xlabel('Target Value')
    ax3.set_ylabel('Number of Examples')
    ax3.set_title('Number of Examples per Target Value')
    ax3.grid(True)

    ax1.legend()
    ax2.legend()
    ax3.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(folder, file_name))
    plt.close()

def save_shap_summary(shap_values, folder, file_name):
    num_features = shap_values.shape[1]
    feature_names = [
        f"mid_changes_{i}" if 0 <= i < 7 else
        f"top_deviation_{i}" if 7 <= i < 14 else
        f"bottom_deviation_{i}" if 14 <= i < 21 else
        f"high_deviation_{i}" if 21 <= i < 28 else
        f"low_deviation_{i}" if 28 <= i < 35 else
        f"direction_{i}" for i in range(num_features)
    ]

    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, feature_names=feature_names, show=False,  max_display=num_features)
    plt.savefig(os.path.join(folder, file_name), bbox_inches='tight')
    plt.close()

def save_calculate_calibration_curve(y_true_prob, y_pred_prob, folder, file_name, n_bins=20):
    bins = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_pred_prob, bins) - 1

    prob_true = []
    prob_pred = []

    for i in range(n_bins):
        if np.any(bin_indices == i):
            prob_true.append(y_true_prob[bin_indices == i].mean())
            prob_pred.append(y_pred_prob[bin_indices == i].mean())

    prob_true = np.array(prob_true)
    prob_pred = np.array(prob_pred)

    plt.figure(figsize=(8, 6))
    plt.plot(prob_pred, prob_true, marker='o', label='Calibration curve')
    plt.plot([0, 1], [0, 1], linestyle='--', color='grey', label='Perfectly calibrated')
    plt.xlabel('Mean predicted probability')
    plt.ylabel('True probability in each bin')
    plt.title('Calibration Curve')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(folder, file_name))
    plt.close()


def save_candlestick_chart(ohlc_data, folder, filename):
    fig, ax = plt.subplots()
    ohlc_array = [(i, entry['open'], entry['high'], entry['low'], entry['close']) for i, entry in
                  enumerate(ohlc_data)]
    candlestick_ohlc(ax, ohlc_array, width=0.6, colorup='green', colordown='red', alpha=1)
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(os.path.join(folder, filename.replace('.json', '.png')), bbox_inches='tight', pad_inches=0)
    plt.close()


def save_data_to_json(data, folder, filename):
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f)


def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def set_up_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)


def save_multiple_line_plots(normalized_series, folder, filename):
    sns.set(style="whitegrid")
    num_series = normalized_series.shape[0]
    fig, axes = plt.subplots(nrows=num_series, ncols=1, figsize=(10, 2 * num_series), dpi=100)
    if num_series == 1:
        axes = [axes]

    for i, ax in enumerate(axes):
        sns.lineplot(data=normalized_series[i], marker='o', ax=ax, linewidth=2)
        ax.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, filename), bbox_inches='tight', pad_inches=0)
    plt.close()


def create_image_grid(directory):
    # Получаем список файлов PNG из директории
    files = [f for f in os.listdir(directory) if f.endswith('.png')]

    # Проверяем, что файлов хотя бы 4
    if len(files) < 4:
        print("Нужно хотя бы 4 .png файла в директории.")
        return

    # Открываем изображения
    images = [Image.open(os.path.join(directory, file)) for file in files[:4]]

    # Получаем размер изображения
    img_width, img_height = images[0].size

    # Создаем новое изображение для грид-компоновки
    grid_img = Image.new('RGB', (img_width * 2, img_height * 2 + 40), color='white')  # плюс место для текста

    # Загрузка шрифта для подписей (можно настроить путь к шрифту)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Рисуем границы и вставляем изображения
    draw = ImageDraw.Draw(grid_img)

    for i, img in enumerate(images):
        x = (i % 2) * img_width
        y = (i // 2) * (img_height + 40)

        # Вставляем изображение в грид
        grid_img.paste(img, (x, y + 40))

        # Добавляем черную линию-границу
        draw.rectangle([x, y + 40, x + img_width, y + img_height + 40], outline='black', width=5)

        # Добавляем подпись с названием файла
        filename = files[i]
        bbox = draw.textbbox((0, 0), filename, font=font)  # определяем размер текста
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x + (img_width - text_width) / 2, y + 10), filename, font=font, fill='black')

    # Сохраняем итоговое изображение
    grid_img.save(os.path.join(directory, 'grid_image.png'))
    print(f"Грид-изображение сохранено в {directory}")