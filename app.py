from flask import Flask, render_template, request
import joblib
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------
# Flask App Setup
# -----------------------------------

app = Flask(__name__)

# -----------------------------------
# Database Configuration
# -----------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'

db = SQLAlchemy(app)

# -----------------------------------
# Load AI Model and Vectorizer
# -----------------------------------

model = joblib.load("models/phishing_model.pkl")

vectorizer = joblib.load("models/vectorizer.pkl")

# -----------------------------------
# Database Model
# -----------------------------------

class EmailLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.Text)

    result = db.Column(db.String(100))

# -----------------------------------
# Home Route
# -----------------------------------

@app.route("/")
def home():

    return render_template("index.html")

# -----------------------------------
# Prediction Route
# -----------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    # Get Email From Form
    email = request.form["email"]

    # Convert Email Into Vector
    email_vector = vectorizer.transform([email])

    # Predict Using AI Model
    prediction = model.predict(email_vector)[0]

    # -----------------------------------
    # PHISHING EMAIL
    # -----------------------------------

    if prediction == 1:

        result = "⚠️ PHISHING EMAIL DETECTED"

        phishing_confidence = 100

        safe_confidence = 0

        threat_level = "HIGH"

        color = "red"

    # -----------------------------------
    # SAFE EMAIL
    # -----------------------------------

    else:

        result = "✅ SAFE EMAIL"

        phishing_confidence = 0

        safe_confidence = 100

        threat_level = "LOW"

        color = "green"

    # -----------------------------------
    # Save Result To Database
    # -----------------------------------

    new_log = EmailLog(

        email=email,

        result=result

    )

    db.session.add(new_log)

    db.session.commit()

    # -----------------------------------
    # Return Result To HTML
    # -----------------------------------

    return render_template(

        "index.html",

        prediction=result,

        phishing_confidence=phishing_confidence,

        safe_confidence=safe_confidence,

        threat_level=threat_level,

        color=color

    )

# -----------------------------------
# History Page
# -----------------------------------

@app.route("/history")
def history():

    logs = EmailLog.query.all()

    return render_template(

        "history.html",

        logs=logs

    )

# -----------------------------------
# Run Flask App
# -----------------------------------

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)