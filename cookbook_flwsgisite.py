from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = ["Intro", "Dish of the day (recipe)", "Contact us"]

@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    return render_template("index.html", menuitems=menu)

@app.route("/about")
def about():
    print(url_for('about'))
    return render_template("about.html", title="About site", menuitems=menu)


# context manager
#with app.test_request_context():
#    print('url for about-page =', url_for('about'))
#    print('url for index-page =', url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)