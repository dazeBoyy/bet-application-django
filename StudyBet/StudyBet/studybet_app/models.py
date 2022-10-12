import decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser





class Fixture(models.Model):
    BET_RESULTS = ((0, "LOST"),
                   (1, "WON"),
                   (2, "PENDING")
                   )
    bet_win = models.CharField(max_length=256)
    bet_lose = models.CharField(max_length=256)
    bet_name = models.CharField(max_length=256)
    # bet result 0: LOST, 1: WIN
    fixture_result = models.IntegerField(choices=BET_RESULTS, default=2)
    sum_of_bet = models.IntegerField(default=0)

    def __str__(self):
        return self.bet_name

    def save(self, *args, **kwargs):
        super(Fixture, self).save(args, kwargs)

        bets = Bet.objects.filter(fixture=self.id)
        for bet in bets:
            users = User.objects.filter(username=bet.bet_user)
            for user in users:
                accounts = Account.objects.filter(user=user)
                for account in accounts:
                    if self.fixture_result == bet.bet:
                        print(self.fixture_result)
                        print(bet.bet)
                        account.cash = int(bet.bet_amount * bet.bet_course)
                        account.save()
                    else:
                        print(self.fixture_result)
                        print(bet.bet)
                        super(Fixture, self).save(args, kwargs)




# Create your models here.
class Account(models.Model):
    cash = models.DecimalField(validators=[MinValueValidator(0.00)],
                               max_digits=6, decimal_places=2)
    user = models.OneToOneField(User, on_delete= models.CASCADE)


    def __str__(self):
        return self.user.username


class Bet(models.Model):
    fixture = models.ForeignKey(Fixture, related_name="fixture", on_delete=models.CASCADE)
    BET_CHOICES = ((0, "LOST"),
                   (1, "WON"),
                   )

    bet_user = models.ForeignKey(Account, related_name="bet_user", on_delete= models.CASCADE)
    bet_amount = models.DecimalField(validators=[MinValueValidator(0.01)],
                                     max_digits=6, decimal_places=2)

    bet = models.IntegerField(choices=BET_CHOICES)
    bet_course = models.IntegerField(default=2)



    def __str__(self):
        self.fixture.id
        return self.fixture.bet_name

    def save(self, *args, **kwargs):
        super(Bet, self).save(args, kwargs)

        bet = Fixture.objects.filter(bet_name = self.fixture).first()
        user = User.objects.get(username = self.bet_user)
        account = Account.objects.get(user = user)

        if account.cash >= self.bet_amount:
            bet.sum_of_bet += self.bet_amount
            account.cash = account.cash - self.bet_amount
            account.save()
            bet.save()

