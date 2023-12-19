from policyengine_us.model_api import *


class va_low_income_tax_credit_agi_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Eligible for the Virginia low income tax credit"
    definition_period = YEAR
    defined_for = "va_low_income_tax_credit_program_eligibility"

    def formula(tax_unit, period, parameters):
        agi = tax_unit("va_agi", period)
        # Virginia does not account for blind or aged exemptions
        n = tax_unit("exemptions", period)
        state_group = "CONTIGUOUS_US"
        p_fpg = parameters(period).gov.hhs.fpg
        p1 = p_fpg.first_person[state_group]
        pn = p_fpg.additional_person[state_group]
        return agi <= p1 + pn * (n - 1)
