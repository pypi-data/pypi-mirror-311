# CNN Candlestick Patterns Detector
This repository implements a Convolutional Neural Network (CNN) based solution for recognizing candlestick patterns in financial markets. The model identifies specific patterns formed by candlestick sequences, offering insights into potential market movements.

## Project Overview
The CNN model analyzes sequences of 7 consecutive candlesticks and detects recognizable patterns that can indicate various market conditions. This repository includes tools for dataset management, model training, and pattern detection, with support for remote GPU servers for faster training.

## Key Features:
* CNN-based Pattern Detection: Optimized for identifying patterns in candlestick data.
* Complete Dataset Management: Tools for dataset creation, updates, and efficient searching. 
* Training and Testing Pipeline: Integrated training and validation setup. 
* Remote Server GPU Training: Includes a script for setting up a GPU server to accelerate training.

## Installation
To install the project, first download the package:

```aiignore
pip install cnn_candlestick_patterns_detector
```

## Example Usage
Here’s an example of how to use the model to classify candlestick data:

```aiignore
from s7.cnn_soft_labels_multiclass_classifier import CNNSoftLabelsMulticlassClassifierS7

# Initialize classifier with config
cnn_classifier = CNNSoftLabelsMulticlassClassifierS7(
    config_path='models_config.json'
)

# Example candlestick data
data = [
    {"datetime": "2022-07-20 20:59:00", "open": 17.542, "high": 17.555, "low": 17.54, "close": 17.542, "volume": 720650},
    {"datetime": "2022-07-20 21:00:00", "open": 17.544, "high": 17.595, "low": 17.538, "close": 17.5759, "volume": 1764380.0},
    {"datetime": "2022-07-20 21:01:00", "open": 17.5745, "high": 17.59, "low": 17.568, "close": 17.585, "volume": 773420},
    {"datetime": "2022-07-20 21:02:00", "open": 17.5852, "high": 17.59, "low": 17.575, "close": 17.586, "volume": 629650},
    {"datetime": "2022-07-20 21:03:00", "open": 17.586, "high": 17.615, "low": 17.586, "close": 17.61, "volume": 1592680.0},
    {"datetime": "2022-07-20 21:04:00", "open": 17.612, "high": 17.628, "low": 17.605, "close": 17.626, "volume": 937160},
    {"datetime": "2022-07-20 21:05:00", "open": 17.6269, "high": 17.64, "low": 17.616, "close": 17.621, "volume": 1110960.0}
]

# Classify the data and print the resulting vector
vector = cnn_classifier.classify_2d(data)
print(vector)

```
## Configuration Example

Below is an example of the model configuration file (models_config.json) that defines the model paths for each class:

```aiignore
{
  "class_0": {
    "models_paths": [
      "models/softlabels_class_0/CandlesPatterns_7_1e8b48a1-b104-4a56-85fb-d3876957ae3c.pth",
      "models/softlabels_class_0/CandlesPatterns_7_6a6cae5e-1f60-4108-b039-fedfce2ea334.pth",
      "models/softlabels_class_0/CandlesPatterns_7_07a3e3cc-664a-4d33-a757-9d2da2859283.pth",
      "models/softlabels_class_0/CandlesPatterns_7_9da7d35e-5cdb-476d-873a-647d528de214.pth",
      "models/softlabels_class_0/CandlesPatterns_7_13041449-abaf-477b-a788-4e9f1c42695b.pth",
      "models/softlabels_class_0/CandlesPatterns_7_b804bd78-e74f-4620-8eaf-e710e853a96c.pth",
      "models/softlabels_class_0/CandlesPatterns_7_cd4617c1-e08f-4430-a446-9f62f997d556.pth",
      "models/softlabels_class_0/CandlesPatterns_7_ce3900d5-3270-401d-9cd4-ef11ac4a324c.pth",
      "models/softlabels_class_0/CandlesPatterns_7_e2e05bd7-456b-4ae2-bef6-0bba87a72fdb.pth",
      "models/softlabels_class_0/CandlesPatterns_7_eb2233fb-6438-4f33-b8cf-02139b74de06.pth"
    ]
  },
  "class_1": {
    "models_paths": [
      "models/softlabels_class_1/CandlesPatterns_7_46cc9cc0-13fe-477a-b64a-228ba41d7994.pth",
      "models/softlabels_class_1/CandlesPatterns_7_67d2082a-a328-4639-a8d4-851cb290cd73.pth",
      "models/softlabels_class_1/CandlesPatterns_7_549b5b35-ce68-4b5f-92ac-387939dd43f4.pth",
      "models/softlabels_class_1/CandlesPatterns_7_56369c65-1943-430a-94df-775594a0f5eb.pth",
      "models/softlabels_class_1/CandlesPatterns_7_b34220e3-3d78-4ef9-8176-442daefda696.pth",
      "models/softlabels_class_1/CandlesPatterns_7_c65aae4f-e0c5-4cf5-af0e-0df55f4c31f9.pth",
      "models/softlabels_class_1/CandlesPatterns_7_c827f143-b993-4364-b07e-a9e2754c23e4.pth",
      "models/softlabels_class_1/CandlesPatterns_7_c9907b91-9f64-4edb-8e36-14c13e3bcada.pth",
      "models/softlabels_class_1/CandlesPatterns_7_d528c8d6-f97a-4e64-b8d0-a8120fecddeb.pth",
      "models/softlabels_class_1/CandlesPatterns_7_eb2ddacf-c347-4422-ac14-82e025c0d6ed.pth"
    ]
  },
  "class_2": {
    "models_paths": [
      "models/softlabels_class_2/CandlesPatterns_7_0e9ff235-acf4-498e-b696-54e633f15353.pth",
      "models/softlabels_class_2/CandlesPatterns_7_1a3dbd45-212d-4be2-8b32-589240ab201c.pth",
      "models/softlabels_class_2/CandlesPatterns_7_5e3f3ff0-31cd-415c-9060-3a38eec7b1e7.pth",
      "models/softlabels_class_2/CandlesPatterns_7_7ab22d36-eff9-4ad7-8a77-2e67646aeb90.pth",
      "models/softlabels_class_2/CandlesPatterns_7_8cdf2838-8bac-4fc2-948c-991fded7df0d.pth",
      "models/softlabels_class_2/CandlesPatterns_7_74d91267-2bbc-4cc1-a231-9359271efefe.pth",
      "models/softlabels_class_2/CandlesPatterns_7_373f4359-c346-4e3b-a48a-c6c6e1c487a4.pth",
      "models/softlabels_class_2/CandlesPatterns_7_ae6148da-e17a-4814-9d29-06537997d8f4.pth",
      "models/softlabels_class_2/CandlesPatterns_7_c7389fa3-2905-4d83-9502-2363aae91c26.pth",
      "models/softlabels_class_2/CandlesPatterns_7_f92b9083-3010-49d9-8f0c-0563d1ad5252.pth"
    ]
  },
  "class_3": {
    "models_paths": [
      "models/softlabels_class_3/CandlesPatterns_7_5a5f7054-2207-47b5-b1fa-6b975e332102.pth",
      "models/softlabels_class_3/CandlesPatterns_7_5ff7f5c1-3f33-40b7-ac59-fbe2c4afa7bc.pth",
      "models/softlabels_class_3/CandlesPatterns_7_6cad2218-0956-4510-8942-6341fbe96d9c.pth",
      "models/softlabels_class_3/CandlesPatterns_7_6ec46f19-e2da-4eeb-9e02-962f445189c9.pth",
      "models/softlabels_class_3/CandlesPatterns_7_7ae80d05-009c-433c-9ccf-00a6e508fd92.pth",
      "models/softlabels_class_3/CandlesPatterns_7_367a6186-63a5-4994-a290-dcf3909e7cab.pth",
      "models/softlabels_class_3/CandlesPatterns_7_386a96da-afa0-432c-8c44-aefd7b5ec2c0.pth",
      "models/softlabels_class_3/CandlesPatterns_7_760cc32a-96d2-4dce-a67d-9f441d962380.pth",
      "models/softlabels_class_3/CandlesPatterns_7_62820686-b1a8-4009-8945-75ca43c517b9.pth",
      "models/softlabels_class_3/CandlesPatterns_7_e7579e8d-ae75-4add-9b14-e90948ec22b4.pth"
    ]
  },
  "class_4": {
    "models_paths": [
      "models/softlabels_class_4/CandlesPatterns_7_1dca4a0c-d5ec-4535-a26f-84f8ac6df4ef.pth",
      "models/softlabels_class_4/CandlesPatterns_7_06d933ff-da57-4a28-b406-2085499750b9.pth",
      "models/softlabels_class_4/CandlesPatterns_7_60a0fa01-9164-4d78-8da4-3a7986c862fc.pth",
      "models/softlabels_class_4/CandlesPatterns_7_786d0a04-2bdb-482b-9fb9-e80b8ac2025a.pth",
      "models/softlabels_class_4/CandlesPatterns_7_8010a956-f62c-48af-a99a-6f1f0fd9069e.pth",
      "models/softlabels_class_4/CandlesPatterns_7_0122196f-8d82-45d4-9178-da439e52baac.pth",
      "models/softlabels_class_4/CandlesPatterns_7_213241c1-866d-4aae-b555-41699d9455e1.pth",
      "models/softlabels_class_4/CandlesPatterns_7_5138034f-9f08-4143-8952-adb85ebeca3b.pth",
      "models/softlabels_class_4/CandlesPatterns_7_becdda44-3fe7-43c5-baef-a87eb8022a56.pth",
      "models/softlabels_class_4/CandlesPatterns_7_c78c40d0-73a3-4ebe-b0af-7be16ae89957.pth"
    ]
  },
  "class_5": {
    "models_paths": [
      "models/softlabels_class_5/CandlesPatterns_7_0db5cf1a-a8e3-4d57-b5e6-6936d19ada03.pth",
      "models/softlabels_class_5/CandlesPatterns_7_7db7b6b9-55b6-4034-b8b4-8b9dbd398eb0.pth",
      "models/softlabels_class_5/CandlesPatterns_7_9d49213a-8ebb-4dfd-8d8e-de8b64e19e74.pth",
      "models/softlabels_class_5/CandlesPatterns_7_649cc4d5-1fb7-4e06-89b1-bd3b77bb4f8c.pth",
      "models/softlabels_class_5/CandlesPatterns_7_696af00c-d70d-414d-9926-62c08962c1aa.pth",
      "models/softlabels_class_5/CandlesPatterns_7_0808eccc-f660-4b5c-b4cc-50355091f2d1.pth",
      "models/softlabels_class_5/CandlesPatterns_7_6898fbb1-2ab6-4b1e-b804-bd809a2543d1.pth",
      "models/softlabels_class_5/CandlesPatterns_7_e9e96230-8516-484a-ba87-ea58922368df.pth",
      "models/softlabels_class_5/CandlesPatterns_7_e327b27a-cac7-4269-b062-36d21f176f09.pth",
      "models/softlabels_class_5/CandlesPatterns_7_fac87f69-a157-468a-9aa4-918c0a8dca47.pth"
    ]
  }
}
```
## Remote Server Setup

1. Update system and install required tools:
```aiignore
sudo apt update
sudo apt install -y git python3.12-venv glances
```
2. Clone the repository:
```aiignore
git clone git@bitbucket.org:MaxUsanin/cnn_candlestick_patterns_detector.git ~/python_deploy/cnn_candlestick_patterns_detector
cd ~/python_deploy/cnn_candlestick_patterns_detector/cnn_candlestick_patterns_detector
```
3. Setup virtual environment:
```aiignore
python3 -m venv patterns_detector
source patterns_detector/bin/activate
pip install -r requirements.txt
```
4. Run the training process:

```aiignore
cd s7
nohup python -m candles_patterns_7_soft_single_main &
```

## Maintenance Commands
* Kill Python processes:
```aiignore
pkill -f python
```
* Reset repository:
```aiignore
git reset --hard
git clean -fdx
git pull origin main
```

This README structure ensures clarity on usage, configuration, and setup steps for both local and remote environments.