class Sequencer:
    def __init__(self):
        self.users = {}
        self.reputation_scores = {}
        self.anchor_log = {}  # user_id: list of anchor_ids for audit

    def register_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                'stake': 0,
                'stake_history': [],        # Track all stake changes (amount, thermodynamic_cost, anchor_id)
                'malicious_behaviors': 0
            }
            self.reputation_scores[user_id] = 100
            self.anchor_log[user_id] = []

    def stake_tokens(self, user_id, amount, thermodynamic_cost=1.0, anchor_id=None):
        """
        Stake tokens with optional thermodynamic cost and anchor ID.
        Thermodynamic cost weights the stake impact.
        """
        if user_id in self.users:
            old_stake = self.users[user_id]['stake']
            self.users[user_id]['stake_history'].append({
                'old_stake': old_stake,
                'amount': amount,
                'thermodynamic_cost': thermodynamic_cost,
                'anchor_id': anchor_id
            })

            # Update stake weighted by thermodynamic cost
            weighted_amount = amount * thermodynamic_cost
            self.users[user_id]['stake'] += weighted_amount

            # Log anchor ID for audit
            if anchor_id:
                self.anchor_log[user_id].append(anchor_id)

    def slash_user(self, user_id, anchor_id=None, entropy_validation_passed=True):
        """
        Slash user stake by halving it.
        Increase penalty if entropy validation fails.
        """
        if user_id in self.users:
            old_stake = self.users[user_id]['stake']
            self.users[user_id]['stake_history'].append({
                'old_stake': old_stake,
                'amount': -old_stake * 0.5,
                'thermodynamic_cost': None,
                'anchor_id': anchor_id
            })

            penalty_factor = 0.5
            if not entropy_validation_passed:
                # Increase penalty by 50% if entropy proof fails
                penalty_factor *= 1.5

            new_stake = old_stake * (1 - penalty_factor)
            self.users[user_id]['stake'] = max(new_stake, 0)

            self.users[user_id]['malicious_behaviors'] += 1

            # Update reputation considering malicious behavior count
            self.update_reputation(user_id)

            # Log anchor ID for audit
            if anchor_id:
                self.anchor_log[user_id].append(anchor_id)

    def update_reputation(self, user_id):
        if self.users[user_id]['malicious_behaviors'] > 0:
            deduction = 10 * self.users[user_id]['malicious_behaviors']
            self.reputation_scores[user_id] = max(0, self.reputation_scores[user_id] - deduction)

    def compete(self):
        """
        Return top 3 users sorted by reputation score descending.
        """
        winners = sorted(self.reputation_scores.items(), key=lambda item: item[1], reverse=True)
        return [user[0] for user in winners[:3]]

    def display_scores(self):
        return self.reputation_scores

    def display_stake_history(self, user_id):
        """
        Return detailed stake history including thermodynamic cost and anchor IDs.
        """
        if user_id in self.users:
            return self.users[user_id]['stake_history']
        return []

    def verify_anchor_integrity(self, user_id, anchor_id):
        """
        Check if the anchor_id exists in the user's anchor log.
        """
        return anchor_id in self.anchor_log.get(user_id, [])

if __name__ == '__main__':
    sequencer = Sequencer()
    sequencer.register_user('user1')
    sequencer.stake_tokens('user1', 100, thermodynamic_cost=1.2, anchor_id='anchor123')
    sequencer.register_user('user2')
    sequencer.stake_tokens('user2', 200, thermodynamic_cost=1.0, anchor_id='anchor456')
    sequencer.slash_user('user1', anchor_id='anchor789', entropy_validation_passed=False)
    sequencer.stake_tokens('user1', 50, thermodynamic_cost=0.8, anchor_id='anchor101112')

    print('Reputation Scores:', sequencer.display_scores())
    print('Competition Winners:', sequencer.compete())
    print('User1 Stake History:', sequencer.display_stake_history('user1'))
    print('User1 Anchor Integrity (anchor789):', sequencer.verify_anchor_integrity('user1', 'anchor789'))