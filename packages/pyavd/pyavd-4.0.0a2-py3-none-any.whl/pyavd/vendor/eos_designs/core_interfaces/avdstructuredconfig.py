from pyavd.vendor.avdfacts import AvdFacts

from .ethernet_interfaces import EthernetInterfacesMixin
from .port_channel_interfaces import PortChannelInterfacesMixin
from .router_bgp import RouterBgpMixin
from .router_ospf import RouterOspfMixin


class AvdStructuredConfigCoreInterfaces(
    AvdFacts,
    EthernetInterfacesMixin,
    PortChannelInterfacesMixin,
    RouterBgpMixin,
    RouterOspfMixin,
):
    """
    The AvdStructuredConfig Class is imported by "get_structured_config" to render parts of the structured config.

    "get_structured_config" imports, instantiates and run the .render() method on the class.
    .render() runs all class methods not starting with _ and of type @cached property and inserts the returned data into
    a dict with the name of the method as key. This means that each key in the final dict corresponds to a method.

    The Class uses AvdFacts, as the base class, to inherit the render, _hostvars, keys and other attributes.
    All other methods are included as "Mixins" to make the files more managable.

    The order of the @cached_properties methods imported from Mixins will also control the order in the output.
    """
