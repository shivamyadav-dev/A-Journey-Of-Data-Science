# Seattle House Price Prediction

This project is an end-to-end machine learning application that predicts house prices in King County, WA (which includes Seattle). It features a complete workflow from data analysis and model training to an interactive web application built with Streamlit.



## Project Overview

The primary goal of this project is to create a reliable Automated Valuation Model (AVM) using real estate data. The model is trained on the King County House Sales dataset and is deployed in a user-friendly web interface where users can input property features to get a real-time price estimate.

### Key Features

* **Interactive UI:** A simple and intuitive web interface for users to input property details.
* **Predictive Model:** Utilizes a Linear Regression model trained on key housing attributes.
* **Data Analysis:** A comprehensive exploratory data analysis (EDA) is included in the Jupyter Notebook to understand feature relationships and correlations.

## Technical Stack

* **Language:** Python
* **Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
* **Web Framework:** Streamlit
* **IDE:** Jupyter Notebook

## Dataset

The project uses the **King County House Sales dataset**, which contains sales price data for homes sold between May 2014 and May 2015. The dataset includes 21,613 observations with 21 features, such as square footage, number of bedrooms/bathrooms, location (latitude/longitude), and grade.

## Project Structure

* `House_data.csv`: The raw dataset used for training and analysis.
* `house price .ipynb`: A Jupyter Notebook containing the full exploratory data analysis, data preprocessing, and model development process.
* `app.py`: The Streamlit script that loads the trained model and runs the interactive web application.

    
