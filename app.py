import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Video to Prompt AI", layout="centered")

st.markdown("<h3 style='text-align: center;'>🎬 AI Video/Image to Prompt</h3>", unsafe_allow_html=True)
st.write("Upload gambar atau video, AI akan membuatkan prompt detail untukmu.")

# 2. Ambil API Key & Setup Gemini
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Key belum disetting di Secrets!")
    st.stop()

# 3. UI Pilihan & Upload
option = st.selectbox("Apa yang ingin kamu upload?", ("Gambar (Image)", "Video"))
uploaded_file = st.file_uploader("Pilih file...", type=["jpg", "png", "jpeg", "mp4"])

# 4. Logika Utama (Tombol ditekan)
if st.button("🚀 Generate Prompt"):
    if uploaded_file is not None:
        # PENTING: Kita ganti ke model EXPERIMENTAL (-exp) yang biasanya jatah gratisnya banyak!
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        with st.spinner('Sedang melihat & berpikir... (Tunggu sebentar)'):
            try:
                if option == "Gambar (Image)":
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Gambar yang diupload", width=400)
                    
                    prompt = "Deskripsikan gambar ini secara sangat detail dalam bahasa Inggris sebagai prompt untuk AI Image Generator. Fokus pada gaya visual, pencahayaan, dan subjek."
                    response = model.generate_content([prompt, image])
                    
                    st.success("Selesai! Ini Prompt-nya:")
                    st.code(response.text, language="markdown")
                    
                elif option == "Video":
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        video_path = tmp_file.name

                    st.video(video_path)
                    
                    video_file = genai.upload_file(path=video_path)
                    
                    import time
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = genai.get_file(video_file.name)

                    if video_file.state.name == "FAILED":
                        st.error("Gagal memproses video.")
                    else:
                        prompt_video = "Tonton video ini. Buatkan prompt teks detail bahasa Inggris untuk AI Video Generator."
                        response = model.generate_content([video_file, prompt_video])
                        st.success("Selesai! Ini Prompt-nya:")
                        st.code(response.text, language="markdown")
                        
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Silakan upload file dulu ya!")

st.markdown("---")
st.caption("Dibuat untuk Komunitas Blogger")
