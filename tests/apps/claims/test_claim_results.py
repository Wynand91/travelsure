from django.core import mail
from django.test import TestCase

from apps.claims.enums import ClaimStatus
from tests.factories import UserFactory, PolicyFactory, ClaimFactory


class TestClaimResult(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.policy = PolicyFactory(user=self.user)
        self.claim = ClaimFactory(policy=self.policy)
        assert self.claim.status == ClaimStatus.PENDING
        # clear any mails created by factories
        mail.outbox.clear()

    def test_claim_approved(self):
        # mock admin user updating claim status
        self.claim.status = ClaimStatus.APPROVED
        self.claim.save()

        # check email was sent
        assert len(mail.outbox) == 1
        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == 'Claim Result'
        assert 'Your claim has been reviewed an approved.' in email.body
        assert email.to == [self.user.username]


    def test_claim_denied(self):
        # mock admin user updating claim status
        self.claim.status = ClaimStatus.REJECTED
        self.claim.save()

        # check email was sent
        assert len(mail.outbox) == 1
        # Inspect the email content
        email = mail.outbox[0]
        assert email.subject == 'Claim Result'
        assert 'Unfortunately your claim has been denied.' in email.body
        assert email.to == [self.user.username]
