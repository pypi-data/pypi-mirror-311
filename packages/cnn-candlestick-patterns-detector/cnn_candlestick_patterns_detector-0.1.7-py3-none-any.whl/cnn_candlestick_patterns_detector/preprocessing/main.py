from cnn_candlestick_patterns_detector.preprocessing.dataset_archive_operations import unpack_archive, group_by_probability
from cnn_candlestick_patterns_detector.preprocessing.dataset_calculations import calculate_statistic
from cnn_candlestick_patterns_detector.preprocessing.dataset_verifications import check_consistency

# target_class = 'softlabels_class_5'
for target_class in ['softlabels_class_0', 'softlabels_class_1', 'softlabels_class_2', 'softlabels_class_3', 'softlabels_class_4', 'softlabels_class_5']:
    archive_path = f'/\\s7\\datasets\\{target_class}.7z'
    extracted_dir = unpack_archive(archive_path)
    # fix_json_files(extracted_dir)
    # remove_duplicates(extracted_dir)
    # generate_chart(extracted_dir)
    # transform_candles_to(extracted_dir, 'inverted_reverse_candles')
    group_by_probability(extracted_dir)
    check_consistency(extracted_dir)
    calculate_statistic(extracted_dir)


# extract_path = f'D:\\WORK\\cnn_candlestick_patterns_detector\\s7\\data_provider\\data\\{target_class}'
# check_consistency(extract_path)
# update_probabilities(extract_path)
# calculate_statistic(extract_path)
# repack_archive(extract_path)

# root_folder = f'D:\WORK\cnn_candlestick_patterns_detector\s7\data_provider\data\softlabels_class_1'
# create_image_grid(root_folder, 'p_0.90')
# create_image_grid(root_folder, 'p_0.85')
# create_image_grid(root_folder, 'p_0.80')
# create_image_grid(root_folder, 'p_0.75')
# create_image_grid(root_folder, 'p_0.70')
# create_image_grid(root_folder, 'p_0.65')
# create_image_grid(root_folder, 'p_0.60')
# create_image_grid(root_folder, 'p_0.55')
# create_image_grid(root_folder, 'p_0.50')
# create_image_grid(root_folder, 'p_0.45')
# create_image_grid(root_folder, 'p_0.40')
# create_image_grid(root_folder, 'p_0.35')
# create_image_grid(root_folder, 'p_0.30')
# create_image_grid(root_folder, 'p_0.25')
# create_image_grid(root_folder, 'p_0.20')
# create_image_grid(root_folder, 'p_0.15')
# create_image_grid(root_folder, 'p_0.10')
# create_image_grid(root_folder, 'p_0.05')
# create_image_grid(root_folder, 'p_0.00')