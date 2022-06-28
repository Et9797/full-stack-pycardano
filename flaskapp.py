from flask import Flask, render_template, jsonify, request
from build_tx import *


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/cbor", methods=["GET", "POST"])
def get_cbor():
    """Returns unsigned tx cbor"""
    if request.method == "POST":
        unsigned_tx = build_unsigned_tx(request.json)
        return jsonify({
            "cborHex": unsigned_tx.to_cbor()
        })


@app.route("/submit", methods=["GET", "POST"])
def submit_tx():
    if request.method == "POST":
        signed_tx = compose_tx_and_witness(request.json)
        chain_context.submit_tx(signed_tx.to_cbor())
        print("######## Transaction submitted. ########")
        return '', 200


if __name__ == "__main__":
    app.run()