from cnn_candlestick_patterns_detector.preprocessing.cnn_soft_labels_dataset_checker import CNNSoftLabelsDatasetChecker
from cnn_candlestick_patterns_detector.preprocessing.dataset_orginizer import compare_and_delete
from cnn_candlestick_patterns_detector.s7.architecture.candles_patterns_7 import CandlesPatterns_7

target_probability = '0.85'
target_class = 'softlabels_class_1'

CNNSoftLabelsDatasetChecker(
    model_type=CandlesPatterns_7,
    models_paths=[
        "../s7/models/softlabels_class_1/CandlesPatterns_7_46cc9cc0-13fe-477a-b64a-228ba41d7994.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_67d2082a-a328-4639-a8d4-851cb290cd73.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_549b5b35-ce68-4b5f-92ac-387939dd43f4.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_56369c65-1943-430a-94df-775594a0f5eb.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_b34220e3-3d78-4ef9-8176-442daefda696.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_c65aae4f-e0c5-4cf5-af0e-0df55f4c31f9.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_c827f143-b993-4364-b07e-a9e2754c23e4.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_c9907b91-9f64-4edb-8e36-14c13e3bcada.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_d528c8d6-f97a-4e64-b8d0-a8120fecddeb.pth",
      "../s7/models/softlabels_class_1/CandlesPatterns_7_eb2ddacf-c347-4422-ac14-82e025c0d6ed.pth"
    ],
    dataset_path=f'/datasets/{target_class}.7z',
    target_probability=target_probability,
    threshold=0.1
).check_and_save()

compare_and_delete(f'D:\WORK\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\s7\out\dataset_checking',
                    f'D:\WORK\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\s7\datasets\\{target_class}\p_{target_probability}')


