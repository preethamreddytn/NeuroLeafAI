# BioAgriCure - Plant Disease Detection

A premium website for detecting plant diseases using Convolutional Neural Networks (CNN) built with Python and Flask.

## Features

- Upload images of plants for disease detection
- CNN-powered disease identification
- Detailed information on symptoms and cures
- Responsive design with light/dark mode
- Animated backgrounds using Vanta.js
- Parallel scrolling effects
- Premium UI with custom buttons and animations

## Project Structure

```
BioAgriCure/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cnn_model.py
│   │   └── disease_detector.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── api.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   └── result.html
│   └── utils/
│       ├── __init__.py
│       └── preprocessing.py
│
├── data/
├── models/
├── config.py
├── requirements.txt
├── run.py
├── train.py
├── planning.md
├── test_setup.py
└── README.md
```

## Setup Instructions

1. **Clone the repository** (or copy the files to your local machine)

2. **Create a virtual environment**:
   ```bash
   python -m venv bac_env
   source bac_env/bin/activate  # On Windows: bac_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the dataset**:
   - Download the dataset from: https://www.kaggle.com/datasets/jawadali1045/20k-multi-class-crop-disease-images
   - Extract and organize the dataset in the `data/` directory with the following structure:
     ```
     data/
     ├── train/
     │   ├── class1/
     │   ├── class2/
     │   └── ...
     └── validation/
         ├── class1/
         ├── class2/
         └── ...
     ```

5. **Train the model** (optional, if you want to retrain):
   ```bash
   python train.py
   ```

6. **Run the application**:
   ```bash
   python run.py
   ```

7. **Access the website**:
   Open your browser and go to `http://localhost:5000`

## Technologies Used

- **Backend**: Python, Flask
- **Machine Learning**: TensorFlow, Keras
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: None (file-based storage for simplicity)
- **Animations**: Vanta.js for background effects

## Design Elements

The website incorporates design elements from the provided buttons.md file:

1. **Back-to-top button** with hover effects
2. **Special button styles** for interactive elements
3. **Hero header** with animated background using Vanta.js
4. **Light/Dark mode** toggle
5. **Parallel scrolling** sections
6. **Motion/moving background** effects

## Model Architecture

The CNN model consists of:
- 4 convolutional layers with max pooling
- 2 dense layers with dropout for regularization
- Softmax activation for multi-class classification

## Dataset

The model is trained on the "20K Multi-class Crop Disease Images" dataset from Kaggle, which contains images of various plant diseases across multiple crop types.

## Current Status

✅ Project structure created
✅ Frontend templates implemented
✅ CSS styling with light/dark mode
✅ JavaScript functionality for UI elements
✅ Backend routes and API endpoints
✅ Configuration files
✅ Setup test script

⏳ Model training (requires dataset download and training)
⏳ Full integration of CNN model with web interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dataset provided by Jawad Ali on Kaggle
- UI components inspired by uiverse.io
- Background animations powered by Vanta.js# NeuroLeafAI
