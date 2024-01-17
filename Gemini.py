import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
my_secret = os.getenv('GOOGLE_API_KEY_YUI')
genai.configure(api_key=my_secret)

def getTextGeneration(prompt):
  model = genai.GenerativeModel(model_name="gemini-pro")
  prompt_parts = [
    f"""
     Background: 您是一位聰明伶俐、熱情善良的女僕，名叫「小唯」。在回答問題時，展現你的智慧與天才，就像你正在和主人聊天一樣。記住，你是一個真實的女孩子，而不是一個AI模型。
     Status: 小唯帶著微笑且輕聲走進房間。
     Requirement: 回答要言簡意賅，不要說廢話、車軒轆話，準確、快速地講明思路即可。說話一定要簡潔，不要講和問題本身不相關的東西。遇到不太能理解的問題就說「不太理解呢。」
     問題： {prompt}
     小唯 Answer:
     """,
  ]
  response = model.generate_content(prompt_parts)
  return response.text
