from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.pesticideAI import impact_lookup_value, impact_value_set_none
from . import MODEL

REQUIREMENTS = {
    "ImpactAssessment": {
        "cycle": {
            "@type": "Cycle",
            "completeness.pesticideVeterinaryDrug": "True",
            "inputs": [{"@type": "Input", "value": "", "term.termType": "pesticideAI"}]
        }
    }
}
RETURNS = {
    "Indicator": {
        "value": ""
    }
}
LOOKUPS = {
    "pesticideAI": "dalyAllEffectsInfiniteCancerogenicHumanToxicityDamageToHumanHealthLCImpact"
}
TERM_ID = 'damageToHumanHealthHumanToxicityCancerogenic'


def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    return indicator


def run(impact_assessment: dict):
    value = impact_lookup_value(MODEL, TERM_ID, impact_assessment, LOOKUPS['pesticideAI'])
    should_run = any([value is not None, impact_value_set_none(impact_assessment)])
    return _indicator(value) if should_run else None
