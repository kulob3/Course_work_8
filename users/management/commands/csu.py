from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Create a super user"

    def handle(self, *args, **options):
        user = User.objects.create(email="adm@1.ru")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("admin")
        user.save()
