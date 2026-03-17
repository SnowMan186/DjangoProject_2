from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailings.models import Mailing


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры"'

    def handle(self, *args, **options):
        managers_group, _ = Group.objects.get_or_create(name="Менеджеры")

        content_type = ContentType.objects.get_for_model(Mailing)
        can_view_all_mailings_perm, _ = Permission.objects.get_or_create(
            codename="can_view_all_mailings",
            name="Может просматривать все рассылки",
            content_type=content_type
        )
        managers_group.permissions.add(can_view_all_mailings_perm)