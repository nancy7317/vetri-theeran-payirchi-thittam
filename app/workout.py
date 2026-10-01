from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class WorkoutRequest(BaseModel):
    age: int
    weight: float
    goal: str = "weight loss"

@router.post("/generate-workout")
def generate_workout(req: WorkoutRequest):
    try:
        model = genai.GenerativeModel(os.getenv("GEMINI_WORKOUT_MODEL", "gemini-1.5-flash"))
       prompt = f"You are FitBuddy AI. Create a full Monday to Friday workout plan for Age {req.age}, Weight {req.weight}kg, Goal {req.goal}. For each day give Day name, 3 exercises with sets and reps, and 1 diet tip."
        res = model.generate_content(prompt)
        return {"plan": res.text}
    except Exception as e:
        return {"error": str(e)}
