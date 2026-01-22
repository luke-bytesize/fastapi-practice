from app.post.application.ports.inbound import CreatePostCommand, CreatePostUseCase                                                                        
from app.post.application.ports.outbound import PostRepository                                                                                             
from app.post.domain.model import Post                                                                                                                     
                                                                                                                                                            
                                                                                                                                                            
class CreatePostService(CreatePostUseCase):                                                                                                                
    def __init__(self, post_repo: PostRepository):                                                                                                         
        self.post_repo = post_repo                                                                                                                         
                                                                                                                                                            
    def create_post(self, command: CreatePostCommand) -> int:                                                                                              
        # 1. 도메인 객체 생성                                                                                                                              
        post = Post(                                                                                                                                       
            id=None,                                                                                                                                       
            title=command.title,                                                                                                                           
            content=command.content,                                                                                                                       
            author_id=command.author_id,                                                                                                                   
        )                                                                                                                                                  
                                                                                                                                                            
        # 2. 비즈니스 로직 검증                                                                                                                            
        post.validate()                                                                                                                                    
                                                                                                                                                            
        # 3. 저장 (Output Port 사용)                                                                                                                       
        post_id = self.post_repo.save(post)                                                                                                                
                                                                                                                                                            
        return post_id 