from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Dict
from system_prompt import system_prompt

app = FastAPI()
OPENAI_API_KEY = "Api key of openai"
client = OpenAI(api_key=OPENAI_API_KEY)

class HoroscopeOutput(BaseModel):
    energy_of_the_day: str
    personal_and_mental_space: str
    work_and_career: str
    money: str
    relationship: str
    health: str
    lucky_tips: str
    summary: str
    energy_of_the_day_hindi: str
    personal_and_mental_space_hindi: str
    work_and_career_hindi: str
    money_hindi: str
    relationship_hindi: str
    health_hindi: str
    lucky_tips_hindi: str
    summary_hindi: str
    overall_score: int
    work_score: int
    money_score: int
    love_score: int
    health_score: int
    affirmations: List[str]
    affirmations_hindi: List[str]

class HoroscopeResponse(BaseModel):
    horoscopes: List[HoroscopeOutput]

class Planet(BaseModel):
    name: str
    degree: float = Field(..., ge=0, le=30)

class PlanetData(BaseModel):
    planets: Dict[int, List[Planet]]

class HoroscopeData(BaseModel):
    date: str
    vara: str
    tithi: str
    rashi: str
    nakshatra: str
    planets: Dict[str, List[Planet]]


@app.post("/")
def get_horoscope(input: List[HoroscopeData]):
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate horoscope for: {input}"}
        ],
        response_format=HoroscopeResponse
    )
    print(response)
    return {"Output": response.choices[0].message.parsed}