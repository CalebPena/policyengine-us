from policyengine_us.model_api import *


class ri_standard_deduction_phase_out(Variable):
    value_type = float
    entity = TaxUnit
    label = "Rhode Island standard deduction phase out"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://tax.ri.gov/sites/g/files/xkgbur541/files/2021-11/2021-tax-rate-and-worksheets.pdf"
        "https://tax.ri.gov/sites/g/files/xkgbur541/files/2022-12/2022%20Tax%20Rate%20and%20Worksheets.pdf"
    )
    defined_for = StateCode.RI

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.ri.tax.income.deductions.standard.phase_out

        agi = tax_unit("ri_agi", period)

        excess_agi = agi - p.start

        excess_agi_step = excess_agi / p.increment

        return p.percentage.calc(excess_agi_step)
