# 14-2nd-SUWEE-backend
# Suwee Project

<img src="https://trello-attachments.s3.amazonaws.com/5fc465951dfcce1dc3a95814/5fc48e535151e366256bb3ef/14fd0811cb2d556ca69cc0bc8aafded7/logo_black.png" height="100"/>

## 개요

#### 목적 : [밀리의서재](https://www.millie.co.kr//) 클론

#### 일정 : 2020년 11월 30일 (월) ~ 12월 11일 (금), 12일간 진행

#### 참여자 :

- Frontend : 신세원, 류지혜, 공주민
- Backend : 고수희(PM), 정현석, 백승진

> 밀리의서재의 다양한 기능을 구현한다.

## 핵심 기능 Key Feature

### 메인페이지 ( + 기능 )
- 메인화면 (현재 날짜 기준 이전 일자 출간 책 조회, 커밍순 놓치기 아쉬운 책 조회,
					베스트셀러 조회, 오늘의 책 조회, 이번주 취향별 추천책 조회 구현)
- 회원가입 페이지 / 로그인 ( 회원가입 데이터 넣기, 로그인 기능 - 쿠키발급, 문자인증, 
              					카카오 소셜 로그인 구현  )
- 도서 상세페이지 (도서 상세페이지, 함께읽는사람, 리뷰 생성,삭제,조회, 리뷰 좋아요, 완독률 구현)
- 내 서재 페이지(내 서재에 담기, 내 서재조회, 내 서재 책리스트 정렬, 내 서재통계 구현 )
- 검색 결과 페이지 (책 검색 검색시 결과 페이지 구현)



## 백엔드 멤버의 기능 구현

- 전체
    - modeling

- 고수희(PM)
    - TodayBookView : 메인 페이지 오늘의책 조회
    - RecentlyBookView : 
    - CommingSoonBookView : 커밍순 놓치기 아쉬운 책 조회
    - BestSellerBookView : 메인 페이지 베스트 셀러 책 조회
    - RecommendBookView : 
    - 모든 View UnitTest : UinTest 
    
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

## Contributing

- Thanks to [Wecode](https://wecode.co.kr/)

## Reference

- [밀리의서재](https://www.millie.co.kr/)
- [unsplash.com](https://unsplash.com/)
- [Google Books APIs](https://developers.google.com/books)

## Links

- 멤버 후기
  - [고수희]
  - [정현석](https://velog.io/@cs982607/2%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9B%84%EA%B8%B0)
  - [백승진]

- Repository
  - [프론트엔드](https://github.com/wecode-bootcamp-korea/14-2nd-SUWEE-frontend)
  - [백엔드](https://github.com/wecode-bootcamp-korea/14-2nd-SUWEE-backend)
  
- API Documentation
  - https://documenter.getpostman.com/view/13391325/TVmMhdrD
 

## License

**도서 정보는 Google Books APIs를 사용했습니다.**
