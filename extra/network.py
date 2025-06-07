from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["POST"])
def receive():
    data = request.get_json(force=True)
    print("Received:", data.get("message"))
    return jsonify(status="ok", received=data.get("message"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
