import json
import mariadb
import dbcreds
import dbhelper
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.get('/api/candy')
def get_all_candy():
    try:
        results = dbhelper.run_procedure('call get_all_candy()',[])
        # if results come back as a list jsonify results
        if(type(results) == list):
            return make_response(jsonify(results),200)
        else:
            return make_response('sorry something went wrong',500)
    # some except blocks with possible errors
    except TypeError:
        print('invalid input type, try again.')
    except UnboundLocalError:
        print('coding error')
    except ValueError:
        print('value error, try again')

@app.post('/api/candy')
def new_candy():
        # try to check req endpoint data in dbhelper and calls procedure to create a new client
    try:
        error = dbhelper.check_endpoint_info(request.json,["name","image_url","description"])
        # if it has req info username and password then returns none
        if(error != None):
            return make_response(jsonify(error),400)
        results = dbhelper.run_procedure('call new_candy(?,?,?)',[request.json.get("name"),request.json.get("image_url"),request.json.get("description")])
        # if results come back as a list jsonify results
        if(type(results) == list):
            return make_response(jsonify(results),200)
        else:
            return make_response('sorry something went wrong',500)
    # some except blocks with possible errors
    except TypeError:
        print('invalid input type, try again.')
    except UnboundLocalError:
        print('coding error')
    except ValueError:
        print('value error, try again')

@app.delete('/api/candy')
def delete_candy():
        # try to check req endpoint data in dbhelper and calls procedure to create a new client
    try:
        error = dbhelper.check_endpoint_info(request.json,["id"])
        # if it has req info username and password then returns none
        if(error != None):
            return make_response(jsonify(error),400)
        results = dbhelper.run_procedure('call delete_candy(?)',[request.json.get("id")])
        # if results come back as a list jsonify results
        if(type(results) == list):
            return make_response(jsonify(results),200)
        else:
            return make_response('sorry something went wrong',500)
    # some except blocks with possible errors
    except TypeError:
        print('invalid input type, try again.')
    except UnboundLocalError:
        print('coding error')
    except ValueError:
        print('value error, try again')





if(dbcreds.production_mode == True):
    print("Running Production Mode")
    import bjoern #type: ignore
    bjoern.run(app,"0.0.0.0",5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)
