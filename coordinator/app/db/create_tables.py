from app.db.database import engine
from app.db.base import Base

from app.db.models.worker import Worker

Base.metadata.create_all(bind = engine)
print("Tables created successfully")