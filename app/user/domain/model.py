from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    email: str
    password: str  # 해싱된 비밀번호
    name: str

    def validate_registration(self):
        if "@" not in self.email:
            raise ValueError("유효하지 않은 이메일 형식입니다.")