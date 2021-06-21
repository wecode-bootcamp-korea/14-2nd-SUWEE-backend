import json
from iamport import Iamport

from django.views import View
from django.http  import JsonResponse

from share.decorators import check_auth_decorator

class PaymentView(View):
    @check_auth_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = request.user
            payment  = Payment.objects.create(
                user_id       = user,
                subscribe_day = data['subscribe_day'],
                expired_day   = data['expired_day'],
                method        = data['method'],
                next_payday   = data['next_payday']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        return KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=200)

    @check_auth_decorator
    def get(self, request):
        try:
            user = request.user
            payment = Payment.objects.get(user_id=user)

            payment_list = {
                'user_id'       : payment.user_id,
                'subscribe_day' : payment.subscribe_day,
                'expired_day'   : payment.expired_day,
                'method'        : payment.method,
                'next_payday'   : payment.next_payday,
                'created_at'    : payment.created_at
            }
            return JsonResponse({'payment_list':payment_list}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


