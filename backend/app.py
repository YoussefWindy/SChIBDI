from flask import Flask, render_template, abort, redirect, url_for, request # type: ignore

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('main_home'))

@app.route('/home')
def main_home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		print(request)
	return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
