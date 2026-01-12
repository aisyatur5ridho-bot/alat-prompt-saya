import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import tempfile

# Judul Halaman
st.set_page_config(page_title="Video to Prompt AI", layout="centered")

st.markdown("<h3 style='text-align: center;'>🎬 AI Video/Image to Prompt</h3>", unsafe_allow_html=True)
st.write("Upload gambar atau video, AI akan membuatkan prompt detail untukmu.")

# Ambil API Key dari "Rahasia" Streamlit
api_key = st.secrets["GOOGLE_API_KEY"]

# Konfigurasi Gemini
genai.configure(api_key=api_key)

# Pilihan Tipe File
option = st.selectbox("Apa yang ingin kamu upload?", ("Gambar (Image)", "Video"))

uploaded_file = st.file_uploader("Pilih file...", type=["jpg", "png", "jpeg", "mp4"])

if st.button("🚀 Generate Prompt"):
    if uploaded_file is not None:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        with st.spinner('Sedang melihat & berpikir... (Tunggu sebentar)'):
            try:
                if option == "Gambar (Image)":
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Gambar yang diupload", use_column_width=True)
                    response = model.generate_content(["Deskripsikan gambar ini secara sangat detail dalam bahasa Inggris sebagai prompt untuk AI Image Generator (seperti Midjourney/Stable Diffusion). Fokus pada gaya visual, pencahayaan, subjek, dan komposisi.", image])
                    st.success("Selesai! Ini Prompt-nya:")
                    st.code(response.text, language="markdown")
                    
                elif option == "Video":
                    # Proses Video (Butuh trik file sementara)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        video_path = tmp_file.name

                    st.video(video_path)
                    
                    # Upload ke Gemini File Manager
                    video_file = genai.upload_file(path=video_path)
                    
                    # Tunggu video siap diproses Google
                    import time
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai.get_file(video_file.name)

                    if video_file.state.name == "FAILED":
                        st.error("Gagal memproses video.")
                    else:
                        response = model.generate_content([video_file, "Tonton video ini. Buatkan prompt teks yang sangat detail dalam bahasa Inggris agar saya bisa membuat video serupa menggunakan AI Video Generator (seperti Runway/Sora/Kling). Deskripsikan gerakan kamera, subjek, suasana, dan gaya visualnya."])
                        st.success("Selesai! Ini Prompt-nya:")
                        st.code(response.text, language="markdown")
                        
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Silakan upload file dulu ya!")

st.markdown("---")
st.caption("Dibuat untuk Komunitas Blogger")
