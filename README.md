# 마싯다
배민, 요기요, 쿠팡잇츠 같은 배달 서비스

## 사용 기술 및 환경
- python (3.9)
- Django (4.1.2)
- PostgreSQL (14.5)
- poetry (1.2.2)
- Github Actions
- Docker

## 구현 기능
### 로그인 & 회원가입
- DRF의 authToken을 사용해서 로그인시 토큰을 생성.
- 이메일, 닉네임 validation 설정
- 패스워드는 장고 기본 인증을 따라 DB에 저장될 때 암호화
