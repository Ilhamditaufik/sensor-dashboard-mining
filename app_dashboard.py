import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Load model dan encoder
model = joblib.load("model_sensor.pkl")
le = joblib.load("label_encoder.pkl")

# Fungsi Kirim Email
def send_email_alert(getaran, suhu, tekanan, kelembapan, timestamp):
    sender_email = "ilham030918@gmail.com"
    app_password = "lpilewfghbkiobps"
    receiver_email = "ilham030918@gmail.com"
    subject = "🚨 ALERT BAHAYA Sensor"

    body = f"""
PERHATIAN‼️

Status: *BAHAYA*
Waktu: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Getaran: {getaran} g
Suhu: {suhu} °C
Tekanan: {tekanan} bar
Kelembapan: {kelembapan} %

Segera lakukan pemeriksaan!
"""
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        return True, "✅ Email BAHAYA berhasil dikirim."
    except Exception as e:
        return False, f"❌ Gagal mengirim email: {e}"

# ================= UI ====================
st.set_page_config(page_title="🚨 Dashboard Sensor Manual", layout="wide")
st.title("🚨 Dashboard Sensor Manual (Tanpa Auto-refresh)")

# Button eksekusi
if st.button("🔍 Jalankan Prediksi & Kirim Email jika Bahaya"):
    # Simulasi data sensor
    getaran = np.round(np.random.uniform(0.3, 1.5), 2)
    suhu = np.round(np.random.uniform(30, 65), 1)
    tekanan = np.round(np.random.uniform(1.0, 2.5), 2)
    kelembapan = np.round(np.random.uniform(40, 70), 1)
    timestamp = datetime.now()

    # Prediksi
    features = np.array([[getaran, suhu, tekanan, kelembapan]])
    pred = model.predict(features)
    status = le.inverse_transform(pred)[0]

    # Tampilkan
    st.subheader(f"Status: {status}")
    st.write(f"Getaran: {getaran}, Suhu: {suhu}, Tekanan: {tekanan}, Kelembapan: {kelembapan}")

    # Cek bahaya
    if status == "Bahaya":
        st.error("🚨 STATUS: BAHAYA")
        success, msg = send_email_alert(getaran, suhu, tekanan, kelembapan, timestamp)
        if success:
            st.success(msg)
        else:
            st.error(msg)
    else:
        st.success("✅ Status aman, tidak perlu kirim email.")
