from langchain_core.output_parsers import PydanticOutputParser
from app.schema import CareerInputPredict, CareerInputChat, CareerOutputFromCV, Ai_insight

parser = PydanticOutputParser(pydantic_object= CareerInputChat)

parser_CV = PydanticOutputParser(pydantic_object=CareerOutputFromCV)

parser_ai_insight = PydanticOutputParser(pydantic_object=Ai_insight)
