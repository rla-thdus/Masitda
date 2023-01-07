# MaSitDa
배민, 요기요, 쿠팡잇츠 같은 배달 서비스

## 사용 기술 및 환경
- python (3.9)
- Django (4.1.2)
- PostgreSQL (14.5)
- poetry (1.2.2)
- Github Actions
- Docker

## 구현 기능
### User
- [POST] `/users`
  - 회원가입하는 api입니다.
  - 이메일, 닉네임 validation 설정
  - 패스워드는 장고 기본 인증을 따라 DB에 저장될 때 암호화 합니다.
  - 다음과 같은 내용은 Request Body에 반드시 필요합니다.
    - `nickname`
    - `email`
    - `address`
    - `password`
    - `phone`
    - `role`
- [POST] `/login`
  - 로그인하는 api입니다.
  - DRF의 authToken을 사용해서 토큰을 생성하고 반환 합니다.
  - 다음과 같은 내용은 Request Body에 반드시 필요합니다.
    - `email`
    - `password`
- [POST] `/logout`
  - 로그아웃하는 api입니다.
  - 인증된 유저만 요청할 수 있고, 해당 계정의 토큰을 삭제합니다.
  - 다음과 같은 내용은 Header에 반드시 필요합니다.
    - `Authorization: token {token 값}`

### Restaurant & Menu
- `/restaurants/`
  - get
    - 음식점 목록을 요청하는 api, 누구나 접근 가능
    - 리스트 형식으로 반환
  - post
    - 음식점을 생성하는 api, 사장 권한을 가지고 있는 사용자만 사용 가능
    - 음식점이 성공적으로 생성되면 201 반환, 실패하면 400 반환
- `/restaurants/<int: restaurant_pk>`
  - get
    - 해당 음식점의 자세한 정보를 요청하는 api, 누구나 접근 가능
    - 해당 음식점이 존재하지 않으면 404 반환, 있으면 200과 함께 데이터 반환
  - patch
    - 해당 음식점의 정보를 수정하는  api, 해당 음식점의 사장님만 가능
    - 권한이 없다면 403 반환, 해당 음식점이 없으면 404 반환, 업데이트 성공하면 200 반환, 실패하면 400 반환
    - 부분적으로 수정할 부분만 요청 가능
- `/restaurants/<int: restaurant_pk>/menus`
  - post
    - 음식점에 메뉴를 생성하는 api, 해당 음식점의 사장님만 가능
    - 권한이 없다면 403 반환, 해당 음식점이 없으면 404 반환, 메뉴 생성이 되면 201 반환, 실패하면 400 반환
- `/restaurants/<int: restaurant_pk>/menus/<int: menu_pk>`
  - patch
    - 해당 음식점의 메뉴를 수정하는 api, 해당 음식점의 사장님만 가능
    - 권한이 없으면 403 반환, 해당 음식점이나 메뉴가 없다면 404 반환, 수정이 되면 200 반환, 실패하면 400 반환
    - 부분적으로 수정할 부분만  요청 가능
  - delete
    - 해당 음식점의 메뉴를 삭제하는 api, 해당 음식점의 사장님만 가능
    - 권한이 없으면 403 반환, 해당 음식점이나 메뉴가 없다면 404 반환, 삭제되면 204 반환
