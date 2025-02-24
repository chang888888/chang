import streamlit as st
import os
import subprocess
from urllib.parse import unquote, quote
import uuid
import time

# ✅ 최신 Streamlit 방식 적용
st.set_page_config(page_title="YouTube to MP3 Converter", layout="centered")

# ⏳ 토큰 및 세션 상태 저장소
TOKENS = {}
TOKEN_EXPIRY_TIME = 86400  # 5분 (300초)

# 🎫 UUID 토큰 생성 함수
def generate_token():
    token = str(uuid.uuid4())
    TOKENS[token] = time.time()
    return token

# ✅ 토큰 유효성 검사 함수
def validate_token(token):
    # 토큰이 존재하지 않으면 False
    if token not in TOKENS:
        return False

    # 5분 이내에만 유효
    if time.time() - TOKENS[token] > TOKEN_EXPIRY_TIME:
        del TOKENS[token]  # 만료된 토큰 삭제
        return False

    return True

# 🔐 세션 상태 초기화
if 'is_valid_session' not in st.session_state:
    st.session_state.is_valid_session = False

# 🔄 URL 생성 및 리다이렉트 처리
def handle_url_generation():
    query_params = st.experimental_get_query_params()
    if "generate_url" in query_params:
        # 새로운 UUID 토큰 생성
        new_token = generate_token()
        # 새 URL 생성
        new_url = f"https://youtube-mp3-converter.streamlit.app/?token={new_token}"
        # URL 리다이렉트
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={new_url}">', unsafe_allow_html=True)
        st.stop()

# 🔄 URL 생성 처리
handle_url_generation()

# 🔒 Token 및 Session State 검사
def check_token_and_session():
    query_params = st.experimental_get_query_params()
    token = query_params.get("token", [""])[0]

    # 토큰 검사
    if validate_token(token):
        # 세션 상태 활성화
        st.session_state.is_valid_session = True
        # 사용된 토큰 삭제 (1회용)
        del TOKENS[token]
    else:
        st.error("잘못된 접근입니다. 블로그에서 다시 접속하세요.")
        st.stop()

# 🚦 Streamlit 앱 본문
if st.session_state.is_valid_session:
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
else:
    check_token_and_session()
