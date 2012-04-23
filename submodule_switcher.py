from __future__ import print_function
import argparse
import fileinput
import os
import re
import subprocess
import sys


SUBMODULE_REGEX = re.compile(r'.+?[:/]{1}(?P<account_name>[^/]+?)/(?P<repo_name>[^/]+?)\.git')


def git_submodule_diff(submodule_path):
    cwd = os.getcwd()
    os.chdir(submodule_path)
    diff = subprocess.check_output('git diff master', shell=True)
    os.chdir(cwd)
    return diff


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
    os.chdir(submodule_path)
    subprocess.call('git fetch origin', shell=True)
    subprocess.call('git reset --hard origin/master', shell=True)


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
        type=str,
        help= (
            'The absolute path to the git repository containing the '
            'submodule.')
    )
    parser.add_argument(
        'submodule_relpath',
        type=str,
        help= (
            'The relative path, from the project directory, to the git '
            'submodule you\'d like to switch.')
    )
    parser.add_argument(
        'submodule_repo_name',
        type=str,
        help='The name of the submodule repository to switch.'
    )
    parser.add_argument(
        'fork_account',
        type=str,
        help='The account name of the fork to which to switch the submodule.'
    )
    args = parser.parse_args()
    return vars(args)


def main():
    args = get_argparse_args()
    prj_dir = args.get('project_dir')
    sub_relpath = args.get('submodule_relpath')
    sub_repo_name = args.get('submodule_repo_name')
    fork_account = args.get('fork_account')

    submodule_abspath = os.path.join(prj_dir, sub_relpath)

    if not git_submodule_diff(submodule_abspath):
        set_submodule_remote(
            prj_dir, sub_relpath, sub_repo_name, fork_account)

        git_submodule_sync()
        git_submodule_reset(submodule_abspath)

    else:
        print(
            'ERROR: You have local changes that are not committed to '
            'the master branch in {0}.\nReset these changes and try '
            'again.'.format(sub_relpath)
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
