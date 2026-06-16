"""
Transaction owner for non-HTTP operations.

Use FastAPI's get_db() inside request handlers.

Use UnitOfWork for:
- background jobs
- schedulers
- training rounds
- batch processing
- scripts

Never create UnitOfWork inside a FastAPI request.
"""

from app.db.database import SessionLocal
class UnitOfWork:

    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db
    
    def __exit__(self, exc_type, exc_value, traceback):
        if(exc_type is None):
            self.db.commit()
        else:
            self.db.rollback()
        
        self.db.close()