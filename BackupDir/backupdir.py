#!/usr/bin/env python
import sys
import os
import subprocess
from ConfigParser import RawConfigParser as ConfParser
from ConfigParser import Error

class BackupDir(object):
    def __init__(self, directory, config_file="backupdir.ini"):
        self._setup_config_parser(config_file)
        self.set_environment_keys()
        full_dir_path = self._get_dir_path(directory)
        bucket_name = self._get_bucket_name_from_path(full_dir_path)
        self._backup_dir(bucket_name, full_dir_path)

    def _setup_config_parser(self, config_file):
        self.config_parser = ConfParser()
        self.config_parser.read(config_file)

    def _get_section_option(self, section, option):
        if self.config_parser.has_option(section, option):
            return self.config_parser.get(section, option)
        else:
            return None

    def _get_dir_path(self, dir_name):
        if os.path.isabs(dir_name):
            return dir_name
        else:
            return os.path.abspath(dir_name)

    def _get_bucket_name_from_path(self, dir_name):
        return os.path.basename(dir_name)

    def set_environment_keys(self):
        self.set_encryption_passphrase(self._get_section_option('backend', 'passphrase'))
        username = self._get_section_option('cloudfiles', 'username')
        apikey = self._get_section_option('cloudfiles', 'apikey')
        self.set_cloud_credentials(username, apikey)

    def set_encryption_passphrase(self, phrase):
        os.environ['PASSPHRASE'] = phrase

    def set_cloud_credentials(self, username, apikey):
        os.environ['CLOUDFILES_USERNAME'] = username
        os.environ['CLOUDFILES_APIKEY'] = apikey

    def daemonize(self):
        try:
            if os.fork() != 0:
                sys.exit(0)
            os.setsid()
        except:
                pass

    def _backup_dir(self, bucket_name, dir_path):
        print "%s%s"%(self._get_section_option('backend', 'storage_location'), bucket_name)
        print subprocess.call(["duplicity", "%s"%dir_path, "%s%s"%(self._get_section_option('backend','storage_location'), bucket_name)])



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Error. You must Enter a directory to backup."
        exit
    directory = sys.argv[1]
    if len(sys.argv) ==3:
        backup_dir = BackupDir(directory, sys.argv[2])
    else:
        backup_dir = BackupDir(directory)
