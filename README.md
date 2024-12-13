# 안대훈 2DGP 텀프로젝트
---
# 목차
1. 게임소개
2. 실행흐름도
3. 개발일정
4. 개발결과
---

## 게임소개

> 2D플랫포머슈팅게임 I Wanna be the boshy 스크린샷


![사본 -게임설명](https://github.com/user-attachments/assets/38008a84-ee6e-4102-a4af-6bc2609934f1)

![사본 -게임설명2](https://github.com/user-attachments/assets/fc3d69ae-a7e7-4ce4-b14f-b967ae583bab)



_어려운 난이도로 유명한 I Wanna be 게임 시리즈를 참고하여 2D 플랫포머 슈팅게임을 파이썬 Pico2D모듈을 사용하여 제작한다._

_게임이름은 진짜 개발자가 되기위한 마음으로 I wanna be the developer이며 이번 프로젝트를 통해 개발자로 한걸음 더 가까워 지려한다._

_일반적인 플랫포머 게임은 캐릭터가 일정위치 예시로 화면의 중앙에서 오른쪽으로 이동하면 뒷배경씬이 이동하며 맵이 확대되지만, 이게임의 방식은 포탈방식으로 오른쪽 화면 끝에 다다르면 다음 씬으로 넘어가는 방식을 갖고있다._ 

_맵에는 플레이어를 죽일수있는 장애물, 함정, 세이브블록이 존재하며 게임이 전체적으로 어렵기 때문에 목숨은 무한정으로 주어지지만, 죽으면 세이브를 한 위치나 맵의 첫지점부터 시작한다. 이 게임의 재미포인트는 플레이어를 화나게하는 억지스러운 난이도와 도전정신에 있다._

_이번 프로젝트의 목표는 난이도 신경쓰지않고 플랫폼맵, 함정, 장애물, 세이브블록을 구현하는 것이 목표이다._


---

## 게임 실행흐름도

![게임흐름도](https://github.com/user-attachments/assets/9d275819-3d95-436c-9e6c-8d91e7695fdf)






---

## 개발일정

`1차발표 전까지`
1. 적당한 이미지, 사운드 수집

~~2. 프레임워크, 씬 , 오브젝트 구성~~

~~3. 메인화면과 1스테이지 구현~~

`1차발표 이후부터`
- 1주차일정
  - 메인화면 씬 제작
  - 게임시작 버튼 , 종료버튼
    
11월 4일 완료
![캡처_2024_11_22_03_11_21_932](https://github.com/user-attachments/assets/6798adfa-96b9-4e68-93fc-36649a308dd2)
AI 이미지생성을 이용해 메인게임화면 이미지를 생성


- 2주차일정
  - 게임 씬 제작
  - 캐릭터 이동
  - 플랫폼 배치
 
11월 17일 완료
![캡처_2024_11_22_03_11_51_753](https://github.com/user-attachments/assets/f1d310ae-ad87-4aac-bbf6-3c331098a66d)
Tiled를 통해 맵을 제작 및 배치. 플랫폼처리, 충돌처리는 아직 완성못한단계.


- 3주차일정
  - AI 몬스터 배치
  - behavior tree
 
11월 21일 완료
![캡처_2024_11_22_03_11_42_966](https://github.com/user-attachments/assets/37678948-5bd4-4fb7-b27c-fc0840d36744)
enemy , behavior tree 를 생성하여 간단한 몬스터배치
![캡처_2024_11_22_03_12_19_439](https://github.com/user-attachments/assets/efeec542-7caf-41c9-bf7c-726def10f253)
플레이어와 몬스터의 충돌시 플레이어 게임오버. 게임오버씬 구현


- 4주차일정
  - 총알발사 + 충돌처리
  - 장애물 배치

11월 22일 부분완료
![캡처_2024_11_22_03_12_00_90](https://github.com/user-attachments/assets/0f78887d-fa14-4fa2-b5b5-8113895a0621)
플레이어의 총알이 적에게 닿으면 적과 총알을 동시에 제거
장애물(가시) 미구현


- 5주차일정
  - 중간점검 및 수정
  - (추가)4주차의 장애물 배치 + 세이브기능

- 6주차일정
   - 맵 확장

  ------------- 여기까지 부분완료

- 7주차일정
   - 보스 + 보스공격패턴 제작
 
  


---

## 11월 22일기준 진행사항 (2차발표 추가자료)
-> 3차발표 추가
### 커밋

![캡처_2024_11_22_05_43_13_428](https://github.com/user-attachments/assets/1157014a-4e15-455b-afa0-8508cd45512b)

## 3차발표커밋횟수
| 주차    |  기간                   |커밋횟수|

| 9월 2주 |	2024-09-08 ~ 2024-09-14|	1회	 |

| 10월 1주|	2024-10-06 ~ 2024-10-12|	2회	 |

| 10월 5주|	2024-10-27 ~ 2024-11-02|  2회	 |

| 11월 2주|	2024-11-03 ~ 2024-11-09|	1회	 |

| 11월 4주|	2024-11-17 ~ 2024-11-23|	15회 |

| 12월 1주|	2024-12-01 ~ 2024-12-07|	2회	 |

| 12월 2주|	2024-12-08 ~ 2024-12-14|	9회  |

- 프레임워크 95%
- 오브젝트 100% 
- 스테이지 80% (레벨디자인 필요)
- 게임로직 90% 
- 적캐릭터 70% (단순한AI, 부족한캐릭터)

### 클래스구성

1. scene/
 부모씬으로 다른씬들은 이클래스를 상속받음

2. scene_manager/
 씬들간의 전환을 담당

3. game_scene/
 게임의 핵심적인 로직을 전부관리
 Player, Enemy, Trap, Save와 load 를 이곳에서 처리함

4. player/
 플레이어 캐릭터를 나타내며, 움직임, 충돌 감지 및 기타 게임 내 상호작용을 처리
-상호작용:
Game_Scene: 게임 씬으로부터 업데이트를 받고, 플레이어의 행동에 따른 이벤트를 전달
Enemies & Traps: 적 및 트랩과의 충돌을 감지하고 처리
Save & Load: Save 및 Load 클래스와 연동하여 플레이어 상태를 저장하고 불러옵니다.

5. enemy/
   게임 내 적 엔티티를 나타내며, 행동 트리를 통해 행동을 결정합니다.
-상호작용:
Game_Scene: 게임 씬에 의해 업데이트되고 렌더링됩니다.
Player: 플레이어와의 충돌을 감지하여 게임 오버시킴
BehaviorTree: 행동 트리를 통해 적의 움직임과 행동을 제어

6. behaviortree/
   적의 AI 행동을 구현하며, 복잡하고 동적인 행동을 가능하게 합니다.
-상호작용:
Enemy:적 인스턴스의 행동을 제어하여 움직임과 행동을 결정합니다.

7. Trap & MovingTrap/
   게임 환경 내 정적 및 동적 트랩을 나타냅니다.
-상호작용:
Game_Scene: 게임 씬에 의해 관리되고 업데이트되며, 플레이어와의 충돌을 감지합니다.
Player: 플레이어와의 충돌을 감지하여 게임 오버 조건을 트리거합니다.
Triggers: 트리거를 통해 트랩의 활성화 및 비활성화를 제어합니다.


8. bullet/
  플레이어가 발사하는 총알 오브젝트
-상호작용:
Player: 플레이어가 총알을 직접발사
Enemy: 총알에맞는적 사살

9. Save Load
  게임상태의 저장과 불러오기
-상호작용:
Game_Scene & Player: 게임 씬과 플레이어 상태를 저장하고 불러오는 역할을 합니다.
Load: 저장된 게임 상태를 불러와 복원합니다.

10. TiledMap
   게임 맵을 관리하며, 타일 데이터를 로드하고 맵 레이아웃에 따른 충돌을 처리합니다.
-상호작용:
 Game_Scene: 맵을 로드하고 렌더링하며, 플레이어와 적의 충돌 데이터를 제공합니다.


---

## 핵심 메카닉
1. 플레이어 이동 및 컨트롤
플레이어는 좌우 이동, 점프, 게임 내 오브젝트와의 상호작용이 가능합니다.

2. 트랩
정적 트랩: 고정된 위치에 있으며, 플레이어와 충돌 시 게임 오버를 유발합니다.
동적 트랩: 사전 정의된 패턴(예: 상, 하, 좌, 우)으로 움직이며, 게임에 동적인 난이도를 추가합니다.
활성화: 트리거를 통해 트랩을 활성화하거나 비활성화할 수 있습니다.

3. 세이브 & 로드 시스템
저장: 플레이어의 위치, 현재 스테이지 등 게임 상태를 저장합니다.
불러오기: 저장된 게임 상태를 불러와 이전 진행 상황을 복원합니다.


---

## 아쉬웠던점
1. 구현하고싶었으나 못한것들
- 보스 (우선순위가 뒤로밀리다보니 나중으로 미루다 결국 구현x)
- 더많은스테이지 (생각보다 맵 레벨디자인이 어려워서 수정이 많이 필요해짐)

2. 팔기위해 보충할것들
   - 앞의 1번에서 말해왔던것들을 구현해야함

3. 구현에 어려웠던점
   - 캐릭터와 맵간의 충돌처리 구현을 원하는대로 구현하기위해 여러번 로직을 바꾸면서 시간이 너무 오래 소요되었다.
   - 구현을 끝냈다 싶은것도 추가적으로 개발하다보니 수정할점이 너무나 많이생겨서 시간배분에 어려움이 있었다.
   - 패키징을 아직도 해결못했다.
   

## 준비사항

### Python Pico2d 모듈
### i wanna be the guy 소스







