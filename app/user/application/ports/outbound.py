from abc import ABC, abstractmethod
from typing import Optional

from app.user.domain.model import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
