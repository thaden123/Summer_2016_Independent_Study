#!/usr/bin/python
from graph import *
import random
# choose one
# import statistics as np
# stdvar = np.stdev
import numpy as np
stdvar = np.std


fileNames = ["p2p-Gnutella31.txt","Email-Enron.txt","Email-EuAll.txt","Amazon0302.txt","web-NotreDame.txt","web-Stanford.txt","web-Google.txt","web-BerkStan.txt"]


print "\nstarting file read...", " ", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), "\n"
for i in fileNames:
    cur = open(i,"r")
    cur.next()
    cur.next()
    print '%-25s %s' % (i, cur.next().split('\n')[0])
    cur.close()
# Change "fileNames[...]" to run different files
# current testing
for i in fileNames[-1:]:
    print "\n", i, " ", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), "\n"
    ti = time.clock()
    tw = time.time()
    cur = open(i,"r")
    wrr = open("stats." + i,"a")
    wrr.write(cur.next())
    wrr.write(cur.next())
    line = cur.next()
    wrr.write(line)
    curN = line.split('\n')[0].split(' ')[2]
    curM = line.split('\n')[0].split(' ')[4]
    if i == "web-Google.txt":
        curGraph = Graph(int(916428))
    else:
        curGraph = Graph(int(curN) + 1)
    cur.seek(0)
    for j in cur:
        if not j[0] == '#':
            l = j.split('\n')[0].split('\t')
            curGraph.add_edge(int(l[0]),int(l[1]))
    curGraph.sort()
    wrr.write("#Graph build took " + str(time.time() - tw) + "\n")
    countBFS = int(0)
    countTS = int(0)
    fail_time = int(0)
    count_different = int(0)
    one_sided_results = []
    two_sided_results = []
    START_TIME = time.time()
    wrr.write("#algorithm--ss------mean------------std-------------max-------------min-------failtime\n")
    for x in range(1):
        sample_size = 10 ** (x + 2)
        a, b, t = curGraph.sample(sample_size)
        for y in range(sample_size):
            print a[y].get_name(), "  ----->  ", b[y].get_name()
            time_o, success_o, path_length_o, yyy = curGraph.one_sided(a[y],b[y])
            time_t, success_t, path_length_t, yyx = curGraph.two_sided(a[y],t[y])
            if path_length_o is not path_length_t:
                count_different += 1
            if success_o:
                one_sided_results.append(time_o)
            else:
                fail_time += time_o
            if success_t:
                two_sided_results.append(time_t)
            else:
                fail_time += time_t

            Graph.print_nodes(yyy)
            Graph.print_nodes(yyx)
            print "ONE_SIDED - ", time_o," | ",success_o," | ",path_length_o
            print "TWO_SIDED - ", time_t, " | ", success_t, " | ", path_length_t
            print y, "/", sample_size,", ", Graph.sugar_time(time.time() - START_TIME)," running time, ",count_different," different\n"





        if len(one_sided_results) is 0:
            print "\n\nUnsuccessful>>\nONE_SIDED -- Apparently there were no paths between any of the randomly generated ", sample_size, " pairs\n"
            wrr.write("ONE_SIDED\t" + str(sample_size) + "NO SUCCESSFUL PATHS\t:(\n")
        elif len(one_sided_results) is 1:
            print "\n\nSuccessful>>\nONE_SIDED\t", sample_size, "\t", len(one_sided_results), "\t", np.mean(one_sided_results), "\t" \
                "", "0", "\t", max(one_sided_results), "\t", min(one_sided_results), "\t" \
                "", 100 - len(one_sided_results), "\t", fail_time, "\n"
            wrr.write("ONE_SIDED\t" + str(sample_size) + "\t" + str(np.mean(one_sided_results)) + "\t"
                "" + "0" + "\t" + str(max(one_sided_results)) + "\t"
                "" + str(min(one_sided_results)) + "\t" + str(fail_time) + "\n")
        else:
            print "\n\nSuccessful>>\nONE_SIDED\t", sample_size, "\t", len(one_sided_results), "\t", np.mean(one_sided_results), "\t" \
                "", stdvar(one_sided_results), "\t", max(one_sided_results), "\t", min(one_sided_results), "\t" \
                "", 100 - len(one_sided_results), "\t", fail_time, "\n"
            wrr.write("ONE_SIDED\t" + str(sample_size) + "\t" + str(np.mean(one_sided_results)) + "\t"
                "" + str(stdvar(one_sided_results)) + "\t" + str(max(one_sided_results)) + "\t"
                "" + str(min(one_sided_results)) + "\t" + str(fail_time) + "\n")
        if len(two_sided_results) is 0:
            print "\n\nUnsuccessful>>\nTWO_SIDED -- Apparently there were no paths between any of the randomly generated ", sample_size, " pairs\n"
            wrr.write("TWO_SIDED\t" + str(sample_size) + "NO SUCCESSFUL PATHS\t:(\n")
        elif len(two_sided_results) is 1:
            print "\n\nSuccessful>>\nTWO_SIDED\t", sample_size, "\t", len(two_sided_results), "\t", np.mean(two_sided_results), "\t" \
                "", "0", "\t", max(two_sided_results), "\t", min(two_sided_results), "\t" \
                "", 100 - len(two_sided_results), "\t", fail_time, "\n"
            wrr.write("TWO_SIDED\t" + str(sample_size) + "\t" + str(np.mean(two_sided_results)) + "\t"
                "" + "0" + "\t" + str(max(two_sided_results)) + "\t"
                "" + str(min(two_sided_results)) + "\t" + str(fail_time) + "\n")
        else:
            print "\n\nSuccessful>>\nTWO_SIDED\t", sample_size, "\t", len(two_sided_results), "\t", np.mean(two_sided_results), "\t" \
                "", stdvar(two_sided_results), "\t", max(two_sided_results), "\t", min(two_sided_results), "\t" \
                "", 100 - len(two_sided_results), "\t", fail_time, "\n"
            wrr.write("TWO_SIDED\t" + str(sample_size) + "\t" + str(np.mean(two_sided_results)) + "\t"
                "" + str(stdvar(two_sided_results)) + "\t" + str(max(two_sided_results)) + "\t"
                "" + str(min(two_sided_results)) + "\t" + str(fail_time) + "\n")
        del(one_sided_results)
        del(two_sided_results)
        del(fail_time)
        del(count_different)
    wrr.close()




# TODO manual garbage collection

