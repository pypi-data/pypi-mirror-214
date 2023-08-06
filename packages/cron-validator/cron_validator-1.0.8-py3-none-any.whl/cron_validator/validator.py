from dateutil import rrule

from .regexes import ElementPart, Version, element_kind_map, regex_dict
from .util import replace_names, ts_to_datetime


class CronValidator:
    @classmethod
    def parse(cls, expression, version=Version.UNIX):
        """

        :param str expression:
        :return:
        """
        expression = replace_names(expression)
        parts = expression.split(" ")
        if len(parts) != 5:
            raise ValueError("Invalid expression")
        elements = []
        for i in range(0, 5):
            m = regex_dict[version][i].fullmatch(parts[i])
            if not m:
                raise ValueError(f"Invalid expression part {i}")
            kind = None
            body = None
            for key, value in m.groupdict().items():
                if value:
                    kind = key
                    body = value
                    break
            element_cls = element_kind_map.get(kind)
            elements.append(element_cls(part=ElementPart(i + 1), body=body))
        return elements

    @classmethod
    def match_timestamp(cls, expression, ts, tz_name):
        """

        :param expression:
        :param ts:
        :param tz_name:
        :return:
        """
        dt = ts_to_datetime(ts, tz_name)
        elements = cls.parse(expression)
        for element in elements:
            if not element.match(dt):
                return False
        return True

    @classmethod
    def match_datetime(cls, expression, dt, version=Version.UNIX):
        """

        :param expression:
        :param dt:
        :return:
        """
        elements = cls.parse(expression, version)
        for element in elements:
            if not element.match(dt):
                return False
        return True

    @classmethod
    def get_execution_time(cls, expression, from_dt, to_dt, version=Version.UNIX):
        """

        :param expression:
        :param from_dt:
        :param to_dt:
        :param version:
        :return:
        """
        for dt in rrule.rrule(rrule.MINUTELY, dtstart=from_dt, until=to_dt):
            if cls.match_datetime(expression, dt, version):
                yield dt.replace(second=0, microsecond=0)
