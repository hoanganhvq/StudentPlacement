
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal

class CareerInputChat(BaseModel):
    cgpa: Optional[float] = Field(default=None)
    backlogs: Optional[int] = Field(default=None)
    college_tier: Optional[Literal['Tier 1', 'Tier 2', 'Tier 3']] = Field(default=None)
    country: Optional[Literal['Germany', 'USA', 'UK', 'Canada', 'India']] = Field(default=None)
    university_ranking_band: Optional[Literal['Top 100', '100-300', '300+']] = Field(default=None)
    internship_count: Optional[int] = Field( description="Số lần thực tập (nếu có)", default=None)
    aptitude_score: Optional[float] = Field(ge=30, le=100, description="Điểm đánh giá năng lực định lượng từ 30 đến 100", default=None)
    communication_score: Optional[float] = Field(ge=30, le=100, description="Điểm đánh giá kỹ năng giao tiếp từ 30 đến 100", default=None)
    specialization: Optional[Literal["AI/ML", "Data Science", "Cybersecurity", "Cloud", "Core CS"]] = Field( description="Chuyên ngành", default=None)
    industry: Optional[Literal["Tech", "Finance", "Healthcare", "Consulting", "Manufacturing", "Other"]] = Field( description="Ngành nghề", default=None)
    internship_quality_score: Optional[float] = Field(ge=1, le=10, description="Điểm đánh giá chất lượng thực tập từ 1 đến 10", default=None)
    
    next_question: Optional[Optional[str]] = Field(description="Câu hỏi tự nhiên để thu thập các thông tin còn thiếu", default="Bạn có thể cho tớ biết thêm thông tin không?")
    is_off_topic: bool = Field(default=False)
    analysis_feedback: str = Field(default="")
    is_complete: bool = Field(description="True nếu đã thu thập đủ 11 trường dữ liệu", default=False)

class CareerInputPredict(BaseModel):
    cgpa: Optional[float] = Field(default=None)
    backlogs: Optional[int] = Field(default=None)
    college_tier: Optional[Literal['Tier 1', 'Tier 2', 'Tier 3']] = Field(default=None)
    country: Optional[Literal['Germany', 'USA', 'UK', 'Canada', 'India']] = Field(default=None)
    university_ranking_band: Optional[Literal['Top 100', '100-300', '300+']] = Field(default=None)
    internship_count: Optional[int] = Field( description="Số lần thực tập (nếu có)", default=None)
    aptitude_score: Optional[float] = Field(ge=30, le=100, description="Điểm đánh giá năng lực định lượng từ 30 đến 100", default=None)
    communication_score: Optional[float] = Field(ge=30, le=100, description="Điểm đánh giá kỹ năng giao tiếp từ 30 đến 100", default=None)
    specialization: Optional[Literal["AI/ML", "Data Science", "Cybersecurity", "Cloud", "Core CS"]] = Field( description="Chuyên ngành", default=None)
    industry: Optional[Literal["Tech", "Finance", "Healthcare", "Consulting", "Manufacturing", "Other"]] = Field( description="Ngành nghề", default=None)
    internship_quality_score: Optional[float] = Field(ge=1, le=10, description="Điểm đánh giá chất lượng thực tập từ 1 đến 10", default=None)
    
   
class ChatInput(BaseModel):
    message: str
    current_data: CareerInputPredict



#Du lie tra ra
class FeatureImpace(BaseModel):
    name: str
    value: float
class Explanation(BaseModel):
    top_strength: Optional[FeatureImpace]
    top_weakness: Optional[FeatureImpace]
    all_impacts: List[FeatureImpace]

class ExplanationResponse(BaseModel):
    placement: Explanation
    salary: Optional[Explanation]

class PredictionResponse(BaseModel):
    status: str
    probability: float
    ai_insights_placement: List[str]
    ai_insights_salary: List[str]
    estimated_salary: float
    explanations: Dict[str, Any] 