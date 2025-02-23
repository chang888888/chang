import streamlit as st
from pytube import YouTube
import os
from pydub import AudioSegment
import requests

st.title("YouTube to MP3 Converter")

url = st.text_input("YouTube URL을 입력하세요:")
output_name = st.text_input("파일 이름 (확장자 없이):")

def download_video(url, output_name):
    try:
        # User-Agent 설정 (YouTube 차단 방지)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        
        # YouTube에서 비디오 정보 가져오기
        yt = YouTube(url, headers=headers)
        stream = yt.streams.filter(only_audio=True).first()
        temp_file = stream.download(filename=f"{output_name}.mp4")

        # MP3로 변환
        audio = AudioSegment.from_file(temp_file)
        output_file = f"{output_name}.mp3"
        audio.export(output_file, format="mp3")

        # 임시 파일 삭제
        os.remove(temp_file)
        return output_file
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return None

if st.button("MP3 다운로드"):
    if not url or not output_name:
        st.error("URL과 파일 이름을 모두 입력해주세요.")
    else:
        output_file = download_video(url, output_name)
        if output_file:
            st.success(f"MP3 파일 생성 완료: {output_file}")
            st.download_button(label="MP3 파일 다운로드", data=open(output_file, "rb"), file_name=f"{output_name}.mp3")
