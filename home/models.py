from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import Profile
# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserGoal(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_all_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user} {self.date} {self.is_all_completed}"


class Goal(BaseModel):
    user_goal = models.ForeignKey(
        UserGoal, on_delete=models.CASCADE, related_name='goals')
    goal = models.CharField(max_length=5000, blank=True, default='')
    is_completed = models.BooleanField(default=False)


@receiver(post_save, sender=Goal)
def save_goal(sender, instance, **kwargs):
    goals = Goal.objects.filter(
        user_goal=instance.user_goal, is_completed=False)
    instance.user_goal.is_all_completed = not goals.exists()
    instance.user_goal.save()
