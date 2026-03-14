from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Mailing


class Command(BaseCommand):
    help = 'Creates default groups with permissions.'

    def handle(self, *args, **kwargs):
        content_types = ContentType.objects.get_for_models(Mailing)

        group_admins, created = Group.objects.get_or_create(name="Administrators")
        if created:
            print("Группа Administrators создана.")

        group_admins.permissions.add(
            *(Permission.objects.filter(content_type__in=content_types.values()))
        )
