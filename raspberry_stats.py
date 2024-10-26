from flask import Flask, render_template, flash
import json
import os

app = Flask(__name__)

@app.route('/')
def raspberry():
    try:
        # Construct the path to the JSON file
        data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'synthetic_data_single_rpi.json')
        
        # Open and load the JSON data
        with open(data_file_path, 'r') as f:
            data = json.load(f)
        
        if not data:
            flash("No data found in synthetic_data_single_rpi.json.", "warning")
        
        return render_template('raspberry_site.html', data=data)
    
    except FileNotFoundError:
        flash("Data file 'synthetic_data_single_rpi.json' not found.", "danger")
        return render_template('raspberry_site.html', data=[])
    
    except json.JSONDecodeError as e:
        flash(f"Error decoding JSON data: {e}", "danger")
        return render_template('raspberry_site.html', data=[])
    
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "danger")
        return render_template('raspberry_site.html', data=[])

if __name__ == "__main__":
    app.run(debug=True, port=5001)