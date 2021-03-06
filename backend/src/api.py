import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
import traceback
app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE,OPTIONS'
    )
    return response

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json
        {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
     where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })

'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_new_drink(payload):
    body = request.get_json()
    title = body.get('title', None)
    recipe = json.dumps(body.get('recipe', None))
    try:
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
        return jsonify({
            'success': True,
            'drinks': [new_drink.long()],
        })
    except Exception:
        traceback.print_exc()
        abort(422)


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
     where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    body = request.get_json()
    drink = Drink.query.get(drink_id)
    if(drink is None):
        abort(404)
    
    recipe = body.get('recipe', None)
    drink.title = body.get('title', None)
    drink.recipe =  recipe if type(recipe) == str else json.dumps(recipe)
    try:
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })
    except:
        traceback.print_exc()
        abort(422)


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
     where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    body = request.get_json()
    drink = Drink.query.get(drink_id)
    if(drink is None):
        abort(404)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink.id,
        })
    except Exception:
        traceback.print_exc()
        abort(422)

# Error Handling
'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
                jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
        }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity"
        }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400
'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error: AuthError):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
        }), error.status_code


@app.errorhandler(Exception)
def auth_error(error: Exception):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "something went wrong"
        }), 500
