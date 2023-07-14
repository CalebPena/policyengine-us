from policyengine_us.model_api import *


class nm_agi(Variable):
    value_type = float
    entity = TaxUnit
    label = "New Mexico modified gross income"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.NM
    reference = "https://klvg4oyd4j.execute-api.us-west-2.amazonaws.com/prod/PublicFiles/34821a9573ca43e7b06dfad20f5183fd/856ebf4b-3814-49dd-8631-ebe579d6a42b/Personal%20Income%20Tax.pdf"  # p63
