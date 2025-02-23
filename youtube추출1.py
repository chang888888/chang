import streamlit as st
import os
import subprocess
from urllib.parse import unquote

# 허용된 Referrer와 User-Agent 목록
ALLOWED_REFERRER = "https://best-no1.blogspot.com"
ALLOWED_USER_AGENTS = [
    "Mozilla", "Chrome", "Safari", "Edge", "Firefox"
]

def check_referrer_and_user_agent():
    # Referrer 확인
    referrer = st.experimental_get_query_params().get("referrer", [""])[0]
    referrer = unquote(referrer)

    # User-Agent 확인
    user_agent = st.request.headers.get("User-Agent", "")

    # Referrer가 올바른지 확인
    if referrer != ALLOWED_REFERRER:
        st.error("이 프로그램은 해당 블로그에서만 사용할 수 있습니다.")
        return False

    # User-Agent가 허용된 브라우저인지 확인
    if not any(agent in user_agent for agent in ALLOWED_USER_AGENTS):
        st.error("올바른 브라우저에서만 접근 가능합니다.")
        return False

    return True

# Referrer와 User-Agent 확인
if check_referrer_and_user_agent():
    st.title("YouTube to MP3 Converter")

    url = st.text_input("YouTube URL을 입력하세요:")
    output_name = st.text_input("파일 이름 (확장자 없이):")

    if st.button("MP3 다운로드"):
        if not url or not output_name:
            st.error("URL과 파일 이름을 모두 입력해주세요.")
        else:
            try:
                # 유튜브 오디오 다운로드 (yt-dlp 사용)
                temp_file = f"{output_name}.webm"
                command_download = [
                    "yt-dlp", "-f", "bestaudio", "--output", temp_file, url
                ]
                subprocess.run(command_download, check=True)

                # FFmpeg를 사용하여 MP3로 변환
                output_file = f"{output_name}.mp3"
                command_convert = [
                    "ffmpeg", "-i", temp_file, "-q:a", "0", "-map", "a", output_file
                ]
                subprocess.run(command_convert, check=True)

                # 임시 파일 삭제
                os.remove(temp_file)
                st.success(f"MP3 파일 생성 완료: {output_file}")
                st.download_button(label="MP3 파일 다운로드", data=open(output_file, "rb"), file_name=f"{output_name}.mp3")

            except Exception as e:
                st.error(f"오류 발생: {e}")
