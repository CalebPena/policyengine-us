from policyengine_us.model_api import *


class mi_standard_deduction_tier_three(Variable):
    value_type = float
    entity = TaxUnit
    label = "Michigan standard deduction"
    unit = USD
    definition_period = YEAR
    reference = (
        "http://legislature.mi.gov/doc.aspx?mcl-206-30",
        "https://www.michigan.gov/taxes/iit/retirement-and-pension-benefits/michigan-standard-deduction",
        "https://www.michigan.gov/taxes/-/media/Project/Websites/taxes/Forms/2022/2022-IIT-Forms/BOOK_MI-1040.pdf#page=16",
    )
    defined_for = "mi_standard_deduction_tier_three_eligible"

    def formula(tax_unit, period, parameters):
        # Part 9 (c) - a person born in 1946 through 1952 and
        # beginning January 1, 2018 for a person born after 1945 who has retired as of January 1, 2013,
        # the sum of the deductions under subsection (1)(f)(i), (ii), and (iv) is limited to $35,000.00 for a single return
        # and, except as otherwise provided under this subdivision, $55,000.00 for a joint return
        p = parameters(
            period
        ).gov.states.mi.tax.income.deductions.standard.tier_three
        # Core deduction based on filing status.
        filing_status = tax_unit("filing_status", period)

        person = tax_unit.members
        uncapped_pension_income = person("taxable_pension_income", period)
        military_retirement_pay = person("military_retirement_pay", period)
        military_service_income = person("military_service_income", period)
        taxable_social_security = person("taxable_social_security", period)
        mi_exemptions = tax_unit("mi_exemptions", period)

        filer_eligible = person("is_tax_unit_head", period)
        spouse_eligible = person("is_tax_unit_spouse", period)
        is_head_or_spouse = filer_eligible | spouse_eligible

        reductions = (
            tax_unit.sum(
                (
                    military_retirement_pay
                    + military_service_income
                    + taxable_social_security
                )
                * is_head_or_spouse
            )
            + mi_exemptions
        )
        sd3_amount = max_(
            p.amount[filing_status] - reductions,
            0,
        )

        return min_(tax_unit.sum(uncapped_pension_income), sd3_amount)
