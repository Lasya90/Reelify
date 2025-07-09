import streamlit as st
import os
import ffmpeg
import shutil

# Temporary folders
TEMP_DIR = "temp"
AUDIO_PATH = os.path.join(TEMP_DIR, "audio.wav")
VERTICAL_VIDEO = os.path.join(TEMP_DIR, "vertical_output.mp4")

os.makedirs(TEMP_DIR, exist_ok=True)

st.title("🎬 Reelify - Video Processor")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
if uploaded_file:
    input_path = os.path.join(TEMP_DIR, uploaded_file.name)

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded")

    if st.button("Extract Audio & Convert Video to Reel Format"):
        # Extract Audio
        st.info("🔊 Extracting audio...")
        try:
            ffmpeg.input(input_path).output(AUDIO_PATH, **{'q:a': 0, 'map': 'a'}).run()
            st.success("✅ Audio extracted: audio.wav")
        except ffmpeg.Error as e:
            st.error(f"Audio extraction failed: {e}")

        # Resize to 1080x1920 with padding
        st.info("🎥 Converting to vertical format...")
        try:
            ffmpeg.input(input_path).output(
                VERTICAL_VIDEO,
                vf="scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
            ).run()
            st.success("✅ Converted video saved as vertical_output.mp4")

            st.video(VERTICAL_VIDEO)
        except ffmpeg.Error as e:
            st.error(f"Video resizing failed: {e}")

    if st.button("Clean Temporary Files"):
        shutil.rmtree(TEMP_DIR)
        st.success("🧹 Cleaned temp files.")
