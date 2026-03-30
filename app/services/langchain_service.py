from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from app.langchain_logic.prompts import CV_EXTRACT_PROMPT_TEMPLATE as CV_EXTRACT_PROMPT
from app.langchain_logic.parser import parser
load_dotenv()

class LangChainService:
    def __init__(self):
        self.llm = ChatGroq(
            model = "llama-3.3-70b-versatile",
            groq_api_key = os.getenv("GEMENI_API_KEY"),
            temperature = 0.2 # Adjust temperature lower to make the output more deterministic, or higher for more creativity
        )
        prompt_template = ChatPromptTemplate.from_template(CV_EXTRACT_PROMPT)
        self.chain = prompt_template | self.llm | parser
    
    def process_input(self, text_content: str, current_data: dict):
        try:
            result =  self.chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "context": text_content,
                "current_data": current_data,
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
    
    