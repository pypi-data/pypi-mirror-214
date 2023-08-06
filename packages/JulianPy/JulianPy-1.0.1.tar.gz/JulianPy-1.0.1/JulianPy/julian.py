# this module aims to be the best astronomical julian date and irregular date library Python had, has, and will have.


import datetime
import math

def CJDN(date=datetime.datetime.now()):
    return round(julian_date(date))

def div(x, y):
    return math.floor(x/y), x%y


def current_julian_date():
    """Returns current julian date"""
    date = datetime.datetime.now()
    time = date.timestamp() * 1000
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() else 0
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5

def tomorrow_julian_date():
    """returns tomorrow's julian date"""
    date = datetime.datetime.now() + datetime.timedelta(days=1)
    time = date.timestamp() * 1000
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() else 0
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5

def future_julian_date(hoursadd = 0, minutesadd = 0, secondsadd =0):
    """defaults to current if no specifications made. HOURS, MINUTES, AND SECONDS CANNOT BE NEGATIVE"""
    date = datetime.datetime.now() + datetime.timedelta(hours= hoursadd, minutes = minutesadd, seconds=secondsadd)
    time = date.timestamp() * 1000
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() else 0
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5

def julian_date(date = datetime.datetime.now()):
    """Given any date in the future or past, return julian date"""
    time = date.timestamp() * 1000
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() else 0
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5

def epoch_days(date=datetime.datetime.now()):
    """returns days since Jan 1st, 2000. Negative if before this date"""
    return julian_date(date) - 2451545

def day_percent(date=datetime.datetime.now()):
    """ Returns decimal portion of Julian Date"""
    whole = julian_date(date)
    return whole - math.floor(whole)

def islamic_date(CJDNtime=None, date=datetime.datetime.now()):
    """given the date, we return islamic year, islamic month, islamic day"""
    if CJDNtime:
        cjdn = CJDNtime
    else:
        cjdn = CJDN(date)
    a, e1 = div(30 * cjdn - 58442554, 10631)
    m, e2 = div(11 * (math.floor(e1/30)) + 330, 325)
    d = math.floor(e2/11) + 1
    return a, m, d

def babylonian_date(CJDNtime = None, date=datetime.datetime.now()):
    """given the date, we return the approximate babylonian year, babylonian month, babylonian day. NOTE APPROXIMATE"""
    if CJDNtime:
        cjdn = CJDNtime
    else:
        cjdn = CJDN(date)
    m1, e1 = div((235 * cjdn) - 377685891, 6940)
    a, e2 = div((19 * m1) + 5, 235)
    m = math.floor(e2/19) + 1
    d = math.floor(e1/235) + 1
    return a, m, d



"""VERY IMPORTANT FUNCTION TO CONVERT FROM JULIAN DATE TO NORMAL DATE"""
def from_julian(j):
    """Returns datetime.datetime object given julian date J"""
    J1970 = 2440588
    dayMs = 24 * 60 * 60 * 1000
    return datetime.datetime.fromtimestamp((j + 0.5 - J1970) * dayMs / 1000.0)


"""TRIGONOMETRIC FUNCTIONS FOR CONVENIENCE. THESE TAKE IN DEGREE INPUT INSTEAD OF RADIANS"""
def sin(x): return math.sin(math.radians(x))
def cos(x): return math.cos(math.radians(x))
def tan(x): return math.tan(math.radians(x))
def acos(x): return math.degrees(math.acos(x))
def asin(x): return math.degrees(math.asin(x))
def atan2(y, x): return math.degrees(math.atan2(y, x))