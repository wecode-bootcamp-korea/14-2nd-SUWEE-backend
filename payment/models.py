from django.db import models


class Payment(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
    subscribe_day  = models.IntegerField()
    expired_day    = models.DateField()
    method         = models.CharField(max_length=45)
    next_payday    = models.DateField()
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
