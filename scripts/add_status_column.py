"""
Add status column to fundraiser_master table

Run this script to add the status column to your existing database
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# Get database URL from .env
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def add_status_column():
    with engine.connect() as connection:
        try:
            # Check if status column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'fundraiser_master' 
                AND column_name = 'status'
            """)
            result = connection.execute(check_query)
            
            if result.fetchone():
                print("[OK] Status column already exists!")
                return
            
            # Add status column with default value 'pending'
            alter_query = text("""
                ALTER TABLE fundraiser_master 
                ADD COLUMN status VARCHAR DEFAULT 'pending'
            """)
            connection.execute(alter_query)
            connection.commit()
            
            print("[SUCCESS] Added 'status' column to fundraiser_master table!")
            print("          Default value: 'pending'")
            
            # Update existing rows to have 'pending' status
            update_query = text("""
                UPDATE fundraiser_master 
                SET status = 'pending' 
                WHERE status IS NULL
            """)
            connection.execute(update_query)
            connection.commit()
            
            print("[SUCCESS] Updated all existing fundraisers to 'pending' status")
            
        except Exception as e:
            print(f"[ERROR] {e}")
            connection.rollback()

if __name__ == "__main__":
    print("Adding status column to fundraiser_master table...")
    add_status_column()
    print("\n[DONE] Database migration complete!")
