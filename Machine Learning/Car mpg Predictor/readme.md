# 🚗 Advanced Regression Techniques for Vehicle Fuel Efficiency Prediction

This project presents an end-to-end machine learning application designed to predict the fuel efficiency (Miles Per Gallon) of a vehicle. The primary focus is on exploring and implementing advanced regression techniques—specifically Ridge (L2) and Lasso (L1) regularization—to build a robust predictive model. The final model is deployed in an interactive web application using Streamlit.

## ✨ Features

-   **Interactive Web App:** A user-friendly interface built with Streamlit allows for real-time MPG predictions based on user-input vehicle specifications.
-   **Automated Data Pipeline:** The script handles all necessary data cleaning, including imputation of missing values and one-hot encoding for categorical features.
-   **Advanced Model Implementation:** The project goes beyond a baseline model to implement and analyze Ridge and Lasso regression, demonstrating techniques for regularization and feature selection.
-   **Non-Linear Analysis:** Utilizes Polynomial Features to effectively capture the complex, non-linear relationships between a vehicle's attributes and its fuel efficiency.

## 💻 Demo

*A brief demo of the Streamlit application in action.*

![Demo GIF of the Streamlit App](<https://github.com/shivamyadav-dev/A-Journey-Of-Data-Science/blob/main/Machine%20Learning/Car%20mpg%20Predictor/app%20demo.png?raw=true>)

## 🛠️ Tech Stack

-   **Language:** Python
-   **Core Libraries:** Pandas, NumPy, Scikit-learn 
-   **Web Framework:** Streamlit 
-   **Data Analysis & Visualization:** Statsmodels, Matplotlib, Seaborn 

## 🧠 Model & Analysis Deep Dive

The analysis for this project, detailed in the `l1,l2,slr.py` script, focuses on creating a model that is not only accurate but also robust and interpretable.

#### 1. Data Preprocessing

Before model training, the raw `car-mpg.csv` dataset underwent several key preprocessing steps:
* The `car_name` column was dropped as it serves as a unique identifier and offers no predictive value.
* The categorical `origin` column was one-hot encoded to convert it into a numerical format suitable for the model.
* Missing values in the `horsepower` column, denoted by `'?'`, were identified and imputed using the median value of the column to ensure data integrity.

#### 2. Model Selection & Regularization

A standard **Linear Regression** model served as the initial baseline. However, to address potential overfitting and improve generalization, more advanced techniques were employed:

* **Ridge Regression (L2):** This technique was implemented to introduce a penalty on the magnitude of the coefficients.This helps to prevent overfitting by ensuring that the model does not rely too heavily on any single feature, leading to better performance on unseen data.
* **Lasso Regression (L1):** Lasso was used for its dual benefit of regularization and feature selection.By shrinking the coefficients of less important features to exactly zero, it effectively performs an automated feature selection process, helping to identify the most significant predictors of fuel efficiency.

#### 3. Handling Non-Linearity

* **Polynomial Features:** Real-world data rarely follows perfect linear relationships. To account for this, polynomial features were generated.This technique allows a linear model to fit more complex, curved relationships (e.g., between horsepower and MPG), leading to a more accurate representation of the underlying data patterns.

