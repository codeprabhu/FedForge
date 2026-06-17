from coordinator.app.db.database import engine
from coordinator.app.db.base import Base

from coordinator.app.db.models.worker import Worker

print(list(Worker.__table__.columns.keys()))
Base.metadata.create_all(bind = engine)
print("Tables created successfully")