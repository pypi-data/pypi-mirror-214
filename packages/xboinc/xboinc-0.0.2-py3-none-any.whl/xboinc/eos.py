import os, subprocess
from pathlib import Path
from time import sleep
import random

EOS_MGM_URL = 'root://eosuser.cern.ch'
eos_env = {**os.environ, 'EOS_MGM_URL': EOS_MGM_URL}

def _eos_path(path):
    path = Path(path).resolve()
    return path.as_posix().replace('home-','user/')

def eos_exists(path):
    try:
        path = Path(path).resolve()
        cmd = subprocess.run(['eos', 'find', '-name', path.name, _eos_path(path.parent)],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=eos_env)
        if cmd.returncode != 0 or cmd.stdout == b'':
            return False
        return Path(cmd.stdout.decode('UTF-8').strip()).resolve().stat().st_size!=0
    except Exception as e:
        print(f"Failed eos_exists for {path}!", e)
        return False

def eos_rm(path):
    try:
        path = Path(path).resolve()
        cmd = subprocess.run(['eos', 'rm', _eos_path(path)], stdout=subprocess.PIPE, env=eos_env)
        return cmd
    except Exception as e:
        print(f"Failed eos_rm for {path}!", e)

def mv_from_eos(source, target, maximum_trials=10, wait=2.7):
    try:
        target = Path(target).resolve()
        for i in range(maximum_trials):
            cmd = subprocess.run(['xrdcp', '--cksum', 'adler32', _eos_path(source), target.as_posix()])
            if cmd.returncode == 0 and target.exists() and target.stat().st_size!=0:
                eos_rm(source)
                return cmd
            if i != maximum_trials-1:
                print(f"Failed to move {str(source)} to {str(target)}!\nRetrying ({i})..")
                sleep(abs(wait+random.normalvariate(0, 0.1*wait)))
        print(f"Failed to move {str(source)} to {str(target)}!\nGiving up.")
        return cmd  
    except Exception as e:
        print(f"Failed to move {str(source)} to {str(target)}!", e)

def mv_to_eos(source, target, maximum_trials=10, wait=2.7):
    try:
        source = Path(source).resolve()
        target = Path(target, source.name).resolve()
        for i in range(maximum_trials):
            cmd = subprocess.run(['xrdcp', '--cksum', 'adler32', source.as_posix(), _eos_path(target)])
            if cmd.returncode == 0 and eos_exists(target):
                source.unlink()
                return cmd
            if i != maximum_trials-1:
                print(f"Failed to move {str(source)} to {str(target)}!\nRetrying ({i})..")
                sleep(abs(wait+random.normalvariate(0, 0.1*wait)))
        print(f"Failed to move {str(source)} to {str(target)}!\nGiving up.")
        return cmd
    except Exception as e:
        print(f"Failed to move {str(source)} to {str(target)}!", e)

