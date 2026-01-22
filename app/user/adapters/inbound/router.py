from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.user.application.ports.inbound import RegisterUserCommand, RegisterUserUseCase
from app.user.container import UserContainer
from app.user.domain.exceptions import UserAlreadyExistsError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
@inject
def register(
    command: RegisterUserCommand,
    use_case: RegisterUserUseCase = Depends(Provide[UserContainer.register_user_use_case]),
):
    try:
        use_case.register_user(command)
        return {"message": "Success"}
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
