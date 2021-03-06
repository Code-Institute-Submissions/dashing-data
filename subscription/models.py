from django.db import models
from django.contrib.auth.models import User

class SubscriptionType(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    description = models.CharField(max_length=254, blank=False)
    length_months = models.IntegerField(blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "subscription_type_id: " + str(self.pk)

class UserSubscription(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type_id = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    status = models.CharField(max_length=20, blank=False, default='None')

    def __str__(self):
        return "user_id: " + str(self.user_id) + \
            " subscription_type_id: " + str(self.subscription_type_id) + \
            " subscription_id: " + str(self.pk)