import re
from .hydra_lib import Error, is_not_empty, get_stage, get_flow, get_identify_param, valid_date, valid_time
from .hydra_lib import PERIODS

GROUP_0 = r'933(?P<period>\d{2})'
GROUP_1 = r'1(?P<group_1>\d{4}|/{4})'
GROUP_2 = r'2(?P<group_2>\d{4}|/{4})'
GROUP_3 = r'3(?P<group_3>\d{4}|/{4})'
GROUP_4 = r'4(?P<group_4>\d{4}|/{4})'
GROUP_5 = r'5(?P<group_5>\d{4}|/{4})'
GROUP_6 = r'6(?P<group_6>\d{4}|/{4})'
GROUP_7 = r'7(?P<YY>\d{2})(?P<GG>\d{2})'

SECTION_3 = f'^({GROUP_0})?(\s{GROUP_1})?(\s{GROUP_2})?(\s{GROUP_3})?\
(\s{GROUP_4})?(\s{GROUP_5})?(\s{GROUP_6})?(\s{GROUP_7})?'


class StageAndFlow:
    """Average, higher and lowest levels and flows per day, decade, month and other periods
    from Section 3"""

    def __init__(self, report):
        self._report = report
        self._period = None
        self._avg_stage = None
        self._max_stage = None
        self._min_stage = None
        self._avg_flow = None
        self._max_flow = None
        self._min_flow = None
        self._YY = None
        self._GG = None
        self._parse()

    def _parse(self):
        report = self._report
        match = re.match(SECTION_3, report)
        if match is None:
            raise Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._period = parsed.get('period')
        self._avg_stage = parsed.get('group_1')
        self._max_stage = parsed.get('group_2')
        self._min_stage = parsed.get('group_3')
        self._avg_flow = parsed.get('group_4')
        self._max_flow = parsed.get('group_5')
        self._min_flow = parsed.get('group_6')
        self._YY = parsed.get('YY')
        self._GG = parsed.get('GG')


    @property
    def period(self, verbose=True):
        if is_not_empty(self._period):
            return get_identify_param(self._period, PERIODS, verbose=verbose)
        else:
            return None

    @property
    def avg_stage(self):
        if is_not_empty(self._avg_stage):
            return get_stage(self._avg_stage)
        else:
            return None

    @property
    def max_stage(self):
        if is_not_empty(self._max_stage):
            return get_stage(self._max_stage)
        else:
            return None

    @property
    def min_stage(self):
        if is_not_empty(self._min_stage):
            return get_stage(self._min_stage)
        else:
            return None

    @property
    def avg_flow(self):
        if is_not_empty(self._avg_flow):
            return get_flow(self._avg_flow)
        else:
            return None

    @property
    def max_flow(self):
        if is_not_empty(self._max_flow):
            return get_flow(self._max_flow)
        else:
            return None

    @property
    def min_flow(self):
        if is_not_empty(self._min_flow):
            return get_flow(self._min_flow)
        else:
            return None

    @property
    def day_of_max(self):
        if is_not_empty(self._YY):
            return valid_date(self._YY)

    @property
    def time_of_max(self):
        if is_not_empty(self._GG):
            return valid_time(self._GG)

    def decode(self):
        output = {}
        if self.period is None:
            raise Error(f'Identify parameter is empty')
        output['period'] = self.period
        if self.avg_stage is not None:
            output['avg_stage'] = self.avg_stage
        if self.max_stage is not None:
            output['max_stage'] = self.max_stage
        if self.min_stage is not None:
            output['min_stage'] = self.min_stage
        if self.avg_stage is not None:
            output['avg_discharge'] = self.avg_flow
        if self.max_flow is not None:
            output['max_discharge'] = self.max_flow
        if self.min_flow is not None:
            output['min_discharge'] = self.min_flow
        if self.day_of_max is not None:
            output['day_of_max'] = self.day_of_max
            output['hour_of_max'] = self.time_of_max

        return output
