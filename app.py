import streamlit as st
import os
import tempfile
import subprocess
from pathlib import Path

st.set_page_config(
    page_title="Batch Video Automation Tool",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main > div {
    padding-top: 0.5rem;
}

.block-container {
    max-width: 1100px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: 600;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("Features")

    st.markdown("""
- 📹 Batch Video Processing
- 🎵 Audio Synchronization
- 🏷 Dual Logo Overlay
- ⚡ FFmpeg Automation
- 🌐 Browser-based UI
- ⬇ Download Processed Videos
""")

    st.divider()

    st.caption("Built with Python • Streamlit • FFmpeg")

# ---------------- Header ---------------- #

header_logo, header_text = st.columns(
    [1, 8],
    vertical_alignment="center"
)

with header_logo:
    st.image("assets/logo.png", width=65)

with header_text:
    st.markdown(
        """
        <h1 style="margin:0;padding:0;">
        Batch Video Automation Tool
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            margin-top:6px;
            color:#6c757d;
            font-size:1.05rem;
        ">
        Automate repetitive video processing by combining videos,
        audio tracks, and logos.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.divider()



# ---------------- Feature Cards ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("📹\n\n**Batch Processing**")

with c2:
    st.info("🎵\n\n**Audio Sync**")

with c3:
    st.info("🏷️\n\n**Dual Logo Overlay**")

with c4:
    st.info("⚡\n\n**FFmpeg**")

st.divider()

# ---------------- Tabs ---------------- #

tab1, tab2 = st.tabs(["🎬 Upload & Process", "ℹ️ About"])

# ---------------- About Tab ---------------- #

with tab2:

    st.subheader("Overview")

    st.write(
        "A prototype media automation workflow built as an internship mini task. "
        "Automates the repetitive process of combining video, audio, and branding "
        "assets into finished output files — all through a browser interface, no "
        "terminal needed."
    )

    st.divider()

    st.subheader("Workflow")

    st.markdown("""
1. Upload your video files (.mp4)
2. Upload matching audio tracks (.mp3) — paired by order
3. Upload two branding logos (.png)
4. Click **Generate Batch Videos**
5. Preview each output and download
""")

    st.divider()

    st.subheader("Technology Stack")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Python**\n\nCore processing logic and file handling")

    with col_b:
        st.markdown("**Streamlit**\n\nBrowser-based UI with no frontend code")

    with col_c:
        st.markdown("**FFmpeg**\n\nVideo/audio encoding and logo overlay")

    st.divider()

    st.subheader("Deployment")

    st.write(
        "Deployed on Render. Any machine with Python and FFmpeg installed "
        "can run this locally with `streamlit run app.py`."
    )

# ---------------- Upload Tab ---------------- #

with tab1:

    st.subheader("Upload Files")

    left, right = st.columns(2)

    with left:

        videos = st.file_uploader(
            "📹 Upload Videos",
            type=["mp4"],
            accept_multiple_files=True
        )

        logo1 = st.file_uploader(
            "🏷 Upload Logo 1",
            type=["png"]
        )

    with right:

        audios = st.file_uploader(
            "🎵 Upload Audios",
            type=["mp3"],
            accept_multiple_files=True
        )

        logo2 = st.file_uploader(
            "🏷 Upload Logo 2",
            type=["png"]
        )

    st.divider()

    # ---------------- Upload Summary ---------------- #

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        if videos:
            st.success(f"📹 **Videos**\n\n{len(videos)} Selected")
        else:
            st.info("📹 **Videos**\n\nNone selected")

    with s2:
        if audios:
            st.success(f"🎵 **Audios**\n\n{len(audios)} Selected")
        else:
            st.info("🎵 **Audios**\n\nNone selected")

    with s3:
        if logo1:
            st.success(f"🏷 **Logo 1**\n\n{logo1.name}")
        else:
            st.info("🏷 **Logo 1**\n\nNot selected")

    with s4:
        if logo2:
            st.success(f"🏷 **Logo 2**\n\n{logo2.name}")
        else:
            st.info("🏷 **Logo 2**\n\nNot selected")

    # ---------------- Uploaded File List Expander ---------------- #

    if videos or audios:
        with st.expander("View Selected Files"):
            if videos:
                st.write("### Videos")
                for v in videos:
                    st.write("•", v.name)
            if audios:
                st.write("### Audios")
                for a in audios:
                    st.write("•", a.name)

    st.divider()

    generate = st.button(
        "🚀 Generate Batch Videos",
        type="primary"
    )

    if generate:

        if not videos or not audios or not logo1 or not logo2:
            st.error("Please upload all required files before continuing.")

        else:

            with st.spinner("Generating videos..."):

                progress = st.progress(0)

                status = st.empty()

                download_section = st.container()

                logo1_bytes = logo1.read()
                logo2_bytes = logo2.read()

                total = min(len(videos), len(audios))

                generated_files = []

                for i in range(total):

                    progress.progress(i / total, text=f"Video {i+1} / {total}")

                    status.info(f"Processing video {i+1} of {total}...")

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

                    # ---------------- FFmpeg Command (original logic preserved) ---------------- #

                    command = (
                        f'ffmpeg -y '
                        f'-i "{video_path}" '
                        f'-i "{audio_path}" '
                        f'-i "{logo1_path}" '
                        f'-i "{logo2_path}" '
                        f'-filter_complex '
                        f'"[2:v]scale=100:-1[l1];'
                        f'[3:v]scale=100:-1[l2];'
                        f'[0:v][l1]overlay=20:20[tmp1];'
                        f'[tmp1][l2]overlay=W-w-20:20[v]" '
                        f'-map "[v]" '
                        f'-map 1:a '
                        f'-shortest '
                        f'-c:v libx264 '
                        f'-c:a aac '
                        f'"{output}"'
                    )

                    process = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )

                    if process.returncode != 0:

                        st.error(
                            f"❌ FFmpeg failed while processing "
                            f"{videos[i].name}"
                        )

                        with st.expander("View FFmpeg Error"):
                            st.code(process.stderr)

                        for path in [video_path, audio_path, logo1_path, logo2_path]:
                            try:
                                if os.path.exists(path):
                                    os.remove(path)
                            except Exception:
                                pass

                        continue

                    if os.path.exists(output):
                        generated_files.append(output)
                    else:
                        st.warning(f"{output} was not created.")

                    for path in [video_path, audio_path, logo1_path, logo2_path]:
                        try:
                            if os.path.exists(path):
                                os.remove(path)
                        except Exception:
                            pass

                progress.progress(100, text="Done")

                status.success("Processing complete.")

            # ---------------- Downloads ---------------- #

            st.divider()

            st.subheader("Downloads")

            if generated_files:

                with download_section:

                    st.success(
                        f"Successfully generated {len(generated_files)} video(s)."
                    )

                    for idx, file_path in enumerate(generated_files, start=1):

                        st.markdown(f"**Output {idx}**")

                        preview_col, download_col = st.columns([2, 1])

                        with preview_col:
                            st.video(file_path)

                        with download_col:
                            st.write("")
                            st.write("")
                            with open(file_path, "rb") as file:
                                st.download_button(
                                    label=f"⬇ Download Output {idx}",
                                    data=file,
                                    file_name=Path(file_path).name,
                                    mime="video/mp4",
                                    use_container_width=True
                                )

                        st.divider()

                status.success("✅ Batch Processing Complete!")

            else:

                status.error("No output videos were generated.")

# ---------------- Footer ---------------- #

st.divider()

st.caption("Built with Python • Streamlit • FFmpeg")

