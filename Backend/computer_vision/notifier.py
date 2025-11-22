import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================================
# KONFIGURASI
# ================================
GMAIL_ADDRESS = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_app_password"
TARGET_EMAIL = "receiver_email@gmail.com"


def send_notification(phone_number, message):
    """
    Mengirim notifikasi via Gmail.
    Param 'phone_number' tetap dipertahankan agar kompatibel dengan app.py,
    tapi tidak digunakan di email.
    """

    try:
        # Compose email
        msg = MIMEMultipart()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = TARGET_EMAIL
        msg["Subject"] = "🚨 FloorEye Alert: Lantai Kotor Terdeteksi"

        msg.attach(MIMEText(message, "plain"))

        # Send email using SMTP Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, TARGET_EMAIL, msg.as_string())
        server.quit()

        print("[INFO] Notifikasi email berhasil dikirim.")

    except Exception as e:
        print("[ERROR] Gagal mengirim email:", e)
