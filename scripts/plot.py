import Gnuplot
import numpy as np
import sys

if __name__ == '__main__':
    plot = False
    if (sys.argv[1] == '-p'):
        plot = True

    p = Gnuplot.Gnuplot(debug=True)
    if (plot):
        p("set terminal pngcairo transparent truecolor size 1024,786")
        p("set output 'freq.png'")
        p("set boxwidth 0.5")
        p("set style fill solid")
#        p("unset xtics")
#        p("unset ytics")
#        p("set xtics ('501' 1,'502' 2,'292' 3,'904' 4,'246' 5,'349' 6,'296' 7,'241' 8,'354' 9,'356' 10,'81' 11,'250' 12,'249' 13,'689' 14,'245' 15,'92' 16,'242' 17,'350' 18,'321' 19,'348' 20,'361' 21,'298' 22,'366' 23,'357' 24,'362' 25,'291' 26,'80' 27,'355' 28,'169' 29,'99' 30,'358' 31,'88' 32,'395' 33,'244' 34,'351' 35,'665' 36,'295' 37,'144' 38,'75' 39) nomirror rotate")
        p("set ytics nomirror")
        p("set ylabel 'Frequency' offset 1.0,0 font ',14'")
        p("set xlabel 'Residue ID' offset 1.0,0 font ',14'")
        p("unset key")
        p("set border 3")
        p("plot 'freq_per_res.dat' u 4:3 with boxes")
    del p
