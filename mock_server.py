from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/tests/<path:path>')
def static_files(path):
    return send_from_directory('tests', path)

@app.route('/tests/csv_submit', methods=['POST'])
def csv_submit():
    data = request.json
    expected = 10 + 7 + 12  # A rows sum = 29

    if data["answer"] == expected:
        return jsonify({
            "correct": True,
            "reason": "",
            "url": None
        })
    else:
        return jsonify({
            "correct": False,
            "reason": "Incorrect sum",
            "url": None
        })

if __name__ == "__main__":
    app.run(port=9000)
