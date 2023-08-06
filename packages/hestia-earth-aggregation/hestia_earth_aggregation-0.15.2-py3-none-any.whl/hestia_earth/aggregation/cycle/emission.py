from hestia_earth.schema import EmissionJSONLD, EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version
from hestia_earth.aggregation.utils.term import METHOD_MODEL
from hestia_earth.aggregation.utils.emission import is_in_system_boundary


def _new_emission(term: dict, value: float = None):
    # only add emissions included in the System Boundary
    if is_in_system_boundary(term.get('@id')):
        node = EmissionJSONLD().to_dict()
        node['term'] = linked_node(term)
        if value is not None:
            node['value'] = [value]
            node['statsDefinition'] = EmissionStatsDefinition.CYCLES.value
        node['methodModel'] = METHOD_MODEL
        node['methodTier'] = EmissionMethodTier.TIER_1.value
        return _aggregated_version(node, 'term', 'statsDefinition', 'value', 'methodModel', 'methodTier')
