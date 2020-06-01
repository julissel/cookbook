from flask import Flask, render_template, url_for, request, flash
from configparser import ConfigParser


app = Flask(__name__)
conf = ConfigParser()
conf.read('cookbook_config.conf')
app.config['SECRET_KEY'] = conf['CONFIG']['SECRET_KEY']

menu = [{"name": "Intro", "url": "intro-cookbook"},
        {"name": "Dish of the day (recipe)", "url": "main-dish"},
        {"name": "Contact us", "url": "contact"}]


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", menu=menu)


@app.route("/about")
def about():
    return render_template("about.html", title="About site", menu=menu)


@app.route("/profile/<int:country>/<path:username>")
def profile(username, country):
    return f"User: {username}, country {country}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Message sent', category='success')
        else:
            flash('Sending error', category='error')

    return render_template('contacts.html', title='Contact us', menu=menu)


# context manager
#with app.test_request_context():
#    print('url for about-page =', url_for('about'))
#    print('url for index-page =', url_for('index'))
#    print('url for profile =', url_for("profile", username='Maria', country=643))


if __name__ == "__main__":
    app.run(debug=True)
