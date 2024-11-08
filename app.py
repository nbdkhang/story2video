import streamlit as st
from processing.text_processing import format_prompt, split_sentence, sentence_sum, format_story
from processing.image_generation import generate_image
from processing.audio_video_creation import create_audio, create_image

# Giao diện người dùng Streamlit
st.title("Tạo Video từ Văn Bản")

# Nhập văn bản
text = st.text_area("Nhập nội dung văn bản để tạo video:")

if text:
    # Xử lý văn bản và tạo câu chuyện
    story_img = format_story(text)
    story_audio = split_sentence(text)

    clips = []
    for i, (audio_sentence, img_sentence) in enumerate(zip(story_audio, story_img)):
        audio_file = f"audio_{i}.mp3"
        image_file = f"image_{i}.png"

        create_audio(audio_sentence, audio_file)
        create_image(img_sentence, audio_sentence, image_file)

        # Tạo video clip từ hình ảnh và âm thanh
        img_clip = ImageClip(image_file).set_duration(4)
        audio_clip = AudioFileClip(audio_file)
        img_clip = img_clip.set_duration(audio_clip.duration)
        video_clip = img_clip.set_audio(audio_clip)
        clips.append(video_clip)

    # Kết hợp các video clip lại
    final_video = concatenate_videoclips(clips, method="compose")

    # Xuất video
    final_video.write_videofile("output_video.mp4", fps=24)

    # Tải video
    st.video("output_video.mp4")