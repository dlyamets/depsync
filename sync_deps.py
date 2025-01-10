#!/usr/bin/python3

import json
import argparse
import os
import shutil
import subprocess


DEPENDENCIES_PATH_KEY = 'dependencies_path'


class Dependency():
    def __init__(self, path: str, repo: str, version: str):
        self.path: str = path
        self.repo: str = repo
        self.version: str = version
        
    def __repr__(self):
        return f'Dependency repo: {self.repo}, path: {self.path}, version: {self.version}'
        
    def sync(self):
        current_work_directory = os.getcwd()
        
        if os.path.isdir(self.path):
            print(f'Directory discovered: {self.path} it will be removed and re-clonned')
            shutil.rmtree(self.path, ignore_errors=True)
            
        os.makedirs(self.path)
        print(f'Directory created for: {self.path}')
        os.chdir(self.path)
        print(f'Clonning repo: {self.repo}, version: {self.version} ...')
        
        subprocess.run([f'git clone {self.repo} .'], 
                    shell=True, capture_output=False, text=True, check=True)
        subprocess.run([f'git checkout {self.version}'], 
                    shell=True, capture_output=False, text=True, check=True)
        print(f'Repository {self.repo} clonned in {self.path} and checked out on {self.version}')
        
        os.chdir(current_work_directory)


def extract_dependencies(json_config: dict):
    dependencies = []
    dependencies_folder = None
    
    current_work_directory = os.getcwd()
    
    for dep in json_config:
        d = json_config[dep]
        if isinstance(d, str) and dep == DEPENDENCIES_PATH_KEY:
            dependencies_folder = d        
    
    if dependencies_folder is None:
        print(f'ERR: dependencies path not defined. Abort.')
        return None, None

    for dep in json_config:
        d = json_config[dep]
        if isinstance(d, dict):
            try:
                path = os.path.join(current_work_directory, dependencies_folder, d['path'])
                dependencies.append(Dependency(path, d['repo'], d['version']))
            except KeyError as e:
                print(f'ERR: missed key {e} in {d}')

    return dependencies_folder, dependencies
        


def main():
    parser = argparse.ArgumentParser(prog='git repositories synchronizer')

    parser.add_argument('-cfg', '--config', required=True,
                        help='Path to configuration file. File must contain: '
                        '{ "dependencies_path" : "relatively configuration file" }')
    
    args = parser.parse_args()
    
    # Get path to config file
    cfg_path = args.config
    
    start_directory = os.getcwd()
    cfg_file_dir = os.path.dirname(cfg_path)
    cfg_file_basename = os.path.basename(cfg_path)
    
    if cfg_file_dir != '':
        os.chdir(cfg_file_dir)

    # Read configuration file
    with open(cfg_file_basename) as f:
        json_config = json.load(f)

    # Retrive dependencies from configuration file
    dependencies_path, deps_list = extract_dependencies(json_config)
    
    print(f'Dependencies folder: {dependencies_path}')
    for dep in deps_list:
        print('===============================================')
        print(f'Dependency: {os.path.basename(dep.path)}, version: {dep.version}')
        dep.sync()
    


if __name__ == "__main__":
    main()