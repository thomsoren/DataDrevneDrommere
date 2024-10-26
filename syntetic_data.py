from flask import Flask, jsonify
from datetime import datetime, timedelta
import random
import math
import json

app = Flask(__name__)

# Simulation parameters
hours_to_simulate = 48  # Simulate for 48 hours
start_time = datetime.utcnow()

def generate_solar_energy(hour):
    """
    Generates solar energy as a function of the hour of the day (sinusoidal pattern).
    Min value at midnight (0), max value at noon (12).
    """
    # Assume the solar generation is 0 at night (hours 0-6 and 18-24) and peaks around midday.
    if 6 <= hour < 18:
        # Sinusoidal pattern for day hours
        return max(0, 5 * math.sin(math.pi * (hour - 6) / 12))
    return 0  # No solar generation at night

def generate_consumption():
    """
    Generates random consumption values for each hour.
    The consumption follows a stochastic pattern with some randomness.
    """
    return round(random.uniform(1.5, 3.5), 2)

def generate_power_prices(hour):
    """
    Simulates hourly power prices.
    Lower prices during the night, higher during peak hours (8 AM to 8 PM).
    """
    if 8 <= hour < 20:
        return round(random.uniform(0.25, 0.45), 2)  # Higher prices during the day
    else:
        return round(random.uniform(0.10, 0.20), 2)  # Lower prices at night

def simulate_battery_control(consumption, solar_energy, price, battery_charge):
    """
    Simulates battery charging/discharging based on consumption, solar generation, and power prices.
    """
    if solar_energy > consumption:
        # If there's excess solar energy, store it in the battery
        battery_charge += solar_energy - consumption
        action = "Charging from Solar"
    elif price < 0.2:
        # If the price is low, charge from the grid
        battery_charge += 1  # Charge with 1 kWh from grid
        action = "Charging from Grid (Low Price)"
    else:
        # Discharge the battery to supply power if possible
        if battery_charge > 0:
            discharge = min(consumption, battery_charge)
            battery_charge -= discharge
            action = f"Discharging {discharge} kWh"
        else:
            action = "No Battery Action (Depleted)"
    
    # Ensure the battery charge doesn't exceed 100% capacity (e.g., 10 kWh max)
    battery_charge = min(battery_charge, 10)
    return battery_charge, action

# Generate the synthetic data
data = []
battery_charge = 5  # Assume the battery starts half charged (5 kWh)

for hour_offset in range(hours_to_simulate):
    timestamp = start_time + timedelta(hours=hour_offset)
    hour_of_day = timestamp.hour

    solar_energy = generate_solar_energy(hour_of_day)
    consumption = generate_consumption()
    price = generate_power_prices(hour_of_day)
    battery_charge, battery_action = simulate_battery_control(consumption, solar_energy, price, battery_charge)

    entry = {
        "timestamp": timestamp.isoformat() + "Z",
        "solarEnergy_kW": round(solar_energy, 2),
        "consumption_kW": consumption,
        "powerPrice": price,
        "batteryCharge_kWh": round(battery_charge, 2),
        "batteryAction": battery_action
    }
    data.append(entry)

# Save to a JSON file
with open('synthetic_data_single_rpi.json', 'w') as f:
    json.dump(data, f, indent=4)

# Flask route to serve the data
@app.route('/raspberry_data')
def get_raspberry_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)