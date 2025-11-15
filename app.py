# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------
# Page config & dark styling
# -------------------------------
st.set_page_config(page_title="Energy Consumption Predictor", layout="centered")

st.markdown("""
    <style>
        .reportview-container, .main {
            background-color: #0f1113;
            color: #e6eef6;
        }
        .stApp {
            background-color: #0f1113;
        }
        .stSlider > div > div > div {
            color: #EEE !important;
        }
        .block-container {
            padding-top: 1rem;
        }
        .stCheckbox label, .stSelectbox label {
            color: #e6eef6;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar (Navigation / Info)
# -------------------------------
st.sidebar.title("⚡ Navigation")
st.sidebar.markdown("""
### Sections:
- 🧮 **Energy Prediction**
- 📊 **Hourly Insights**
- ℹ️ **About**
""")
st.sidebar.info("Built by Asif — Data Science Student")

# -------------------------------
# Load model safely
# -------------------------------
MODEL_PATH = Path("energy_model.pkl")
if not MODEL_PATH.exists():
    st.error("Model file `energy_model.pkl` not found. Please save the trained model in the project root.")
    st.stop()

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Try to read model expected feature names
model_feature_names = None
if hasattr(model, "feature_names_in_"):
    model_feature_names = list(model.feature_names_in_)
elif hasattr(model, "get_booster"):  # XGBoost objects fallback
    # For xgboost sklearn API it may not have feature_names_in_ saved; leave None
    model_feature_names = None

# -------------------------------
# Page header
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #F5F5F5;'>⚡ Energy Consumption Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #BBBBBB;'>Predict household electricity usage based on daily usage patterns.</p>", unsafe_allow_html=True)

# -------------------------------
# Inputs (grouped)
# -------------------------------
with st.expander("🧮 Enter Prediction Inputs", expanded=True):
    hour = st.slider("⏱ Select Hour of Day (0-23)", 0, 23, 19)
    month = st.selectbox("📅 Select Month", list(range(1, 13)), index=0)
    is_weekend = st.selectbox("🗓 Is it Weekend?", ["No", "Yes"])
    is_weekend = 1 if is_weekend == "Yes" else 0
    sub_3 = st.slider("🔥 Estimated High-Power Appliance Usage Level (0 = low, 30 = high)", 0, 30, 10)

# -------------------------------
# Prepare sensible defaults (if hourly_data exists)
# -------------------------------
hourly_csv = Path("hourly_data.csv")
defaults = {}
hourly_df = None
if hourly_csv.exists():
    try:
        # try to load with index
        hourly_df = pd.read_csv(hourly_csv, index_col=0, parse_dates=True)
    except Exception:
        try:
            hourly_df = pd.read_csv(hourly_csv, parse_dates=True)
        except Exception:
            hourly_df = None

    if hourly_df is not None:
        # if index is datetime-like but hour column missing, add it
        if 'hour' not in hourly_df.columns:
            try:
                hourly_df['hour'] = hourly_df.index.hour
            except Exception:
                if 'DateTime' in hourly_df.columns:
                    hourly_df['DateTime'] = pd.to_datetime(hourly_df['DateTime'], errors='coerce')
                    hourly_df.set_index('DateTime', inplace=True)
                    hourly_df['hour'] = hourly_df.index.hour
        # numeric medians
        try:
            med = hourly_df.median(numeric_only=True)
            defaults = med.to_dict()
        except Exception:
            defaults = {}

def get_default(col):
    """Return sensible default for a missing feature column."""
    if col in defaults and not pd.isna(defaults[col]):
        return float(defaults[col])
    if 'Sub_metering' in col:
        return 0.0
    if col in ['hour', 'month', 'day_of_week', 'is_weekend']:
        return 0
    # fallback numeric default
    return 0.0

# -------------------------------
# Build input row matching model features
# -------------------------------
# If model_feature_names known, use it; otherwise use a recommended set
if model_feature_names:
    features_expected = model_feature_names
else:
    # fallback feature set (common minimal features you used)
    features_expected = ['Global_reactive_power', 'Voltage', 'Sub_metering_3',
                         'hour', 'day_of_week', 'month', 'is_weekend']

# Create the row dict
row = {}
for f in features_expected:
    if f == 'hour':
        row[f] = hour
    elif f == 'month':
        row[f] = month
    elif f == 'is_weekend':
        row[f] = is_weekend
    elif f == 'Sub_metering_3':
        row[f] = sub_3
    elif f == 'day_of_week':
        # we didn't collect day number; default 0 (or derive if you want)
        row[f] = 0
    else:
        row[f] = get_default(f)

# Build DataFrame in exact column order expected
input_df = pd.DataFrame([row], columns=features_expected)

# -------------------------------
# Prediction
# -------------------------------
try:
    prediction = model.predict(input_df)[0]
except Exception as e:
    st.error(f"Prediction failed: {e}")
    st.write("Model expected features:", features_expected)
    st.write("Input provided:", input_df.to_dict(orient='records')[0])
    st.stop()

st.markdown("---")
st.markdown("""
<div style="padding: 20px; border-radius: 10px; background-color: #1E1E1E; border: 1px solid #333;">
    <h3 style="color: #90EE90;">🔋 Predicted Energy Consumption:</h3>
    <h2 style="color: #FFFFFF;">{:.3f} kW</h2>
    <p style="color: #AAAAAA;">Higher value = higher electricity usage.</p>
</div>
""".format(prediction), unsafe_allow_html=True)

# -------------------------------
# Hourly insight plot (robust)
# -------------------------------
st.markdown("---")
st.markdown("<h2 style='color:#F5F5F5;'>📊 Hourly Consumption Insight</h2>", unsafe_allow_html=True)

show_plot = st.checkbox("Show Hourly Consumption Pattern")

if show_plot:
    df = None
    if hourly_df is not None:
        df = hourly_df.copy()
    else:
        # try to load on demand with multiple guesses
        try:
            df = pd.read_csv(hourly_csv, index_col=0, parse_dates=True)
        except Exception:
            try:
                df = pd.read_csv(hourly_csv, parse_dates=True)
                if 'DateTime' in df.columns:
                    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
                    df.set_index('DateTime', inplace=True)
            except Exception:
                df = None

    if df is None:
        st.warning("hourly_data.csv not found or unreadable. To show this plot, save your resampled hourly dataframe as 'hourly_data.csv'.")
    else:
        if 'Global_active_power' not in df.columns:
            st.error("hourly_data.csv must contain 'Global_active_power' column.")
        else:
            if 'hour' not in df.columns:
                try:
                    df['hour'] = df.index.hour
                except Exception:
                    if 'DateTime' in df.columns:
                        df['hour'] = pd.to_datetime(df['DateTime']).dt.hour
                    else:
                        st.error("Could not create 'hour' column. Ensure hourly_data.csv contains a DateTime index or 'DateTime' column.")
                        df = None
            if df is not None:
                hourly_avg = df.groupby('hour')['Global_active_power'].mean()
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linewidth=2)
                ax.set_title("Average Consumption by Hour of Day", color="#F5F5F5")
                ax.set_xlabel("Hour", color="#BBBBBB")
                ax.set_ylabel("Power (kW)", color="#BBBBBB")
                ax.grid(True, alpha=0.25)
                ax.tick_params(colors="#BBBBBB")
                st.pyplot(fig)

# -------------------------------
# About / Footer
# -------------------------------
st.markdown("---")
st.markdown("**About:** This app predicts household energy consumption based on a trained RandomForest model. Save `energy_model.pkl` (trained model) and optionally `hourly_data.csv` (resampled hourly data) in the app folder.")
st.markdown("**Tip:** If you want the app to use fewer features, retrain the model with only the features you want to ask the user for.")
