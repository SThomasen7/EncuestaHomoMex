import hashlib
import HomoMex
import flask
from flask import session
import uuid
import json

def get_qsets(email):
    """Gets this users question set ordering"""

    with open("HomoMex/static/questions2/{}.json".format(email), 'r') as fptr:
            data = json.load(fptr)

    return data

def loginuser(email, password):
    """Logs the user in"""
    connection = HomoMex.model.get_db()

    login_request = "SELECT * FROM users " + \
                    "WHERE email = '" + sanitize(email) + "' "
    
    cur = connection.execute(login_request)
    users = cur.fetchone()

    if (users is not None and
            match_pass(password, users['password'])):
        #session[IP]['logged_in'] = True
        session['WARN'] = 0
        session['userid'] = users['userid']
        session['email'] = sanitize(email)
        session['completed'] = users['completed'] == 'True'
        session['currQ'] = users['currentq']
    else:
        return False
    
    return True


def hash_pass(password):
    """Hash pass."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


# I will assume that we will not change the passwords initially stored in
# the database, for now. So if the db_string contains no '$' it's just
# a string comparison.
def match_pass(password, db_string):
    """Match pass."""
    if '$' not in db_string:
        return password == db_string

    # Get DB info
    split = db_string.split("$")
    algorithm = split[0]
    salt = split[1]
    password_hash = split[2]

    # Hash password with db's salt.
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_out = hash_obj.hexdigest()

    return password_out == password_hash

def sanitize(string):
    return string.strip()
