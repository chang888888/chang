import streamlit as st
import os
import subprocess
from urllib.parse import unquote
import uuid
import time

# 허용된 Referrer
ALLOWED_REFERRER = "https://best-no1.blogspot.com"

# 임시 토큰 저장소
tokens = {}

# UUID 토큰 생성 함수
def generate_token():
    token = str(uuid.uuid4())
    tokens[token] = time.time()
    return token

# 토큰 유효성 검사 함수
def validate_token(token):
    # 토큰이 존재하지 않으면 False
    if token not in tokens:
        return False

    # 5분 이내에만 유효
    if time.time() - tokens[token] > 300:
        del tokens[token]  # 만료된 토큰 삭제
        return False

    # 유효한 토큰은 사용 후 삭제
    del tokens[token]
    return True

# Referrer와 Token 검사
def check_referrer_and_token():
    # URL 파라미터에서 Referrer와 Token 확인
    query_params = st.query_params  # ✅ 최신 방식으로 수정
    referrer = query_params.get("referrer", [""])[0]
    referrer = unquote(referrer)
    token = query_params.get("token", [""])[0]

    # Referrer 검사
    if not referrer.startswith(ALLOWED_REFERRER):
        st.error("이 프로그램은 해당 블로그에서만 사용할 수 있습니다.")
        return False

    # 토큰 검사
    if not validate_token(token):
        st.error("접근 권한이 유효하지 않습니다. 블로그에서 다시 접속하세요.")
        return False

    return True

# URL 생성 및 리다이렉트 처리
def handle_url_generation():
    query_params = st.query_params  # ✅ 최신 방식으로 수정
    if "generate_url" in query_params:
        # 새로운 UUID 토큰 생성
        new_token = generate_token()
        # 새 URL 생성
        new_url = f"https://youtube-mp3-converter.streamlit.app/?referrer={ALLOWED_REFERRER}&token={new_token}"
        # URL 리다이렉트
        st.markdown(f'<meta http-equiv="refresh" content="0; URL={new_url}">', unsafe_allow_html=True)
        st.stop()

# URL 생성 처리
handle_url_generation()

# Streamlit 앱 본문
if check_referrer_and_token():
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
    st.error("잘못된 접근입니다.")
