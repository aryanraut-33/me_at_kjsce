# forecast_air_quality.py
# This script performs time series forecasting on the Air Quality dataset.

# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

def forecast_air_quality():
    """
    Main function to run the air quality forecasting experiment.
    """
    print("======================================================")
    print("===         Experiment 1: Air Quality Dataset      ===")
    print("======================================================")

    # --- Step 2: Load the Dataset ---
    print("\n[INFO] Loading Air Quality data...")
    try:
        # The dataset uses a comma separator. Ensure this matches your file.
        df = pd.read_csv('AirQualityUCIFinal.csv', sep=',')
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("\n[ERROR] 'AirQualityUCIFinal.csv' not found. Please ensure the file is in the correct directory.")
        return

    # --- Step 3: Data Cleaning and Preprocessing ---
    print("\n[INFO] Cleaning and preprocessing data...")

    # Combine 'Date' and 'Time' into a single datetime object. Coerce errors to NaT (Not a Time).
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True, errors='coerce')

    # Drop rows where DateTime could not be parsed
    df.dropna(subset=['DateTime'], inplace=True)

    # Set the new 'DateTime' column as the index
    df.set_index('DateTime', inplace=True)

    # Select the target series 'CO(GT)'
    ts = df['CO(GT)']

    # Replace -200 (used for missing values) with NumPy's Not a Number (NaN)
    ts = ts.replace(-200, np.nan)

    # Coerce to numeric type, turning any conversion errors into NaN
    ts = pd.to_numeric(ts, errors='coerce')
    print(f"Missing values before processing: {ts.isnull().sum()}")

    # Resample the hourly data to daily averages and interpolate missing days
    ts_daily = ts.resample('D').mean().interpolate(method='linear')
    print(f"Missing values after resampling and interpolation: {ts_daily.isnull().sum()}")
    print("\nFirst 5 rows of the processed daily time series:")
    print(ts_daily.head())

    # --- Step 4: Visualize the Time Series ---
    print("\n[INFO] Visualizing the time series data...")
    plt.figure(figsize=(14, 7))
    plt.plot(ts_daily, label='Daily Average CO(GT)')
    plt.title('Daily Average CO(GT) Levels')
    plt.xlabel('Date')
    plt.ylabel('CO(GT) Concentration')
    plt.grid(True)
    plt.legend()
    plt.show()

    # --- Step 5: Fit the ARIMA Model ---
    print("\n[INFO] Fitting the ARIMA model...")
    # The order (p, d, q) = (5, 1, 0) is a common starting point.
    # p=5: Autoregressive part uses 5 previous values.
    # d=1: The series is differenced once to make it stationary.
    # q=0: No moving average part.
    model = ARIMA(ts_daily, order=(5, 1, 0))
    model_fit = model.fit()

    print("\nARIMA Model Summary:")
    print(model_fit.summary())

    # --- Step 6: Forecast Future Values ---
    print("\n[INFO] Forecasting future values for the next 30 days...")
    forecast_steps = 30
    forecast = model_fit.forecast(steps=forecast_steps)

    # Create a DataFrame for the forecast with a proper date index
    last_date = ts_daily.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.DateOffset(days=1), periods=forecast_steps, freq='D')
    forecast_df = pd.DataFrame({'Forecasted_CO(GT)': forecast.values}, index=forecast_dates)
    print("\nForecast for the next 30 days:")
    print(forecast_df.head())

    # --- Step 7: Visualize the Forecast ---
    print("\n[INFO] Visualizing the forecast against historical data...")
    plt.figure(figsize=(14, 7))
    plt.plot(ts_daily, label='Observed')
    plt.plot(forecast_df, label='Forecast', color='red', linestyle='--')
    plt.title('Daily Average CO(GT) Levels - Observed vs. Forecast')
    plt.xlabel('Date')
    plt.ylabel('CO(GT) Concentration')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("\n--- Air Quality Experiment Complete ---")

if __name__ == "__main__":
    forecast_air_quality()