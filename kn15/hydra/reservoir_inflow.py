import re
from .hydra_lib import Error, is_not_empty, get_flow, valid_date

GROUP_0 = r'955(?P<YY>\d{2})'
GROUP_1 = r'1(?P<group_1>\d{4}|/{4})'
GROUP_2 = r'2(?P<group_2>\d{4}|/{4})'
GROUP_3 = r'3(?P<group_3>\d{4}|/{4})'
GROUP_4 = r'4(?P<group_4>\d{4}|/{4})'
GROUP_5 = r'5(?P<group_5>\d{4}|/{4})'
GROUP_6 = r'6(?P<group_6>\d{4}|/{4})'
GROUP_7 = r'7(?P<group_7>\d{4}|/{4})'

SECTION_5 = f'^({GROUP_0})?(\s{GROUP_1})?(\s{GROUP_2})?(\s{GROUP_3})?\
(\s{GROUP_4})(\s{GROUP_5})?(\s{GROUP_6})?(\s{GROUP_7})?'


class Inflow:
    """Water inflow into reservoirs from Section 5"""

    def __init__(self, report):
        self._report = report
        self._YY = None
        self._total_inflow = None
        self._side_inflow = None
        self._water_area_inflow = None
        self._prev_total_inflow = None
        self._prev_side_inflow = None
        self._prev_water_area_inflow = None
        self._water_discharge = None
        self._parse()

    def _parse(self):
        report = self._report
        match = re.match(SECTION_5, report)
        if match is None:
            raise Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._YY = parsed.get('YY')
        self._total_inflow = parsed.get('group_1')
        self._side_inflow = parsed.get('group_2')
        self._water_area_inflow = parsed.get('group_3')
        self._prev_total_inflow = parsed.get('group_4')
        self._prev_side_inflow = parsed.get('group_5')
        self._prev_water_area_inflow = parsed.get('group_6')
        self._water_discharge = parsed.get('group_7')

    @property
    def total_inflow(self):
        if is_not_empty(self._total_inflow):
            return get_flow(self._total_inflow)
        else:
            return None

    @property
    def side_inflow(self):
        if is_not_empty(self._side_inflow):
            return get_flow(self._side_inflow)
        else:
            return None

    @property
    def water_area_inflow(self):
        if is_not_empty(self._water_area_inflow):
            return get_flow(self._water_area_inflow)
        else:
            return None

    @property
    def prev_total_inflow(self):
        if is_not_empty(self._prev_total_inflow):
            return get_flow(self._prev_total_inflow)
        else:
            return None

    @property
    def prev_side_inflow(self):
        if is_not_empty(self._prev_side_inflow):
            return get_flow(self._prev_side_inflow)
        else:
            return None

    @property
    def prev_water_area_inflow(self):
        if is_not_empty(self._prev_water_area_inflow):
            return get_flow(self._prev_water_area_inflow)
        else:
            return None

    @property
    def water_discharge(self):
        if is_not_empty(self._water_discharge):
            return get_flow(self._water_discharge)
        else:
            return None

    def decode(self):
        output = {}
        if self.total_inflow is not None:
            output['reservoir_total_inflow'] = self.total_inflow
        if self.side_inflow is not None:
            output['reservoir_side_inflow'] = self.side_inflow
        if self.water_area_inflow is not None:
            output['reservoir_water_area_inflow'] = self.water_area_inflow
        if self.prev_total_inflow is not None:
            output['reservoir_sum_previous_total_inflow'] = self.prev_total_inflow
        if self.prev_side_inflow is not None:
            output['reservoir_sum_previous_side_inflow'] = self.prev_side_inflow
        if self.prev_water_area_inflow is not None:
            output['reservoir_sum_previous_water_area_inflow'] = self.prev_water_area_inflow
        if self.water_discharge is not None:
            output['reservoir_water_discharge'] = self.water_discharge

        return output, valid_date(self._YY)
