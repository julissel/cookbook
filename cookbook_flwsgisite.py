from flask import Flask, render_template, url_for


app = Flask(__name__)
menu = ["Intro", "Dish of the day (recipe)", "Contact us"]


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", menuitems=menu)


@app.route("/about")
def about():
    return render_template("about.html", title="About site", menuitems=menu)


@app.route("/profile/<int:country>/<path:username>")
def profile(username, country):
    return f"User: {username}, country {country}"


# context manager
#with app.test_request_context():
#    print('url for about-page =', url_for('about'))
#    print('url for index-page =', url_for('index'))
#    print('url for profile =', url_for("profile", username='Maria', country=643))


if __name__ == "__main__":
    app.run(debug=True)
