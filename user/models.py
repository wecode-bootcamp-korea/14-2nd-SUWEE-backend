import time
import hmac
import base64
import hashlib
import requests
import json
import datetime
from random import randint

from django.db      import models
from django.utils   import timezone

from model_utils.models import TimeStampedModel

import my_settings


class User(models.Model):
    nickname     = models.CharField(max_length=45)
    password     = models.CharField(max_length=200, null=True)
    email        = models.EmailField(max_length=45, null=True)
    image_url    = models.URLField(max_length=200, null=True)
    phone_number = models.CharField(max_length=11, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    kakao_id     = models.CharField(max_length=45, null=True)
    books        = models.ManyToManyField('book.Book', through='UserBook')

    class Meta :
        db_table = 'users'

class UserBook(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    book        = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    page        = models.IntegerField()
    time        = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta :
        db_table = 'user_books'

class SMSAuthRequest(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=50)
    auth_number  = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'sms_auth_requests'

    def save(self, *args, **kwargs):
        self.auth_number = randint(100000, 1000000)
        super().save(*args, **kwargs)
        self.send_sms()

    def send_sms(self):
        url = 'https://sens.apigw.ntruss.com'
        uri = '/sms/v2/services/ncp:sms:kr:261818325710:python/messages'
        api_url = url + uri

        body = {
            "type"        : "SMS",
            "contentType" : "COMM",
            "from"        : "01027287069",
            "content"     : "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number),
            "messages"    : [{"to": self.phone_number}]
        }

        timeStamp      = str(int(time.time() * 1000))
        access_key     = "IOtPwtO8ScDz19bkE6va"
        string_to_sign = "POST " + uri + "\n" + timeStamp + "\n" + access_key
        signature      = self.make_signature(string_to_sign)

        headers = {
            "Content-Type"             : "application/json; charset=UTF-8",
            "x-ncp-apigw-timestamp"    : timeStamp,
            "x-ncp-iam-access-key"     : access_key,
            "x-ncp-apigw-signature-v2" : signature
        }

        requests.post(api_url, data = json.dumps(body), headers = headers)

    def make_signature(self, string):
        secret_key    = bytes(my_settings.SECRET_KEY['sms'], 'UTF-8')
        string        = bytes(string, 'UTF-8')
        string_hmac   = hmac.new(secret_key, string, digestmod = hashlib.sha256).digest()
        string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
        
        return string_base64

    @classmethod
    def check_auth_number(cls, p_num, c_num):
        time_limit    = timezone.now() - datetime.timedelta(minutes = 5)
        result        = cls.objects.filter(
                            phone_number  = p_num,
                            auth_number   = c_num,
                            modified__gte = time_limit
                        )
        return result.exists()

