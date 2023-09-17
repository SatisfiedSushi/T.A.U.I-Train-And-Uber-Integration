from flask import Flask, render_template, request
from MapEmbed import map_inputs

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)

@app.route('/')
def embed():
    start, end, mode, path_string, markers = map_inputs("5900 N Keating Ave", "5501 N Kedzie Ave", "driving")
    return render_template('embed.html', start=start, end=end, mode=mode, path=path_string, markers=markers, api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True)
