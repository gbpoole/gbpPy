from distutils.core import setup

from setuptools import setup, find_packages
from codecs import open
from os import path
import subprocess
import re, os

# Find the project root directory
git_repo = git.Repo(os.path.realpath(__file__), search_parent_directories=True)
dir_root = git_repo.git.rev_parse("--show-toplevel")

# The following code which handles versioning was patterned after a solution posted by 'Sven' here: 
# https://stackoverflow.com/questions/6786555/automatic-version-number-both-in-setup-py-setuptools-and-source-code

# Read the version file in the project directory
PROJECT_DIRECTORY = path.abspath(os.path.normpath(os.path.join(dir_root,'/../')))
VERSIONFILE=os.path.join(PROJECT_DIRECTORY,".version")
version_string = None
with open(VERSIONFILE,'rt') as fp:
    version_string = fp.read().strip()
if version_string==None or version_string=="":
    raise RuntimeError("Unable to load version string from %s." % (VERSIONFILE,))

# Check that there's a git repository in the project directory and that the
#   version in the .version file agrees with what's in the git tag.
if os.path.exists(os.path.join(PROJECT_DIRECTORY, '.git')):
    # Get the hash of the HEAD commit
    cmd = 'git rev-parse --verify --short HEAD'
    git_hash = subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()
    # Get the list of project tags
    tags =  [tag.strip() for tag in subprocess.check_output('git tag', shell=True, universal_newlines=True).strip().split('\n')]
    # If the tag in the version file is not in the list of project tags ...
    git_version_string = 'v'+version_string
    if not git_version_string in tags:
        # ... then add that tag to the HEAD commit
        cmd = 'git tag -a %s %s -m "tagged by setup.py"' % (git_version_string, git_hash)        
        print('Error: Version tag is out-of-date.  Run the following command to update it and then try again:')
        print(cmd)
        exit(1)
        # ... or, replace the previous three lines with the following commented-out line to do this automatically
        #subprocess.check_output(cmd, shell=True, universal_newlines=True)
else:
    raise RuntimeError("Unable to find the project's git repository at %s." % (PROJECT_DIRECTORY,))

print('Current version used by `setup.py`:',version_string)

package_name = "gbpPy"
setup(name=package_name,
      version=version_string,
      description="The gbpPy project's Python package",
      author='Gregory B. Poole',
      author_email='gbpoole@gmail.com',
      install_requires=['Click'],
      entry_points='''
          [console_scripts]
          sample_gbpPy_script=s.scripts.s:sample_gbpPy_script
          '''%s(package_name,package_name),
      packages=find_packages(),
     )
