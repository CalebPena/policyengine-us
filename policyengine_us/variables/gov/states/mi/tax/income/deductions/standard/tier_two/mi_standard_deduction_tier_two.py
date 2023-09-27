from policyengine_us.model_api import *


class mi_standard_deduction_tier_two(Variable):
    value_type = float
    entity = TaxUnit
    label = "Michigan tier two standard deduction"
    unit = USD
    definition_period = YEAR
    reference = (
        "http://legislature.mi.gov/doc.aspx?mcl-206-30",  # (b)&(c)
        "https://www.michigan.gov/taxes/iit/retirement-and-pension-benefits/michigan-standard-deduction",
        "https://www.michigan.gov/taxes/-/media/Project/Websites/taxes/Forms/2022/2022-IIT-Forms/BOOK_MI-1040.pdf#page=15",
    )
    defined_for = StateCode.MI

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.mi.tax.income.deductions.standard.tier_two
        # Core deduction based on filing status.
        filing_status = tax_unit("filing_status", period)
        # HAVE TO CHECK THIS
        sd2_age_eligible = tax_unit(
            "mi_standard_deduction_tier_two_eligible", period
        )
        # age_older = tax_unit("greater_age_head_spouse", period)
        # age_threshold = age_older >= p.min_age
        ssa_eligible = tax_unit(
            "mi_standard_deduction_tier_two_increase_eligible", period
        )

        person = tax_unit.members
        # (9), (b)
        # If the person has not reached the age of 67 (which is mathematically impossible) and is born betwee 1946 and 1952
        # then the person is eligible to a pension benefit deduction of 20,000 or 40,000, based on filing status
        uncapped_pension_income = person("taxable_pension_income", period)
        # CHECK PARAMETER NAME

        # If the person has surpassed the age of 67 and was born between 1946 and 1952 (which in 2022 is the only possible outcome)
        # the person is allows a general standard deduction of 20,000 or 40,000, based on income, no matter what income
        # CHECK PARAMETER METADATA
        military_retirement_pay = person("military_retirement_pay", period)
        military_service_income = person("military_service_income", period)

        filer_eligible = person("is_tax_unit_head", period)
        spouse_eligible = person("is_tax_unit_spouse", period)
        is_head_or_spouse = filer_eligible | spouse_eligible

        sd2_amount = max_(
            p.amount.capped_deduction[filing_status] * sd2_age_eligible
            + p.amount.increase * ssa_eligible
            - tax_unit.sum(
                (military_retirement_pay + military_service_income)
                * is_head_or_spouse
            ),
            0,
        )
        capped_pension_income = min_(
            tax_unit.sum(uncapped_pension_income), sd2_amount
        )

        # sd2_amount = where(
        #     total_eligible == 0,
        #     p.amount.non_qualifying[filing_status],
        #     where(
        #         total_eligible == 1,
        #         p.amount.single_qualifying[filing_status],
        #         p.amount.both_qualifying[filing_status],
        #     ),
        # )

        return where(sd2_age_eligible == 0, 0, capped_pension_income)
