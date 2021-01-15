from time import time
from functools import partial
from multiprocessing.pool import Pool

from download import setup_download_dir, get_links, download_link

#CLIENT_ID = 'replace with your client ID'
from imgur_credentials import client_id as CLIENT_ID

def main():
   ts = time()
   download_dir = setup_download_dir()
   links = [l for l in get_links(CLIENT_ID)]
   download = partial(download_link, download_dir)
   with Pool(8) as p:
       p.map(download, links)
   print('Took {}s'.format(time() - ts))

if __name__ == '__main__':
   main()
