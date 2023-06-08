import os
import subprocess
import sys
from typing import List, Union

def get_package_manager(files: List[str]) -> str:
    if 'Cargo.toml' in files:
        return 'cargo'
    elif 'yarn.lock' in files:
        return 'yarn'
    elif 'package-lock.json' in files:
        return 'npm'

def format_monorepo(path: str):
    git_status = subprocess.run(['git', 'status'], capture_output=True)
    sub_folders = [
        name for name in os.listdir('.')
            if os.path.isdir(os.path.join('.', name)) and name in str(git_status.stdout)
    ]
    if len(sub_folders) == 0:
        print("There aren't any projects to format")
        return None

    for sub_folder in sub_folders:
        files = os.listdir(sub_folder)
        package_manager = get_package_manager(files)
        format_repo(f'{path}/{sub_folder}', package_manager)

def format_repo(path: str, package_manager: Union[str, None]):
    if package_manager == None:
        print(f'project "{path}" could not be formatted')
        return None

    subprocess.run([package_manager, 'format'], text=True, cwd=path)

if __name__ == '__main__':
    files = os.listdir('./')
    if 'cargo.toml' not in files or 'yarn.lock' not in files or 'package-lock.json' not in files:
        format_monorepo(os.getcwd())
    else:
        package_manager = get_package_manager(files)
        format_repo(os.getcwd(), package_manager)

    argv = sys.argv
    subprocess.run(['git', 'commit', '-m', sys.argv[0]], text=True)
