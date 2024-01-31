from flask import Flask, render_template, request, redirect, url_for, flash, session
import random
import secrets

SECRET = secrets.token_hex(64)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random-secret')
def random_secret():
    return random.choice(SECRET)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')