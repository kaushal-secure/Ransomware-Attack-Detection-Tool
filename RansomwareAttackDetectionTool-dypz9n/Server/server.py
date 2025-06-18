from flask import Flask,render_template,redirect,request,session
import joblib
import numpy as np

model = joblib.load("../models/model1.pkl")
features = joblib.load("../models/features.pkl")


app = Flask(__name__)
app.secret_key = 'asd84a5d6d6sd5a6dq4asc4d6wed4s65c5d4ed6as5sad46d56as5d56d56qd6eedwe4e8d'

@app.route("/")
def Home():
    if "login" not in session:
        return redirect("/login")
    data = {"features":list(features)}
    if("output" in session):
        data["output"] = session["output"]
        session.pop("output")
    return render_template("home.html",data = data)


@app.route("/login",methods = ["POST","GET"])
def Login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        data = request.form
        print(data)
        if(data["username"] == "admin" and data["password"] == "admin"):
            session["login"] = 1
            return redirect("/")
    return "Error"


@app.route("/logout")
def logout():
    session.pop("login")
    return redirect("/login")


@app.route("/predict", methods=["POST"])
def Predict():
    user_inputs = request.form
    vals = []
    for f in features:
        vals.append(user_inputs[f])
    vals = [np.array([int(x) for x in vals])]
    pred = model.predict(vals)[0]
    
    # Convert pred to a native Python int
    pred = int(pred)

    # Add attack detection and precautionary messages
    if pred == 1:
        attack_message = "Warning: Ransomware attack detected! Immediate action is required. Disconnect the affected device from the network and initiate incident response procedures to contain and mitigate the threat."
        session["output"] = {"value": pred, "message": attack_message}
    else:
        precaution_message = "No ransomware detected. However, it's crucial to maintain regular backups and keep your software updated to safeguard against potential threats. Always stay vigilant and monitor your system for any unusual activity."
        session["output"] = {"value": pred, "message": precaution_message}
    
    return redirect("/")

@app.route("/api/predict", methods=["POST"])
def PredictApi():
    user_inputs = request.form
    vals = []
    for f in features:
        vals.append(user_inputs[f])
    vals = [np.array([int(x) for x in vals])]
    pred = model.predict(vals)[0]
    
    # Convert pred to a native Python int
    pred = int(pred)

    # Add attack detection and precautionary messages
    if pred == 1:
        attack_message = "Warning: Ransomware attack detected! Immediate action is required. Disconnect the affected device from the network and initiate incident response procedures to contain and mitigate the threat."
        return {"value": pred, "output": "Attack Detected", "message": attack_message}
    else:
        precaution_message = "No ransomware detected. However, it's crucial to maintain regular backups and keep your software updated to safeguard against potential threats. Always stay vigilant and monitor your system for any unusual activity."
        return {"value": pred, "output": "Not Detected", "message": precaution_message}


    

@app.route("/dashboard")
def Dashboard():
    if "login" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

app.run(debug=True)
