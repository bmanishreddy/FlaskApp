from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import jsonify, make_response
import os
import json

app =  Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/Flask"
os.path.join(basedir,'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#Endpoint to create a user

@app.route("/user",methods=["POST"])
def add_user():
    try:
        username = request.json['username']
        email = request.json['email']
        new_user = User(username, email)
        db.session.add(new_user)
        db.session.commit()
        # print(new_user)
        syncresp = user_schema.dump(new_user)
        return jsonify(syncresp)
    except:
        raise InvalidUsage('Duplicate message id ', status_code=400)
        #syncresp = {"error":"Duplicateid "}



    #return jsonify(new_user)

#get all the users


@app.route("/user",methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = user_schema.dump(all_users)
    return jsonify(result.data)

##to get a specific user

@app.route("/user/<id>",methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

#updating a user
@app.route("/user/<id>",methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    user.email = email
    user.username = username
    db.session.commit()
    return user_schema.jsonify(user)

#deleting a user
@app.route("/user/<id>",methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)
