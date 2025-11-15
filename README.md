⚡ Energy Consumption Optimization (ML-Based Prediction)

📘 Overview
This project focuses on analyzing and predicting household energy consumption patterns using machine learning.
The main goal is to understand energy usage trends and build a model that can optimize power consumption for better efficiency.
Phase 1 (Data Cleaning & Preprocessing) has been completed.
Phase 2 (Model Training & Interpretation) has also now been completed.

🧩 Phase 1 – Data Understanding & Preprocessing
✔ Tasks Completed:
Data loading and inspection
Replaced missing values and converted data types
Unified date and time into a DateTime index
Resampled data to hourly level to reduce noise and learn clear patterns

Feature extraction:
hour, day, day_of_week, month, is_weekend
Outlier and distribution exploration
Correlation heatmap and feature relationship analysis

Feature encoding and scaling where required

🤖 Phase 2 – Model Building & Evaluation
Linear Regression	MAE :- 0.171,	RMSE:- 0.228,	R²:- 0.640	Baseline Trend Fit
RandomForest Regressor (Final)	MAE:- 0.109,	RMSE:- 0.154,	R²:-0.780 	Captures non-linear usage behavior

Interpretation:
The RandomForest model clearly performed better, showing that energy usage is non-linear and depends heavily on behavior + appliance usage patterns.

🔍 Key Insights From Feature Importance
Sub_metering_3 is the strongest driver of total power usage
→ Indicates high-power appliances like water heaters or AC

Hour of the day strongly influences consumption
→ Evening usage peaks between 7 PM – 10 PM

Weekend vs Weekday difference is small
→ Daily routines matter more than weekly patterns

📈 Consumption Pattern Visualization
Average usage pattern across the day shows clear behavior:
Low consumption early morning
Small rise during morning activity (7–9 AM)
Strong peak in evening (7–10 PM) when high-power appliances are used
Save and include your plot here (if stored):
results/average_hourly_consumption.png

📂 Dataset
This project uses the Household Electric Power Consumption Dataset.
Download from:
https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption

Dataset is not included in this repository due to GitHub file size limits.
Place the dataset in a folder named data/ inside the project directory.

🚀 How to Run This Project
git clone https://github.com/AsifShaikh-ui/Energy_prediction.git
cd Energy_prediction
pip install -r requirements.txt
# Place dataset inside /data/ folder
jupyter notebook notebooks/03_model_training.ipynb

📊 4. Visual Insights

### **Feature Importance**
<img width="327" height="245" alt="image" src="https://github.com/user-attachments/assets/e6eb05b6-2afe-45b3-8319-2da65798d090" />


### **Hourly Consumption Pattern**
<img width="291" height="368" alt="image" src="https://github.com/user-attachments/assets/f25ce030-6ef2-4a97-ad1f-6409ddb8a621" />


---

## 🌐 5. Streamlit Dashboard

The deployed web app includes:

- 🎛 Interactive input controls (hour, month, weekend, appliance usage)  
- 📈 Hourly consumption visualization  
- 🔍 Clean dark UI with sidebar navigation  
- 🧮 Real-time energy consumption prediction  
- ⚙️ Auto-adjustment for missing model features  
- 💻 Publicly deployed on Streamlit Cloud  

### To run locally:
pip install -r requirements.txt
streamlit run app.py

