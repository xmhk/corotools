import numpy as np
import datetime as dt
from .base_data import REFDATE

class dateobj():
    """basic date object with some transformations

    Parameters
    ----------
    y : array or list containing the year values of the time series (length n)
    m : array or list containing the months values of the time series (length n)
    d : array or list containing the days values of the time series (length n)
    refdate : reference date (as datetime object), optional

    Data fields:
    ------------
    dt : time data as liste of python datetime.datetime objects
    d : array of days, starting from startdate
    week : array with calendar weeks
    refdate : reference date (set in initializer or in corotools base data file
    x : time series dates normalized to range of 0 .. 1

    Methods:
    -------
    d2x(d) : converts days to x
    x2d(x) : converts x to days
    d2dt(d) : converts days to datetime objects
    x2dt(x) : converts x to datetime objects
    adddays(n) : give an array of days (self.d) extended by n days

    """
    def __init__(self, y, m, d, refdate = REFDATE):
        self.dt = [dt.datetime(int(y[i]), int(m[i]), int(d[i]), 0, 0, 0) for i in np.arange(0,len(m))]
        self.week = np.array( [dd.isocalendar()[1] for dd in self.dt] )
        self.d = np.array([(x-refdate).days for x in self.dt])     
        self.__normxoffs = self.d[0]
        self.__normx = self.d - self.__normxoffs
        self.normxfact = 1. / np.max(self.__normx)
        self.x = self.__normx  * self.normxfact
        self.refdate = refdate

    def d2x(self, d):
        "days to normalized x"
        return (d - self.__normxoffs) * self.normxfact
    def x2d(self, x):
        "normalized x to days"
        return x / self.normxfact + self.__normxoffs
    def d2dt(self, d):
        "days to datetime obj"
        return [self.refdate + dt.timedelta(days=float( d[i]) ) for i, x in enumerate(d)]
    def x2dt(self, x):
        "normalized x to datetime obj "
        return self.d2dt(self.x2d(x))
    def adddays(self, numdays):
        "return vector of days with numdays additional days"
        return np.arange( self.d[0], self.d[-1]+1+numdays)
    

class dataset():
    """class: basic time series dataset

    Parameters:
    -----------
    data : time series data as 4-column array (year, month, day, y-value)
    countrykey : string
    refdate : reference date (optional)

    Data fields:
    -----------
    raw_data : original data array
    countrykey : country key
    refdate : reference date
    y : y-values
    normy : y values normalized to maximum
    dy : difference of y values compared to last day in series
    dy_weekly_mean : weekly mean of dy for each day
    normdy : normalized difference dy
    do : dateobj (date object) for the time series
    """
    def __init__(self, data, countrykey, refdate=REFDATE):
        self.raw_data = data.copy()
        self.countrykey = countrykey
        self.refdate = refdate
        self.y = self.raw_data[:,3].copy()
        if np.max(self.y)>0:
            self.normyfact =  np.max(self.y)
        else:
            self.normyfact = 1
        self.normy = self.y / self.normyfact
        self.dy = np.zeros(len(self.y))
        self.dy[1::] = self.y[1::]-self.y[0:-1]
        self.normdy = self.dy / self.normyfact
        self.do = dateobj( data[:,0], data[:,1], data[:,2], refdate = REFDATE)
        tmpl = []
        for i, w in enumerate( self.do.week):
            indices = np.nonzero( np.multiply(  self.do.week == w ,
                                                np.array([x.year for x in self.do.dt])==self.do.dt[i].year))
            tmpl.append( np.mean(  self.dy[indices] ) )
        self.dy_weekly_mean = np.array(tmpl)
        
    
