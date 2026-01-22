from dataclasses import dataclass # dataclass는 무슨 역할이고, 왜 필요해?
from typing import Optional
from datetime import datetime

# 작업 흐름
# 폴더 구조를 만든다. (__init__.py 도 포함)
'''
  ┌──────┬─────────────┬────────────────────────┬───────────────────────┐                                                                                    
  │ 순서  │   레이어      │          파일           │         설명           │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 1    │ 폴더 구조     │ -                      │ ← 지금 여기           │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 2    │ Domain      │ model.py               │ Post 엔티티           │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 3    │ Domain      │ exceptions.py          │ 도메인 예외           │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 4    │ Application │ ports/inbound.py       │ UseCase 인터페이스    │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 5    │ Application │ ports/outbound.py      │ Repository 인터페이스 │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 6    │ Application │ services.py            │ UseCase 구현체        │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 7    │ Adapter     │ outbound/orm_model.py  │ DB 테이블 매핑        │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 8    │ Adapter     │ outbound/repository.py │ Repository 구현체     │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 9    │ Adapter     │ inbound/router.py      │ API 엔드포인트        │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 10   │ DI          │ container.py           │ 의존성 주입 설정      │                                                                                    
  ├──────┼─────────────┼────────────────────────┼───────────────────────┤                                                                                    
  │ 11   │ Main        │ main.py                │ 라우터 연결           │                                                                                    
  └──────┴─────────────┴────────────────────────┴───────────────────────┘ 
'''

# 도메인 모델은 외부에 의존하는 것이 없다.
# @dataclass는 getter와 setter를 자동으로 생성해준다.
# Optional[int] 는 id가 none이 될 수 있다는 것을 의미한다. 새 게시글은 id가 없기 때문이다.
@dataclass
class Post:
    id: Optional[int] # Optional은 뭐야? 그리고 id는 필수적인거 아니야? 
    title: str
    content: str
    author_id: int
    create_at: Optional[datetime] = None
    
    def validate(self):
        if len(self.title) < 2:
            raise ValueError("제목은 2자 이상이어야 합니다.") # raise는 뭐야?
        if len(self.content) < 10:
            raise ValueError("내용은 10자 이상이어야 합니다.")
        
