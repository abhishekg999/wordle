from flask import Flask
app = Flask(__name__)


from flask import request, jsonify, flash, render_template
from flask import abort, redirect, url_for

from markupsafe import escape
import json

import random
import sqlite3
from sqlite3 import Error

from wordle import Wordle

w = Wordle()

print(w.guesses)
@app.route('/', methods=['GET'])
def index():
	return render_template('index_template_flask.html', guesses=w.guesses, n_let=5, n_g=6)

@app.route('/guess', methods=['POST'])
def guess():
	guess = escape(request.form.get('guess')).lower()
	print(guess)
	w.guess(guess);

	return redirect(url_for('index'))

if __name__ == '__main__':
	with open("seceret_.key", "r") as f:
		app.secret_key = f.read()

	app.run()