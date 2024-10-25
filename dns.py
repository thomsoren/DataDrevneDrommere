from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    # query i dns 

    # hvilke entries har vi

    # display i html
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)