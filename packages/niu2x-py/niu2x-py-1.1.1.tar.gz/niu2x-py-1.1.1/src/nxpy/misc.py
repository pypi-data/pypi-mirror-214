import os
import sys
import hashlib
import contextlib
import logging
import shutil


def abort(*vargs):
    logging.error(*vargs)
    sys.exit(1)


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def env(name, default):
    if name in os.environ:
        return os.environ[name]
    return default


def env_required(name):
    if name in os.environ:
        return os.environ[name]
    abort(f"please set {name}")


def md5_file(path):
    hashmd5 = hashlib.md5()
    with open(path, 'rb') as myfile:
        while True:
            b = myfile.read(8096)
            if not b:
                break
            hashmd5.update(b)
    return hashmd5.hexdigest()


def md5(bs):
    hashmd5 = hashlib.md5()
    hashmd5.update(bs)
    return hashmd5.hexdigest()


def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def read_utf8_file(path):
    file = open(path, 'rt', encoding='utf-8')
    content = file.read()
    file.close()
    return content


def read_raw_file(path):
    file = open(path, 'rb')
    content = file.read()
    file.close()
    return content


def write_utf8_file(path, content):
    dirname = os.path.dirname(path)
    ensure_dir(dirname)
    file = open(path, 'wt', encoding='utf-8')
    file.write(content)
    file.close()


def write_raw_file(path, content):
    dirname = os.path.dirname(path)
    ensure_dir(dirname)
    file = open(path, 'wb')
    file.write(content)
    file.close()


def remove(path):
    shutil.rmtree(path)
