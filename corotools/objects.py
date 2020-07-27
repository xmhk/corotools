import numpy as np
import datetime as dt
from .base_data import REFDATE

class dateobj():
    """basic date object with some transformations

    arguments:
        y : array or list containing the year values of the time series (length n)
        m : array or list containing the months values of the time series (length n)
        d : array or list containing the days values of the time series (length n)

    optional parameters:
       refdate : reference date

    data fields:
           dt : time data as liste of python datetime.datetime objects
            d : array of days, starting from startdate
      refdate : reference date (set in initializer or in corotools base data file
            x : time series dates normalized to range of 0 .. 1




    """
    def __init__(self, y, m, d, refdate = REFDATE):
        self.dt = [dt.datetime(int(y[i]), int(m[i]), int(d[i]), 0, 0, 0) for i in np.arange(0,len(m))]
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
    """basic time series dataset"""
    def __init__(self, data, idtag, refdate=REFDATE):
        self.raw_data = data.copy()
        self.idtag = idtag
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
        
    
