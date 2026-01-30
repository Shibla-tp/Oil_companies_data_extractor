from flask import Flask, jsonify
from hunter_service import fetch_and_save_csv
from email_service import send_emails_from_csv
from domains import BRAND_DOMAINS

app = Flask(__name__)

CSV_FILE = "uae_company_list.csv"

@app.route("/fetch-emails", methods=["GET"])
def fetch_emails():
    file = fetch_and_save_csv(BRAND_DOMAINS, CSV_FILE)
    return jsonify({
        "status": "success",
        "message": "Emails fetched & CSV generated",
        "file": file
    })

@app.route("/send-emails", methods=["POST"])
def send_emails():
    send_emails_from_csv(CSV_FILE)
    return jsonify({
        "status": "success",
        "message": "Emails sent from CSV"
    })

if __name__ == "__main__":
    app.run(debug=True)
