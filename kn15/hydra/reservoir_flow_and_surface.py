import re
from .hydra_lib import Error, is_not_empty, get_stage, get_flow, get_scale, valid_date, valid_time, valid_month
from .hydra_lib import WIND_DIRECTION_SCALE, WAVE_DIRECTION_SCALE, WATER_SURFACE_SCALE

GROUP_0 = r'966(?P<MM>\d{2})'
GROUP_1 = r'1(?P<group_1>\d{4}|/{4})'
GROUP_2 = r'2(?P<group_2>\d{4}|/{4})'
GROUP_3 = r'3(?P<group_3>\d{4}|/{4})'
GROUP_4 = r'4(?P<group_4>\d{4}|/{4})'
GROUP_5 = r'5(?P<group_5_YY>\d{2})(?P<group_5_GG>\d{2})'
GROUP_6 = r'6(?P<group_6_part_0>\d{2})(?P<group_6_part_1>\d{2})'
GROUP_7 = r'7(?P<group_7_part_0>\d)(?P<group_7_part_1>\d{2})(?P<group_7_part_2>\d)'
GROUP_8 = r'8(?P<group_8_YY>\d{2})(?P<group_8_GG>\d{2})'

SECTION_4 = f'^({GROUP_0})?(\s{GROUP_1})?(\s{GROUP_2})?(\s{GROUP_3})?\
(\s{GROUP_4})(\s{GROUP_5})?(\s{GROUP_6})?(\s{GROUP_7})?(\s{GROUP_8})?'


class FlowAndSurface:
    """Measured water flows; state of the surface of the lake, reservoir from Section 6"""

    def __init__(self, report):
        self._report = report
        self._MM = None
        self._stage = None
        self._flow = None
        self._area = None
        self._depth = None
        self._flow_YY = None
        self._flow_GG = None
        self._wind_direction = None
        self._wind_speed = None
        self._wave_direction = None
        self._wave_depth = None
        self._surface_condition = None
        self._surface_YY = None
        self._surface_GG = None
        self._parse()

    def _parse(self):
        report = self._report
        match = re.match(SECTION_4, report)
        if match is None:
            raise Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._MM = parsed.get('MM')
        self._stage = parsed.get('group_1')
        self._flow = parsed.get('group_2')
        self._area = parsed.get('group_3')
        self._depth = parsed.get('group_4')
        self._flow_YY = parsed.get('group_5_YY')
        self._flow_GG = parsed.get('group_5_GG')
        self._wind_direction = parsed.get('group_6_part_0')
        self._wind_speed = parsed.get('group_6_part_1')
        self._wave_direction = parsed.get('group_7_part_0')
        self._wave_depth = parsed.get('group_7_part_1')
        self._surface_condition = parsed.get('group_7_part_2')
        self._surface_YY = parsed.get('group_8_YY')
        self._surface_GG = parsed.get('group_8_GG')

    @property
    def month(self):
        if is_not_empty(self._MM):
            return valid_month(self._MM)
        else:
            return None

    @property
    def stage(self):
        if is_not_empty(self._stage):
            return get_stage(self._stage)
        else:
            return None

    @property
    def flow(self):
        if is_not_empty(self._flow):
            return get_flow(self._flow)
        else:
            return None

    @property
    def area(self):
        if is_not_empty(self._area):
            return get_flow(self._area)
        else:
            return None

    @property
    def depth(self):
        if is_not_empty(self._depth):
            return int(self._depth)
        else:
            return None

    @property
    def flow_measure_day(self):
        if is_not_empty(self._flow_YY):
            return valid_date(self._flow_YY)
        else:
            return None

    @property
    def flow_measure_time(self):
        if is_not_empty(self._flow_GG):
            return valid_time(self._flow_GG)
        else:
            return None

    @property
    def wind_direction(self, verbose=True):
        if is_not_empty(self._wind_direction):
            return get_scale(self._wind_direction, WIND_DIRECTION_SCALE, verbose=verbose)
        else:
            return None

    @property
    def wind_speed(self):
        if is_not_empty(self._wind_speed):
            return int(self._wind_speed)
        else:
            return None

    @property
    def wave_direction(self, verbose=True):
        if is_not_empty(self._wave_direction):
            return get_scale(self._wave_direction, WAVE_DIRECTION_SCALE, verbose=verbose)
        else:
            return None

    @property
    def wave_depth(self):
        if is_not_empty(self._wave_depth):
            return int(self._wave_depth)
        else:
            return None

    @property
    def surface_condition(self, verbose=False):
        if is_not_empty(self._surface_condition):
            return get_scale(self._wave_direction, WATER_SURFACE_SCALE, verbose=verbose)
        else:
            return None

    @property
    def surface_obser_day(self):
        if is_not_empty(self._surface_YY):
            return valid_date(self._surface_YY)
        else:
            return None

    @property
    def surface_obser_time(self):
        if is_not_empty(self._surface_GG):
            return valid_time(self._surface_GG)
        else:
            return None


    def decode_flow(self):
        output = {}
        if self.month is not None:
            output['measure_month'] = self.month
        if self.stage is not None:
            output['stage'] = self.stage
        if self.flow is not None:
            output['discharge'] = self.flow
        if self.area is not None:
            output['cross-sectional_area'] = self.area
        if self.depth is not None:
            output['max_water_depth'] = self.depth
        if self.flow_measure_day is not None:
            output['measure_day'] = self.flow_measure_day
        if self.flow_measure_time is not None:
            output['measure_synophour'] = self.flow_measure_time

        return output

    def decode_surface(self):
        output = {}
        if self.month is not None:
            output['measure_month'] = self.month
        if self.wind_direction is not None:
            output['reservoir_wind_direction'] = self.wind_direction
        if self.wind_speed is not None:
            output['reservoir_wind_speed'] = self.wind_speed
        if self.wave_direction is not None:
            output['reservoir_wave_direction'] = self.wave_direction
        if self.wave_depth is not None:
            output['reservoir_wave_depth'] = self.wave_depth
        if self.surface_condition is not None:
            output['reservoir_water_surface_condition'] = self.surface_condition
        if self.surface_obser_day is not None:
            output['measure_day'] = self.surface_obser_day
        if self.surface_obser_time is not None:
            output['measure_synophour'] = self.surface_obser_time

        return output
