import datetime
import re
from .hydra import StandardObservation, StageAndFlow, StageAndVolume, Inflow, FlowAndSurface, Disaster
from .hydra import Error, valid_date, valid_time, EMPTY_OUTPUT


IDENTIFIER = r'(?P<basin>\d{2})(?P<station_id>\d{3})'
MEASURE_TIME = r'(?P<YY>(0[1-9]|[12][0-9]|3[01]))(?P<GG>([01][0-9]|2[0-3]))(?P<n>\d)'
ADDITIONAL_SECTIONS_TAGS = r'9[22|33|44|55|66|77]\d{2}'

NullValue = 'NIL'


class KN15:
    @staticmethod
    def parse():
        pass

    def __init__(self, report, ts=None):
        super().__init__()
        self._report = report
        self._ts = ts
        self._basin = None
        self._station_id = None
        self._YY = None
        self._GG = None
        self._n = None
        self._standard_daily = None
        self._previous_standard_daily = []
        self._stage_and_flow = []
        self._reservoir_stage_and_volume_daily = []
        self._reservoir_inflow_daily = []
        self._reservoir_flow_and_surface = []
        self._disasters = []
        self._literal_part = None
        self._parse()

    def __repr__(self):
        return(self._report)

    def _parse(self):

        identifier = self._report[:5]
        self._basin = identifier[:2]
        self._station_id = identifier[2:]
        measure_time = self._report[6:11]
        match = re.match(MEASURE_TIME, measure_time)
        if match is None:
            if self._ts is not None:
                self.ts_to_date()
        else:
            parsed = match.groupdict()
            self._YY = parsed.get('YY')
            self._GG = parsed.get('GG')
            self._n = parsed.get('n')

        self.get_literal_part()
        parts = re.split(fr'\s(?={ADDITIONAL_SECTIONS_TAGS})', self._report[12:])
        if not re.match(ADDITIONAL_SECTIONS_TAGS, parts[0]):
            self._standard_daily = parts[0]
        for part in parts:
            if re.match(r'922(\d{2})(\s.*)', part):
                self._previous_standard_daily.append(part)
            if re.match(r'933(\d{2})(\s.*)', part):
                self._stage_and_flow.append(part)
            if re.match(r'944(\d{2})(\s.*)', part):
                self._reservoir_stage_and_volume_daily.append(part)
            if re.match(r'955(\d{2})(\s.*)', part):
                self._reservoir_inflow_daily.append(part)
            if re.match(r'966(\d{2})(\s.*)', part):
                self._reservoir_flow_and_surface.append(part)
            if re.match(r'9770[1-7](\s.*)', part):
                self._disasters.append(part)


    @property
    def n(self):
        match = re.match(r'[1-5,7]', self._n)
        if match is None:
            return None
        return int(self._n)

    @property
    def identifier(self):
        return f'{self._basin}{self._station_id}'

    @property
    def basin(self):
        return self._basin

    @property
    def measure_time(self):
        if self._GG is None:
            return None
        return str(valid_time(self._GG))

    @property
    def measure_day(self):
        if self._YY is None:
            return None
        return str(valid_date(self._YY))

    @property
    def standard_daily(self):
        if self._standard_daily is not None:
            return self._standard_daily
        else:
            return None

    @property
    def previous_standard_daily(self):
        if len(self._previous_standard_daily) > 0:
            return self._previous_standard_daily
        else:
            return None

    @property
    def stage_and_flow(self):
        if len(self._stage_and_flow) > 0:
            return self._stage_and_flow
        else:
            return None

    @property
    def reservoir_stage_and_volume_daily(self):
        if len(self._reservoir_stage_and_volume_daily) > 0:
            return self._reservoir_stage_and_volume_daily
        else:
            return None

    @property
    def reservoir_inflow_daily(self):
        if len(self._reservoir_inflow_daily) > 0:
            return self._reservoir_inflow_daily
        else:
            return None

    @property
    def reservoir_flow_and_surface_period(self):
        if len(self._reservoir_flow_and_surface) > 0:
            return self._reservoir_flow_and_surface
        else:
            return None

    @property
    def disasters(self):
        if len(self._disasters) > 0:
            return self._disasters
        else:
            return None

    def prepare_head(self, day=None):
        out = dict({
            'identifier': self.identifier,
            'basin': self.basin,
            'day_of_month': self.measure_day,
            'synophour': self.measure_time,
            'special_marks': self._literal_part
        })
        if day != None:
            out['day_of_month'] = str(day)
            out['synophour'] = '8'
        out.update(EMPTY_OUTPUT)
        return out

    def decode(self):
        out = []
        if self.standard_daily is not None:
            output = self.prepare_head()
            body, _ = StandardObservation(self.standard_daily).decode()
            if body is not None:
                output.update(body)
            out.append(output)

        if self.previous_standard_daily is not None:
            for previous_standard_daily in self.previous_standard_daily:
                body, day = StandardObservation(previous_standard_daily).decode()
                output = self.prepare_head(day)
                if body is not None:
                    output.update(body)
                out.append(output)

        if self.stage_and_flow is not None:
            for stage_and_flow in self.stage_and_flow:
                body = StageAndFlow(stage_and_flow).decode()
                output = self.prepare_head()
                if body is not None:
                    output.update(body)
                out.append(output)

        if self.reservoir_stage_and_volume_daily is not None:
            for stage_and_volume in self.reservoir_stage_and_volume_daily:
                body, day = StageAndVolume(stage_and_volume).decode()
                output = self.prepare_head(day)
                if body is not None:
                    output.update(body)
                out.append(output)

        if self.reservoir_inflow_daily is not None:
            for inflow in self.reservoir_inflow_daily:
                body, day = Inflow(inflow).decode()
                output = self.prepare_head(day)
                if body is not None:
                    output.update(body)
                out.append(output)

        if self.reservoir_flow_and_surface_period is not None:
            for flow_and_surface in self.reservoir_flow_and_surface_period:
                body = FlowAndSurface(flow_and_surface).decode_flow()
                output = self.prepare_head()
                if body is not None:
                    output.update(body)
                out.append(output)
                body = FlowAndSurface(flow_and_surface).decode_surface()
                output = self.prepare_head()
                if body is not None:
                    output.update(body)
                out.append(output)

        if self.disasters is not None:
            for disaster in self.disasters:
                body = Disaster(disaster).decode()
                output = self.prepare_head()
                if body is not None:
                    output.update(body)
                out.append(output)

        return out

    def get_literal_part(self):
        """Split '_report' to numeral array and text part (if exist)"""
        regex = '([(0-9\/\)\s]*)\s([а-яА-Яa-zA-Z].*)'
        report = self._report
        if re.search(regex, report):
            pattern = re.compile(regex)
            row = pattern.findall(report)
            literal_part = row[0][1]
        else:
            literal_part = None
        self._literal_part = literal_part
        return literal_part

    def ts_to_date(self):
        """Convert received date to date attributes"""
        dt = datetime.datetime.fromtimestamp(float(self._ts))
        self._YY = dt.day


def bulletin_reports(bulletin):
    """
    each report in bulletin start with new line and ended with '='
    return iterator for reports in bulletin  
    """
    report_bounds = re.compile(r'((.)*?)=', re.DOTALL | re.MULTILINE)
    return map(lambda m: re.sub(r"\s+", ' ', m.group(1)).strip(), re.finditer(report_bounds, bulletin))

def clean(string, artifacts='\x0f\x0e'):
    """Input sometimes contain unvisible artifacts (\x0f, \x0e)
    which deleted by this function. 
    Set 'artifacts' to delete other artifacts."""
    encoding = 'koi8-r'
    artifacts = [ord(x) for x in artifacts]
    byte_string = string.encode(encoding)
    out_byte_string = byte_string
    for i in range(len(byte_string)):
        if byte_string[i] in artifacts:
            for j in range(len(out_byte_string)):
                if out_byte_string[j] == byte_string[i]:
                    out_byte_string = out_byte_string[:j] + out_byte_string[j+1:]
                    break
    return out_byte_string.decode(encoding)

def decode(bulletin):
    bulletin = clean(bulletin)
    header = bulletin.split()[0].upper()
    if header != 'HHZZ':
        raise TypeError(f'Report does not contain HHZZ in first line. "{header}" was received .')
    bulletin = bulletin.replace('HHZZ','')
    return  bulletin_reports(bulletin)


