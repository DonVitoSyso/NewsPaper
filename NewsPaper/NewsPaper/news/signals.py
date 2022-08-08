# D6
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор

from .models import Post
from .tasks import new_post_subscription
# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
# @receiver(post_save, sender=Post)
@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, **kwargs):
    print(F'Post start...')
    new_post_subscription(instance)
