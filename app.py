from flask import Flask, render_template, request
from MapEmbed import map_inputs

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def embed():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        return render_template('input.html', start=start, end=end, api_key=api_key)
        #start, end, mode, path_string, markers = map_inputs(start, end)
        #return render_template('embed.html', start=start, end=end, mode=mode, path=path_string, markers=markers, api_key=api_key)
    #start = "5900 N Keating Ave"
    #end = "5501 N Kedzie Ave"
    return render_template('input.html', start='', end='', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True)
