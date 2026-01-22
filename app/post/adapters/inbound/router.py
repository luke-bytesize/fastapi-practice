from dependency_injector.wiring import Provide, inject                                                                                                     
from fastapi import APIRouter, Depends, HTTPException                                                                                                      
                                                                                                                                                            
from app.post.application.ports.inbound import CreatePostCommand, CreatePostUseCase                                                                        
from app.post.container import PostContainer                                                                                                               
from app.post.domain.exceptions import PostNotFoundError
                                                                                                                                             
#  - Router는 Input Adapter (외부 요청 → Application으로 전달)                                                                                                
#  - 비즈니스 로직 없이 요청 전달 + 응답 변환만 담당                                                                                                          
#  - 예외를 HTTP 응답으로 변환


# URL 접두사 @RequestMapping("/posts") 같은 느낌
# tags=["posts"] 는 Swagger 를 위한 API 문서 분류용이다.
router = APIRouter(prefix="/posts", tags=["posts"])                                                                                                        
                                                                                                                                                            
# POST 요청 처리 @PostMapping 개념                                                                                                                                             
@router.post("")                                                                                                                                           
@inject # Autowired 느낌. 의존성 주입 자동으로 해줌.    
# Depends(Provide[...]) 생성자 주입. PostContainer에서 등록된 create_post_use_case 가져와서 주입.
# Depends는 FastAPI의 함수로, 이 안에 들어간 파라미터를 주입받을 거라는 것을 의미한다.
# Provide[]는 dependency-injector의 함수로 컨테이너에서 ~을 가져오라는 것을 의미한다.                                                                                    
def create_post(                                                                                                                                           
    command: CreatePostCommand,                                                                                                                            
    use_case: CreatePostUseCase = Depends(Provide[PostContainer.create_post_use_case]),                                                                    
):                                                                                                                                                         
    try:                                                                                                                                                   
        post_id = use_case.create_post(command)                                                                                                            
        return {"post_id": post_id, "message": "게시글이 생성되었습니다."}                                                                                 
    except ValueError as e:                                                                                                                                
        raise HTTPException(status_code=400, detail=str(e)) # ResponseStatusException. 에러 응답.