from django.db import models


class Member(models.Model):
    """A member of team"""
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contribute = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model"""
        return self.name


class Contribution(models.Model):
    """What is amount was given per time"""
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.amount}"

    def get_amount(self):
        return self.amount

    def get_member(self):
        return self.member


class Expence(models.Model):
    """What is amount was spent and why"""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.purpose}: {self.amount}"

    def get_amount(self):
        return self.amount
