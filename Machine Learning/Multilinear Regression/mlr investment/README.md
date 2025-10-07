# 💰 Startup Profit Predictor

This project is a web application built with Streamlit that predicts the profit of a startup based on its expenditures. It utilizes a Multiple Linear Regression model to provide insights and predictions.

## 🚀 Live Demo
 


## ✨ Features

-   **Interactive Interface**: An easy-to-use web interface to input startup spending on Research, Promotion, and Digital Marketing.
-   **Categorical Input**: Allows selection of the startup's location (State), which is factored into the prediction.
-   **Real-Time Prediction**: Instantly calculates and displays the predicted profit based on the inputs.
-   **Model Performance Metrics**: Displays the model's performance with Training and Testing R² scores to show its accuracy and generalization capability.
-   **Statistical Analysis**: Includes a detailed Ordinary Least Squares (OLS) summary, highlighting that **Research spend** is the most statistically significant predictor of a startup's profit.
-   **Data Preview**: Shows a preview of the head of the dataset used for training.

## 🛠️ Tech Stack

-   **Backend & ML**: Python
-   **Web Framework**: Streamlit
-   **Data Manipulation**: Pandas, NumPy
-   **Machine Learning**: Scikit-learn
-   **Statistical Analysis**: Statsmodels

## 🧠 Model Details

The core of this application is a Multiple Linear Regression model built using Scikit-learn.

-   **Target Variable**: `Profit`
-   **Features**:
    -   `Research` (Numerical)
    -   `Promotion` (Numerical)
    -   `DigitalMarketing` (Numerical)
    -   `State` (Categorical: Hyderabad, Bangalore, Chennai)

The categorical `State` feature is preprocessed using one-hot encoding. The analysis script `mlr.py` demonstrates the process of backward elimination to identify the most significant features, which informed the final model presented in the `app.py` Streamlit application.

## 📊 Dataset

The model is trained on the `Investment.csv` dataset. This dataset contains 50 instances of startup data with the following columns:

-   `DigitalMarketing`
-   `Promotion`
-   `Research`
-   `State`
-   `Profit`

## ⚙️ Setup and Installation

To run this project locally, please follow these steps:

**1. Clone the repository:**

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

```
**2. Create and activate a virtual environment:**
```
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

```
 **3. Install the required dependencies:**
 ```
-`streamlit`
 -`pandas`
-` numpy`
-` scikit-learn` 
-`statsmodels`
** Then, run the installation command:**
pip install -r requirements.txt
```


**4. Run the Streamlit application:**
```
Make sure the Investment.csv file is in the same directory as app.py.

Your web browser should open a new tab with the running application.
```

**📁 File Structure**
```
.
├── app.py              # The main Streamlit application script
├── mlr.py              # Script for model building and statistical exploration
├── Investment.csv      # The dataset used for training the model
├── requirements.txt    # List of Python dependencies
└── README.md           # Project documentation

```
