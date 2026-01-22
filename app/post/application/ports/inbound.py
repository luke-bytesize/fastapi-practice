from abc import ABC, abstractmethod
from pydantic import BaseModel


# BaseModel은 @RequestBody라고 생각하면 된다. 요청을 데이터 담는 객체이다.
# dto를 command라고 하는 이유: 이거 나중에 Req라고 하는게 낫겠다.
class CreatePostCommand(BaseModel):                                                                                                                        
    title: str                                                                                                                                             
    content: str                                                                                                                                           
    author_id: int 

class CreatePostUseCase(ABC):                                                                                                                              
    @abstractmethod                                                                                                                                        
    def create_post(self, command: CreatePostCommand) -> int:     # 나중에 여기 int를 Response로 변경하면 됨.                                                                                         
        pass