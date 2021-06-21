import jwt
import re
import bcrypt
import json
import requests
from datetime import datetime

from django.http        import JsonResponse
from django.db          import transaction
from django.views       import View
from django.shortcuts   import redirect
from django.db.models   import Q

from .models import (
    User,
    UserBook,
    SMSAuthRequest,
)
from library.models import (
    Library,
)

import my_settings


def generate_token(user_id):
    token = jwt.encode(
                {'user_id':user_id},
                my_settings.SECRET_KEY['secret'],
                algorithm=my_settings.JWT_ALGORITHM
            ).decode('utf-8')

    return token

class SignUpView(View):
    def check_password_pattern(self, password):
        check_password  = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

        return check_password.match(password)

    def check_phonenumber_pattern(self, phone_number):
        check_phone_num = re.compile('^[0-9]{11}$')

        return check_phone_num.match(phone_number)

    def proc_post(self, data):
        try:
            valid_phone_number = self.check_phonenumber_pattern(data['phone_number'])
            valid_password     = self.check_password_pattern(data['password'])
            if not valid_phone_number or not valid_password:
                return JsonResponse({"message":"INVALID_REQUEST"}, status=400)

            if User.objects.filter(Q(phone_number=data['phone_number'])|
                                    Q(nickname=data['nickname'])).exists():
                return JsonResponse({"message":"INVALID_REQUEST"}, status=409)

            user = User.objects.create(
                        nickname     = data['nickname'],
                        phone_number = data['phone_number'],
                        password     = bcrypt.hashpw(
                                            data['password'].encode('utf-8'),
                                            bcrypt.gensalt()
                                        ).decode(),
                    )
            
            if not Library.objects.filter(user_id = user.id):
                Library.objects.create(user_id = user.id, name = user.nickname, image_url = '')
                        
            return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    @transaction.atomic
    def post(self, request):
        data = json.loads(request.body)

        return self.proc_post(data)

class SignInView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            phone_number = data['phone_number']
            password     = data['password']
            user         = User.objects.filter(phone_number = phone_number)
            if not user.exists():
                return JsonResponse({"message":"USER_NOT_EXIST"}, status=400)

            user = user.first()
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message":"USER_NOT_EXIST"}, status=400)

            token = generate_token(user.id)

            return JsonResponse({"message":"SUCCESS", "access_token":token}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class SignInWithKakaoView(View):
    @transaction.atomic
    def post(self, request):
        try:
            token         = request.headers['Authorization']
            profile       = requests.post(
                                    "https://kapi.kakao.com/v2/user/me",
                                    headers = {'Authorization':f'Bearer {token}'},
                                    data    = 'property_keys=["kakao_account.email"]'
                                )
            profile       = profile.json()
            kakao_id       = profile.get('id', None)

            if not kakao_id:
                return JsonResponse({"message":"INVALID_TOKEN"}, status=400)

            kakao_account = profile.get('kakao_account')
            nickname      = kakao_account['profile'].get('nickname', '')
            thumbnail     = kakao_account['profile'].get('thumbnail_image_url', '')
            email         = kakao_account.get('email', '')
            obj, created  = User.objects.update_or_create(
                                email    = email,
                                defaults = {
                                            'kakao_id'  : str(kakao_id),
                                            'nickname'  : nickname,
                                            'image_url' : thumbnail,
                                            'updated_at': datetime.now(),
                                            'email'     : email,
                                            }
                             )
            user = None
            if obj:
                user = obj
            elif created:
                user = created
            
            token = generate_token(user.id)
             
            if not Library.objects.filter(user__kakao_id = str(kakao_id)):
                Library.objects.create(user_id = user.id, name = user.nickname, image_url = '')
            
            return JsonResponse({"message":"SUCCESS", "access_token":token}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class SMSCheckView(View):
    @transaction.atomic
    def post(self, request):
        try:
            data    = json.loads(request.body)
            phone_number = data['phone_number']
            SMSAuthRequest.objects.update_or_create(phone_number=phone_number)

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request):
        try:
            phone_number = request.GET.get('phone_number', '')
            auth_number  = request.GET.get('auth_number', 0)
            result       = SMSAuthRequest.check_auth_number(phone_number, auth_number)

            return JsonResponse({'message': 'SUCCESS', 'result': result}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


