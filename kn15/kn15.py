import re
import click
from hydra.daily_standard import StandardObservation
from hydra.stage_and_flow import StageAndFlow
from hydra.hydra_lib import Error, valid_date, valid_time

report_bounds = re.compile(r'^(.*?)=', re.DOTALL | re.MULTILINE)

IDENTIFIER = r'(?P<basin>\d{2})(?P<station_id>\d{3})'
MEASURE_TIME = r'(?P<YY>\d{2})(?P<GG>\d{2})(?P<n>[1-5,7])'
ADDITIONAL_SECTIONS_TAGS = r'9[22|33|44|55|66|77|88]\d{2}'

NullValue = 'NIL'


class KN15():
    @staticmethod
    def parse():
        pass

    def __init__(self, report):
        super().__init__()
        self._report = report
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
        self._reservoir_flow_and_surface_period = []
        self._disasters = []
        self._parse()

    def _parse(self):
        identifier = self._report[:5]
        self._basin = identifier[:2]
        self._station_id = identifier[2:]
        measure_time = self._report[6:11]
        match = re.match(MEASURE_TIME, measure_time)
        if match is None:
            raise Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._YY = parsed.get('YY')
        self._GG = parsed.get('GG')
        self._n = parsed.get('n')

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
                self._reservoir_flow_and_surface_period.append(part)
            if re.match(r'9770[1-5](\s.*)', part):
                self._disasters.append(part)

        return parsed

    @property
    def identifier(self):
        return int(f'{self._basin}{self._station_id}')

    @property
    def basin(self):
        return int(self._basin)

    @property
    def measure_time(self):
        return valid_time(self._GG)

    @property
    def measure_day(self):
        """measure day of month"""
        return valid_date(self._YY)


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
        if len(self._reservoir_flow_and_surface_period) > 0:
            return self._reservoir_flow_and_surface_period
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
            'synophour': self.measure_time
        })
        if day != None:
            out['day_of_month'] = int(day)
            out['synophour'] = 8
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

        return out



def bulletin_reports(bulletin):
    """
    each report in bulletin start with new line and ended with '='
    return iterator for reports in bulletin  
  """
    return map(lambda m: re.sub(r"\s+", ' ', m.group(1)).strip(), re.finditer(report_bounds, bulletin))


def decode(bulletin):
    if bulletin.split()[0].upper() != 'HHZZ':
        raise TypeError("Report does not contain HHZZ in first line")
    return bulletin_reports(bulletin[4:])


def parse_file(filename):
    with open(filename, 'r') as f:
        bulletin = f.read()
        for report in decode(bulletin):
            try:
                return KN15(report).decode()
            except Exception as ex:
                print(ex)


def parse_report(report):
    try:
        return KN15(report).decode()
    except Exception as ex:
        print(ex)


@click.command()
@click.option('--filename', help='path to file', default=False)
@click.option('--report', help='Report string to decode', default=False)
def parse(filename, report):
    if filename:
        print(parse_file(filename))
    if report:
        print(parse_report(report))


if __name__ == "__main__":
    parse()
