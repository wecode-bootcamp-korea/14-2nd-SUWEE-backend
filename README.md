# SUWEE's Library Clone Project

<img src="https://trello-attachments.s3.amazonaws.com/5fc465951dfcce1dc3a95814/5fc48e535151e366256bb3ef/14fd0811cb2d556ca69cc0bc8aafded7/logo_black.png" height="100"/>

## 개요

#### 목적
[밀리의서재](https://www.millie.co.kr//) 서비스 클론
> 밀리의 서재는 개인화 기반 독서 추천 서비스로 정기 구독형 서비스이다.

#### 일정
2020년 11월 30일 (월) ~ 12월 11일 (금), 11일간 진행

#### 팀원

- Frontend : 신세원, 류지혜, 공주민
- Backend : 고수희(PM), 정현석, 백승진

## 구현 기능

- 메인페이지 조회
- 회원가입/  로그인 
- 도서 상세페이지
- 내 서재 페이
- 검색 결과 페이지

## 멤버별 기능 구현 사항

- 전체
    - 데이터 모델링

- 고수희(PM)
    - 메인 페이지
    - 내 서재 페이지
    - 유닛 테스트
    
- 정현석
    - 데이터 수집 및 db_uploader, db_truncate 작성
    - BookDetailView: 도서 상세페이지 조회 기능
    - ReviewView : 도서 리뷰 조회, 생성, 삭제 기능
    - ReviewLikeView: 도서 리뷰의 좋아요 생성, 삭제 기능
    - MyLibraryView : 내 서재에 도서 담기 기능 
    - 모든 View UnitTest : UinTest
    
- 백승진
    - 데이터 수집
    - SearchBookView : 책 검색 기능
    - SignUpView : 회원가입 기능
    - SignInView : 로그인 기능
    - SignInWithKakaoView : 카카오 소셜 로그인 기능
    - SMSCheckView : 문자 인증 기능
    - check_auth_decorator : 로그인 데코레이터 기능
    - 모든 View UnitTest : UinTest

## Links

- 프로젝트 후기
  - [고수희]
  - [정현석](https://velog.io/@cs982607/2%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9B%84%EA%B8%B0)
  - [백승진]

- Repository
  - [프론트엔드](https://github.com/wecode-bootcamp-korea/14-2nd-SUWEE-frontend)
  - [백엔드](https://github.com/wecode-bootcamp-korea/14-2nd-SUWEE-backend)
  
- API Documentation
  - https://documenter.getpostman.com/view/13391325/TVmMhdrD
 
## Contributing

- Thanks to [Wecode](https://wecode.co.kr/)

## Reference

이 프로젝트는 밀리의 서재 사이트를 참조하여 학습목적으로 만들었습니다.
실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

- [밀리의서재](https://www.millie.co.kr/)
- [unsplash.com](https://unsplash.com/)
- [Google Books APIs](https://developers.google.com/books)

## License

**도서 정보는 Google Books APIs를 사용했습니다.**

