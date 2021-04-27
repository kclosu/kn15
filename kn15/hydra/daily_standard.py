import re
from .hydra_lib import Error, is_not_empty, valid_date, get_stage, get_flow, get_conditions, get_scale, get_amount,\
    get_status
from .hydra_lib import ICE_CONDITIONS, WATER_CONDITIONS, SNOW_DEPTH_SCALE, PRECIPITATION_DURATION_SCALE, MODE_GROUPS,\
    ICE_CONDITION_MATCHS, WATER_CONDITION_MATCHS

GROUP_1 = r'1(?P<group_1>\d{4}|/{4})'
GROUP_2 = r'2(?P<group_2>\d{4}|/{4})'
GROUP_3 = r'3(?P<group_3>\d{4}|/{4})'
GROUP_4 = r'4(?P<group_4_part_0>\d{2}|/{2})(?P<group_4_part_1>\d{2}|/{2})'
GROUP_5 = r'5(?P<group_5>\d{4}|/{4})'
GROUP_6 = r'6(?P<group_6>\d{4}|/{4})'
GROUP_7 = r'7(?P<group_7_part_0>\d{3}|/{3})(?P<group_7_part_1>\d|/)'
GROUP_8 = r'8(?P<group_8>\d{4}|/{4})'
GROUP_9 = r'9(?P<group_9_part_0>\d{3}|/{3})(?P<group_9_part_1>\d|/)'
GROUP_0 = r'0(?P<group_0_part_0>\d{3}|/{3})(?P<group_0_part_1>\d|/)'

STANDARD_OBSERVATION = f'^(\s?{GROUP_1})?(\s?{GROUP_2})?(\s?{GROUP_3})?(\s?{GROUP_4})?(\s?{GROUP_5})*(\s?{GROUP_6})*\
(\s?{GROUP_7})?(\s?{GROUP_8})?(\s?{GROUP_9})?(\s?{GROUP_0})?'

class StandardObservation:
    """Data of daily standard single-term observations at the hydrological station for the current day
     from Section 1 or for one or several past days from Section 2 """

    def __init__(self, report):
        self._report = report
        self._YY = None
        self._stage = None
        self._change_stage = None
        self._prev_stage = None
        self._water_temp = None
        self._air_temp = None
        self._ice_conditions = []
        self._water_conditions = []
        self._ice_thickness = None
        self._snow_depth = None
        self._flow = None
        self._precip_amount_half = None
        self._precip_duration_half = None
        self._precip_amount = None
        self._precip_duration = None
        self._parse()

    def _parse(self):
        report = self._report
        if re.match(r'922(\d{2})(\s.*)', self._report):
            self._YY = self._report[3:5]
            report = self._report[6:]
        match = re.match(STANDARD_OBSERVATION, report)
        if match is None:
            raise Error("Couldn't parse standard observation with regular expression")
        parsed = match.groupdict()
        self._stage = parsed.get('group_1')
        self._change_stage = parsed.get('group_2')
        self._prev_stage = parsed.get('group_3')
        self._water_temp = parsed.get('group_4_part_0')
        self._air_temp = parsed.get('group_4_part_1')
        self._ice_conditions = re.findall(GROUP_5, report)
        self._water_conditions = re.findall(GROUP_6, report)
        self._ice_thickness = parsed.get('group_7_part_0')
        self._snow_depth = parsed.get('group_7_part_1')
        self._flow = parsed.get('group_8')
        self._precip_amount_half = parsed.get('group_9_part_0')
        self._precip_duration_half = parsed.get('group_9_part_1')
        self._precip_amount = parsed.get('group_0_part_0')
        self._precip_duration = parsed.get('group_0_part_1')

    @property
    def stage(self):
        """Return 'stage' from Group_1"""
        if is_not_empty(self._stage):
            return get_stage(self._stage)
        else:
            return None

    @property
    def change_stage(self):
        if is_not_empty(self._change_stage):
            sing = int(self._change_stage[-1])
            change_stage = int(self._change_stage[:-1])
            if sing == 0:
                return 0
            if sing == 1:
                return change_stage
            if sing == 2:
                return change_stage * -1
            else:
                raise Error(f'Incorrect format in block: 2{self._change_stage}')
        else:
            return None

    @property
    def previous_stage(self):
        """Return 'stage' from Group_3 """
        if is_not_empty(self._prev_stage):
            return get_stage(self._prev_stage)
        else:
            return None

    @property
    def water_temperature(self):
        """Work incorrect.
        Instruction does not explain different between 1 and 10 in code '10'"""
        if is_not_empty(self._water_temp):
            if self._air_temp is not None and self._air_temp == '99':
                return int(self._water_temp)
            else:
                return int(self._water_temp) / 10
        else:
            return None

    @property
    def air_temperature(self):
        if self._air_temp is not None and self._air_temp not in ('//', '99'):
            air_temp = int(self._air_temp)
            return air_temp if air_temp < 50 else (50 - air_temp)
        else:
            return None

    @property
    def ice_conditions(self, verbose=True):
        if len(self._ice_conditions) == 0:
            return None
        conditions = get_conditions(self._ice_conditions, ICE_CONDITIONS, verbose=verbose)
        return conditions if len(conditions) > 0 else None

    @property
    def water_conditions(self, verbose=True):
        if len(self._water_conditions) == 0:
            return None
        conditions = get_conditions(self._water_conditions, WATER_CONDITIONS, verbose=verbose)
        return conditions if len(conditions) > 0 else None

    @property
    def ice_thickness(self):
        if is_not_empty(self._ice_thickness):
            return int(self._ice_thickness)
        else:
            return None

    @property
    def snow_depth(self, verbose=True):
        if is_not_empty(self._snow_depth):
            return get_scale(self._snow_depth, SNOW_DEPTH_SCALE, verbose=verbose)
        else:
            return None

    @property
    def daily_flow(self):
        if is_not_empty(self._flow):
            return get_flow(self._flow)
        else:
            return None

    @property
    def precipitation_duration_half(self, verbose=True):
        if is_not_empty(self._precip_duration_half):
            return get_scale(self._precip_duration_half, PRECIPITATION_DURATION_SCALE[:-1], verbose=verbose)
        else:
            return None

    @property
    def precipitation_amount_half(self, verbose=False):
        if is_not_empty(self._precip_amount_half):
            return get_amount(self._precip_amount_half, verbose=verbose)
        else:
            return None

    @property
    def precipitation_duration(self, verbose=True):
        if is_not_empty(self._precip_duration):
            return get_scale(self._precip_duration, PRECIPITATION_DURATION_SCALE, verbose=verbose)
        else:
            return None

    @property
    def precipitation_amount(self, verbose=False):
        if is_not_empty(self._precip_amount):
            return get_amount(self._precip_amount, verbose=verbose)
        else:
            return None

    @property
    def water_status(self, verbose=False):
        key = 'water_code_status'
        if verbose:
            key = 'water_status'
        water_status = {key: []}
        if len(self._ice_conditions) != 0:
            water_status[key].extend(get_status(self._ice_conditions, ICE_CONDITION_MATCHS, MODE_GROUPS, verbose=verbose))
        if len(self._water_conditions) != 0:
            water_status[key].extend(get_status(self._water_conditions, WATER_CONDITION_MATCHS, MODE_GROUPS, verbose=verbose))
        if water_status == {key: []}:
            return None
        return water_status

    def decode(self):

        output = {}
        if self.stage is not None:
            output['stage'] = self.stage
        if self.change_stage is not None:
            output['change_stage'] = self.change_stage
        if self.previous_stage is not None:
            output['previous_stage'] = self.previous_stage
        if self.water_temperature is not None:
            output['water_temperature'] = self.water_temperature
        if self.air_temperature is not None:
            output['air_temperature'] = self.air_temperature
        if self.ice_conditions is not None:
            output['ice_conditions'] = self.ice_conditions
        if self.water_conditions is not None:
            output['water_conditions'] = self.water_conditions
        if self.ice_thickness is not None:
            output['ice_thickness'] = self.ice_thickness
        if self.snow_depth is not None:
            output['snow_depth'] = self.snow_depth
        if self.daily_flow is not None:
            output['discharge'] = self.daily_flow
        if self.precipitation_duration_half is not None:
            output['precipitation_duration_by_half_day'] = self.precipitation_duration_half
        if self.precipitation_amount_half is not None:
            output['precipitation_amount_by_half_day'] = self.precipitation_amount_half
        if self.precipitation_duration is not None:
            output['precipitation_duration'] = self.precipitation_duration
        if self.precipitation_amount is not None:
            output['precipitation_amount'] = self.precipitation_amount
        if self.water_status is not None:
            output.update(self.water_status)

        return output, valid_date(self._YY)
