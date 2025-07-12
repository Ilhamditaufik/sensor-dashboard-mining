import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import matplotlib.pyplot as plt

# Load model & encoder
model = joblib.load("model_sensor.pkl")
le = joblib.load("label_encoder.pkl")

# Load data historis
data = pd.read_csv("sensor_data.csv")

# Fungsi kirim email
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

# ==================================
# UI
st.set_page_config(page_title="🚨 Dashboard Sensor Pertambangan", layout="wide")
st.title("🚨 Dashboard Sensor Pertambangan")

st.write("Masukkan data sensor secara manual:")

getaran = st.slider("Getaran (g)", 0.0, 2.0, 0.5, 0.1)
suhu = st.slider("Suhu (°C)", 0, 100, 35, 1)
tekanan = st.slider("Tekanan (Bar)", 0.0, 5.0, 1.2, 0.1)
kelembapan = st.slider("Kelembapan (%)", 0, 100, 45, 1)

if st.button("🔍 Prediksi Status & Kirim Email jika Bahaya"):
    timestamp = datetime.now()
    features = np.array([[getaran, suhu, tekanan, kelembapan]])
    pred = model.predict(features)
    status = le.inverse_transform(pred)[0]

    st.subheader(f"Status Prediksi: {status}")
    st.write(f"Getaran: {getaran} g")
    st.write(f"Suhu: {suhu} °C")
    st.write(f"Tekanan: {tekanan} Bar")
    st.write(f"Kelembapan: {kelembapan} %")

    if status == "Bahaya":
        st.error(f"🚨 STATUS BAHAYA: {status}\nSegera lakukan pemeriksaan alat!")
        st.markdown(
            """
            <audio autoplay>
            <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg">
            </audio>
            """,
            unsafe_allow_html=True
        )
        success, msg = send_email_alert(getaran, suhu, tekanan, kelembapan, timestamp)
        if success:
            st.success(msg)
        else:
            st.error(msg)
    elif status == "Perlu Pemeriksaan":
        st.warning(f"⚠️ STATUS: {status}")
    else:
        st.success(f"✅ STATUS: {status}")

# ==================================
st.markdown("---")
st.header("📈 Grafik Tren Sensor Historis")

sensor_option = st.selectbox(
    "Pilih sensor untuk grafik:",
    ("getaran", "suhu", "tekanan", "kelembapan")
)

fig, ax = plt.subplots()
ax.plot(data["id"], data[sensor_option], marker="o")
ax.set_xlabel("ID Data")
ax.set_ylabel(sensor_option.capitalize())
ax.set_title(f"Tren {sensor_option.capitalize()}")

st.pyplot(fig)

st.dataframe(data)
