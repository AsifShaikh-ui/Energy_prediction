import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Energy Consumption Predictor", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #111;
        }
        .main {
            background-color: #111;
        }
        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: #EEE !important;
        }
        .stSlider > div > div > div {
            color: #EEE !important;
        }
    </style>
""", unsafe_allow_html=True)

model = joblib.load("energy_model.pkl")

st.title("⚡Energy Consumption Prediction")
st.write("Predict household electricity usage based on daily usage patterns.")

hour = st.slider("⏱ Select Hour of Day (0-23)", 0, 23, 19)
month = st.selectbox("📅 Select Month", range(1, 13))
is_weekend = st.selectbox("🗓 Is it Weekend?", ["No", "Yes"])
is_weekend = 1 if is_weekend == "Yes" else 0

st.write("---")

sub_3 = st.slider("🔥 Estimated High-Power Appliance Usage Level (0 = low, 30 = high)", 0, 30, 10)

import numpy as np

try:
    hourly_df = pd.read_csv("hourly_data.csv", index_col=0, parse_dates=True)
except Exception:
    hourly_df = None

defaults = {}
if hourly_df is not None:
    med = hourly_df.median(numeric_only=True)
    defaults = med.to_dict()
else:
    defaults = {}

def get_default(col):
    if col in defaults and not np.isnan(defaults[col]):
        return float(defaults[col])
    if 'Sub_metering' in col:
        return 0.0
    if col in ['hour', 'month', 'day_of_week', 'is_weekend']:
        return 0
    return 0.0

model_features = list(model.feature_names_in_)
row = {}
for f in model_features:
    if f == 'hour':
        row[f] = hour
    elif f == 'month':
        row[f] = month
    elif f == 'is_weekend':
        row[f] = is_weekend
    elif f == 'Sub_metering_3':
        row[f] = sub_3
    elif f == 'day_of_week':
        row[f] = 0
    else:
        row[f] = get_default(f)

input_df = pd.DataFrame([row], columns=model_features)

prediction = model.predict(input_df)[0]
st.subheader(f"🔋 Predicted Energy Consumption: **{prediction:.3f} kW**")
st.caption("Higher value = higher electricity usage.")

st.write("---")

if st.checkbox("📈 Show Hourly Consumption Pattern Insight"):

    try:
        df = pd.read_csv("hourly_data.csv", index_col=0, parse_dates=True)
    except Exception:
        df = pd.read_csv("hourly_data.csv", parse_dates=True)

        if 'DateTime' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
            df.set_index('DateTime', inplace=True)
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.set_index('date', inplace=True)
        else:
            st.error("hourly_data.csv missing a DateTime index/column. Please save the hourly dataframe with its DateTime index or a 'DateTime' column.")
            df = None

    if df is not None:
        
        if 'Global_active_power' not in df.columns:
            st.error("hourly_data.csv does not contain 'Global_active_power' column.")
        else:
            
            if 'hour' not in df.columns:
                try:
                    df['hour'] = df.index.hour
                except Exception:
                    if 'DateTime' in df.columns:
                        df['hour'] = pd.to_datetime(df['DateTime']).dt.hour
                    else:
                        st.error("Could not determine hour values. Ensure hourly_data.csv contains a DateTime index or a 'DateTime' column.")
                        df = None

    if df is not None:
        hourly_avg = df.groupby('hour')['Global_active_power'].mean()
        fig, ax = plt.subplots(figsize=(7,4))
        ax.plot(hourly_avg.index, hourly_avg.values, marker='o')
        ax.set_title("Average Consumption by Hour of Day")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Power (kW)")
        ax.grid(True)
        st.pyplot(fig)
