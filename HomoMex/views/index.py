"""
HomoMex index (main) view.

URLs include:
/
"""
import HomoMex
import flask
from flask import session
from flask import redirect, url_for
from HomoMex.views.util import sanitize

@HomoMex.app.route('/')
def show_index():
    """Display / route."""

    if 'userid' not in session:
        return redirect(url_for('login'))
    
    connection = HomoMex.model.get_db()
    login_request = "SELECT tutorial FROM users " + \
                    "WHERE email = '" + sanitize(session['email']) + "' "
 
    cur = connection.execute(login_request)
    data = cur.fetchone()

    #print(data['tutorial'])
    context = { 'tutorial_completed': data['tutorial'] }
    return flask.render_template("index.html", **context)

@HomoMex.app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404
