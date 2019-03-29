from cx_Freeze import setup, Executable
import sys
# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = None
if sys.platform=='win32':
    base = 'Win32GUI' 

executables = [
    Executable('./source/game.py', base=base, targetName = 'I_Have_Time')
]

setup(name='I_Have_Time',
      version = '1.0',
      description = 'Game written entirely in Python using Pygame.',
      options = dict(build_exe = buildOptions),
      executables = executables)
