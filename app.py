from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
import os

app = Flask(__name__)

# !!! IMPORTANT: CHANGE THIS FOR PRODUCTION !!!
# Use an environment variable for the secret key in production for security.
# For Render, you can set an environment variable called SECRET_KEY.
app.secret_key = os.environ.get('SECRET_KEY', 'your_super_secret_key_that_you_must_change_for_production')


# Define the static folder path.
# This should resolve correctly on Render as well.
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
app.config['STATIC_FOLDER'] = STATIC_FOLDER

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('home.html')

@app.route('/products')
def products():
    """Renders the products page."""
    return render_template('products.html')

@app.route('/performance')
def performance():
    """Renders the performance page."""
    return render_template('performance.html')

@app.route('/whyus')
def whyus():
    """Renders the whyus page."""
    return render_template('whyus.html')

@app.route('/security')
def security():
    """Renders the security page."""
    return render_template('security.html')

@app.route('/strategy')
def strategy():
    """Renders the strategy page."""
    return render_template('strategy.html')

@app.route('/market')
def market():
    """Renders the market page."""
    return render_template('market.html')

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html')

@app.route('/api/trading_data')
def get_trading_data():
    """
    Reads trading.csv and report.csv, processes the data, and returns it as JSON.
    The data is structured into slides, with each slide containing 6 trade rows
    and corresponding summary statistics.
    """
    try:
        # Load trading data
        trading_csv_path = os.path.join(app.config['STATIC_FOLDER'], 'trading.csv')
        # Ensure 'Date/Time' is read as string to preserve original format if desired, or parse as datetime
        trading_df = pd.read_csv(trading_csv_path, dtype={'Date/Time': str})

        # Load report data
        report_csv_path = os.path.join(app.config['STATIC_FOLDER'], 'report.csv')
        report_df = pd.read_csv(report_csv_path)

        slides_data = []
        num_trades = len(trading_df)
        trades_per_slide = 6
        num_slides = (num_trades + trades_per_slide - 1) // trades_per_slide # Calculate number of slides

        effective_num_slides = num_slides # Show all available slides based on data

        for i in range(effective_num_slides):
            start_idx = i * trades_per_slide
            end_idx = min((i + 1) * trades_per_slide, num_trades)

            # Extract trade data for the current slide
            current_trades = trading_df.iloc[start_idx:end_idx].to_dict(orient='records')

            # Get corresponding summary report data for the current slide
            # Assuming report_df has one row per slide's summary
            current_summary = {}
            if i < len(report_df):
                current_summary = report_df.iloc[i].to_dict()

            slides_data.append({
                'trades': current_trades,
                'summary': current_summary
            })

        return jsonify({'slides': slides_data})

    except FileNotFoundError as e:
        app.logger.error(f"CSV file not found: {e}")
        return jsonify({"error": f"Required CSV file not found. Please ensure '{e.filename}' exists in the 'static' folder."}), 404
    except pd.errors.EmptyDataError:
        app.logger.error("One of the CSV files is empty.")
        return jsonify({"error": "One of the CSV files is empty. Please check the content."}), 400
    except Exception as e:
        app.logger.error(f"An error occurred while processing CSVs: {e}")
        return jsonify({"error": "An internal server error occurred while fetching data."}), 500

if __name__ == '__main__':
    # Ensure your static/trading.csv and static/report.csv files are committed to your repository.
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))