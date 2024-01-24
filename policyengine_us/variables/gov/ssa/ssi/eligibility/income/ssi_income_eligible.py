from policyengine_us.model_api import *


class ssi_income_in_sga(Variable):
    value_type = bool
    entity = Person
    label = "Income less than the SGA limit"
    definition_period = YEAR
    reference = "https://www.ssa.gov/OP_Home/cfr20/416/416-0971.htm"

    def formula(person, period, parameters):
        income = person("ssi_earned_income", period)
        monthly_income = income / MONTHS_IN_YEAR
        sga = parameters(period).gov.ssa.ssi.income.limit.sga

        # SGA does not apply to blind individuals
        is_blind = person("is_blind", period)

        return (monthly_income < sga) | is_blind
