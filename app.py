import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Video to Prompt AI", layout="centered")
st.markdown("<h3 style='text-align: center;'>🎬 AI Video/Image to Prompt</h3>", unsafe_allow_html=True)

# 2. Ambil API Key & Setup Gemini
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Key belum disetting di Secrets!")
    st.stop()

# 3. UI Pilihan & Upload
option = st.selectbox("Apa yang ingin kamu upload?", ("Gambar (Image)", "Video"))
uploaded_file = st.file_uploader("Pilih file...", type=["jpg", "png", "jpeg", "mp4"])

# 4. Logika Utama
if st.button("🚀 Generate Prompt"):
    if uploaded_file:
        # KITA PAKAI MODEL YANG TERTULIS DI DAFTAR AKUN ANDA
        # Nama ini diambil dari screenshot daftar hijau Anda
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        with st.spinner('Sedang berpikir... (Tunggu sebentar)'):
            try:
                if option == "Gambar (Image)":
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Gambar Upload", width=400)
                    
                    prompt = "Deskripsikan gambar ini detail bahasa Inggris untuk AI Image Generator."
                    response = model.generate_content([prompt, image])
                    
                    st.success("Selesai! Ini Prompt-nya:")
                    st.code(response.text, language="markdown")
                    
                elif option == "Video":
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        tmp.write(uploaded_file.read())
                        video_path = tmp.name

                    st.video(video_path)
                    video_file = genai.upload_file(path=video_path)
                    
                    # Tunggu processing
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai.get_file(video_file.name)

                    if video_file.state.name == "FAILED":
                        st.error("Video gagal diproses.")
                    else:
                        prompt_vid = "Buatkan prompt detail bahasa Inggris untuk video ini."
                        response = model.generate_content([video_file, prompt_vid])
                        st.success("Selesai! Ini Prompt-nya:")
                        st.code(response.text, language="markdown")
                        
            except Exception as e:
                # Jika masih error kuota (429), kita kasih pesan jelas
                if "429" in str(e):
                    st.error("⚠️ Kuota Gratis Harian Habis. Coba lagi besok atau ganti akun Google.")
                else:
                    st.error(f"Error: {e}")
    else:
        st.warning("Upload file dulu ya bos!")
