from cron_validator.util import str_to_datetime
from cron_validator.validator import CronValidator
from cron_validator.regexes import Version


def test_match_minute():
    dt_str = "2019-04-23 1:00"
    dt = str_to_datetime(dt_str)

    assert CronValidator.match_datetime("* * * * *", dt)
    assert CronValidator.match_datetime("0 * * * *", dt)
    assert CronValidator.match_datetime("0-30 * * * *", dt)
    assert CronValidator.match_datetime("0/30 * * * *", dt)
    assert CronValidator.match_datetime("0/1 * * * *", dt)
    assert CronValidator.match_datetime("1/1 * * * *", dt) is False
    assert CronValidator.match_datetime("1,2,3,4 * * * *", dt) is False
    assert CronValidator.match_datetime("30 * * * *", dt) is False


def test_match_hour():
    dt_str = "2019-04-23 1:00"
    dt = str_to_datetime(dt_str)

    assert CronValidator.match_datetime("* * * * *", dt)
    assert CronValidator.match_datetime("* 1 * * *", dt)
    assert CronValidator.match_datetime("* 0 * * *", dt) is False
    assert CronValidator.match_datetime("* 0-5 * * *", dt)
    assert CronValidator.match_datetime("* 0/5 * * *", dt) is False
    assert CronValidator.match_datetime("* 0/1 * * *", dt)
    assert CronValidator.match_datetime("* 1/1 * * *", dt)
    assert CronValidator.match_datetime("* 2/1 * * *", dt) is False
    assert CronValidator.match_datetime("* 1,2,3,4 * * *", dt)
    assert CronValidator.match_datetime("* 2,3,4 * * *", dt) is False


def test_match_day_of_month():
    dt_str = "2019-04-23 1:00"
    dt = str_to_datetime(dt_str)

    assert CronValidator.match_datetime("* * * * *", dt)
    assert CronValidator.match_datetime("* * 23 * *", dt)
    assert CronValidator.match_datetime("* * 1 * *", dt) is False
    assert CronValidator.match_datetime("* * 1-5 * *", dt) is False
    assert CronValidator.match_datetime("* * 1-23 * *", dt)
    assert CronValidator.match_datetime("* * 1/5 * *", dt) is False
    assert CronValidator.match_datetime("* * 1/1 * *", dt)
    assert CronValidator.match_datetime("* * 1/1 * *", dt)
    assert CronValidator.match_datetime("* * 24/1 * *", dt) is False
    assert CronValidator.match_datetime("* * 23,2,3,4 * *", dt)
    assert CronValidator.match_datetime("* * 2,3,24 * *", dt) is False


def test_match_month():
    dt_str = "2019-04-23 1:00"
    dt = str_to_datetime(dt_str)

    assert CronValidator.match_datetime("* * * * *", dt)
    assert CronValidator.match_datetime("* * * 4 *", dt)
    assert CronValidator.match_datetime("* * * 5 *", dt) is False
    assert CronValidator.match_datetime("* * * 1-5 *", dt)
    assert CronValidator.match_datetime("* * * 1-3 *", dt) is False
    assert CronValidator.match_datetime("* * * 1/5 *", dt) is False
    assert CronValidator.match_datetime("* * * 5/1 *", dt) is False
    assert CronValidator.match_datetime("* * * 1/1 *", dt)
    assert CronValidator.match_datetime("* * * 2,3,4 *", dt)
    assert CronValidator.match_datetime("* * * 2,3,5 *", dt) is False


def test_match_day_of_week():
    dt_str = "2019-04-23 1:00"  # Is a Tuesday
    dt = str_to_datetime(dt_str)

    assert CronValidator.match_datetime("* * * * *", dt)
    assert CronValidator.match_datetime("* * * * 2", dt)
    assert CronValidator.match_datetime("* * * * 5", dt) is False
    assert CronValidator.match_datetime("* * * * 2-5", dt)
    assert CronValidator.match_datetime("* * * * 2-3", dt)
    assert CronValidator.match_datetime("* * * * 2/5", dt)
    assert CronValidator.match_datetime("* * * * 5/1", dt) is False
    assert CronValidator.match_datetime("* * * * 1/1", dt)
    assert CronValidator.match_datetime("* * * * 3,4,5", dt) is False
    assert CronValidator.match_datetime("* * * * 2,3,1", dt)


def test_match_eb_syntax():
    dt_str = "2023-04-28 1:00"
    dt = str_to_datetime(dt_str)
    assert CronValidator.match_datetime("* * * * 30W", dt, version=Version.EB)
    assert CronValidator.match_datetime("* * * * 5L", dt, version=Version.EB)

    dt_str = "2022-02-28 1:00"
    dt = str_to_datetime(dt_str)
    assert CronValidator.match_datetime("* * L * *", dt, version=Version.EB)

    dt_str = "2022-02-27 1:00"
    dt = str_to_datetime(dt_str)
    assert CronValidator.match_datetime("* * L * *", dt, version=Version.EB) is False

    dt_str = "2020-02-28 1:00"
    dt = str_to_datetime(dt_str)
    assert CronValidator.match_datetime("* * L * *", dt, version=Version.EB) is False

    dt_str = "2020-02-29 1:00"
    dt = str_to_datetime(dt_str)
    assert CronValidator.match_datetime("* * L * *", dt, version=Version.EB)

