from .objects import dataset
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker
import numpy as np

def plot_rates(Md, Mdea, key, figsize=(6.5,3), startdate=None):
    """plot the time series of new cases and dead for a specific country
    
    Parameters:
    -----------
    Md : cases dictionary created by get_jhu_data function
    Mdea : dead dictionary created by get_jhu_data function
    key: country (or continent) key for data to plot
    figsize : default (6.5,3), optional
    startdate : datetime object, used to set left limit of the plot

    Returns:
    --------
    list containing [figure handle, ax1 handle, ax2 handle]
    """
    adata = dataset( Md[key], key )
    adatad = dataset ( Mdea[key], key )
    if startdate is None:
        startdate = adata.do.dt[0]
    # modify startdate on first significant number of cases
    #for minnum in [10, 100]:
    #    if np.max(adata.y)>minnum:
    #        a=[i for i,x in enumerate(adata.y>minnum) if x]
    #        startdate = adata.do.dt[a[0]]
    
    # days intervall for xticks
    daysrange = (adata.do.dt[-1] - startdate).days
    tickintervall = 14
    if daysrange > 5*28:
        tickintervall = 28
    if daysrange>12*28:
        tickintervall = 2 * 28
    # index of startdate: get y scaling
    startdateindx = np.nonzero(np.array([(x - startdate).days for x in adata.do.dt]) > 0)[0][0]

    f = plt.figure(tight_layout=True, figsize=figsize, dpi=120)
    # first subplot: cases
    ax1 = plt.subplot(211)
    plt.title(key)
    plt.bar(adata.do.dt, adata.dy, align='center', color='r',alpha=0.7,zorder=3)
    plt.step(adata.do.dt, adata.dy_weekly_mean,where='mid', c='b', lw=1.5)
    plt.grid(True, which='major', zorder=1)
    plt.grid(True,which='minor', lw = 0.5, c='0.9', zorder=1)
    
    # second subplot: dead
    ax2 = plt.subplot(212)
    plt.bar(adatad.do.dt, adatad.dy, align='center', color='r',alpha=0.7,zorder=3)
    plt.step(adatad.do.dt, adatad.dy_weekly_mean,where='mid', c='b', lw=1.5)
    plt.grid(which='major')
    plt.grid(which='minor',lw=0.5, c='0.9', zorder=1)
    for ax in [ax1,ax2]:
        ax.set_xlim(left = startdate)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=tickintervall)) 
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # set y scaling
    if np.min(adata.dy)<-10:
        ymin=-100
    else:
        ymin=-10
    ax1.set_ylim([ymin, np.quantile(adata.dy[startdateindx::], 0.98)*2])
    
    if np.min(adatad.dy)<-10:
        ymin=-100
    else:
        ymin=-10
    ax2.set_ylim([ymin, np.quantile(adatad.dy[startdateindx::], 0.98)*2])
    
    ax1.set_ylabel('new cases')
    ax2.set_ylabel('new dead')

    #for label in ax1.get_xticklabels():
    #    label.set_ha("right")
    #    label.set_rotation(45)

    return f, ax1, ax2