from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 5000, debug= True)


    
