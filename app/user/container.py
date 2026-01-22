from dependency_injector import containers, providers
from sqlalchemy.orm import Session

from app.user.adapters.outbound.repository import UserPersistenceAdapter
from app.user.application.services import RegisterUserService


class UserContainer(containers.DeclarativeContainer):
    """User 모듈의 DI 컨테이너"""

    wiring_config = containers.WiringConfiguration(
        modules=["app.user.adapters.inbound.router"]
    )

    # 외부에서 주입받는 DB 세션
    db_session = providers.Dependency(instance_of=Session)

    # Output Port 구현체 (Secondary Adapter)
    user_repository = providers.Factory(
        UserPersistenceAdapter,
        session=db_session,
    )

    # Use Case 구현체 (Application Service)
    register_user_use_case = providers.Factory(
        RegisterUserService,
        user_repo=user_repository,
    )
