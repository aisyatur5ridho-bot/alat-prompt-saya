if st.button("🚀 Generate Prompt"):
    if uploaded_file is not None:
        # Kita pakai model LITE yang ada di daftar akun Anda (Pasti Gratis & Jalan)
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
        
        with st.spinner('Sedang melihat & berpikir... (Tunggu sebentar)'):
            try:
                if option == "Gambar (Image)":
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Gambar yang diupload", width=400) # update parameter width
                    
                    # Prompt untuk analisis gambar
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
