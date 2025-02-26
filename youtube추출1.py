import streamlit as st
import os
import subprocess

# 허용할 블로그 주소
ALLOWED_REFERRER = "https://best-no1.blogspot.com"

def check_referrer():
    # Referrer 확인 (st.query_params 사용)
    query_params = st.query_params
    referrer = query_params.get("referrer", "")

    # 리스트일 경우 첫 번째 값 가져오기
    if isinstance(referrer, list):
        referrer = referrer[0]

    # 디버깅: Referrer 값 출력
    st.write(f"디버깅 - Referrer: {referrer}")

    # Referrer가 블로그에서 온 경우만 True 반환
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

    if st.button("MP3 파일변환"):
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
