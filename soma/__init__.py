from __future__ import division

from logger import logger
from cmdlineparser import Options, parse_commandline
from kafka_writer import KafkaWriterConfig, KafkaWriter

import os
import json
import random
from datetime import datetime
from time import sleep
import psutil
from mpi4py import MPI


import numpy as np
from numpy.fft import fft2, ifft2
from math import ceil, fabs


MASTER = 0

def main():

    size = 10000           # lengt of vector v
    ITER = 50              # number of iterations to run for each report


    comm = MPI.COMM_WORLD
    # size = comm.Get_size()

    # Configure and connect to the Kafka data backbone server.
    # This is done only once by the rank 0 MPI process.
    #
    if comm.rank == MASTER:

        # Parse the command line
        #
        try:
            options = parse_commandline()

        except Exception, ex:
            logger.error("Command line parsing error: %s", str(ex))
            comm.Abort(-1)

        # Connect to Kafka
        #
        kw_cfg = KafkaWriterConfig(Host=options.KafkaHost, Topic=options.KafkaTopic)
        try:
            kw = KafkaWriter(kw_cfg)
            kw.connect()
            logger.info('connecting to Kafka backbone via %s', kw_cfg.Host)
        except Exception, ex:
            logger.error("Error connecting to Kafka backbone via %s: %s",  kw_cfg.Host, str(ex) )
            comm.Abort(-1)

    # SYNC HERE
    # comm.Barrier()

    my_size = size // comm.size     # Every process computes a vector of lenth *my_size*
    size = comm.size*my_size        # Make sure size is a integer multiple of comm.size
    my_offset = comm.rank*my_size

    # This is the complete vector
    vec = np.zeros(size)            # Every element zero...
    vec[0] = 1.0                    #  ... besides vec[0]

    # Create my (local) slice of the matrix
    my_M = np.zeros((my_size, size))
    for i in xrange(my_size):
        j = (my_offset+i-1) % size
        my_M[i,j] = 1.0

    while True:
        comm.Barrier()                    ### Start stopwatch ###
        t_start = MPI.Wtime()

        for t in xrange(ITER):
            my_new_vec = np.inner(my_M, vec)

            comm.Allgather(
                [my_new_vec, MPI.DOUBLE],
                [vec, MPI.DOUBLE]
            )

        comm.Barrier()
        t_diff = MPI.Wtime() - t_start    ### Stop stopwatch ###

        # if fabs(vec[iter]-1.0) > 0.01:
        #     pprint("!! Error: Wrong result!")

        if comm.rank == MASTER:
            data = {
                'timestamp': str(datetime.now()),
                'throughput': ITER/t_diff,
                'mpi_processes': comm.size
            }

            kw.write( json.dumps(data, sort_keys=True) )
            # print " %d iterations of size %d in %5.2fs: %5.2f iterations per second" % (ITER, size, t_diff, ITER/t_diff)
