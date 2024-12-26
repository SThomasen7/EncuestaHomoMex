"""
HomoMex song view.

URLs include:
/song/
"""
import HomoMex
import flask
from flask import session
from flask import redirect, url_for, request
from HomoMex.views.util import get_qsets

import time
import json

import csv 

SONGLEN = 210
SONGFILE = "sampled_songs_part_2.csv"

import sys
csv.field_size_limit(sys.maxsize)

@HomoMex.app.route('/song/', methods=['GET', 'POST'])
def song():
    """Displays the personal info page"""
    if 'userid' not in session:
        return redirect(url_for('login'))

    connection = HomoMex.model.get_db()
    
    # Validate user
    login_request = "SELECT * FROM users " + \
                    "WHERE userid="+str(session['userid'])+" "
    cur = connection.execute(login_request)
    users = cur.fetchone()
    if users == None:
        return redirect(url_for('login'))
    else:
        session['currQ'] = users['currentq']
        session['completed'] = users['completed']

    # Check if we have finished
    if(session['currQ'] >= SONGLEN):
        connection = HomoMex.model.get_db()
        update = "UPDATE users SET completed='True' WHERE userid="+\
                str(session['userid'])+";"
        connection.execute(update)
        session["completed"] = "True"

    # If finished redirect to end
    if session['completed'] == "True":
        return redirect(url_for('fin'))

    # Get users qset
    questions = get_qsets(session['email'])
    # Get songs
    songs = list()
    #with open(f"HomoMex/data/{SONGFILE}", 'r') as fptr:
        #songs = json.load(fptr)
    songs = load_songs()

    # Index info
    idx = session['currQ']
    song = songs[questions[idx]][-1]
    songidx = questions[idx]

    # If the time has not started, start it.
    requestqry = f"""
        select * from response
        where userid="{session['userid']}"
            and q_id="{songidx}"
        """
    cur = connection.execute(requestqry)
    respon = cur.fetchone()

    now = time.time()
    # If the question hasn't been started, start the question
    if respon == None:
        begin_question = f"""
            INSERT INTO response (userid, q_id, local_id, starttime) VALUES
            ("{session['userid']}", "{songidx}", "{session['currQ']}", "{now}")
        """
        connection.execute(begin_question)

    warning = "" 
    respuesta = None

    # Handle the submitted information.
    if request.method == 'POST':
         
        if "respuesta" not in request.form:
            warning = "Porfavor, elige una respuesta."
        else:
            valid=True
            # Sacamos la respuesta
            respuesta = request.form.get("respuesta")
            if respuesta not in ('lgbt_fobico', 'nolgbt_fobico'):
                warning = "Algo salió mal."
                valid = False

            # Sacamos las líneas lgbtfobicos
            f_lines = ""
            if "song" in request.form:
                for ele in sorted(request.form.getlist("song")):
                    if not ele.isnumeric():
                        warning="Algo salió mal."
                        valid = False
                f_lines = ",".join(sorted(request.form.getlist("song")))

            if respuesta == 'lgbt_fobico' and f_lines == "":
                warning = "Si la canción tiene contenido lgbtfóbico, por favor elija las líneas que contengan contenido fóbico."
                valid = False
            if respuesta == 'nolgbt_fobico' and f_lines != "":
                warning = "Si la canción no es lgbtfóbico no se puede indicar que hay líneas que contengan contenido fóbico."
                valid = False

            # Sí todos los datos están bien, continuamos.
            if valid:
                # Se actualiza el currentq de la tabla users
                session['currQ'] += 1
                update = f"""
                    update users set currentq="{session['currQ']}"
                        where userid="{session['userid']}"
                """
                connection.execute(update)

                # se actualiza la respuesta para esta pregunta
                update = f"""
                    UPDATE response 
                    SET endtime={str(now)},
                        answer='{respuesta}',
                        lines='{f_lines}'
                    WHERE userid='{str(session['userid'])}' and
                            q_id='{str(songidx)}'
                    """
                
                connection.execute(update)
                return redirect(url_for('song'))

    # Render the page
    context = {
                'qid': session['currQ'] + 1,
                'song': list(enumerate(song.strip().split("\n"))),
                'warning' : warning
              }

    return flask.render_template("song.html", **context)



@HomoMex.app.route('/fin/', methods=['GET', 'POST'])
def fin():
    """final de encuesta"""
    if 'userid' not in session:
        return redirect(url_for('login'))
    if 'completed' not in session:
        return redirect(url_for('song'))

    return flask.render_template("fin.html")


def load_songs():
  with open(f"HomoMex/data/{SONGFILE}", 'r') as fptr:
    canciones = list()
    for line in csv.reader(fptr):
      canciones.append(line)
  return canciones[1:]
