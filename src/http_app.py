from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "success"})

if __name__ == "__main__":
    app.run(debug=True)
