from typing import Optional                                                                                                                                
                                                                                                                                                             
from sqlalchemy.orm import Session                                                                                                                         
                                                                                                                                                            
from app.post.adapters.outbound.orm_model import PostEntity                                                                                                
from app.post.application.ports.outbound import PostRepository                                                                                             
from app.post.domain.model import Post                                                                                                                     
                                                                                                                                                            
                                                                                                                                                            
class PostPersistenceAdapter(PostRepository):                                                                                                              
    def __init__(self, session: Session):                                                                                                                  
        self.session = session                                                                                                                             
                                                                                                                                                            
    def save(self, post: Post) -> int:                                                                                                                     
        entity = PostEntity(                                                                                                                               
            title=post.title,                                                                                                                              
            content=post.content,                                                                                                                          
            author_id=post.author_id,                                                                                                                      
        )                                                                                                                                                  
        self.session.add(entity)        # Insert 준비.                                                                                                                     
        self.session.commit()           # DB에 반영                                                                                                            
        self.session.refresh(entity)    # 생성된 id 가져오기.                                                                                                                
        return entity.id                                                                                                                                   
                                                                                                                                                            
    def find_by_id(self, post_id: int) -> Optional[Post]:                                                                                                  
        entity = self.session.query(PostEntity).filter_by(id=post_id).first()                                                                              
        if not entity:                                                                                                                                     
            return None

        # Entity -> Domain으로 변환.
        # Service는 Domain 객체만 다루고, DB 기술 (SQLAlchemy)는 모름.                                                                                                                         
        return Post(                                                                                                                                       
            id=entity.id,                                                                                                                                  
            title=entity.title,                                                                                                                            
            content=entity.content,                                                                                                                        
            author_id=entity.author_id,                                                                                                                    
            created_at=entity.created_at,                                                                                                                  
        ) 