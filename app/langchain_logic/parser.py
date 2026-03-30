from langchain_core.output_parsers import PydanticOutputParser
from app.schema import CareerInputPredict, CareerInputChat

parser = PydanticOutputParser(pydantic_object= CareerInputChat)

