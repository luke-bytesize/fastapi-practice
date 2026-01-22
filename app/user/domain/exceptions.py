class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.message = f"이미 존재하는 이메일입니다: {email}"
        super().__init__(self.message)