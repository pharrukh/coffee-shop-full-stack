import os
from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_short():
    return jsonify({'success': True, 'drinks': [drink.short() for drink in Drink.query.all()]})


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    return jsonify({'success': True, 'drinks': get_drinks_long()})


@app.route('/drinks/', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    drink = request.get_json()

    new_drink = Drink()
    new_drink = Drink(title=drink['title'], recipe=json.dumps(drink['recipe']))
    new_drink.insert()

    return jsonify({'success': True, 'drinks': get_drinks_long()})


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)

    update_data = request.get_json()

    if 'title' in update_data:
        drink.title = update_data['title']

    if 'recipe' in update_data:
        drink.recipe = update_data['recipe']

    drink.update()

    return jsonify({'success': True, 'drinks': get_drinks_long()})


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    drink.delete()
    return jsonify({'success': True, 'delete': id})


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    # TODO: this can be improved
    if error.status_code == 401:
        return render_template('errors/401.html'), 401
    if error.status_code == 403:
        return render_template('errors/403.html'), 403
    return render_template('errors/500.html'), 500


@app.errorhandler(401)
def server_error(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(403)
def server_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(422)
def server_error(error):
    return render_template('errors/422.html'), 422


@app.errorhandler(405)
def server_error(error):
    return render_template('./errors/405.html'), 405


@app.errorhandler(409)
def server_error(error):
    return render_template('./errors/405.html'), 409


def get_drinks_long():
    return [drink.long() for drink in Drink.query.all()]
