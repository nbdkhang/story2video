from moviepy.editor import *
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os
from deep_translator import GoogleTranslator
from image_generation import generate_image
from processing.text_processing import format_prompt, split_sentence, sentence_sum, format_story
import textwrap

text='''
Đây là một câu truyện cổ tích về loài vật kể về một con cáo bắt gặp một chùm nho chín đỏ căng mọng hấp dẫn khiến cáo thèm nhỏ rãi nên đã có ý định nhảy lên để hái chùm nho. Vì khoảng cách của cáo và chùm nho khá xa nên nó đã đi xa gốc cây một khoảng để lấy được đà nhảy lên hái chùm nho, nhưng lần nhảy đầu tiên thì cáo không với tới chỉ cần một xíu nữa là có thể hái được chùm nho.
Nó cố gắng thử thêm vài lần nữa nhưng dù cố gắng đến mấy cũng không thể, tất cả đều vô ích. Cáo ngồi xuống và nhìn chùm nho tức tối, và tự nhủ thầm rằng nó ngu lắm, chùm nho còn xanh làm sao mà ăn được, nó phải mất bao nhiêu công chỉ để hái chùm nho còn xanh và chua chát kia không đáng người ta ngó tới. Sau đó khinh khỉnh bỏ đi không thèm hái nữa.
'''
story_img = format_story(text)
story_audio = split_sentence(text)

# Tạo âm thanh từ văn bản
def wrap_text(text, width):
    return "\n".join(textwrap.wrap(text, width))
def create_audio(text, filename):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
font_path = "/content/Arial.ttf"
# Tạo hình ảnh từ văn bản
def create_image(text_img, text_audio, filename):
    en_text = GoogleTranslator(source='vi', target='en').translate(text_img)
    en_text = en_text + " highly detailed & reality,  vibrant colors and no confusion between objects"
    img = generate_image(en_text)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 20)
    wrapped_text = wrap_text(text_audio, 50)
    d.text((10, 10), wrapped_text, fill=(255, 255, 255), font=font)
    img.save(filename)

# Danh sách các video clip
clips = []

# Tạo video cho từng đoạn văn
for i, (audio_sentence, img_sentence) in enumerate(zip(story_audio, story_img)):
    audio_file = f"audio_{i}.mp3"
    image_file = f"image_{i}.png"

    create_audio(audio_sentence, audio_file)
    create_image(img_sentence,audio_sentence, image_file)

    # Tạo video clip từ hình ảnh và âm thanh
    img_clip = ImageClip(image_file).set_duration(4)  # Hiển thị hình ảnh trong 4 giây
    audio_clip = AudioFileClip(audio_file)

    img_clip = img_clip.set_duration(audio_clip.duration)

    video_clip = img_clip.set_audio(audio_clip)
    clips.append(video_clip)

# Kết hợp các video clip lại
final_video = concatenate_videoclips(clips, method="compose")

# Xuất video
final_video.write_videofile("cinderella_video.mp4", fps=24)

# Xóa tệp âm thanh và hình ảnh tạm thời
for i in range(len(story_audio)):
    os.remove(f"audio_{i}.mp3")
    os.remove(f"image_{i}.png")