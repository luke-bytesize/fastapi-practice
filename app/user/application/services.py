from app.user.application.ports.inbound import RegisterUserCommand, RegisterUserUseCase
from app.user.application.ports.outbound import UserRepository
from app.user.domain.exceptions import UserAlreadyExistsError
from app.user.domain.model import User


class RegisterUserService(RegisterUserUseCase):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, command: RegisterUserCommand) -> None:
        # 1. 중복 체크 (Output Port 사용)
        if self.user_repo.find_by_email(command.email):
            raise UserAlreadyExistsError(command.email)

        # 2. 도메인 객체 생성
        user = User(
            id=None,
            email=command.email,
            password=command.password,  # 실무에선 여기서 해싱 로직 포함
            name=command.name,
        )

        # 3. 비즈니스 로직 검증
        user.validate_registration()

        # 4. 저장 (Output Port 사용)
        self.user_repo.save(user)
