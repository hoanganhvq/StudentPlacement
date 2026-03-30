from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.schema import CareerInputPredict, ChatInput
from app.services.model_service import model_service, PredictionResponse
from fastapi.encoders import jsonable_encoder
from app.services.langchain_service import LangChainService

import fitz  
import uvicorn
langchain_service = LangChainService()
app = FastAPI(title="He thong Tu van su nghiep thong minh")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return{
        "message": "AI server is ok"
    }

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_career(data: CareerInputPredict):
    try:
        result = model_service.predict(data)
        print("Return ok: ")
        print(result)
        return result
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý Model: {str(e)}")


@app.post("/api/chat/extract")
async def extract_info(file: UploadFile = File(None), message: str = None):
    if file is None and message is None:
        raise HTTPException(status_code=400, detail="Cần cung cấp file CV hoặc đoạn chat để trích xuất thông tin.")
    
    content = ""
    if file:
        pdf_data = await file.read()
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        content = " ".join([page.get_text() for page in doc])
    elif message:
        content = message

    result = langchain_service.process_input(content)
    return result

@app.post("/api/handle_chat")
async def handle_chat(data: ChatInput):
    try:
        print("Goi handle chat")
        result = langchain_service.process_input(
            text_content=data.message, 
            current_data=data.current_data.dict() # Chuyển pydantic sang dict
        )
        return result
    except Exception as e:
        print(f"Error in handle_chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý chat: {str(e)}")

if __name__ == "__main__":
    print("Dang chay server.....")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
