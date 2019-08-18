
import numpy as np


if __name__ == '__main__':
    current_account_money = 1000
    isa_money = 1000
    n_years = 1

    for _ in range(n_years):
        current_account_money += current_account_money * 0.01

        for _ in range(365):  # day
            loc_ = 0.0002  # note: annualised_return = ((1 + loc_) ** 365) - 1
            scale_ = 0.005
            returns = np.maximum(
                -0.1, np.minimum(
                    0.1, np.random.normal(loc=loc_, scale=scale_)))
            isa_money += isa_money * returns

    print(f"current_account_money: {current_account_money}")
    print(f"isa_money: {isa_money}")
