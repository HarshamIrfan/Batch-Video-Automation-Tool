import streamlit as st
import os
import tempfile
import subprocess

st.title("Batch Video Automation Tool")

videos = st.file_uploader("Upload Videos", type=["mp4"], accept_multiple_files=True)
audios = st.file_uploader("Upload Audios", type=["mp3"], accept_multiple_files=True)
logo1 = st.file_uploader("Upload Logo 1", type=["png"])
logo2 = st.file_uploader("Upload Logo 2", type=["png"])

if st.button("Generate Batch Videos"):

    if not videos or not audios or not logo1 or not logo2:
        st.error("Upload all required files!")
    else:

        logo1_bytes = logo1.read()
        logo2_bytes = logo2.read()

        for i in range(min(len(videos), len(audios))):

            videos[i].seek(0)
            audios[i].seek(0)

            video_bytes = videos[i].read()
            audio_bytes = audios[i].read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as v:
                v.write(video_bytes)
                video_path = v.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as a:
                a.write(audio_bytes)
                audio_path = a.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as l1:
                l1.write(logo1_bytes)
                logo1_path = l1.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as l2:
                l2.write(logo2_bytes)
                logo2_path = l2.name

            output = f"output_{i}.mp4"

            command = f'ffmpeg -y -i "{video_path}" -i "{audio_path}" -i "{logo1_path}" -i "{logo2_path}" ' \
                      f'-filter_complex "[2:v]scale=100:-1[l1];[3:v]scale=100:-1[l2];[0:v][l1]overlay=20:20[tmp1];[tmp1][l2]overlay=W-w-20:20[v]" ' \
                      f'-map "[v]" -map 1:a -shortest -c:v libx264 -c:a aac "{output}"'

            process = subprocess.run(command, shell=True, capture_output=True, text=True)

            if process.returncode != 0:
                st.error(f"FFmpeg Failed for file {i+1}")
                st.text(process.stderr)
                continue

            if os.path.exists(output):
                with open(output, "rb") as file:
                    st.download_button(
                        label=f"Download Output {i+1}",
                        data=file,
                        file_name=output,
                        mime="video/mp4"
                    )
            else:
                st.error(f"{output} was not created")

        st.success("Batch Processing Complete!")