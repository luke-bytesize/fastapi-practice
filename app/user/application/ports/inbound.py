from abc import ABC, abstractmethod
from pydantic import BaseModel

class RegisterUserCommand(BaseModel):
    email: str
    password: str
    name: str

class RegisterUserUseCase(ABC):
    @abstractmethod
    def register_user(self, command: RegisterUserCommand) -> None:
        pass