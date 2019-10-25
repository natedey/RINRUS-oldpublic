import Gnuplot
from numpy import *
import sys,os

if __name__ == '__main__':
    plot = False
    if (sys.argv[1] == '-p'):
        plot = True

    dat = genfromtxt('freq_per_res.dat',usecols=(1,2))
    new_col = []
    for i in range(dat.shape[0]):
        new_col.append([i+1])
    new_col = array(new_col)
    newd = hstack((new_col,dat))
    savetxt('freq_plot.dat',newd,fmt='%6d %6d %10d')
    p = Gnuplot.Gnuplot(debug=True)
    if (plot):
#        p("set terminal png transparent truecolor size 1024,786")
#        p("set output 'freq.png'")
        p("set terminal postscript enhanced color")
        p("set output 'freq.eps'")
        p("set boxwidth 0.5")
        p("set style fill solid")
        p("set xrange [0.5:%d+0.5]"%dat.shape[0])
        for i in range(dat.shape[0]):
            p("set xtics add ('%d' %d) nomirror rotate"%(dat[i,0],i+1))
#        p("unset xtics")
#        p("unset ytics")
#        p("set xtics ('501' 1,'502' 2,'292' 3,'904' 4,'246' 5,'349' 6,'296' 7,'241' 8,'354' 9,'356' 10,'81' 11,'250' 12,'249' 13,'689' 14,'245' 15,'92' 16,'242' 17,'350' 18,'321' 19,'348' 20,'361' 21,'298' 22,'366' 23,'357' 24,'362' 25,'291' 26,'80' 27,'355' 28,'169' 29,'99' 30,'358' 31,'88' 32,'395' 33,'244' 34,'351' 35,'665' 36,'295' 37,'144' 38,'75' 39) nomirror rotate")
        p("set ytics nomirror")
        p("set ylabel 'Frequency' offset 1.0,0 font ',14'")
        p("set xlabel 'Residue ID' offset 1.0,0 font ',14'")
        p("unset key")
        p("set border 3")
        p("plot 'freq_plot.dat' u 1:3 with boxes")
    del p
    os.system("convert freq.eps -rotate 90 freq.png")
    os.system("rm freq.eps")
