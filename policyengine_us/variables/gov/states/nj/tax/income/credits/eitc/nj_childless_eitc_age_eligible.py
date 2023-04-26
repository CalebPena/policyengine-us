from policyengine_us.model_api import *


class nj_childless_eitc_age_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "New Jersey Eligible for EITC"
    definition_period = YEAR
    reference = "https://law.justia.com/codes/new-jersey/2022/title-54a/section-54a-4-7/"
    defined_for = StateCode.NJ

    def formula(tax_unit, period, parameters):
        # Return True if all federal EITC conditions are met, except with modified age paramaters and household has no children.

        # Check if filing status is separate.
        filing_status = tax_unit("filing_status", period)
        separate = filing_status == filing_status.possible_values.SEPARATE

        # Check if tax unit has any EITC qualifying children.
        person = tax_unit.members
        eitc_qualifying_child = person("is_eitc_qualifying_child", period)
        no_qualifying_children = tax_unit("eitc_child_count", period) == 0

        # Get the NJ EITC paramaeter tree.
        p = parameters(period).gov.states.nj.tax.income.credits.eitc

        # Check if the filer meets NJ EITC age requirements.
        age = person("age", period)
        min_age = p.eligibility.age.min
        max_age = p.eligibility.age.max
        meets_age_requirements = (age >= min_age) & (age <= max_age)
        is_filer = person("is_tax_unit_head", period)
        filer_age_eligible = (
            tax_unit.sum(is_filer & meets_age_requirements) > 0
        )

        return (
            ~separate
            & no_qualifying_children
            & filer_age_eligible
            & tax_unit("nj_eitc_income_eligible", period)
        )
