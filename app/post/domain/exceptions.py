class PostNotFoundError(Exception):
    def __init__(self, post_id: int):
        self.message = f"게시글을 찾을 수 없습니다: {post_id}" 
        super().__init__(self.message)   