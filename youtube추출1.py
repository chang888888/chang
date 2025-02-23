import streamlit as st
import os
import subprocess
from urllib.parse import urlparse

# 허용된 Referrer
ALLOWED_REFERRER = "best-no1.blogspot.com"

# Referrer 확인 함수
def check_referrer():
    referrer = st.experimental_get_query_params().get("referrer", [""])[0]
    if ALLOWED_REFERRER in urlparse(referrer).netloc:
        return True
    else:
        st.error("이 프로그램은 해당 블로그에서만 사용할 수 있습니다.")
        return False

# Referrer 확인
if check_referrer():
    st.title("YouTube to MP3 Converter")

    url = st.text_input("YouTube URL을 입력하세요:")
    output_name = st.text_input("파일 이름 (확장자 없이):")

    if st.button("MP3 다운로드"):
        if not url or not output_name:
            st.error("URL과 파일 이름을 모두 입력해주세요.")
        else:
            try:
                temp_file = f"{output_name}.webm"
                command_download = [
                    "yt-dlp", "-f", "bestaudio", "--output", temp_file, url
                ]
                subprocess.run(command_download, check=True)

                output_file = f"{output_name}.mp3"
                command_convert = [
                    "ffmpeg", "-i", temp_file, "-q:a", "0", "-map", "a", output_file
                ]
                subprocess.run(command_convert, check=True)

                os.remove(temp_file)
                st.success(f"MP3 파일 생성 완료: {output_file}")
                st.download_button(label="MP3 파일 다운로드", data=open(output_file, "rb"), file_name=f"{output_name}.mp3")

            except Exception as e:
                st.error(f"오류 발생: {e}")
