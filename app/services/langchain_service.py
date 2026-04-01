from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from openai import api_key
from app.langchain_logic.prompts import CHAT_EXTRACT_PROMPT_TEMPLATE as CHAT_EXTRACT_PROMPT
from app.langchain_logic.prompts import CV_EXTRACT_PROMPT_TEMPLATE as CV_EXTRACT_PROMPT
from app.langchain_logic.parser import parser, parser_CV

load_dotenv()

class LangChainService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="google/gemini-2.5-flash", # Thêm prefix 'google/' theo chuẩn OpenRouter
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPEN_ROUTER"),
            temperature=1,
            default_headers={
                "HTTP-Referer": "http://localhost:3000", # Tùy chọn: Để OpenRouter xếp hạng app của bạn
                "X-Title": "Career Advisory System"      # Tùy chọn
            },
            max_tokens=1000
        )
        prompt_template_chat = ChatPromptTemplate.from_template(CHAT_EXTRACT_PROMPT)
        self.chain_chat = prompt_template_chat | self.llm | parser

        prompt_template_cv = ChatPromptTemplate.from_template(CV_EXTRACT_PROMPT)
        self.chain_cv = prompt_template_cv | self.llm | parser

    
    def process_input_pdf(self, content:str):
        try:
            print("Ham cailol")
            result = self.chain_cv.invoke({
                "format_instructions": parser.get_format_instructions(),
                "context": content,
            })
            if hasattr(result, "dict"):
                final_result = result.dict()
            else:
                final_result = result
            print("Extracted data from: ", final_result)
            return final_result

        except Exception as e:
            print(f"Error in LangChainService in reading CV: {str(e)}")
            return {"error": "Đã có lỗi xảy ra khi xử lý thông tin. Vui lòng thử lại sau."}

    def process_input(self, text_content: str, missing_field: list, user_msg: str = None):
        try:
            print("User message: ", user_msg)
            print("Current data: ", missing_field)

            # clean_data = {k: (v if v is not None else "Chưa có") for k, v in current_data.items()}

            # print("Clean data sent to LLM: ", clean_data)
            result =  self.chain_chat.invoke({
                "format_instructions": parser.get_format_instructions(),
                "context": text_content,
                "missing_field": missing_field,
                "user_msg": user_msg
            })
            if hasattr(result, "dict"):
                final_result = result.dict()
            else:
                final_result = result
            print("Extracted data: ", final_result)
            return final_result
        except Exception as e:
            print(f"Error in LangChainService: {str(e)}")
            return {"error": "Đã có lỗi xảy ra khi xử lý thông tin. Vui lòng thử lại sau."}
    
    