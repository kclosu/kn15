import re
from .daily_standard import StandardObservation
from .hydra_lib import Error, get_identify_param
from .hydra_lib import DISASTER_TYPES_SHORT

GROUP_0 = r'9770(?P<type>\d)'
GROUP_1 = r'(?P<digital_group>[(0-9\/\)\s]*)'
GROUP_2 = r'(?P<literal_group>[а-яА-Яa-zA-Z].*)'

SECTION_7 = f'({GROUP_0})\s({GROUP_1})\s({GROUP_2})'


class Disaster:
    """information about natural (specially dangerous) hydrological phenomena and
    abstract changes in the regime of water bodies from Section 7"""

    def __init__(self, report):
        self._report = report
        self._type = None
        self._observation = None
        self._special_marks = None
        self._parse()

    def _parse(self):
        report = self._report
        match = re.match(SECTION_7, report)
        if match is None:
            raise Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._type = parsed.get('type')
        self._observation = parsed.get('digital_group')
        self._special_marks = parsed.get('literal_group')

    @property
    def disaster_type(self, verbose=True):
        if self._type is not None:
            return get_identify_param(self._type, DISASTER_TYPES_SHORT, verbose=verbose)
        else:
            return None

    @property
    def observation(self):
        if self._observation is not None:
            body, _ = StandardObservation(self._observation).decode()
            if body is not None:
                return body
        return None

    @property
    def special_marks(self):
        return self._special_marks

    def decode(self):
        output = {}
        if self.disaster_type is not None:
            output['disaster_type'] = self.disaster_type
        if self.observation is not None:
            output.update(self.observation)
        if self.special_marks is not None:
            output['special_marks'] = self.special_marks

        return output
