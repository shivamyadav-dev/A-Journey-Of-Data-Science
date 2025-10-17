# 🏠 USA Housing Valuation Engine & Model Comparison Platform

This project is an end-to-end machine learning application that not only predicts housing prices but also serves as an interactive platform for comparing the performance of **13 different regression models**.

The primary goal was to move beyond a single predictive model and build a tool that demonstrates a critical real-world data science workflow: training multiple models, rigorously evaluating their performance, and deploying the results in a user-friendly interface.

## ✨ Key Features

-   **Interactive Model Selection:** The Streamlit application allows users to choose from 13 different trained models in real-time to see how each one predicts the final price.
-   **Comprehensive Model Evaluation:** A systematic approach was used to train and evaluate a wide range of regressors, from simple linear models to complex ensembles like XGBoost and LightGBM.
-   **Dynamic "AI Report Card":** The application features a live dashboard that displays the R² score and Mean Absolute Error ($) for the selected model, providing instant transparency into its performance.
-   **End-to-End Workflow:** The project covers the full lifecycle, from data ingestion and model training (`models.py`) to deployment in a polished web app (`app.py`).

## 🚀 Live Demo

*A brief demonstration of the Streamlit application, showcasing the model selection and the dynamic "AI Report Card".*

![Demo of the USA Housing Valuation Engine](<https://raw.githubusercontent.com/shivamyadav-dev/A-Journey-Of-Data-Science/refs/heads/main/Machine%20Learning/Housing%20Price%20Predictor(Regression)/webpage%20ss.png>)

## 🛠️ Tech Stack

-   **Language:** Python
-   **Web Framework:** Streamlit
-   **Core ML Libraries:** Scikit-learn, XGBoost, LightGBM
-   **Data Handling:** Pandas, NumPy, Pickle

## 🧠 Project Workflow & Analysis

The project is broken down into two main components: model training/evaluation and the interactive application.

### 1. Model Training & Evaluation (`models.py`)

This script is the core of the analytical work. The process is as follows:
1.  **Data Loading:** The `USA_Housing.csv` dataset is loaded using Pandas.
2.  **Feature Selection:** The relevant features are selected, and the data is split into training and testing sets.
3.  **Model Training Loop:** A dictionary containing 13 different Scikit-learn, XGBoost, and LightGBM models is defined. The script iterates through each one, training it on the training data.
4.  **Performance Evaluation:** For each trained model, predictions are made on the test set, and key performance metrics (MSE, MAE, and R²) are calculated.
5.  **Saving Artifacts:** The evaluation results are saved to `model evaluation.csv`, and each trained model is serialized and saved as a `.pkl` file for use in the application.

### 2. Interactive Application (`app.py`)

This script serves the trained models in an interactive Streamlit application.
1.  **User Interface:** The app provides sliders and input boxes for the user to enter housing features (income, age, rooms, etc.).
2.  **Model Selection:** A dropdown menu is populated with the names of all 13 trained models.
3.  **Real-Time Prediction:** When the user selects a model and clicks "Predict," the corresponding `.pkl` file is loaded, and a price prediction is generated.
4.  **Performance Dashboard:** The app reads the `model evaluation.csv` file to display the R² and MAE for the currently selected model, giving the user immediate feedback on its expected accuracy and average error in dollars.

