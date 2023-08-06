from hestia_earth.schema import PracticeStatsDefinition, TermTermType
from hestia_earth.utils.model import find_primary_product

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.practice import _new_practice
from hestia_earth.models.utils.crop import is_orchard
from .utils import get_region_factor
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "products": [{
            "@type": "Product",
            "primary": "True",
            "term.termType": "crop"
        }],
        "site": {
            "@type": "Site",
            "or": [
                {"region": {"@type": "Term"}},
                {"country": {"@type": "Term"}}
            ]
        }
    }
}
RETURNS = {
    "Practice": [{
        "value": "",
        "statsDefinition": "spatial"
    }]
}
LOOKUPS = {
    "crop": "isOrchard",
    "region-landUseManagement": "longFallowRatio"
}
TERM_ID = 'longFallowRatio'


def _practice(value: float):
    practice = _new_practice(TERM_ID)
    practice['value'] = [round(value, 7)]
    practice['statsDefinition'] = PracticeStatsDefinition.SPATIAL.value
    return practice


def _run(cycle: dict):
    site = cycle.get('site')
    region_factor = get_region_factor(TERM_ID, site, TermTermType.LANDUSEMANAGEMENT)

    logRequirements(site, model=MODEL, term=TERM_ID,
                    region_factor=region_factor)

    should_run = all([region_factor])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return [_practice(region_factor)] if should_run else []


def _should_run(cycle: dict):
    product = find_primary_product(cycle) or {}
    not_orchard_crop = not is_orchard(MODEL, product.get('term', {}).get('@id'))

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    not_orchard_crop=not_orchard_crop)

    should_run = all([not_orchard_crop])
    logShouldRun(cycle, MODEL, TERM_ID, should_run)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else []
