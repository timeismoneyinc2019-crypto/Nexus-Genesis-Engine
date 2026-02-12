import hashlib

class ReputationManager:
    def __init__(self):
        self.reputations = {}  # user_id: reputation_score
        self.anchor_log = {}   # user_id: list of anchor_ids for audit

    def get_reputation(self, user_id):
        return self.reputations.get(user_id, 0)

    def update_reputation(self, user_id, amount, anchor_id=None, thermodynamic_cost=None):
        """
        Update reputation with optional entropic anchor data.
        Reputation change can be weighted by thermodynamic_cost.
        """
        weight = thermodynamic_cost if thermodynamic_cost is not None else 1.0
        adjusted_amount = amount * weight

        if user_id in self.reputations:
            self.reputations[user_id] += adjusted_amount
        else:
            self.reputations[user_id] = adjusted_amount

        if anchor_id:
            self.anchor_log.setdefault(user_id, []).append(anchor_id)

    def verify_anchor_integrity(self, user_id, anchor_id):
        """
        Verify if the anchor_id exists in the user's anchor log.
        """
        return anchor_id in self.anchor_log.get(user_id, [])

class SlashingManager:
    def __init__(self):
        self.penalties = {}  # user_id: penalty_score

    def apply_slashing(self, user_id, penalty, entropy_validation_passed=True):
        """
        Apply slashing penalty. If entropy validation fails, increase penalty.
        """
        adjusted_penalty = penalty
        if not entropy_validation_passed:
            # Increase penalty by 50% if entropy proof fails
            adjusted_penalty *= 1.5

        if user_id in self.penalties:
            self.penalties[user_id] += adjusted_penalty
        else:
            self.penalties[user_id] = adjusted_penalty