import re
from .hydra_lib import is_not_empty, key_in_dict, get_stage, get_flow, valid_date, valid_time
from .hydra_lib import PERIODS

PERIOD = r'933(?P<period>\d{2})'
AVG_STAGE = r'1(?P<avg_stage>\d{4}|/{4})'
MAX_STAGE = r'2(?P<max_stage>\d{4}|/{4})'
MIN_STAGE = r'3(?P<min_stage>\d{4}|/{4})'
AVG_FLOW = r'4(?P<avg_flow_int_part>\d)(?P<avg_flow>\d{3})'
MAX_FLOW = r'5(?P<max_flow_int_part>\d)(?P<max_flow>\d{3})'
MIN_FLOW = r'6(?P<min_flow_int_part>\d)(?P<min_flow>\d{3})'
TIME_OF_MAX = r'7(?P<YY>\d{2})(?P<GG>\d{2})'

STAGE_AND_FLOW = f'^({PERIOD})?(\s{AVG_STAGE})?(\s{MAX_STAGE})?(\s{MIN_STAGE})?\
(\s{AVG_FLOW})(\s{MAX_FLOW})?(\s{MIN_FLOW})?(\s{TIME_OF_MAX})?'


class Error(Exception):
    """Class for exceptions raised when parsing report string"""
    pass


class StageAndFlow():

    def __init__(self, report):
        self._report = report
        self._period = None
        self._avg_stage = None
        self._max_stage = None
        self._min_stage = None
        self._avg_flow = None
        self._avg_flow_int_part = None
        self._max_flow = None
        self._max_flow_int_part = None
        self._min_flow = None
        self._min_flow_int_part = None
        self._YY = None
        self._GG = None
        self._parse()

    def _parse(self):
        report = self._report
        match = re.match(STAGE_AND_FLOW, report)
        if match is None:
            raise KN15Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._period = parsed.get('period')
        self._avg_stage = parsed.get('avg_stage')
        self._max_stage = parsed.get('max_stage')
        self._min_stage = parsed.get('min_stage')
        self._avg_flow = parsed.get('avg_flow')
        self._avg_flow_int_part = parsed.get('avg_flow_int_part')
        self._max_flow = parsed.get('max_flow')
        self._max_flow_int_part = parsed.get('max_flow_int_part')
        self._min_flow = parsed.get('min_flow')
        self._min_flow_int_part = parsed.get('min_flow_int_part')
        self._YY = parsed.get('YY')
        self._GG = parsed.get('GG')


    @property
    def period(self, verbose=True):
        if is_not_empty(self._period):
            period = int(self._period)
            if key_in_dict(period, PERIODS):
                if verbose:
                    return PERIODS[period]
                else:
                    return period
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
            return get_flow(self._avg_flow, self._avg_flow_int_part)
        else:
            return None

    @property
    def max_flow(self):
        if is_not_empty(self._max_flow):
            return get_flow(self._max_flow, self._max_flow_int_part)
        else:
            return None

    @property
    def min_flow(self):
        if is_not_empty(self._min_flow):
            return get_flow(self._min_flow, self._min_flow_int_part)
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
        if self.period is not None:
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
