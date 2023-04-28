import numpy as np


class Validator():
    """
        The validator class is to represent the validator in the PoS Ethereum Blockchain.

        Parameters:
            self. strategy : The strategy of the validator, 0 for honest, 1 for malicious
            self. status : The status of the validator, 0 for propose, 1 for vote
            self. current_balance : The current balance of the validator
            self. effective_balance : The effective balance of the validator
        ----------

        Input for functions:
            total_active_balance: The total active balance of all the validators, to update the base reward
            proportion_of_honest: The proportion of honest validators, to update the current balance and effective balance.
        ----------
    """

    def __init__(self, strategy, status, current_balance, effective_balance) -> None:
        self.strategy = strategy
        self.status = status
        self.current_balance = current_balance
        self.effective_balance = effective_balance
        self.reward = 0

    def get_base_reward(self, total_active_balance) -> float:
        # base_reward = effective_balance * base_reward_factor /
        #               (base_rewards_per_epoch * sqrt(sum(active_balance)))
        # where base_reward_factor is 64, base_rewards_per_epoch is 4
        # and sum(active balance) is the total staked ether across all active validators.
        base_reward = self.effective_balance * \
            4 / np.sqrt(total_active_balance)
        return base_reward

    def duty_weight(self, alpha) -> float:
        # when the validator play the honest strategy
        if self.strategy == 0:
            # when the validator is a proposer
            if self.status == 0:
                return 1/8
            # when the validator is a voter
            elif self.status == 1:
                return 27/32
            else:
                raise ValueError("The status of the validator is not valid.")
        # when the validator play the malicious strategy
        elif self.strategy == 1:
            # when the validator is a proposer: missing proposing
            if self.status == 0:
                return 0
            # when the validator is a voter: missing voting
            elif self.status == 1:
                return alpha * -27/32
            else:
                raise ValueError("The status of the validator is not valid.")
        else:
            raise ValueError("The strategy of the validator is not valid.")

    def update_balances(self, proportion_of_honest, alpha, total_active_balance, proposer_strategy) -> float:
        base_reward = self.get_base_reward(
            total_active_balance=total_active_balance)

        duty_weight = self.duty_weight(alpha)

        if proportion_of_honest > 1/2:
            if proposer_strategy == 0:  # honest proposer, a valid block
                if self.strategy == 0:  # honest voters vote, all honest validators get rewards
                    update = duty_weight * base_reward * proportion_of_honest
                else:  # malicious voters do not vote, all malicious validators get penalized
                    update = - duty_weight * base_reward * proportion_of_honest
            else:  # malicious proposer, an invalid block
                if self.strategy == 0:  # honest voters misses voting, all honest validators get penalized
                    update = - duty_weight * base_reward * proportion_of_honest
                else:  # since honest proposers are larger than 1/2, the malicious proposer is detected and penalized heavily
                    if self.status == 0:  # proposer
                        update = - base_reward * proportion_of_honest
                    else:  # malicious voters vote for it but no consensus is reached.
                        update = 0
        else:  # proportion_of_honest <= 1/2, malicious validaters are larger
            if proposer_strategy == 0:  # honest proposer, a valid block
                if self.strategy == 0:  # honest voters vote, but no consensus is reached, all honest validators get 0
                    update = 0
                else:  # malicious voters do not vote, all malicious validators get penalized
                    update = - duty_weight * base_reward * \
                        (1 - proportion_of_honest)
            else:  # malicious proposer, an invalid block
                if self.strategy == 0:  # honest voters misses voting, all honest validators get penalized
                    update = - duty_weight * base_reward * \
                        (1 - proportion_of_honest)
                else:  # malicious voters vote for it, all malicious validators get rewards
                    update = duty_weight * base_reward * \
                        (1 - proportion_of_honest)
        self.reward = update

        # update the current balance
        self.current_balance = self.current_balance + update
        # update the effective balance
        if update > 1.25:
            self.effective_balance = self.effective_balance + 1
        elif update < - 0.5:
            self.effective_balance = self.effective_balance - 1
        else:
            pass

        # set bound to effective balance from 0 to 32
        self.effective_balance = max(0, self.effective_balance)
        self.effective_balance = min(32, self.effective_balance)

        return

    def __str__(self) -> str:
        return '<Validator strategy={}, status={}, current_balance={}, effective_balance={}>'.format(self.strategy, self.status, self.current_balance, self.effective_balance)
