import json
import bcrypt
from unittest.mock  import patch, MagicMock

from django.test import TestCase, Client

from .models import (
        User,
        SMSAuthRequest,
)
from .views  import SMSCheckView

class UserTest(TestCase):
    def setUp(self):
        client = Client()

        SMSAuthRequest.objects.create(phone_number='01011112222')
        password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt())
        User.objects.create(phone_number='01011112222', password = password.decode(), nickname='test_user')

    def tearDown(self):
        User.objects.all().delete()
        SMSAuthRequest.objects.all().delete()

    def test_user_signup_post_success(self):
        body = {
                'phone_number' : '01012347654',
                'password'     : 'SuweePW1?',
                'nickname'     : 'goblin',
                }

        response = self.client.post(
                        '/user/sign_up', 
                        json.dumps(body), 
                        content_type = 'application/json'
                    )
        self.assertEqual(response.status_code, 201)        
        
        User.objects.last().delete()

    def test_user_signup_post_key_error(self):
        body = {
                'phone'    : '01012347654',
                'password' : 'SuweePW1?',
                'nickname'     : 'goblin',
                }

        response = self.client.post(
                        '/user/sign_up', 
                        json.dumps(body), 
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_user_signup_post_invalid_request_phone_number(self):
        body = {
                'phone_number' : '010-1213-7654',
                'password'     : 'SuweePW1?',
                'nickname'     : 'goblin',
                }

        response = self.client.post(
                        '/user/sign_up', 
                        json.dumps(body), 
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_REQUEST'})

    def test_user_signup_post_invalid_request_password(self):
        body = {
                'phone_number' : '01012347654',
                'password'     : 'Suw',
                'nickname'     : 'goblin',
                }

        response = self.client.post(
                        '/user/sign_up', 
                        json.dumps(body), 
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_REQUEST'})

    def test_user_signup_post_invalid_request_duplicate(self):
        User.objects.create(
                phone_number = '01011112222', 
                password     = 'Suweasdff!@#KJ@ePW1',
                nickname     = 'goblin',
        )

        body = {
                'phone_number' : '01011112222',
                'password'     : 'Suweasdff!@#KJ@ePW1',
                'nickname'     : 'goblin',
                }

        response =  self.client.post(
                        '/user/sign_up',
                        json.dumps(body),
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"message":"INVALID_REQUEST"})
        User.objects.last().delete()

    def test_user_signin_post_success(self):
        body = {
                'phone_number' : '01011112222',
                'password'     : '12345678'
                }

        response =  self.client.post(
                        '/user/sign_in',
                        json.dumps(body),
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 200)

    def test_user_signin_post_key_error(self):
        body = {
                'phone_number' : '01011112222',
                'passrd'       : '12345678'
                }

        response =  self.client.post(
                        '/user/sign_in',
                        json.dumps(body),
                        content_type = 'application/json'
                     )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

    def test_user_signin_post_user_not_exist(self):
        body = {
                'phone_number' : '01011112223',
                'password'     : '12345678'
                }

        response =  self.client.post(
                        '/user/sign_in',
                        json.dumps(body),
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"USER_NOT_EXIST"})

    def test_user_signin_post_invalid_password(self):
        body = {
                'phone_number' : '01011112222',
                'password'     : 'Suweasdff!@#KJ@ePW1'
                }

        response =  self.client.post(
                        '/user/sign_in',
                        json.dumps(body),
                        content_type = 'application/json'
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"USER_NOT_EXIST"})

    def test_user_signin_with_kakao_invalid_token(self):
        headers={"HTTP_Authorization":"wrongtoken@!#@"}
        
        response = self.client.post(
                        '/user/kakao_sign_in',
                        content_type = 'application/json',
                        **headers
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_TOKEN"})

    def test_user_signin_with_kakao_key_error(self):
        headers ={"HTTP_token":"wrongtoken@!#@"}

        response = self.client.post(
                        '/user/kakao_sign_in',
                        content_type = 'application/json',
                        **headers
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

    @patch('user.views.requests')
    def test_user_signin_with_kakao_success(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {
                        'id'            : 12345,
                        'kakao_account' : {
                            'profile'   : {
                                'nickname':'test_user',
                                'thumbnail_image_url':'image_url_info',
                                'email':'test@example.com'
                            }
                        }
                    }

        mocked_request.post = MagicMock(return_value=FakeResponse())
        
        headers = {'HTTP_Authorization':'fake_token.1234'}
        response = self.client.post('/user/kakao_sign_in',
                        content_type='application/json', 
                        **headers
                    )

        self.assertEqual(response.status_code, 200)

    def test_user_smscheck_get_success(self):
        sms_info = SMSAuthRequest.objects.get(phone_number='01011112222')
        response = self.client.get('/user/authSMS', {'phone_number':'01011112222','auth_number':sms_info.auth_number }) 
        
        self.assertEqual(response.json(), {"message":"SUCCESS", "result":True})
        self.assertEqual(response.status_code, 200)
     
