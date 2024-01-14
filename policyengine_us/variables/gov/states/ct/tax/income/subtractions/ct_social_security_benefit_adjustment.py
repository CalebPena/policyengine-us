from policyengine_us.model_api import *


class ct_social_security_benefit_adjustment(Variable):
    value_type = float
    entity = TaxUnit
    unit = USD
    label = "Connecticut social security benefit adjustment"
    reference = (
        # Connecticut General Statutes, Chapter 229, Sec. 12-701, (20), (b), (x), (iii) and (iv)
        "https://www.cga.ct.gov/current/pub/chap_229.htm#sec_12-701"
        # 2022 Form CT-1040 Connecticut Resident Income Tax Return Instructions
        "https://portal.ct.gov/-/media/DRS/Forms/2022/Income/2022-CT-1040-Instructions_1222.pdf#page=24"
    )
    definition_period = YEAR
    defined_for = StateCode.CT

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.ct.tax.income.subtractions
        filing_status = tax_unit("filing_status", period)
        # Line 41, Part A and Part B
        us_taxable_ss = tax_unit("tax_unit_taxable_social_security", period)
        ss_rate = p.social_security.rate.social_security
        ss_fraction = us_taxable_ss * ss_rate
        excess = tax_unit(
            "ct_social_security_benefit_adjustment_magi_excess", period
        )
        # Line 41, Part C and Part D
        # Lesser of 25% of MAGI excess and 25% of taxable social security benefits
        magi_rate = p.magi_excess
        capped_ss_fraction = min_(ss_fraction, magi_rate * excess)

        agi = tax_unit("adjusted_gross_income", period)
        # Line 41, Part E and Part F
        # Difference between taxable social security benefits and capped social security fraction
        adjusted_ss_benefit = max_(us_taxable_ss - capped_ss_fraction, 0)
        reduction_threshold = p.social_security.reduction_threshold[
            filing_status
        ]
        # Adjustment determined based on AGI amount compared to reduction threshold
        agi_under_reduction_threshold = agi < reduction_threshold
        return where(
            agi_under_reduction_threshold, us_taxable_ss, adjusted_ss_benefit
        )
