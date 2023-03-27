from flask import Flask, render_template,request
import model as m

app = Flask(__name__)
@app.route("/")
def search():
    return render_template("index.html")

@app.route("/sub",methods=["POST"])
def give():
    try:
        if request.method == "POST":
            searchquery = request.form["search"]
            search_results=m.search(searchquery)
            return render_template("sub.html", n=search_results)
    except Exception as e:
        app.logger.error(str(e))
        return render_template("error.html")


if __name__ == "__main__":
    app.run()