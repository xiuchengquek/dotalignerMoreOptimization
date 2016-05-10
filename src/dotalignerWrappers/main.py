import subprocess
import sys
import numpy as np
from multiprocessing import Lock, Process, Queue, current_process
from zipfile import ZipFile
import os



def prepare_jobs_list(listOfFile):
    fileList = []
    with open(listOfFile) as f:
        for line in f:
            fields = line.split('\t')
            fileList.append((fields[0], fields[1]))
    return fileList

def generate_combinations(work_queue):

    for samples in iter(work_queue.get, 'STOP'):
        outfile = 'dotaligner_command/%s %s.dotaligner.command.txt' % (samples[0], samples[1])
        fh_out = open(outfile, 'w')
        for k in np.arange(0 ,1.1, 0.1):
            for t in np.arange(0 ,1.1, 0.1):
                for o in np.arange(0.2 ,1.1, 0.2):
                    for e in np.arange(0.2 ,1.1, 0.2):
                        for s in np.arange(100 ,1100, 100):
                            for T in np.arange(1,11,1):
                                for p0 in [0.001, 0.005]:
                                    fh_out.write("/usr/bin/time -f \"\t%E\t%M\" {dotaligner} -k {k} -t {t} -o {o} -e {e} -s {s} -T {T} -p0 {p0} -d ./data/ps/{dp1}.dp.pp -d ./data/ps/{dp2}.dp.pp\n".format(
                                            dotaligner = 'DotAligner',
                                            k = k,
                                            t = t,
                                            o = o,
                                            e = e,
                                            s = s,
                                            T = T,
                                            p0 = p0,
                                            dp1 = samples[0],
                                            dp2 = samples[1]
                                        ))
        fh_out.close()

        with ZipFile(outfile + '.zip' , 'w') as zip_out:
            zip_out.write(outfile)




def main():


    if not os.path.exists('dotaligner_command'):
        os.mkdir('dotaligner_command')

    fileList = prepare_jobs_list(sys.argv[1])
    n = sys.argv[2]
    #grouped_file = [fileList[i : i + n] for i in range(0, len(fileList), n)]

    work_queue =  Queue()

    for x in fileList:
        work_queue.put(x)

    for w in range(int(n)):
        Process(target=generate_combinations, args=[work_queue]).start()

    for x in fileList:
        work_queue.put('STOP')











if __name__ == '__main__' :
    main()










