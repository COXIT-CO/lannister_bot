from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from lannister_auth.models import LannisterUser, Role


class BonusRequest(models.Model):
    # class BonusRequestStatus(models.TextChoices):
    #     CREATED = "Cr", _("Created")
    #     APPROVED = "Appr", _("Approved")
    #     REJECTED = "Rj", _("Rejected")
    #     DONE = "Done", _("Done")

    class BonusRequestType(models.TextChoices):
        REFERAL = "Referral", _("Referral")
        OVERTIME = "Overtime", _("Overtime")

    creator = models.ForeignKey(LannisterUser, on_delete=models.PROTECT)
    status = models.ForeignKey(
        "BonusRequestStatus", related_name="statuses", on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        LannisterUser, related_name="reviewer", on_delete=models.SET_NULL, null=True
    )
    bonus_type = models.CharField(max_length=50, choices=BonusRequestType.choices)
    description = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=3)
    payment_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        try:
            reviewer = LannisterUser.objects.get(username=self.reviewer.username)
            is_reviewer = Role.objects.get(id=2) in reviewer.roles.all()
            if not is_reviewer:
                raise ValueError(
                    _(
                        "Selected user is not a reviewer. Select a valid user with reviewer role."
                    )
                )
            self.reviewer = reviewer
        except (AttributeError, ValueError):
            # if reviewer is null
            pass
        finally:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.creator}'s bonus request. Reviewer assigned - {self.reviewer}"


# TODO: implement history
class BonusRequestsHistory(models.Model):
    bonus_request = models.ForeignKey(
        BonusRequest, related_name="requests", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"Request id: {self.bonus_request.pk}, opened by {self.bonus_request.creator}"

    class Meta:
        verbose_name_plural = "Bonus requests history"


class BonusRequestStatus(models.Model):
    status_name = models.CharField(max_length=45, unique=True, null=False)

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = "Bonus status"
        verbose_name_plural = "Bonus statuses"


def create_history(sender, instance, created, *args, **kwargs):
    if created:
        BonusRequestsHistory.objects.get_or_create(bonus_request=instance)


@receiver(post_save, sender=BonusRequest)
def add_status_change_to_history(sender, instance, *args, **kwargs):
    previous = BonusRequestsHistory.objects.filter(id=instance.id).first()
    if (
        not previous
        or previous.bonus_request.status.status_name != instance.status.status_name
    ):
        BonusRequestsHistory.objects.create(bonus_request=instance)


def create_bonus_requests_status(sender, instance, created, *args, **kwargs):
    if created:
        BonusRequestStatus.objects.get_or_create(status_name="Created")
        BonusRequestStatus.objects.get_or_create(status_name="Approved")
        BonusRequestStatus.objects.get_or_create(status_name="Rejected")
        BonusRequestStatus.objects.get_or_create(status_name="Done")


pre_save.connect(create_bonus_requests_status, BonusRequest)
