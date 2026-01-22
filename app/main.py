from fastapi import FastAPI
from pydantic import BaseModel
from app import post, user

# 최종 폴더 구조                                                                                                                                             
                                                                                                                                                             
#   app/                                                                                                                                                       
#   ├── main.py                 ← 깔끔! setup() 호출만                                                                                                         
#   ├── infrastructure/                                                                                                                                        
#   │   └── database.py                                                                                                                                        
#   ├── user/                                                                                                                                                  
#   │   ├── __init__.py         ← setup() 정의                                                                                                                 
#   │   ├── container.py                                                                                                                                       
#   │   ├── domain/                                                                                                                                            
#   │   ├── application/                                                                                                                                       
#   │   └── adapters/                                                                                                                                          
#   └── post/                                                                                                                                                  
#       ├── __init__.py         ← setup() 정의                                                                                                                 
#       ├── container.py                                                                                                                                       
#       ├── domain/                                                                                                                                            
#       ├── application/                                                                                                                                       
#       └── adapters/

app = FastAPI()

# 모듈 등록
user.setup(app)
post.setup(app)


class HealthCheck(BaseModel):
    status: str = "ok"


@app.get("/", response_model=HealthCheck)
async def health_check():
    return HealthCheck()
