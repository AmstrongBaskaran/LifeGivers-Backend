from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.fundraiser_schema import FundraiserCreate
from app.models.fundraiser_model import FundraiserMaster
from app.database import get_db
import cloudinary.uploader

router = APIRouter(
    prefix="/fundraiser",
    tags=["Fundraisers"]
)

import asyncio
import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. CREATE FUNDRAISER (Async + Parallel Uploads)
@router.post("/", status_code=201)
async def create_fundraiser(data: FundraiserCreate, db: Session = Depends(get_db)):
    """
    Creates a new fundraising campaign.
    Uploads all provided images in parallel to Cloudinary.
    """
    try:
        logger.info(f"Received campaign creation request for user {data.user_id}")
        fundraiser_dict = data.model_dump()
        image_fields = ["medical_report_url", "hospital_report_url", "id_proof_url", "campaign_image_url"]
        
        # Parallel upload logic
        upload_tasks = []
        fields_to_upload = []

        for field in image_fields:
            base64_data = fundraiser_dict.get(field)
            if base64_data and base64_data.startswith("data:"):
                logger.info(f"Preparing to upload {field}...")
                fields_to_upload.append(field)
                # Use to_thread to run blocking Cloudinary calls in parallel
                upload_tasks.append(asyncio.to_thread(cloudinary.uploader.upload, base64_data))
            else:
                logger.warning(f"Field {field} is empty or not Base64 data")

        if upload_tasks:
            logger.info(f"Starting parallel upload of {len(upload_tasks)} images...")
            upload_results = await asyncio.gather(*upload_tasks, return_exceptions=True)
            
            for field, result in zip(fields_to_upload, upload_results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to upload {field}: {str(result)}")
                    # Critical: remove the Base64 string so we don't store it in the DB
                    fundraiser_dict[field] = None
                else:
                    logger.info(f"Successfully uploaded {field}")
                    fundraiser_dict[field] = result["secure_url"]

        # Save to database
        new_fundraiser = FundraiserMaster(**fundraiser_dict)
        db.add(new_fundraiser)
        db.commit()
        db.refresh(new_fundraiser)
        
        logger.info(f"Campaign {new_fundraiser.fundraiser_id} created successfully")
        return {
            "fundraiser_id": new_fundraiser.fundraiser_id,
            "status": "success",
            "message": "Campaign created successfully with parallel image uploads"
        }
    except Exception as e:
        logger.error(f"Critical error in create_fundraiser: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database or Server error: {str(e)}")


# 2. GET / SEARCH LOGIC
@router.get("/")
def get_all_fundraisers(db: Session = Depends(get_db)):
    """ Returns every fundraiser in the database """
    return db.query(FundraiserMaster).all()

@router.get("/{fundraiser_id}")
def get_fundraiser_by_id(fundraiser_id: int, db: Session = Depends(get_db)):
    """ Returns a single fundraiser by its ID """
    fundraiser = db.query(FundraiserMaster).filter(FundraiserMaster.fundraiser_id == fundraiser_id).first()
    if not fundraiser:
        raise HTTPException(status_code=404, detail="Fundraiser not found")
    return fundraiser



# 3. STATUS & VERIFICATION LOGIC
@router.get("/status/pending")
def get_pending_fundraisers(db: Session = Depends(get_db)):
    """ Returns campaigns waiting for admin approval """
    return db.query(FundraiserMaster).filter(FundraiserMaster.status == "pending").all()

@router.get("/status/approved")
def get_approved_fundraisers(db: Session = Depends(get_db)):
    """ Returns only campaigns that are approved and live """
    return db.query(FundraiserMaster).filter(FundraiserMaster.status == "approved").all()

@router.patch("/{fundraiser_id}/status")
def update_status(fundraiser_id: int, status: str, story_text: str | None = None, db: Session = Depends(get_db)):
    """
    Admin Action: Approve or Reject a campaign.
    If Approved, the campaign becomes visible on the Home Page.
    Admins can also edit the story text before approving.
    """
    if status not in ["approved", "rejected", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status type")
    
    fundraiser = db.query(FundraiserMaster).filter(FundraiserMaster.fundraiser_id == fundraiser_id).first()
    if not fundraiser:
        raise HTTPException(status_code=404, detail="Fundraiser not found")

    fundraiser.status = status
    if story_text: # Allow admin to clean up the story before it goes live
        fundraiser.story_text = story_text
        
    db.commit()
    return {"message": f"Fundraiser is now {status}"}


# -----------------------------------------------------------------
# 4. DELETE & UPDATE
# -----------------------------------------------------------------
@router.delete("/{fundraiser_id}")
def delete_fundraiser(fundraiser_id: int, db: Session = Depends(get_db)):
    fundraiser = db.query(FundraiserMaster).filter(FundraiserMaster.fundraiser_id == fundraiser_id).first()
    if not fundraiser:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(fundraiser)
    db.commit()
    return {"message": "Success"}
