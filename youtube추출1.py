import streamlit as st
import yt_dlp
import os

# 제목
st.title("YouTube to MP3 Converter")

# YouTube URL 및 파일 이름 입력
youtube_url = st.text_input("YouTube URL을 입력하세요:")
file_name = st.text_input("파일 이름 (확장자 없이):")

# MP3 다운로드 버튼
if st.button("MP3 다운로드"):
    if youtube_url and file_name:
        # 다운로드 옵션 설정
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{file_name}.mp3",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            st.success(f"MP3 파일 생성 완료: {file_name}.mp3")

            # 파일 다운로드 링크 제공
            with open(f"{file_name}.mp3", "rb") as file:
                btn = st.download_button(
                    label="MP3 파일 다운로드",
                    data=file,
                    file_name=f"{file_name}.mp3",
                    mime="audio/mpeg"
                )
            
            # 다운로드 후 파일 삭제
            os.remove(f"{file_name}.mp3")

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
    else:
        st.error("YouTube URL과 파일 이름을 모두 입력하세요.")
