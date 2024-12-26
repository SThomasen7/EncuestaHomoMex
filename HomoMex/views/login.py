"""
HomoMex login view

URLs include:
/login/
/logout/
"""
import HomoMex
import flask
from flask import session
from flask import redirect, url_for, request
from HomoMex.views.util import loginuser, hash_pass, match_pass

@HomoMex.app.route('/login/', methods=['GET', 'POST'])
def login():
    """Login"""
    print(request)
    if 'WARN' not in session:
        session['WARN'] = 0
    context = { "warning": "" } 
    
    # On form input.
    if request.method == 'POST':
        # Connect to database
        connection = HomoMex.model.get_db()

        if(request.form['entry'] == 'Entrar'):
            # Successful login
            if loginuser(request.form['email'].lower(), request.form['password']):
                session['WARN'] = 0
                return redirect(url_for('show_index'))
            else:

                session['WARN'] += 1
                warn = "Nombre de usuario o contraseña inválido."
                if session['WARN'] >= 3:
                    warn += " Si tienes problemas al ingresar, contacta stasen@umich.edu"
                context['warning'] = warn

    return flask.render_template("login.html", **context)

# ONLY POST METHOD ALLOWED? WHY IS A POST METHOD NEEDED HERE
@HomoMex.app.route('/logout/')
def logout():
    """Logout."""
    # Redirect to login if not logged in
    session.clear()
    return redirect(url_for('login'))

@HomoMex.app.route('/entrar/')
def entrar():
    return redirect(url_for('login'))

@HomoMex.app.route('/salir/')
def salir():
    return redirect(url_for('logout'))
