## Create Database Flask Tutorial Reference: http://www.datasciencebytes.com/bytes/2015/02/28/using-flask-to-answer-sql-queries/

# Imports: Flask
from flask import Flask
from flask import request
from flask import g
from flask import render_template

# Import: Logging to track events when app runs
import logging

# Import: Time related functions
import time

# Import: SQL 
import sqlite3

# Logging
#logging.basicConfig(filename='NYC311.log', level=logging.INFO)

DATABASE = 'NYC311.db' # Table name: "complaints" with cols: "borough", "agency", "minute"

# Create an instance of class "Flask" with name of running application as the arg
app = Flask(__name__)
app.config.from_object(__name__)

# Function to connect to database
def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])
    
## ------------------------------------------------------------------------ ##
# Copied from: http://flask.pocoo.org/docs/0.11/appcontext/
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

# teardown_appcontext: Registers a function to be called when the application context ends    
@app.teardown_appcontext 
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
## ----------------------------------------------------------------------- ##

# Function to execute query        
def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    return rows
    
# View database: 50 rows
@app.route("/viewdb")
def viewdb():
    # Table name: complaints
    rows = execute_query("""SELECT * FROM complaints LIMIT 50""")
    return '<br>'.join(str(row) for row in rows)


# View schema
@app.route('/schema')
def view_schema():
    # Table name: complaints 
    # Pragma returns one row for each column in the named table
    rows = execute_query("""PRAGMA table_info(complaints)""")
    return '<br>'.join(str(row) for row in rows)
    
@app.route('/')
def index():
    return render_template('index.html')



# Print data
@app.route("/query/")
def print_data():
    """
    Respond to a query of the format:
    app/?borough=Manhattan&minute=600
    with NYC 311 data for the "borough" and "minute" specified in the query
    """
    # Time just before query execution
    start_time = time.time()
    
    # Cursor object
    cur = get_db().cursor()
    
    # ---- Get Inputs from URL: /?borough=Manhattan&minute=600 ---- #
    try:
        # Convert input to integer
        #minute = int(request.args.get('minute'))
        minute = request.args.get('minute')
        
        if minute is None:
            print "Argument not provided!"
    except ValueError:
        return "Time must be an integer"
        
    borough = request.args.get('borough')
    # -------------------------------------------------------------- #

    # ---- Execute Query based on inputs ---- #
    # Table name: "complaints" with cols: "borough", "complaint", "minute"
    result = execute_query(
        """SELECT agency, count(*)
           FROM complaints
           WHERE borough = ? AND minute = ?
           GROUP BY agency""",
        (borough, minute)
    )
    # NOTE: result is a list with tuples of form: (u'agency, count)
    # e.g. [(u'NYPD', 25), (u'DOT', 50), (u'HPD', 80)]
    # --------------------------------------- #
    
    # ---- Convert row in result to csv format ---- #
    # map(function, iterable): Apply function to every item of iterable and return a list of the results. A tuple is an iterable!
    str_rows = [','.join(map(str, TUPLE)) for TUPLE in result]
    # --------------------------------------------- #
    
    # Time just after query execution
    query_time = time.time() - start_time
    
    # Log time taken for query execution
    logging.info("executed query in %s" % query_time)
    
    # Close cursor
    cur.close()
    
    # Return result in csv format
    header = 'agency,count\n' # NOTE: NO space between strings, just a comma
    csv_out = header + '\n'.join(str_rows)
    return csv_out



if __name__ == '__main__':
    app.run(debug=True)
    
## Calling example: http://localhost:5000/?borough=Manhattan&minute=600


    