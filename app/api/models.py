from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True)
    company = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.id,self.user.username, self.user.email, self.birthday, self.company, self.location)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Followers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='followers_user_followed')  # User who is followed
    followed_by_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='followers_follower')  # User one who following
    followed_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'followed_by_id')

    def __str__(self):
        return '{} {} {} {}'.format(self.id, self.user_id.id, self.followed_by_id, self.followed_at)




