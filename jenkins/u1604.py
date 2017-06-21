#/usr/bin/env python
# designed to be run with python 2.7, from the root of the repo

import os
import sys
import subprocess
import platform
from os import path
from os.path import join
import time
import argparse


current_dir = path.abspath(os.getcwd())

def cd(subdir):
    global current_dir
    if subdir.startswith('/'):
        current_dir = subdir
    else:
        current_dir = join(current_dir, subdir)
    if not path.isdir(current_dir):
        print('No such directory [%s]' % current_dir)
        sys.exit(-1)
    print('cd to [%s]' % current_dir)


def cd_repo_root():
    global current_dir
    current_dir = path.abspath(os.getcwd())  # since python never really changes its actual cwd


def mkdir(subdir):
    global current_dir
    full_path = join(current_dir, subdir)
    if not path.isdir(full_path):
        os.makedirs(full_path)


def wget(target_url):
    run(['wget', target_url])


def gunzip(target):
    run(['gunzip', target])


def run(cmdlist):
    global current_dir
    print(' '.join(cmdlist))
    f_out = open('jenkins-out%s.txt', 'w', buffering=1)
    f_in = open('jenkins-out%s.txt', 'r', buffering=1)
    f_in.seek(0)
    p = subprocess.Popen(cmdlist, cwd=current_dir, stdout=f_out, stderr=subprocess.STDOUT, bufsize=1)
    res = ''
    def print_progress():
        line = f_in.readline()
        # if not is_py2():
        #     line = line.decode('utf-8')
        res_lines = ''
        while line != '':
            print(line[:-1])
            res_lines += line
            line = f_in.readline()
            # if not is_py2():
            #     line = line.decode('utf-8')
        return res_lines
        # print(lines)
    p.poll()
    while p.returncode is None:
        res += print_progress()
        time.sleep(1)
        p.poll()
    res += print_progress()
    print('p.returncode', p.returncode)
    assert p.returncode == 0
    return res


def run_until(cmdlist, until):
    """
    Runs until string until appears in output, then kills the process, without
    checking return code, and returns the output so far
    """
    global current_dir
    print(' '.join(cmdlist))
    f_out = open('jenkins-out%s.txt', 'w', buffering=1)
    f_in = open('jenkins-out%s.txt', 'r', buffering=1)
    f_in.seek(0)
    p = subprocess.Popen(cmdlist, cwd=current_dir, stdout=f_out, stderr=subprocess.STDOUT, bufsize=1)
    res = ''
    def print_progress():
        line = f_in.readline()
        # if not is_py2():
        #     line = line.decode('utf-8')
        res_lines = ''
        while line != '':
            print(line[:-1])
            res_lines += line
            line = f_in.readline()
            # if not is_py2():
            #     line = line.decode('utf-8')
        return res_lines
        # print(lines)
    p.poll()
    while p.returncode is None:
        res += print_progress()
        if until in res:
            p.terminate()
            return res
        time.sleep(1)
        p.poll()
    res += print_progress()
    print('p.returncode', p.returncode)
    assert p.returncode == 0
    return res


def maybe_rmtree(tree_dir):
    if path.isdir(tree_dir):
        if platform.uname()[0] == 'Windows':
            run(['rmdir', '/s', '/q', '"%s"' % tree_dir])
        else:
            run(['rm', '-Rf', tree_dir])


def clean_coriander():
    coriander_dir = join(os.environ['HOME'], 'coriander')
    maybe_rmtree(coriander_dir)


def main(git_branch):
    # BASEDIR = os.getcwd()

    clean_coriander()

    coriander_dir = join(os.environ['HOME'], 'coriander')
    run(['git', 'clone', '--recursive', 'https://github.com/hughperkins/coriander', '-b', git_branch, 'coriander_repo'])
    cd('coriander_repo')
    run(['python2', 'install_distro.py', '--git-branch', git_branch])

    cd_repo_root()
    run(['git', 'clone', '--recursive', 'https://github.com/hughperkins/cudnn-training', '-b', git_branch])
    cd('cudnn-training')
    mkdir('build')
    cd('build')
    run(['cmake', '..'])
    run(['cmake', '--build', '.'])

    wget('http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz')
    wget('wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz')
    wget('wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz')
    wget('wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz')
    gunzip('train-images-idx3-ubyte.gz')
    gunzip('train-labels-idx1-ubyte.gz')
    gunzip('t10k-images-idx3-ubyte.gz')
    gunzip('t10k-labels-idx1-ubyte.gz')

    run_until(['./lenet'], until='Training iter 2')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--git-branch', type=str, default='master')
    args = parser.parse_args()
    main(**args.__dict__)
