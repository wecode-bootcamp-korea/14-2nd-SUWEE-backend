from django.db.models   import (
        Sum,
        Avg,
        Q,
        F,
)

from user.models import UserBook


def get_reading_numeric(book_id):
    user_books = UserBook.objects.select_related('book').filter(book_id=book_id)
    if not user_books.exists():
        return {    
            'avg_finish'                        : 0.0,
            'expected_reading_minutes'          : 0,
            'category_avg_finish'               : 0.0,
            'category_expected_reading_minutes' : 0,
            } 

    # 완독할 확률   = 책 완독한 독자/책 전체 독자 * 100 (완독여부는 읽은 page/책 총 page)
    # 완독 예상시간 = 책 완독자 총 reading time / 책 완독자 수 
    total_users         = user_books.count()
    finished_users      = user_books.filter(page__gte=F('book__page'))
    
    avg_finish          = 0.0
    avg_reading_minutes = 0.0
    
    if finished_users.exists():
        avg_finish          = finished_users.count() / total_users * 100
        avg_reading_minutes = finished_users.aggregate(read_time=Avg('time'))['read_time']

    
    # [카테고리] 분야 평균 확률          = [카테고리] 책들 완독자 수 / [카테고리] 책들 총 구독자
    # [카테고리] 분야 평균 완독 예상시간 = [카테고리] 책 완독자 총 reading time / [카테고리] 책들 총 완독자 수
    category_id                       = user_books.first().book.category_id
    total_users                       = UserBook.objects.select_related('book').filter(book__category_id=category_id)
    
    finished_users                    = total_users.filter(page__gte=F('book__page'))
    
    category_avg_finish               = 0.0
    category_expected_reading_minutes = 0.0
    
    if finished_users.exists():
        category_avg_finish               = finished_users.count() / total_users.count() * 100
        category_expected_reading_minutes = finished_users.aggregate(read_time=Avg('time'))['read_time']

    return {    
            'avg_finish'                        : avg_finish,
            'expected_reading_minutes'          : int(avg_reading_minutes),
            'category_avg_finish'               : category_avg_finish,
            'category_expected_reading_minutes' : int(category_expected_reading_minutes),
            }
