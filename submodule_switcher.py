#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import argparse
from contextlib import contextmanager
import fileinput
import os
import re
import subprocess
import sys
import time


SUBMODULE_REGEX = re.compile(r'.+?[:/]{1}(?P<account_name>[^/]+?)/(?P<repo_name>[^/]+?)\.git')


@contextmanager
def cd(directory):
    cwd = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(cwd)


def git_submodule_diff(submodule_path):
    with cd(submodule_path):
        return subprocess.check_output('git diff master', shell=True)


def git_submodule_safety_commit(submodule_path):
    with cd(submodule_path):
        msg = 'Automatic safety commit before submodule switch.'
        timestamp = time.ctime().replace(' ', '-').replace(':', '-')
        branch_name = 'submodule_switcher_{0}'.format(timestamp)
        try:
            subprocess.check_call(
                'git commit -a -m "{0}"'.format(msg),
                shell=True
            )
        except subprocess.CalledProcessError:
            # Do nothing if there is nothing to commit.
            pass
        else:
            subprocess.call('git branch {0}'.format(branch_name), shell=True)


def set_submodule_remote(prj_dir, sub_relpath, sub_repo_name, fork_account):
    submodules_file = os.path.join(prj_dir, '.gitmodules')

    is_target_submodule = False
    for line in fileinput.input(submodules_file, inplace=1):
        line = line.strip('\n')

        if 'submodule' in line:
            if sub_relpath in line:
                is_target_submodule = True
            else:
                is_target_submodule = False

        if is_target_submodule and 'url' in line:
            matches = SUBMODULE_REGEX.match(line)
            account_name = matches.group('account_name')
            repo_name = matches.group('repo_name')

            if sub_repo_name == repo_name:
                line = line.replace(account_name, fork_account)

        print(line)


def git_submodule_sync():
    subprocess.call('git submodule sync', shell=True)


def git_submodule_reset(submodule_path):
    with cd(submodule_path):
        subprocess.call('git fetch origin', shell=True)
        subprocess.call('git reset --hard origin/master', shell=True)


def git_submodule_remote_add_upstream(submodule_path, account_name):
    with cd(submodule_path):
        subprocess.call('git remote rm upstream', shell=True)
        subprocess.call(
            'git remote add upstream {0}'.format(account_name),
            shell=True)


def git_submodule_remote_show(submodule_path):
    with cd(submodule_path):
        subprocess.call('git remote -v', shell=True)


def get_argparse_args():
    parser = argparse.ArgumentParser(
        description= (
            'Switch the origin branch on the specified submodule to a '
            'fork on the specified account name. Example usage: \n'
            '{0} /Users/modocache/app vendor/JSONKit JSONKit modocache'.format(
                __file__))
    )
    parser.add_argument(
        'project_dir',
        help= (
            'The absolute path to the git repository containing the '
            'submodule.')
    )
    parser.add_argument(
        'submodule_relpath',
        help= (
            'The relative path, from the project directory, to the git '
            'submodule you\'d like to switch.')
    )
    parser.add_argument(
        'submodule_repo_name',
        help='The name of the submodule repository to switch.'
    )
    parser.add_argument(
        'fork_account',
        help='The account name of the fork to which to switch the submodule.'
    )
    parser.add_argument(
        '-u', '--upstream_url',
        help='The url a fork to be added as an upstream remote.'
    )
    args = parser.parse_args()
    return vars(args)


def main():
    args = get_argparse_args()
    prj_dir = args.get('project_dir')
    sub_relpath = args.get('submodule_relpath')
    sub_repo_name = args.get('submodule_repo_name')
    fork_account = args.get('fork_account')
    upstream_url = args.get('upstream_url', None)

    submodule_abspath = os.path.join(prj_dir, sub_relpath)

    if not git_submodule_diff(submodule_abspath):
        git_submodule_safety_commit(submodule_abspath)

        set_submodule_remote(
            prj_dir, sub_relpath, sub_repo_name, fork_account)

        git_submodule_sync()
        git_submodule_reset(submodule_abspath)

        if upstream_url:
            git_submodule_remote_add_upstream(submodule_abspath, upstream_url)

        git_submodule_remote_show(submodule_abspath)

    else:
        print(
            'ERROR: You have local changes that are not committed to '
            'the master branch in {0}.\nReset these changes and try '
            'again.'.format(sub_relpath)
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
