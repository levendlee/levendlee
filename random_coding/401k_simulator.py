import math


def simulate(start_age, retire_age, death_age,
             work_tax_rate, retire_tax_rate, earning_tax_rate, return_rate, inflation_rate,
             contrib_limit, contrib_limit_increase):
    balance_401k = 0
    balance_broker = 0

    pre_tax_cost = 0
    roth_cost = 0

    infl_adj_pre_tax_cost = 0
    infl_adj_roth_cost = 0

    for age in range(start_age, retire_age + 1):
        # Total cost out of your compensation. Including taxes.
        cur_roth_cost = contrib_limit / (1 - work_tax_rate)
        cur_pre_tax_cost = contrib_limit

        balance_401k += contrib_limit
        # Use the extra tax savings in a broker account. But need to pay tax on this.
        balance_broker += (cur_roth_cost - cur_pre_tax_cost) * (1 - work_tax_rate)

        pre_tax_cost += cur_pre_tax_cost
        roth_cost += cur_roth_cost

        # Make all money comparable to current
        infl_adj_factor = math.pow(1 + inflation_rate, age - start_age)

        infl_adj_balance_401k = balance_401k / infl_adj_factor
        infl_adj_balance_broker = balance_broker / infl_adj_factor

        infl_adj_pre_tax_cost += cur_pre_tax_cost / infl_adj_factor
        infl_adj_roth_cost += cur_roth_cost / infl_adj_factor

        balance_401k *= 1 + return_rate
        # Need to pay tax on the broker account earnings
        balance_broker *= 1 + return_rate * (1 - earning_tax_rate)
        contrib_limit *= 1 + contrib_limit_increase

        print("At Age: {}".format(age))
        print("\t401K Balance: {:,.2f}; Broker Balance: {:,.2f}; "
              "Pre-Tax Cost: {:,.2f}; Roth Cost: {:,.2f}".format(
            balance_401k, balance_broker, pre_tax_cost, roth_cost))
        print("\tInflation Adjuested:")
        print("\t401K Balance: {:,.2f}; Broker Balance: {:,.2f}; "
              "Pre-Tax Cost: {:,.2f}; Roth Cost: {:,.2f}".format(
            infl_adj_balance_401k, infl_adj_balance_broker,
            infl_adj_pre_tax_cost, infl_adj_roth_cost))

    print("Total After Tax Monery Avaiable at Retirement:")
    print("If You Max Out Pre-Tax All the Time:")
    infl_adj_balance_401k_after_tax = infl_adj_balance_401k * (1 - retire_tax_rate)
    print("\t{:,.2f} + {:,.2f} = {:,.2f}".format(
        infl_adj_balance_401k_after_tax, infl_adj_balance_broker,
        infl_adj_balance_401k_after_tax + infl_adj_balance_broker))
    print("If You Max Out Roth All the Time:")
    print("\t{:,.2f}".format(infl_adj_balance_401k))


simulate(start_age=27, retire_age=65, death_age=80,
         work_tax_rate=0.45, retire_tax_rate=0.32, earning_tax_rate=0.25,
         return_rate=0.1, inflation_rate=0.03,
         contrib_limit=19500, contrib_limit_increase=0.026)
