import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import nltk
import re

nltk.download("punkt")
nltk.download("punkt_tab")

genai.configure(api_key="AIzaSyCkwncvHXfqUSsri-ePJeOv0plRLEjkB_Y")
model = genai.GenerativeModel("gemini-1.5-flash")
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}
PROMPT_FORMAT = """
Thay thế các đại từ trong đoạn văn sau bằng đối tượng cụ thể,
các đại từ có thể là: chúng, nó, họ, mình, bạn, người ta, ai đó, cái này, cái kia, con vật,...
Câu truyền vào như sau:\n\n
{prompt}
"""
PROMPT_SUMMARY = {
    "long_prompt": """
  Bạn là 1 con AI phân tích các nội dung chính trong câu và trả về 1 đoạn hoàn chỉnh
  loại bỏ các từ không cần thiết, các nội dung cần trả lời gồm:
  - đối tượng là gì? màu của đối tượng cần thống nhất?
  - hành động là gì? khoảng cách các vật như thế nào?
  - bối cảnh như thế nào (nếu không đề cập thì tự sinh ra)?.
  Trả về một đoạn ngắn chứa tóm tắt thông tin truyền vào trong 1 câu bằng tiếng anh
  Câu thông tin được truyền vào:
  {prompt}
  Nội dụng phía trước của câu truyện là: 
  {context}
  """,
    "short_prompt": """
  Gợi ý về số lượng ảnh cần để mô tả câu truyện và mô tả cho từng ảnh theo mẫu sau :
  **Số lượng ảnh: x ảnh**

  **Ảnh x:**

  * **Description:**
  * **Note:**
  Ví dụ như
  Xác định các đối tượng trong câu chuyện. Không tạo ra những đối tượng không liên quan
  * **Description:**  Con cáo đang đứng dưới gốc cây, nhìn chùm nho chín đỏ căng mọng trên cao.
  * **Note:** Con cáo nhìn chùm nho trên cao.
  Description là nguyên văn câu câu chuyện
  Dựa vào Description để tạo ra Note
  Note là câu đơn ngắn ngọn bao gổm mô tả hành động, vị trí của đối tượng(trên cao, bên dưới, bên trái, bên phải ...) . Không cần các miêu tả cảm xúc
  Note sẽ được dịch sang tiếng Anh
  Câu truyền vào như sau:\n\n
  {prompt}
  """,
}


def format_prompt(prompt):
    response = model.generate_content(
        PROMPT_FORMAT.format(prompt=prompt), safety_settings=safety_settings
    )
    return response.text.strip()


def split_sentence(paragraph):
    paragraph = " ".join(paragraph.split())
    sentences = [
        sentence for sentence in nltk.sent_tokenize(paragraph) if sentence.strip()
    ]
    return sentences


def story_for_long_type(prompt_summary, paragraph):
    sum = []
    for sentence in paragraph:
        print("sentence:" + sentence)
        response = model.generate_content(
            prompt_summary.format(prompt=sentence, context=sum),
            safety_settings=safety_settings,
        )
        sum.append(response.text.strip())
        print("response:" + response.text.strip())
    return sum


def story_for_short_type(prompt_summary, paragraph):
    response = model.generate_content(prompt_summary.format(prompt=paragraph), safety_settings=safety_settings)
    img_desc = response.text.strip()
    notes = re.findall(r"\*\*Note:\*\* (.+)", img_desc)
    return notes


def format_story(paragraph, prompt_type):
    match prompt_type:
        case "long_prompt":
            text_format = format_prompt(paragraph)
            sentences = split_sentence(text_format)
            story = story_for_long_type(PROMPT_SUMMARY["long_prompt"], sentences)
        case "short_prompt":
            text_format = format_prompt(paragraph)
            sentences = split_sentence(text_format)
            story = story_for_short_type(PROMPT_SUMMARY["short_prompt"], sentences)

    return story
