import multiprocessing

#Number of pending requests
backlog=2048

#Number of active workers
#Recommended: 2-4 * number of cpu cores
workers = multiprocessing.cpu_count() * 2 + 1

#timeout in seconds
timeout = 100


