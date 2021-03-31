import re
from .hydra_lib import Error, is_not_empty, valid_date, get_stage, get_flow, get_conditions, get_duration, get_amount
from .hydra_lib import ICE_CONDITIONS, WATER_CONDITIONS, SNOW_DEPTH_SCALE, PRECIPITATION_DURATION_SCALE

STAGE = r'1(?P<stage>\d{4}|/{4})'
CHANGE_STAGE = r'2(?P<change_stage>\d{3}|/{3})(?P<change_stage_sign>\d|/)'
PREVIOUS_STAGE = r'3(?P<prev_stage>\d{4}|/{4})'
TEMPERATURE = r'4(?P<water_temp>\d{2})(?P<air_temp>\d{2}|/{2})'
ICE = r'5(?P<ice>\d{4})'
WATER = r'6(?P<water_condition>\d{4})'
ICE_THICKNESS = r'7(?P<ice_thickness>\d{3})(?P<snow_depth>\d)'
DISCHARGE = r'8(?P<discharge_integer_part>\d)(?P<discharge>\d{3})'
PRECIPITATION_HALF_DAY = r'9(?P<precip_amount_half>\d{3}|/{3})(?P<precip_duration_half>\d|/)'
PRECIPITATION_DAY = r'0(?P<precip_amount>\d{3}|/{3})(?P<precip_duration>\d|/)'

STANDARD_OBSERVATION = f'^({STAGE})?(\s{CHANGE_STAGE})?(\s{PREVIOUS_STAGE})?(\s{TEMPERATURE})?(\s{ICE})*\
(\s{WATER})*(\s{ICE_THICKNESS})?(\s{DISCHARGE})?(\s{PRECIPITATION_HALF_DAY})?(\s{PRECIPITATION_DAY})?'



class StandardObservation():

    def __init__(self, report):
        self._report = report
        self._YY = None
        self._stage = None
        self._change_stage = None
        self._change_stage_sign = None
        self._prev_stage = None
        self._water_temp = None
        self._air_temp = None
        self._ice_conditions = []
        self._water_conditions = []
        self._ice_thickness = None
        self._snow_depth = None
        self._discharge_integer_part = None
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
            raise KN15Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._stage = parsed.get('stage')
        self._change_stage = parsed.get('change_stage')
        self._change_stage_sign = parsed.get('change_stage_sign')
        self._prev_stage = parsed.get('prev_stage')
        self._water_temp = parsed.get('water_temp')
        self._air_temp = parsed.get('air_temp')
        self._ice_conditions = re.findall(ICE, report)
        self._water_conditions = re.findall(WATER, report)
        self._ice_thickness = parsed.get('ice_thickness')
        self._snow_depth = parsed.get('snow_depth')
        self._flow_integer_part = parsed.get('discharge_integer_part')
        self._flow = parsed.get('discharge')
        self._precip_amount_half = parsed.get('precip_amount_half')
        self._precip_duration_half = parsed.get('precip_duration_half')
        self._precip_amount = parsed.get('precip_amount')
        self._precip_duration = parsed.get('precip_duration')

    @property
    def stage(self):
        """Return 'stage' from Group_1"""
        if is_not_empty(self._stage):
            return get_stage(self._stage)
        else:
            return None

    @property
    def change_stage(self):
        if is_not_empty(self._change_stage_sign):
            sing = int(self._change_stage_sign)
            if sing == 0:
                return 0
            if is_not_empty(self._change_stage) and sing == 1:
                return int(self._change_stage)
            if is_not_empty(self._change_stage) and sing == 2:
                return int(self._change_stage) * -1
            else:
                raise Error(f'Incorrect format in block: 2{self._change_stage}{sing}')
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
        if self._water_temp is not None:
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
        """No check element in list"""
        if is_not_empty(self._snow_depth):
            if verbose:
                return SNOW_DEPTH_SCALE[int(self._snow_depth)]
            else:
                return int(self._snow_depth)
        else:
            return None

    @property
    def daily_flow(self):
        if is_not_empty(self._flow):
            return get_flow(self._flow, self._flow_integer_part)
        else:
            return None

    @property
    def precipitation_duration_half(self, verbose=True):
        if is_not_empty(self._precip_duration_half):
            return get_duration(self._precip_duration_half, PRECIPITATION_DURATION_SCALE[:-1], verbose=verbose)
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
            return get_duration(self._precip_duration, PRECIPITATION_DURATION_SCALE, verbose=verbose)
        else:
            return None

    @property
    def precipitation_amount(self, verbose=False):
        if is_not_empty(self._precip_amount):
            return get_amount(self._precip_amount, verbose=verbose)
        else:
            return None

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

        return output, valid_date(self._YY)
