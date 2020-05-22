from flask import Flask, render_template

app = Flask(__name__)

menu = ["Intro", "Dish of the day (recipe)", "Contact us"]

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", menuitems=menu)

@app.route("/about")
def about():
    return render_template("about.html", title="About site", menuitems=menu)

if __name__ == "__main__":
    app.run(debug=True)