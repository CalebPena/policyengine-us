from policyengine_us.model_api import *
from policyengine_us.variables.gov.ed.pell_grant.pell_grant_formula import PellGrantFormula
from policyengine_us.variables.gov.ed.pell_grant.sai.eligibility_type.pell_grant_eligibility_type import (
    PellGrantEligibilityType,
)


class pell_grant_sai(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
    label = "Pell Grant student aid index"

    def formula(person, period, parameters):
        head_contribution = person("pell_grant_head_contribution", period)
        dependent_contribution = person("pell_grant_dependent_contribution", period)
        formula = person("pell_grant_formula", period)
        eligibility_type = person("pell_grant_eligibility_type", period)
        max_eligible = eligibility_type == PellGrantEligibilityType.MAXIMUM
        p = parameters(period).gov.ed.pell_grant.sai
        min_sai = p.limits.min_sai
        max_sai = 0 if max_eligible else p.limits.max_sai

        unbound = select(
            [
                formula == PellGrantFormula.A,
                formula == PellGrantFormula.B,
                formula == PellGrantFormula.C,
            ],
            [
                head_contribution + dependent_contribution,
                head_contribution,
                head_contribution,
            ],
        )

        return max_(min_(unbound, max_sai), min_sai)
