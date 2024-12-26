"""
HomoMex signup view

URLs include:
/signup/
"""
import HomoMex
import flask
import json
from flask import session
from flask import redirect, url_for, request
from HomoMex.views.util import loginuser, hash_pass, match_pass, sanitize
from random import shuffle

@HomoMex.app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """Signup"""
    context = { "warning": "" } 
    
    if 'WARN' not in session:
        session['WARN'] = 0
    
    # On form input.
    warn = ""
    if request.method == 'POST':
        
        # Send signup information
        if(request.form['entry'] == 'signup'):
            test, warn = signupuser(request.form['email'].lower(), 
                    request.form['password'], request.form['gender'],
                    request.form['age'], request.form['academic level'], request.form['study'],
                    request.form['orientation'])

            if not test:
                session['WARN'] += 1
                if session['WARN'] >= 3:
                    warn += "  Si tienes problemas, contacta Scott en stasen@umich.edu"
                context['warning'] = warn
            else:
                return redirect(url_for('show_index'))

    return flask.render_template("signup.html", **context)


def signupuser(email, password, gender, age, academic, field, orientation):
    """Signs the user up"""
    if '@' not in email:
        return False, "Porfavor, use un correo electrónico válido"

    if orientation == "" or gender == "":
        return False, "Porfavor, ingresa su información demográfica," 
        + "estos datos no se asociarán con usted"
    connection = HomoMex.model.get_db()
    login_request = "SELECT * FROM users " + \
                    "WHERE email = '" + sanitize(email) + "' "
 
    cur = connection.execute(login_request)
    users = cur.fetchone()
    if not age.isdigit():
        return False, "Porfavor, ingrese un entero positivo para la edad"
    if (users is not None):
        return False, "Hay una cuenta ya registrada con este correo"

    if len(password) < 6:
        return False, "La contraseña ha de tener al menos 6 caracteres"

    add_user_request = "INSERT INTO users (email, completed, currentq, " +\
                       "password, age, gender, orientation, aclevel, acfield, "+ \
                       "tutorial, type) VALUES ('" + \
                       sanitize(email) + "', 'False', 0," + \
                       " '" + hash_pass(password) \
                       + "', '" +str(age) + "', '" + gender + "', '" \
                       + orientation + "', '" +academic+ "', '" \
                       + field + "', 'False', 'multi')"

    connection.execute(add_user_request)

    qset = randomize_set(sanitize(email))
    with open("HomoMex/static/questions/{}.json".format(email), 'w') as fptr:
        json.dump(qset, fptr)

    login_request = "SELECT * FROM users " + \
                    "WHERE email = '" + sanitize(email) + "' "
 
    cur = connection.execute(login_request)
    users = cur.fetchone()
    
    return True, ""

def randomize_set(email):
    """Randomizes the questions sets the user will get"""
    # First shuffles the sets of questins
    # Then shuffles each question type within the sets.

    #sets = list(range(0, 7))
    #shuffle(sets)
        
    #questions = list()

    #for i in sets:
        #if i == 6:
            #ten = list(range(0, 5))
        #else:
            #ten = list(range(0, 10))
        #shuffle(ten)
        #for j in ten:
            #questions.append(10*i + j)

    questions = list(range(0,817))
    shuffle(questions)
    return questions
