⚡ Energy Consumption Optimization (ML-Based Prediction)

📘 Overview
This project focuses on analyzing and predicting household energy consumption patterns using machine learning.
The goal is to understand real usage behavior and build a model that can optimize electricity usage for better efficiency.

Phase 1: Data Cleaning & Preprocessing — Completed
Phase 2: Model Training & Interpretation — Completed

🧩 Phase 1 – Data Understanding & Preprocessing
✔ Tasks Completed

Loaded and inspected raw dataset
Replaced missing values and converted all numeric columns to proper types
Unified Date + Time into a single DateTime index
Resampled data to hourly level to reduce noise and extract meaningful patterns

Extracted time-based features:

hour, day, day_of_week, month, is_weekend
Explored distributions and outlier
Created correlation heatmap to analyze feature relationships
Applied feature encoding and scaling where needed

🤖 Phase 2 – Model Building & Evaluation
Model Performance

Linear Regression (Baseline):
MAE: 0.171
RMSE: 0.228
R²: 0.640

Good baseline trend fit

RandomForest Regressor (Final Model):

MAE: 0.109
RMSE: 0.154
R²: 0.780

Captures strong non-linear usage behavior
Interpretation
The RandomForest model performed significantly better, confirming that energy usage is non-linear and depends heavily on:
Human activity patterns
Time of the day
Use of high-power appliances (geysers, AC, heaters)

🔍 Key Insights (Feature Importance)

Sub_metering_3 is the strongest driver of total power consumption → indicates energy-heavy appliances
Hour of the day strongly affects usage → evening peak around 7 PM – 10 PM
Weekend vs weekday difference is small → daily behavior matters more than the week

📈 Consumption Pattern Visualization

Energy usage trend across a day typically shows:
Very low consumption early morning
Minor rise around 7–9 AM
Sharp peak between 7 PM – 10 PM (high-power appliances)
Include your stored plot here:
visualization/average_hourly_consumption.png

📂 Dataset

This project uses the Household Electric Power Consumption Dataset.

🔗 Download Dataset:
https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption

Note: Dataset is not included in this repository due to size limits.
Place it manually inside a folder named data/ in the project directory.

🚀 How to Run This Project
git clone https://github.com/AsifShaikh-ui/Energy_prediction.git
cd Energy_prediction
pip install -r requirements.txt


📊 Visual Insights

Feature Importance

<img width="327" height="345" alt="image" src="https://github.com/user-attachments/assets/f1bfef56-c1f5-48a2-9302-182b7dd3b45c" />

Hourly Consumption Pattern

<img width="291" height="268" alt="image" src="https://github.com/user-attachments/assets/15de7f08-47af-4d56-9d48-43f382a1d3c8" />


🌐 Streamlit Dashboard
The deployed app includes:

🎛 Interactive input controls (hour, month, weekend, high-power usage level)

📈 Hourly consumption insight plot

🔍 Clean dark UI with sidebar navigation

🧮 Real-time prediction using RandomForest

⚙️ Auto-adjustment for missing model features

☁️ Fully deployed on Streamlit Cloud

Run locally:
pip install -r requirements.txt
streamlit run app.py
