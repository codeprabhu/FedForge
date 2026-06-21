"""
Transaction owner for HTTP requests.

Provides request-scoped sessions.

Do not create UnitOfWork inside request handlers.
"""

from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise
    
    finally:
        db.close()