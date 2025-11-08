# Loan Approval Prediction

This project aims to predict whether a loan application will be approved based on various applicant details provided in the `Loan_Data.csv` dataset.

## Workflow

The project follows these main steps:

1.  **Data Loading & Exploration:**
    * Load the `Loan_Data.csv` dataset using pandas.
    * Perform initial exploration to understand data types, missing values, and unique identifiers.
2.  **Exploratory Data Analysis (EDA):**
    * Analyze distributions, relationships, correlations, and outliers using statistical summaries (`describe`, `skew`) and visualizations (histograms, pairplots, heatmaps, countplots, boxplots).
3.  **Data Preprocessing:**
    * Drop the unique identifier column (`Loan_ID`).
    * Engineer a new `Income` feature by combining `ApplicantIncome` and `CoapplicantIncome`.
    * Handle missing values through a combination of row deletion and imputation (using mode or zero).
    * Encode categorical features (like `Gender`, `Married`, `Education`, `Property_Area`, `Credit_History`) into numerical representations.
    * Apply Box-Cox transformation to reduce skewness in `Income` and `LoanAmount`.
    * Scale `Loan_Amount_Term` from months to years.
4.  **Model Training & Evaluation:**
    * Identify an optimal `random_state` for consistent train-test splitting.
    * Split the data into training and testing sets.
    * Train and evaluate multiple classification models using accuracy as the primary metric (Train, Test, and Cross-Validation scores).
    * Use `GridSearchCV` for hyperparameter tuning for several models.
    * Feature selection based on importance is performed for some tree-based models before final evaluation.
5.  **Model Saving:**
    * Save the trained Logistic Regression model (`log_model`) to a file (`loan_prediction_model.pkl`) using `pickle` for future use.

## Models Used

The following classification models were trained and evaluated:

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Support Vector Machine (SVM)
* Decision Tree
* Random Forest
* AdaBoost
* Gradient Boosting
* XGBoost

## Results

Multiple classification models were trained, tuned, and evaluated. The Logistic Regression model was ultimately saved for deployment or further use.

## How to Use

Load the saved model `loan_prediction_model.pkl` using pickle to make predictions on new, preprocessed loan application data.

## Requirements

The analysis relies on the following Python libraries:

* `numpy`
* `pandas`
* `matplotlib`
* `seaborn`
* `scikit-learn`
* `xgboost`
* `pickle`
