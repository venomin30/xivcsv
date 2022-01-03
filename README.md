# FFXIV CSVs
History of all CSVs from FFXIV patches.

## diffgen.py
Requires:
- python3: https://www.python.org/
- git: https://git-scm.com/
- GitPython: https://gitpython.readthedocs.io/en/stable/intro.html

The script will search the git commit history for the most recent commit that has a different Version.txt to the current one. It will then compare the contents of the src directory from that commit to the current src and generate diff files in a diff directory. These files contain all lines that have been added or modified since the previous version.
