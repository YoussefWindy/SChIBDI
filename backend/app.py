from flask import Flask, render_template, abort, redirect, url_for # type: ignore

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('index.html'))

@app.route('/home')
def main_home():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)