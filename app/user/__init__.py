from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.user.adapters.inbound.router import router
from app.user.container import UserContainer

container = UserContainer()
container.wire(modules=["app.user.adapters.inbound.router"])


def get_container(db: Session = Depends(get_db)):
    container.db_session.override(db)
    return container


def setup(app: FastAPI):
    app.include_router(router, dependencies=[Depends(get_container)])
