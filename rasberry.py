from flask import Flask, render_template, abort, flash
from faker import Faker
import random
import json
from datetime import datetime
from decimal import Decimal  # Importer Decimal

fake = Faker()
data = []

for i in range(100):  # Generer 100 datapunkter
    raspberryPi = {
        "raspberryPiId": f"RPi{str(i).zfill(3)}",
        "batterySize_kWh": round(random.uniform(5, 20), 2),
        "maxBatteryPower_kW": round(random.uniform(1, 10), 2),
        "solarPanelSize_peak_kW": round(random.uniform(1, 5), 2),
        "averageConsumption_kWh": round(random.uniform(1, 5), 2),
        "location": {
            "latitude": float(fake.latitude()),  # Konverter til float
            "longitude": float(fake.longitude()),  # Konverter til float
            "region": fake.city()
        },
        "networkTariffs": {
            "peak": round(random.uniform(0.15, 0.30), 2),
            "offPeak": round(random.uniform(0.05, 0.15), 2)
        },
        "solarPanelDirection": random.choice(["Nord", "Sør", "Øst", "Vest"]),
        "consumptionPattern": random.choice(["Fabrikk", "Næringsbygg", "Bolig"]),
        "weather": {
            "temperature": random.randint(-10, 35),
            "humidity": random.randint(30, 90),
            "weatherCondition": random.choice(["Sol", "Skyet", "Regn", "Snø"])
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    data.append(raspberryPi)

# Definer den tilpassede serialiseringsfunksjonen
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

# Lagre til en JSON-fil med tilpasset serialisering
with open('synthetic_data.json', 'w') as f:
    json.dump(data, f, indent=4, default=decimal_default)