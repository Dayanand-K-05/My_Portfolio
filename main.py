from flask import Flask, render_template, request, redirect, flash
import smtplib
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")

# Email Configuration (Use your own credentials)
EMAIL_ADDRESS = os.getenv("EMAIL_KEY")
EMAIL_PASSWORD = os.getenv("PASSWORD_KEY")
RECEIVER_EMAIL = os.getenv("REC_EMAIL")  # Where messages will be sent

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    if not name or not email or not message:
        flash("All fields are required!", "danger")
        return redirect("/")

    try:

        with smtplib.SMTP("smtp.gmail.com") as server:
            msg=(f"Subject:New Message\n\nName:{name}\nEmail:{email}\nMessage:{message}")
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg)

        flash("Message sent successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
