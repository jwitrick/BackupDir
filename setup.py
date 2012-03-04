#!/usr/bin/python

from distutils.core import setup

setup (name = "BackupDir",
       version = "BACKUPDIR_VERSION",
       author = "Justin Witrick",
       author_email = "justin@thewitricks.com",
       description = "This app is for easily backing up a directory using duplicity"
       url = "",
       packages = ['BackupDir'],
       scripts = ['backupdir']
)
