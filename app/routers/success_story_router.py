from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.success_story_model import SuccessStory
from app.schemas.success_story_schema import SuccessStoryCreate, SuccessStoryResponse

router = APIRouter(
    prefix="/success-stories",
    tags=["Success Stories"]
)

@router.get("/", response_model=List[SuccessStoryResponse])
def get_stories(db: Session = Depends(get_db)):
    return db.query(SuccessStory).all()

@router.post("/", response_model=SuccessStoryResponse)
def create_story(story: SuccessStoryCreate, db: Session = Depends(get_db)):
    db_story = SuccessStory(title=story.title, content=story.content)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(SuccessStory).filter(SuccessStory.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    db.delete(story)
    db.commit()
    return {"message": "Story deleted successfully"}
