from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.post.adapters.inbound.router import router
from app.post.container import PostContainer

container = PostContainer()
container.wire(modules=["app.post.adapters.inbound.router"])


def get_container(db: Session = Depends(get_db)):
    container.db_session.override(db)
    return container


def setup(app: FastAPI):
    app.include_router(router, dependencies=[Depends(get_container)])
