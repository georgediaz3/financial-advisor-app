from flask import Flask, jsonify, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route('/api/market-overview', methods=['GET'])
def market_overview():
    try:
        # Fetch daily data for S&P 500 chart (SPY)
        stock = yf.download('SPY', period='1mo', interval='1d')
        if stock.empty:
            return jsonify({"error": "No data retrieved from yfinance for SPY"}), 500

        # Chart data
        prices = stock['Close'].values.tolist()
        timestamps = stock.index.strftime('%Y-%m-%d').tolist()

        return jsonify({"prices": prices, "timestamps": timestamps})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tickers', methods=['GET'])
def tickers():
    try:
        tickers = ['QQQ', 'DIA', 'VGK', 'NVDA', 'VTI', 'SCHG']  # List of tickers
        ticker_data = {}

        for ticker in tickers:
            print(f"Fetching current price for {ticker}")  # Debug log
            try:
                # Fetch ticker info
                ticker_obj = yf.Ticker(ticker)
                price = ticker_obj.history(period='1d')['Close'].iloc[-1]  # Get the last close price
                ticker_data[ticker] = {"current_price": round(price, 2)}
            except Exception as e:
                print(f"Error fetching price for {ticker}: {str(e)}")  # Log errors
                ticker_data[ticker] = {"error": f"Could not fetch price: {str(e)}"}

        return jsonify(ticker_data)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Catch unexpected errors
        return jsonify({"error": str(e)}), 500

@app.route('/api/calculate-401k', methods=['GET', 'POST'])
def calculate_401k_fixed_income():
    try:
        # Extract inputs
        if request.method == 'POST':
            data = request.json
        else:
            data = request.args

        # Inputs
        current_age = int(data.get('current_age', 30))
        retirement_age = int(data.get('retirement_age', 65))
        annual_salary = float(data.get('annual_salary', 60000))
        contribution_percentage = float(data.get('contribution_percentage', 5)) / 100
        employer_match_percentage = float(data.get('employer_match', 50)) / 100
        employer_match_limit_percentage = float(data.get('employer_match_limit', 6)) / 100
        annual_return_rate = 0.07  # Default 7% annual growth

        # Validate inputs
        if current_age >= retirement_age:
            raise ValueError("Current age must be less than retirement age")

        # Calculate years to retirement
        years_to_retirement = retirement_age - current_age

        # Employee contributions
        annual_contribution = annual_salary * contribution_percentage
        total_employee_contributions = annual_contribution * years_to_retirement

        # Employer match (limited by employer match percentage of income)
        annual_employer_match = min(annual_contribution * employer_match_percentage,
                                    annual_salary * employer_match_limit_percentage)
        total_employer_match = annual_employer_match * years_to_retirement

        # Total contributions
        total_contributions = total_employee_contributions + total_employer_match

        # Compound growth calculation
        future_value = total_contributions * ((1 + annual_return_rate) ** years_to_retirement)

        return jsonify({
            "total_employee_contributions": round(total_employee_contributions, 2),
            "total_employer_match": round(total_employer_match, 2),
            "total_contributions": round(total_contributions, 2),
            "projected_growth": round(future_value, 2)
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Server error occurred"}), 500

@app.route('/api/chatgpt', methods=['POST'])
def proxy_chatgpt():
    api_key = "YOUR_SERVER_SIDE_API_KEY"
    payload = request.json
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    return jsonify(response.json())


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route('/tour')
def tour():
    return render_template('tour.html')

@app.route('/planning')
def planning():
    return render_template('planning.html')

@app.route('/rothIRA')
def rothIRA():
    return render_template('rothIRA.html')

@app.route('/four_o_one_k')
def four_o_one_k():
    return render_template('four_o_one_k.html')

@app.route('/pensionplans')
def pensionplans():
    return render_template('pensionplans.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route("/retirmentcalc")
def retirmentcalc():
    return render_template("retirmentcalc.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/taxes")
def taxes():
    return render_template("taxes.html")

if __name__ == '__main__':
    app.run(debug=True)


