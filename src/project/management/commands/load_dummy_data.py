from datetime import timedelta

from apps.claims.enums import ClaimStatus
from apps.claims.models import Claim
from apps.policy.enums import Destination, PolicyType, PolicyStatus
from apps.policy.models import Policy
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the db with a test user'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='test@user.com')
        parser.add_argument('--created_date', default=None)

    @atomic
    def handle(self, *args, **options):
        if settings.ENV != 'development':
            raise CommandError("This command is disabled in production.")

        # noinspection PyPep8Naming
        User: AbstractBaseUser = get_user_model()
        user, _ = User.objects.get_or_create(
            username=options['username'],
            password=make_password('test123')
        )
        now = timezone.now().date()

        # Create a policy
        start_date = now - timedelta(days=30)
        policy = Policy.objects.create(
            user=user,
            destination=Destination.EUROPE,
            start_date=start_date,
            end_date=now,
            policy_type=PolicyType.PREMIUM,
            paid=True,
            status=PolicyStatus.EXPIRED
        )

        # create a claim
        Claim.objects.create(
            policy=policy,
            description='I lost my bag.',
            amount_claimed=200,
            status=ClaimStatus.PENDING
        )

        self.stdout.write(self.style.SUCCESS('Test data loaded.'))
