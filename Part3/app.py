from flask import Flask, render_template, request, send_from_directory
import os
import re
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename
import uuid
import logging
from datetime import datetime

try:
    from .topsis_logic import run_topsis
except Exception:
    from topsis_logic import run_topsis

app = Flask(__name__)

# Storage and limits
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Limit uploads to 5 MB by default
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))

# Email configuration: prefer environment variables for safety
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
# Toggle sending email in dev: set SEND_EMAIL=1 or true to enable
SEND_EMAIL = str(os.environ.get("SEND_EMAIL", "false")).lower() in ("1", "true", "yes")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        file = request.files.get("file")
        weights = request.form.get("weights", "")
        impacts = request.form.get("impacts", "")
        email = request.form.get("email", "")

        if not file or file.filename == "":
            return render_template("index.html", message="No file uploaded")

        if not valid_email(email):
            return render_template("index.html", message="Invalid email format")

        # Parse weights/impacts
        try:
            weights_list = list(map(float, weights.split(",")))
        except Exception:
            return render_template("index.html", message="Invalid weights format; provide comma-separated numbers")

        impacts_list = [s.strip() for s in impacts.split(",") if s.strip()]

        if len(weights_list) != len(impacts_list):
            return render_template("index.html", message="Weights and impacts count mismatch")

        # Sanitize filename and ensure CSV
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        if ext.lower() != ".csv":
            return render_template("index.html", message="Only CSV files are accepted")

        unique_in_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}_{filename}"
        input_path = os.path.join(UPLOAD_FOLDER, unique_in_name)
        output_filename = f"result_{uuid.uuid4().hex}.csv"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        file.save(input_path)

        try:
            run_topsis(input_path, weights_list, impacts_list, output_path)
        except Exception as e:
            logger.exception("TOPSIS processing failed")
            return render_template("index.html", message=str(e))

        # If sending is disabled, provide download link instead of emailing
        if not SEND_EMAIL:
            download_url = f"/download/{output_filename}"
            return render_template("index.html", message=f"Result ready: <a href='{download_url}'>Download</a>")

        # If SEND_EMAIL is true, ensure credentials exist
        if not SENDER_EMAIL or not APP_PASSWORD:
            logger.error("Emailing enabled but SENDER_EMAIL/APP_PASSWORD not set")
            return render_template("index.html", message="Server email not configured")

        # Send email
        msg = EmailMessage()
        msg["Subject"] = "TOPSIS Result"
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg.set_content("Please find the TOPSIS result attached.")

        with open(output_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="csv",
                filename=output_filename,
            )

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
        except Exception:
            logger.exception("Failed to send email")
            return render_template("index.html", message="Processing done but failed to send email")

        return render_template("index.html", message="Result sent successfully via email")

    except Exception as e:
        logger.exception("Unexpected error in submit")
        return render_template("index.html", message="Server error occurred")

@app.route('/download/<path:filename>')
def download(filename):
    # Only serve from outputs folder
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)