import os,sys
import argparse
import numpy as np
from astropy.table import Table
from astropy.io import ascii
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm 

#plt.rcParams['grid.color'] = 'k'
plt.rcParams['grid.linestyle'] = ':'
plt.rcParams['grid.linewidth'] = 0.5

p = argparse.ArgumentParser(description="Calculate the IC electron spectrum of sources")
p.add_argument("-f", "--filename", dest="filename", type=str, default='final_bucle_chip18.csv',
               help='File name')
p.add_argument("-Att", "--Att", dest="Att", type=int, default=7,
               help="Attenuation")
p.add_argument("-Ch", "--Ch", dest="Ch", type=int, default=0,
               help="Channel")
p.add_argument("-Clip_sel", "--Clip_sel", dest="Clip_sel", type=int, default=1,
               help="Clip sel")

args  = p.parse_args()
filename = args.filename
Att      = args.Att
Ch       = args.Ch
Clip_sel = args.Clip_sel

def read_file(filename):
    if not os.path.isfile('../Data/%s' % filename):
	    print ("File ../Data/%s does not exist" % (filename))
	    exit()

    print ("Reading ../Data/%s" % (filename))
    names=['Vin_gen','Ch','Att','Clip_b','Clip_sel','Vin','Vin_err','FWHMin','FWHMin_er','Vout','Vout_er',
           'FHWMo','FHWMo_er','DT','DT_er','dummy1','dummy2','dummy3','dummy4']

    table=ascii.read('../Data/%s' % filename, data_start=1,names=names)
    return table

def Select_event(Att,Ch,Clip_sel):
    # Which Clip_b there are
    Clip_b=table['Clip_b'][np.where((table['Att']==Att) & (table['Ch']==Ch) 
				    & (table['Clip_sel']==Clip_sel)  & (table['Vin_gen']==0.05))]
    # And its number
    Nb=len(Clip_b)

    return Nb,Clip_b

def format_axes(ax):
    ax.set_xlim(0,1.0)
    ax.set_ylim(0,0.6)
    ax.set_xlabel("Vin [V]")
    ax.set_ylabel("Vout [V]")
    ax.legend(loc="upper left",ncol=6,prop={'size':7})
    ax.grid(zorder=0)

def plot_figure(table):
    Nb,Clip_b=Select_event(Att,Ch,Clip_sel)
    color=iter(cm.jet(np.linspace(0,1,Nb)))

    fig,ax =  plt.subplots(1, 1,figsize=(7,5))

    for i in Clip_b:
        print("Plotting Clip_b %i" % i)
        c=next(color)
        Vin=table['Vin'][np.where((table['Att']==Att) & (table['Ch']==Ch) 
                              & (table['Clip_sel']==Clip_sel) & (table['Clip_b']==i))]
        Vout=table['Vout'][np.where((table['Att']==Att) & (table['Ch']==Ch) 
                                & (table['Clip_sel']==Clip_sel) & (table['Clip_b']==i))]
        ax.scatter(Vin,Vout, label="Clip=%.0f" % (i),color=c,zorder=10)
    format_axes(ax)
    fig.savefig("../Figures/Vin_Vout_Ch%.0f_Att%.0f_Clip_sel%.0f.pdf" % (Ch,Att,Clip_sel) )

def write_output(table):
    Vin=table['Vin'][np.where((table['Att']==Att) & (table['Ch']==Ch) 
                              & (table['Clip_sel']==Clip_sel))]
    Vout=table['Vout'][np.where((table['Att']==Att) & (table['Ch']==Ch) 
                                & (table['Clip_sel']==Clip_sel))]
    Clip_b=table['Clip_b'][np.where((table['Att']==Att) & (table['Ch']==Ch) 
                                & (table['Clip_sel']==Clip_sel))]

    outname='../Results/Vin_Vout_Ch%.0f_Att%.0f_Clip_sel%.0f.csv' % (Ch,Att,Clip_sel)
    ascii.write([Vin, Vout, Clip_b], outname, names=['Vin[V]', 'Vout[V]','Clip_b'],overwrite=True)

if __name__ == '__main__':
    table=read_file(filename)
    plot_figure(table)
    write_output(table)



