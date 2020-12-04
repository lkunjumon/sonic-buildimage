#############################################################################
# Target TG48M-P
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fan Drawer status which is available in the platform
#
#############################################################################

try:
    from sonic_platform_base.fan_drawer_base import FanDrawerBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class TargetFanDrawer(FanDrawerBase):
    def __init__(self, index):
        super(TargetFanDrawer, self).__init__()
        self._index = index + 1
        self._led = None

    def get_index(self):
        return self._index

    def get_led(self):
        return self._led


# For platforms with fan drawer(s)
class RealDrawer(TargetFanDrawer):
    def __init__(self, index):
        super(RealDrawer, self).__init__(index)
        self._name = 'drawer{}'.format(self._index)

    def get_name(self):
        return self._name


# For platforms with no physical fan drawer(s)
class VirtualDrawer(TargetFanDrawer):
    def __init__(self, index):
        super(VirtualDrawer, self).__init__(index)

    def get_name(self):
        return 'N/A'

    def set_status_led(self, color):
        return 'N/A'
