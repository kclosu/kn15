import re
from .hydra_lib import Error, is_not_empty, get_stage, get_flow, valid_date

GROUP_0 = r'944(?P<YY>\d{2})'
GROUP_1 = r'1(?P<group_1>\d{4}|/{4})'
GROUP_2 = r'2(?P<group_2>\d{4}|/{4})'
GROUP_3 = r'3(?P<group_3>\d{4}|/{4})'
GROUP_4 = r'4(?P<group_4>\d{4}|/{4})'
GROUP_5 = r'5(?P<group_5>\d{4}|/{4})'
GROUP_6 = r'6(?P<group_6>\d{4}|/{4})'
GROUP_7 = r'7(?P<group_7>\d{4}|/{4})'
GROUP_8 = r'8(?P<group_8>\d{4}|/{4})'

SECTION_4 = f'^({GROUP_0})?(\s?{GROUP_1})?(\s?{GROUP_2})?(\s?{GROUP_3})?\
(\s?{GROUP_4})(\s?{GROUP_5})?(\s?{GROUP_6})?(\s?{GROUP_7})?(\s?{GROUP_8})?'


class StageAndVolume:
    """Reservoir levels and volumes from Section 4 """

    def __init__(self, report):
        self._report = report
        self._YY = None
        self._up_stage = None
        self._avg_stage = None
        self._prev_avg_stage = None
        self._down_stage = None
        self._max_down_stage = None
        self._min_down_stage = None
        self._volume = None
        self._prev_volume = None
        self._parse()

    def _parse(self):
        report = self._report
        match = re.match(SECTION_4, report)
        if match is None:
            raise Error("Couldn't parse section 4 with regular expression")
        parsed = match.groupdict()
        self._YY = parsed.get('YY')
        self._up_stage = parsed.get('group_1')
        self._avg_stage = parsed.get('group_2')
        self._prev_avg_stage = parsed.get('group_3')
        self._down_stage = parsed.get('group_4')
        self._max_down_stage = parsed.get('group_5')
        self._min_down_stage = parsed.get('group_6')
        self._volume = parsed.get('group_7')
        self._prev_volume = parsed.get('group_8')

    @property
    def up_stage(self):
        if is_not_empty(self._up_stage):
            return get_stage(self._up_stage)
        else:
            return None

    @property
    def avg_stage(self):
        if is_not_empty(self._avg_stage):
            return get_stage(self._avg_stage)
        else:
            return None

    @property
    def prev_avg_stage(self):
        if is_not_empty(self._prev_avg_stage):
            return get_stage(self._prev_avg_stage)
        else:
            return None

    @property
    def down_stage(self):
        if is_not_empty(self._down_stage):
            return get_stage(self._down_stage)
        else:
            return None

    @property
    def max_down_stage(self):
        if is_not_empty(self._max_down_stage):
            return get_stage(self._max_down_stage)
        else:
            return None

    @property
    def min_down_stage(self):
        if is_not_empty(self._min_down_stage):
            return get_stage(self._min_down_stage)
        else:
            return None

    @property
    def volume(self):
        if is_not_empty(self._volume):
            return get_flow(self._volume)
        else:
            return None

    @property
    def prev_volume(self):
        if is_not_empty(self._prev_volume):
            return get_flow(self._prev_volume)
        else:
            return None

    def decode(self):
        output = {}
        if self.up_stage is not None:
            output['reservoir_upstream_stage'] = self.up_stage
        if self.avg_stage is not None:
            output['reservoir_avg_stage'] = self.avg_stage
        if self.prev_avg_stage is not None:
            output['reservoir_previous_avg_stage'] = self.prev_avg_stage
        if self.down_stage is not None:
            output['reservoir_downstream_stage'] = self.down_stage
        if self.max_down_stage is not None:
            output['reservoir_max_downstream_stage'] = self.max_down_stage
        if self.min_down_stage is not None:
            output['reservoir_min_downstream_stage'] = self.min_down_stage
        if self.volume is not None:
            output['reservoir_volume'] = self.volume
        if self.prev_volume is not None:
            output['reservoir_previous_volume'] = self.prev_volume

        return output, valid_date(self._YY)
