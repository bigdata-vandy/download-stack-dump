from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import os
import argparse


def get_archive_list():
  with requests.Session() as s:
    resp = s.get("https://archive.org/details/stackexchange")

  # TODO: check response code
  soup = BeautifulSoup(resp.text)

  return ["https://archive.org" + a["href"]
          for a in soup.find_all("a", {"class": "stealth download-pill"})]


def download_archive(archive_url):
  archive_name = os.path.join("archives", os.path.basename(archive_url))

  with requests.Session() as s:
    resp = s.get(archive_url, stream=True)
    with open(archive_name, "wb") as f:
      for chunk in resp.iter_content(chunk_size=1024):
        if chunk:
          f.write(chunk)


def download_archives(nproc=1):
  archives = get_archive_list()

  pool = Pool(nproc)
  pool.map(download_archive, archives[0:3:2])


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Download Stack Exchange"
                                               "Archives")
  parser.add_argument('--nproc',
                      '-n',
                      type=int,
                      default=1,
                      help="number of parallel processes")

  nproc = parser.parse_args().nproc
  download_archives(nproc)
