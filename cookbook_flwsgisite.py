import os
import sqlite3
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from configparser import ConfigParser
from FDataBase import FDataBase


app = Flask(__name__)
conf = ConfigParser()
conf.read('cookbook_config.conf')
app.config['SECRET_KEY'] = conf['CONFIG']['SECRET_KEY']
app.config['DATABASE'] = conf['CONFIG']['DATABASE']
app.config['DEBUG'] = conf['CONFIG']['DEBUG']
app.config['USERNAME'] = conf['CONFIG']['USERNAME']
app.config['PASSWORD'] = conf['CONFIG']['PASSWORD']

app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

menu = [{"name": "Intro", "url": "intro-cookbook"},
        {"name": "Dish of the day (recipe)", "url": "main-dish"},
        {"name": "Contact us", "url": "contact"}]

db_file = 'flsite.db'


@app.route("/index")
@app.route("/")
def index():
    if not os.path.exists(db_file):
        create_bd()

    db = get_db()

    dbase = FDataBase(db)
    return render_template("index.html", menu=dbase.getMenu())  # menu=menu)


@app.route("/about")
def about():
    return render_template("about.html", title="About site", menu=menu)


@app.route("/profile/<int:country>/<path:username>")
def profile(username, country):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"User: {username}, country {country}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Message sent', category='success')
        else:
            flash('Sending error', category='error')

    return render_template('contacts.html', title='Contact us', menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged'], country=session['userCountry']))
    elif request.method == 'POST' and request.form['username'] == 'test_user' and request.form['psw'] == 'qwerty':
        session['userLogged'] = request.form['username']
        session['userCountry'] = request.form['country']
        return redirect(url_for('profile', username=session['userLogged'], country=session['userCountry']))

    return render_template('login.html', title='Authorization', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="The page was not found", menu=menu), 404


# context manager
#with app.test_request_context():
#    print('url for about-page =', url_for('about'))
#    print('url for index-page =', url_for('index'))
#    print('url for profile =', url_for("profile", username='Maria', country=643))


def connect_db():
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        return conn


def create_bd():
    db = connect_db()
    with app.open_resource('script_create_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
