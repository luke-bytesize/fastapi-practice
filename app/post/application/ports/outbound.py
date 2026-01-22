from abc import ABC, abstractmethod                                                                                                                        
from typing import Optional                                                                                                                                
                                                                                                                                                            
from app.post.domain.model import Post                                                                                                                     
                                                                                                                                                            
                                                                                                                                                            
class PostRepository(ABC):                                                                                                                                 
    @abstractmethod                                                                                                                                        
    def save(self, post: Post) -> int:                                                                                                                     
        pass                                                                                                                                               
                                                                                                                                                            
    @abstractmethod                                                                                                                                        
    def find_by_id(self, post_id: int) -> Optional[Post]:                                                                                                  
        pass