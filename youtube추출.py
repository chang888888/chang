import streamlit as st
import os
import subprocess
from urllib.parse import unquote

# 내 블로그 주소 (예: https://best-no1.blogspot.com)
ALLOWED_REFERRER = "https://best-no1.blogspot.com"

def check_referrer():
    # URL 쿼리 파라미터로 전달된 referrer 확인 (디코딩 포함)
    referrer = st.query_params.get("referrer", [""])[0]
    referrer = unquote(referrer)  # URL 디코딩
    
    # 디버그용 (Referrer 정보 확인)
    st.write("디코딩된 Referrer:", referrer)
    
    # Referrer 확인
    if ALLOWED_REFERRER in referrer or referrer.startswith(ALLOWED_REFERRER):
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
