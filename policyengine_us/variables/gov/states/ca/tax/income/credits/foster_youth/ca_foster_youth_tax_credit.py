from policyengine_us.model_api import *


class ca_foster_youth_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "California foster youth tax credit"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.CA

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.ca.tax.income.credits.foster_youth
        person = tax_unit.members

        age = person("age", period)

        is_eligible = person("ca_foster_youth_tax_credit_eligible", period)

        adjustment_factor = parameters(period).gov.states.ca.tax.income.credits.earned_income.adjustment.factor

        base_credit = p.base.calc(age) * adjustment_factor * is_eligible 

        total_base_credit = tax_unit.sum(base_credit)

        earned_income = add(tax_unit, period, ["earned_income"])

        excess_earned_income = max_(earned_income - p.phase_out.start, 0)  

        reduction_amount = max_(
            0, (excess_earned_income / p.phase_out.increment) * p.phase_out.amount
        )

        return max_(0,min_(total_base_credit, total_base_credit - reduction_amount))
