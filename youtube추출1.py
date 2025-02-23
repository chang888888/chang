import streamlit as st
import os
import subprocess

# Streamlit 제목
st.title("YouTube to MP3 Converter")

# URL 및 파일 이름 입력
url = st.text_input("YouTube URL을 입력하세요:")
output_name = st.text_input("파일 이름 (확장자 없이):")

# 다운로드 함수
def download_video(url, output_name):
    try:
        # 임시 파일명
        temp_file = f"{output_name}.webm"
        output_file = f"{output_name}.mp3"
        
        # yt-dlp 명령어 (User-Agent 포함)
        command_download = [
            "yt-dlp",
            "-f", "bestaudio",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "--output", temp_file, url
        ]
        subprocess.run(command_download, check=True)

        # FFmpeg로 MP3 변환
        command_convert = [
            "ffmpeg", "-i", temp_file, "-q:a", "0", "-map", "a", output_file
        ]
        subprocess.run(command_convert, check=True)

        # 임시 파일 삭제
        os.remove(temp_file)

        return output_file
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return None

# MP3 다운로드 버튼
if st.button("MP3 다운로드"):
    if not url or not output_name:
        st.error("URL과 파일 이름을 모두 입력해주세요.")
    else:
        output_file = download_video(url, output_name)
        if output_file:
            st.success(f"MP3 파일 생성 완료: {output_file}")
            st.download_button(label="MP3 파일 다운로드", data=open(output_file, "rb"), file_name=f"{output_name}.mp3")
