import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suwee.settings")

django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('set foreign_key_checks=0')
    cursor.execute('truncate books')
    cursor.execute('truncate categories')
    cursor.execute('truncate libraries')
    cursor.execute('truncate library_books')
    cursor.execute('truncate likes')
    cursor.execute('truncate reviews')
    cursor.execute('truncate users')
    cursor.execute('truncate user_books')
    cursor.execute('truncate keywords')
    cursor.execute('set foreign_key_checks=1')

print ('데이터 베이스 초기화')


