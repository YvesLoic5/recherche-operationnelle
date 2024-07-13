from flask import Flask, render_template, jsonify, request
from hugchat import hugchat

"""chatbot = hugchat.ChatBot(cookie_path="cookies.json")
id = chatbot.new_conversation()
chatbot.change_conversation(id)
"""


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    #result = chatbot.chat(input)
    #print("Response : ", str(result))
    #return str(result)
    
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 6060, debug= True)


    
