from flask import Flask
app = Flask(__name__)


from flask import request, jsonify, flash, render_template
from flask import abort, redirect, url_for
from flask import session

from markupsafe import escape
import json

import random
import sqlite3
from sqlite3 import Error

from wordle import Wordle
from wordle_manager import WordleManager

import base64

WMG = WordleManager()

with open("common-7-letter-words.txt", "r") as f:
    wordAnswerList = f.read().strip(" ").split("\n")
    
with open("word-list-7-letters.txt", "r") as f:
    wordGuessList = f.read().strip(" ").split("\n")
    

def form_id(ip):
	return str(base64.b64encode(str(ip + "wordle_instance").encode('ascii')))

def check_login(ip):
	if 'id' in session and session['id'] == form_id(ip):
		return True

	return False

def page_instance():
	w = WMG.get(session['id'])
	return render_template('index_template_flask.html', guesses=w.guesses, n_let=w.word_length, n_g=w.num_guesses)


@app.route('/', methods=['GET'])
def index():
	print(session)
	if check_login(request.remote_addr):
		return page_instance()
	else:
		print('--------- ELSE -----------------')
		session['id'] = form_id(request.remote_addr)
		WMG.create(form_id(request.remote_addr))
		return redirect(url_for('index'))

@app.route('/guess', methods=['POST'])
def guess():
	if check_login():
		w = WMG.get(session['id'])
		guess = escape(request.form.get('guess')).lower()
		print(guess)
		w.guess(guess);

	return redirect(url_for('index'))

if __name__ == '__main__':
	with open("seceret_.key", "r") as f:
		app.secret_key = f.read()

	app.run(host='0.0.0.0', port=80)