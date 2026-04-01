from langchain_core.output_parsers import PydanticOutputParser
from app.schema import CareerInputPredict, CareerInputChat, CareerOutputFromCV

parser = PydanticOutputParser(pydantic_object= CareerInputChat)

parser_CV = PydanticOutputParser(pydantic_object=CareerOutputFromCV)