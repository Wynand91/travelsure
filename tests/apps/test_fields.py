from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.claims.models import Claim, ClaimStatus  # adjust paths as needed
from tests.factories import ClaimFactory


class TestEnumSmallIntegerField(TestCase):

    def setUp(self):
        # Use a valid Claim instance
        self.claim = ClaimFactory(status=ClaimStatus.APPROVED)

    def test_field_stores_enum_as_int(self):
        claim = Claim.objects.get(pk=self.claim.pk)
        assert isinstance(claim.status, ClaimStatus)
        assert claim.status == ClaimStatus.APPROVED
        assert claim.status.value == 1

    def test_from_db_value_conversion(self):
        Claim.objects.filter(pk=self.claim.pk).update(status=2)  # raw int in DB
        claim = Claim.objects.get(pk=self.claim.pk)
        assert claim.status == ClaimStatus.REJECTED

    def test_to_python_invalid_input(self):
        with self.assertRaises(ValidationError) as exc:
            Claim.objects.create(
                policy=self.claim.policy,
                description="Another",
                amount_claimed=50.00,
                status="1"
            )
        assert str(exc.exception) == "['1 is not a valid ClaimStatus']"

    def test_get_prep_invalid_input(self):
        with self.assertRaises(ValidationError):
            Claim.objects.create(
                policy=self.claim.policy,
                description="Bad status",
                amount_claimed=99.00,
                status="999"
            ).full_clean()

    def test_get_prep_value_from_enum(self):
        value = Claim._meta.get_field("status").get_prep_value(ClaimStatus.REJECTED)
        assert value == 2

    def test_get_prep_value_from_int(self):
        value = Claim._meta.get_field("status").get_prep_value(0)
        assert value == 0

    def test_get_prep_value_invalid_type(self):
        with self.assertRaises(ValidationError):
            Claim._meta.get_field("status").get_prep_value("invalid")

    def test_deconstruct_removes_auto_choices(self):
        field = Claim._meta.get_field("status")
        name, path, args, kwargs = field.deconstruct()
        assert kwargs["enum_class"] == ClaimStatus
        assert "choices" not in kwargs
