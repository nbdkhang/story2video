import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import nltk

nltk.download('punkt')
genai.configure(api_key="AIzaSyCkwncvHXfqUSsri-ePJeOv0plRLEjkB_Y")
model = genai.GenerativeModel('gemini-1.5-flash')
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }
PROMPT_FORMAT='''
Thay thế các đại từ trong đoạn văn sau bằng đối tượng cụ thể,
các đại từ có thể là: chúng, nó, họ, mình, bạn, người ta, ai đó, cái này, cái kia, con vật,...
Câu truyền vào như sau:\n\n
{prompt}
'''
PROMPT_SUMMARY='''
Bạn là 1 con AI phân tích các nội dung chính trong câu và trả về 1 đoạn hoàn chỉnh
loại bỏ các từ không cần thiết, các nội dung cần trả lời gồm:
- đối tượng như thế nào?
- hành động là gì?
- bối cảnh như thế nào (nếu không đề cập thì tự sinh ra)?.
Trả về một đoạn ngắn chứa đầy đủ thông tin truyền vào
Câu thông tin được truyền vào:
{prompt}
'''
def format_prompt(prompt):
  response = model.generate_content(PROMPT_FORMAT.format(prompt=prompt),safety_settings=safety_settings)
  return response.text.strip()

def split_sentence(paragraph):
  paragraph = ' '.join(paragraph.split())
  sentences = [sentence for sentence in nltk.sent_tokenize(paragraph) if sentence.strip()]
  return sentences
def sentence_sum(paragraph):
    sum=[]
    for sentence in paragraph:
        response = model.generate_content(PROMPT_SUMMARY.format(prompt=sentence),safety_settings=safety_settings)
        sum.append(response.text.strip())
    return sum


def format_story(text):
  text_format=format_prompt(text)
  sentences= split_sentence(text_format)
  story = sentence_sum(sentences)
  return story
