from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    # 1: query i dns , list forward
    
    # 2: hvilke entries har vi

    # 3: display i html

    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)