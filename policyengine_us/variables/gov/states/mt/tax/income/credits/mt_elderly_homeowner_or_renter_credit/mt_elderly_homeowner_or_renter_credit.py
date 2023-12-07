from policyengine_us.model_api import *


class mt_elderly_homeowner_or_renter_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Montana Elderly Homeowner/Renter Credit"
    unit = USD
    definition_period = YEAR
    defined_for = "mt_elderly_homeowner_or_renter_credit_eligible"

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.mt.tax.income.credits.elderly_homeowner_or_renter_credit

        # Calculate net_household_income
        standard_exclusion = p.net_household_income.standard_exclusion_amount
        gross_household_income = tax_unit("mt_gross_household_income", period)
        reduced_household_income = max_(
            gross_household_income - standard_exclusion, 0
        )
        net_household_income = (
            p.net_household_income.phase_out_rate.calc(
                reduced_household_income
            )
            * reduced_household_income
        )
        # Credit Computation
        property_tax = add(tax_unit, period, ["real_estate_taxes"])
        rent = add(tax_unit, period, ["rent"])
        credit_amount = max_(
            rent * p.rent_equivalent_tax_rate
            + property_tax
            - net_household_income,
            0,
        )
        capped_credit = min_(credit_amount, p.cap)
        return p.multiplier.calc(gross_household_income) * capped_credit
