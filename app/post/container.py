from dependency_injector import containers, providers                                                                                                      
from sqlalchemy.orm import Session                                                                                                                         
                                                                                                                                                            
from app.post.adapters.outbound.repository import PostPersistenceAdapter                                                                                   
from app.post.application.services import CreatePostService                                                                                                
                                                                                                                                                            
# Container를 @Configuration 클래스라고 생각하면 된다.
# providers.Dependency 는 외부에서 주입받을 의존성이다. (DB 세션)


# 의존성 그래프
#   db_session (외부에서 주입)                                                                                                                                 
#       ↓                                                                                                                                                      
#   post_repository (PostPersistenceAdapter)                                                                                                                   
#       ↓                                                                                                                                                      
#   create_post_use_case (CreatePostService)                                                                                                                   
#       ↓                                                                                                                                                      
#   router.py에서 사용


# 전체 흐름
#   1. engine (커넥션 풀) - 앱 시작 시 1번 생성                                                                                                                
#          ↓                                                                                                                                                   
#   2. SessionLocal (세션 팩토리) - 앱 시작 시 1번 생성                                                                                                        
#          ↓                                                                                                                                                   
#   3. get_db() - 요청마다 세션 1개 생성                                                                                                                       
#          ↓                                                                                                                                                   
#   4. providers.Factory - 요청마다 Repository 객체 생성 (세션 주입) 


# ===========================================================================================                                                                                                                           
#   핵심: Session이 요청마다 다름                                                                                                                              
                                                                                                                                                             
  # 요청 1: Session A 생성                                                                                                                                   
  # 요청 2: Session B 생성                                                                                                                                   
  # 요청 3: Session C 생성                                                                                                                                   
                                                                                                                                                             
#   싱글톤으로 만들면 생기는 문제                                                                                                                              
                                                                                                                                                             
#   # ❌ 싱글톤이라면                                                                                                                                          
#   post_repository = providers.Singleton(PostPersistenceAdapter, session=db_session)                                                                          
#   ┌───────────┬────────────────────────────────────────────────────┐                                                                                         
#   │   시점    │                        상황                        │                                                                                         
#   ├───────────┼────────────────────────────────────────────────────┤                                                                                         
#   │ 요청 1    │ Session A로 Repository 생성 (싱글톤 고정)          │                                                                                         
#   ├───────────┼────────────────────────────────────────────────────┤                                                                                         
#   │ 요청 1 끝 │ Session A 닫힘 (db.close())                        │                                                                                         
#   ├───────────┼────────────────────────────────────────────────────┤                                                                                         
#   │ 요청 2    │ 같은 Repository 사용 → 닫힌 Session A 참조 → 에러! │                                                                                         
#   └───────────┴────────────────────────────────────────────────────┘                                                                                         
#   Factory면 괜찮은 이유                                                                                                                                      
                                                                                                                                                             
#   # ✅ Factory                                                                                                                                               
#   post_repository = providers.Factory(PostPersistenceAdapter, session=db_session)                                                                            
#   ┌────────┬───────────────────────────────────────────────────┐                                                                                             
#   │  시점  │                       상황                        │                                                                                             
#   ├────────┼───────────────────────────────────────────────────┤                                                                                             
#   │ 요청 1 │ Session A → Repository A 생성 → 사용 → 둘 다 버림 │                                                                                             
#   ├────────┼───────────────────────────────────────────────────┤                                                                                             
#   │ 요청 2 │ Session B → Repository B 생성 → 사용 → 둘 다 버림 │                                                                                             
#   └────────┴───────────────────────────────────────────────────┘                                                                                             
#   성능 걱정?                                                                                                                                                 
                                                                                                                                                             
#   Repository 객체 생성: ~0.001ms  ← 무시할 수준                                                                                                              
#   DB 쿼리:            ~5-50ms    ← 99% 차지                                                                                                                  
                                                                                                                                                             
#   Python 객체 생성은 매우 가벼워요.                                                                                                                          
                                                                                                                                                             
#   Spring은 어떻게 싱글톤으로 하나?                                                                                                                           
                                                                                                                                                             
#   프록시 마법!                                                                                                                                               
                                                                                                                                                             
#   @Repository  // 싱글톤                                                                                                                                     
#   public class PostPersistenceAdapter {                                                                                                                      
                                                                                                                                                             
#       @PersistenceContext  // ← 진짜 EntityManager가 아님!                                                                                                   
#       private EntityManager em;  // ← 프록시 객체                                                                                                            
#   }                                                                                                                                                          
                                                                                                                                                             
#   Spring 내부:                                                                                                                                               
#   Repository (싱글톤)                                                                                                                                        
#       → EntityManager 프록시 (싱글톤)                                                                                                                        
#           → 실제 Session (요청마다 다름) ← 프록시가 알아서 연결                                                                                              
                                                                                                                                                             
#   Python에서 같은 패턴 쓰려면 복잡한 프록시 구현이 필요해서, 그냥 Factory로 간단하게 처리하는 거예요.

class PostContainer(containers.DeclarativeContainer):                                                                                                      
    """Post 모듈의 DI 컨테이너"""                                                                                                                          

    # ComponentScan이라 생각하면 된다. 어디에 주입할 지 결정.                                                                                                                    
    wiring_config = containers.WiringConfiguration(                                                                                                        
        modules=["app.post.adapters.inbound.router"]                                                                                                       
    )                                                                                                                                                      
                                                                                                                                                            
    # 외부에서 주입받는 DB 세션                                                                                                                            
    db_session = providers.Dependency(instance_of=Session)                                                                                                 
                                                                                                                                                            
    # Repository (Output Port 구현체)
    # @Bean + prototype scope로 매번 새 인스턴스를 생성한다. (커넥션 풀을 새로 만든다는 의미로 생각하면 될 것 같다.)                                                                                                              
    post_repository = providers.Factory(                                                                                                                   
        PostPersistenceAdapter,                                                                                                                            
        session=db_session,                                                                                                                                
    )                                                                                                                                                      
                                                                                                                                                            
    # UseCase (Application Service)                                                                                                                        
    create_post_use_case = providers.Factory(                                                                                                              
        CreatePostService,                                                                                                                                 
        post_repo=post_repository,                                                                                                                         
    )