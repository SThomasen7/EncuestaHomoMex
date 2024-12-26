"""
HomoMex tutorial view.

URLs include:
/
"""
import HomoMex
import flask
from flask import session, request
from flask import redirect, url_for
from HomoMex.views.util import sanitize

@HomoMex.app.route('/tutorial/', methods=['GET', 'POST'])
def tutorial():
    """Start tutorial"""
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    context = dict()
    return flask.render_template("tutorial.html", **context)
    warn = ""
    if request.method == 'POST':
        if (('q1' not in request.form or request.form['q1'] != "q1-C") or 
            ('q2' not in request.form or request.form['q2'] != "q2-D")):
            warn = "Uno de sus respuestas no fue correcta, por favor, intentelo otra vez."
        else:
            return redirect(url_for("tutorial2"))

    context = { "warn": warn }
    return flask.render_template("tutorial.html", **context)

@HomoMex.app.route('/tutorial2/', methods=['GET', 'POST'])
def tutorial2():
    """Tutorial 2: questions"""
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    context = dict()
    return flask.render_template("tutorial2.html", **context)
    warn = ""
    if request.method == 'POST':
        if (('q1' not in request.form or request.form['q1'] != "q1-A") or 
            ('q2' not in request.form or request.form['q2'] != "q2-B")):
            warn = "Uno de sus respuestas no fue correcta, por favor, intentelo otra vez."
        else:
            return redirect(url_for("tutorial3"))
    context = { "warn": warn }
    return flask.render_template("tutorial2.html", **context)

@HomoMex.app.route('/tutorial3/', methods=['GET', 'POST'])
def tutorial3():
    """Tutorial 3: Guía"""
    if 'userid' not in session:
        return redirect(url_for('login'))

    connection = HomoMex.model.get_db()
    login_request = "SELECT type FROM users " + \
                    "WHERE userid="+str(session['userid'])+" "
    cur = connection.execute(login_request)
    data = cur.fetchone()
    context = { "warn" : "",
                "ambiguo" : data['type'] == "ambig" }
    #if data['type'] == 'binary':
    #    return flask.render_template("tutorial3.html", **context)
    #else:
    return flask.render_template("tutorial3.html", **context)

#@HomoMex.app.route('/tutorial4/', methods=['GET', 'POST'])
#def tutorial4():
    #"""Tutorial 4: Ejemplos """
    #if 'userid' not in session:
        #return redirect(url_for('login'))
#
    ##connection = HomoMex.model.get_db()
    #login_request = "SELECT type FROM users " + \
                    #"WHERE userid="+str(session['userid'])+" "
    #cur = connection.execute(login_request)
    #data = cur.fetchone()
    ##if data['type'] == 'multi':
        #return redirect(url_for('tutorial_final'))
    #context = { "warn" : "",
                #"ambiguo" : data['type'] == "ambig" }
    #return flask.render_template("tutorial4.html", **context)

@HomoMex.app.route('/tutorial_final/', methods=['GET', 'POST'])
def tutorial_final():
    """Tutorial: final """
    if 'userid' not in session:
        return redirect(url_for('login'))

    connection = HomoMex.model.get_db()
    update = "UPDATE users SET tutorial='True' WHERE userid="+\
            str(session['userid'])+";"
    connection.execute(update)
    return flask.render_template("tutorial_final.html")


# Ejemplos que queremos repasar ---------------------------
# No es tan chido como copié y pegué mucho código, pero
# lo hice para evitar tener que tambiar los detalles de
# los usuarios.
tutorial_questions = [
# ***
""" PLAYERA😃ya en @Gravitymty 👈🏻🤩➡DIRECCIÓN Calle Matamoros 917, Barrio Antiguo #Monterrey
    
📱8117168513
                                                                                                      
#guadalajara #jalisco #cdmx #mexico #saltillo #cancun #acapulco #regio #gay #Jockstraps #ropa #suspensorios #underwear #swimwear #gym #RopaInterior #mty #gdl #NL #mx #tienda https://t.co/b0VYFvkZ0
""",
# ***
"""Eres bien marica y no marica de gay.""",
# ***
"""Esto es lo más homosexual que hago.  😂
""",
# ***

"""Una jota cantando opera... Nunca había visto eso...
""",
# ***
"""#26Agosto "ni puto ni joto, soy un ciudadano defiendo tu voto" dicen #VamonosPatriaaCaminar http://t.co/ePkyyv9D""",
# ***
"""Advertencia este twitter contiene imágenes sugerentes y alto contenido homosexual.

🔞🔞🔞🔞🔞🔞🔞
""",
# ***
"""@Bukcles Entiende que esto es gay twitter jaja, y obvio me refiero a los heteros pendejos jajaja a los machitos, los masculinidad frágil. Ni se pa que comentas si tu no eres de esos, bieja mensa https://t.co/fKT93b5uom
""",
# ***
"""Soy. Joto""",
# ***
"""soy:
⚪️ homosexual.
⚪️ heterosexual.
⚪️ bisexual.
🔘 una pendeja que vive ilusionada esperando el follow de @freddyleyva

""",
# ***
"""Es la pareja mas linda que he visto y son HOMOSEXUALES 😍.
""",
# ***
"""@pedromejiam @econokafka Traducción: "Le doy las pompis a López pase lo que pase y digan  lo que digan". Así o más abyecto?
Pura
Puta
Propaganda
Populista
""",
# ***
"""@imostacho_ Lesbiana
""",
# ***
""" Ya lo entie do todo !
Los comunistas no tratan bien a los homosexuales.!
De allí el miedo de este canijo !
 Y por lo que se lee, no sabe tampoco que es el comunismo. https://t.co/Z2totwbTAS
"""
# ***
]

tutorial_answers = [
        "q1-B",
        "q1-A",
        "q1-B",
        "q1-A",
        "q1-B",
        "q1-B",
        "q1-B",
        "q1-B",
        "q1-B",
        "q1-B",
        "q1-C",
        "q1-B",
        "q1-B"
]

razonamiento = [
        """La respuesta deseada para este tuit es No LGBT+fóbico. 
        El tuit tiene que ver con un anuncio para la comunidad LGBT+, 
        pero no tiene contenido discriminativo.""",

        """La respuesta deseada para este tuit es LGBT+fóbico. 
        El tuit usa una palabra indicativa de la comunidad LGBT+ como 
        un insulto, aunque el autor diga \"y no de gay\" el uso es 
        LGBT-fóbico""",

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        En este tuit, el autor puede ser un miembro de la comunidad
        burlando de si mismo. Aunque una interpretación es que el
        autor no es de la comunidad LGBT+, en la cual se consideraría
        un tuit dañíno, damos el benificio de la duda al autor.
        """,

        """La respuesta deseada para este tuit es LGBT+fóbico.
        En este tuit, si el autor es LGBT+ o no, la interpretación
        es negativa hacia la comunidad LGBT+, hace sugerencias
        a esterotipos dañínos.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        Este tuit parece ser de una marcha política
        de gente LGBT+ negando el uso de palabras dañínos contra ellos.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        Este tuit parece indicar que la cuenta es de pornografía.
        El uso de la palabra homosexual es indicativo del contenido
        sin intención discriminativo.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        Aunque el autor hace mención a la comunidad LGBT+, y el
        contenido es agresivo, el autor no está mostrando agresión
        ni odio hacia la comunidad LGBT+
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        Este tuit podría ser de una persona saliendo del closet,
        otra vez damos el benificio de la duda al autor.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        El autor hace mención a sexualidades en un tuit que desea
        crear humor sin la intención de ser lastimoso contra la
        comunidad LGBT+.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        El autor expresa admiración a una pareja LGBT+.
        """,

        """La respuesta deseada para este tuit es no relacionado a 
        la comunidad LGBT+.
        Este tuit trata de temas políticos pero no hace referencia
        a la comunidad LGBT+.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        Realmente no se puede deducir la intención del sin más
        contexto, damos el beneficio de la duda al autor.
        """,

        """La respuesta deseada para este tuit es no LGBT+fóbico.
        El autor expresa su opinión en como un grupo trata a la
        comunidad LGBT+. Si un tuit trata de LGBT+fóbia sin la
        expresión de LGBT+fóbia por parte del autor, la etiqueta deseada
        es no LGBT+fóbico.
        """
]

@HomoMex.app.route('/tutorial5/', methods=['GET', 'POST'])
def tutorial5():
    """Tutorial 5: questions"""
    if 'userid' not in session:
        return redirect(url_for('login'))
    
    if 'tutorial_question' not in session:
        session["tutorial_question"] = 0

    if session["tutorial_question"] == len(tutorial_questions):
        session["tutorial_question"] = 0
        return redirect(url_for("tutorial_final"))

    text = tutorial_questions[session["tutorial_question"]]
    warn = ""
    correcto = False
    answer = None

    if request.method == 'POST':
        answer = True
        if ('q1' not in request.form or request.form['q1'] == 
                tutorial_answers[session["tutorial_question"]]):
            correcto = True
        session["tutorial_question"] += 1

    context = { "warn": warn,
                "respuesta": answer,
                "correcto": correcto,
                "text": text,
                "razonamiento": razonamiento[session["tutorial_question"]-1]
              }
    return flask.render_template("tutorial5.html", **context)

