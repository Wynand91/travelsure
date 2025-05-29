from apps.claims.enums import ClaimStatus


def get_template_for_status(status: ClaimStatus):
    if status == ClaimStatus.APPROVED:
        return 'claim_result_success.html'
    if status == ClaimStatus.REJECTED:
        return 'claim_result_denied.html'
