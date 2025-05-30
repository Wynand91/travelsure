from apps.policy.models import Policy


def calculate_price(policy: Policy):
    # price per day
    price_map = {
        'BASIC': 1,
        'STANDARD': 2,
        'PREMIUM': 3
    }
    delta = policy.end_date - policy.start_date
    return delta.days * price_map[policy.policy_type.name]
