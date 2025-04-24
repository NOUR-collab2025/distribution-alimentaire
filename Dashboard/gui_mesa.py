from flask import Flask, render_template, jsonify
from model import FoodDeliveryModel

app = Flask(__name__)
model = FoodDeliveryModel(5, 5, 2, 10, 10)

@app.route("/")
def index():
    return render_template("index.html")

import traceback

@app.route("/grid_data")
def grid_data():
    try:
        model.step()
        return jsonify({
            "grid": model.get_grid_state(),
            "successful_deliveries": model.successful_deliveries,
            "failed_attempts": model.failed_attempts
        })
    except Exception as e:
        print("🔥 Error in /grid_data:", e)
        traceback.print_exc()  # <-- this line shows the real cause
        return jsonify({"error": str(e)}), 500



@app.route("/reset")
def reset():
    global model
    model = FoodDeliveryModel(5, 5, 2, 10, 10)
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)
