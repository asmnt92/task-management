from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


@receiver(post_save,sender=User)
def conform_acount_in_via_email(sender,instance,created,**kwargs):
    if created:
        user=instance
        user.is_active=False
        user.save()
        token=default_token_generator.make_token(instance)
        activation_url=f"{settings.FRONTEND_URL}auth/activate/{instance.id}/{token}/"

        send_mail(
            subject="Account Confirmation",
            message=f"Click to activate your account: {activation_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False, 
        )



@receiver(post_save,sender=User)
def assign_folr(sender,instance,created,**kwargs):
    if created:
        user_group,create=Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()