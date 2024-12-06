from flask import Flask, request, jsonify, render_template
import json

import torch
import os
from utils import sample_n
from loguru import logger
from tokenizers import Tokenizer

from slanggen import models

logger.add("logs/app.log", rotation="5 MB")


app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

def load_model():
    tokenizer = Tokenizer.from_file("artefacts/tokenizer.json")
    with open("artefacts/config.json", "r") as f:
        config = json.load(f)
    model = models.SlangRNN(config["model"])
    model.load_state_dict(torch.load("artefacts/model.pth"))
    return model, tokenizer

model, tokenizer = load_model()
starred_words = []


def new_words(n, temperature):
    output_words = sample_n(
        n=n,
        model=model,
        tokenizer=tokenizer,
        max_length=20,
        temperature=temperature,
    )
    return output_words

@app.route("/generate", methods=["GET"])
def generate_words():
    try:
        n = int(request.args.get("num_words", 10))
        temperature = float(request.args.get("temperature", 1.0))
    except ValueError as e:
        return jsonify({"error": "Invalid input"}), 400
    try:
        words = new_words(n, temperature)
        return jsonify(words)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/starred", methods=["GET", "POST"])
def handle_starred_words():
    if request.method == "GET":
        return jsonify(starred_words)
    elif request.method == "POST":
        word = request.json.get("word")
        if word not in starred_words:
            starred_words.append(word)
        return jsonify(starred_words)

@app.route("/unstarred", methods=["POST"])
def handle_unstarred_words():
    word = request.json.get("word")
    if word in starred_words:
        starred_words.remove(word)
    return jsonify(starred_words)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
