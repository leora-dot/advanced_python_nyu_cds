from time import time
from queue import Queue
from threading import Thread

from download import setup_download_dir, get_links, download_link

#CLIENT_ID = 'replace with your client ID'
from imgur_credentials import client_id as CLIENT_ID


class DownloadWorker(Thread):
   def __init__(self, queue):
       Thread.__init__(self)
       self.queue = queue

   def run(self):
       while True:
           # Get the work from the queue and expand the tuple
           directory, link = self.queue.get()
           download_link(directory, link)
           self.queue.task_done()

def main():
   ts = time()
   download_dir = setup_download_dir()
   links = [l for l in get_links(CLIENT_ID)]
   # Create a queue to communicate with the worker threads
   queue = Queue()
   # Create 8 worker threads
   for x in range(8):
       worker = DownloadWorker(queue)
       # Setting daemon to True will let the main thread exit even though the workers are blocking
       worker.daemon = True
       worker.start()
   # Put the tasks into the queue as a tuple
   for link in links:
       print('Queueing {}'.format(link))
       queue.put((download_dir, link))
   # Causes the main thread to wait for the queue to finish processing all the tasks
   queue.join()
   print('Took {}'.format(time() - ts))

if __name__ == '__main__':
   main()
