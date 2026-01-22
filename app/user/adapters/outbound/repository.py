from sqlalchemy.orm import Session

from app.user.adapters.outbound.orm_model import UserEntity
from app.user.application.ports.outbound import UserRepository
from app.user.domain.model import User


class UserPersistenceAdapter(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_email(self, email: str) -> User | None:
        entity = self.session.query(UserEntity).filter_by(email=email).first()
        if not entity:
            return None
        return User(
            id=entity.id, email=entity.email, password=entity.password, name=entity.name
        )

    def save(self, user: User) -> None:
        entity = UserEntity(email=user.email, password=user.password, name=user.name)
        self.session.add(entity)
        self.session.commit()
