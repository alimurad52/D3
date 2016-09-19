## Flask and D3 Simple Scatterplot Example: https://github.com/dfm/flask-d3-hello-world

# Imports: Flask and other
from flask import Flask
from flask import request
from flask import render_template

import json
import numpy as np

# Create an instance of class "Flask" with name of running application as the arg
app = Flask(__name__)

@app.route("/")
def index():
    "render index.html when root path requested"
    return render_template("index.html")


@app.route("/data")
@app.route("/data/<int:ndata>")
def data(ndata=50):
    """
    Return a list of "ndata" randomly generated points
    :param ndata: # of data points to return
    "returns: data: JSON of "ndata" data points
    """
    x = 10 * np.random.rand(ndata) - 5
    y = 0.5 * x + 0.5 * np.random.randn(ndata)
    A = 10.0 ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id":i, "x": x[i], "y": y[i], "area": A[i], "color": c[i]} for i in range(ndata)])
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
