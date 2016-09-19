## Flask and D3 Simple Scatterplot Example: http://flask.theoryandpractice.org/

# Imports: Flask and other
from flask import Flask
from flask import request
from flask import render_template

import json
import numpy as np

# Create an instance of class "Flask" with name of running application as the arg
app = Flask(__name__)

@app.route("/index")
def index():
    return render_template("index.html")
    

@app.route("/") # gaus.html: Jinja template if statement
def gindex():
    mux = request.args.get('mux', '')
    muy = request.args.get('muy', '')
    if len(mux) == 0: mux="3.0"
    if len(muy) == 0: muy="3.0"
    return render_template("gaus.html", mux=mux, muy=muy)


@app.route("/data")
@app.route("/data/<int:ndata>")
def data(ndata=100):
    x = 10 * np.random.rand(ndata) - 5
    y = 0.5 * x + 0.5 * np.random.randn(ndata)
    A = 10.0 ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id":i, "x": x[i], "y": y[i], "area": A[i], "color": c[i]} for i in range(ndata)])
    
    
@app.route("/gdata")
@app.route("/gdata/<float:mux>/<float:muy>")
def gdata(ndata=100, mux=0.5, muy=0.5):
    x = np.random.normal(mux, 0.5, ndata)
    y = np.random.normal(muy, 0.5, ndata)
    A = 10.0 ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id":i, "x": x[i], "y": y[i], "area": A[i], "color": c[i]} for i in range(ndata)])


if __name__ == '__main__':
    app.run(debug=True)
    
    
