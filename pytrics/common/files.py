import gzip
import logging
import os
import shutil


def gzip_file(source, dest, delete_source=False):
    logging.info("gzipping %s to %s", source, dest)

    with open(source, 'rb') as f_in:
        with gzip.open(dest, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    if delete_source:
        os.remove(source)


def decompress_gzip_file(source_file, target_file):
    with gzip.open(source_file, 'rb') as f_in:
        with open(target_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
