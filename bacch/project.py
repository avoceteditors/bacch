# Module Imports
import pickle
import os.path
import os
import re

import bacch.read

###########################################
# Pickle Controllers

# Dump Data
def dump(log, data, path):
    try:
        f = open(path, 'bw')
        pickle.dump(data, f)
        f.close()
    except:
        log.warn("Unable to save read data")

# Load Data
def load(config, log, path):

    sync = config['ARGS']['sync']

    if not sync:

        try:
            log.debug("Checking for saved read")
            f = open(path, 'br')
            data = pickle.load(f)
            f.close()

            log.debug("Saved read loaded.")
            data.update_config(config, log)

        except:
            log.debug("Attempt failed")
            log.debug("Reading project from scratch")
            data = Project(config, log)
    else:
        log.debug("Reading project from scratch")
        data = Project(config, log)
        
    log.debug("Project loaded")

    return data

##########################################
# Project Controller Class
class Project():

    def __init__(self, config, log):
        self.config = config
        self.log = log
        self.file_data = {}

        self.source_path = self.config["SYSTEM"]["source"]

        # Read
        self.read_data()

    def update_config(self, config, log):
        self.config["ARGS"] = config["ARGS"]
        self.log = log


    def build_list(self, path, match):
        base = os.listdir(path)
        filelist = []
        for i in base:
            if re.match(match, i):
                filelist.append((i, os.path.join(path, i)))
        return filelist


    def read_data(self):

        ext = self.config["SYSTEM"]["extension"]
        match = '^.*?\.%s' % ext
        filelist = self.build_list(self.source_path, match)

        for i in filelist:
            fname = i[0]
            path = i[1]

            name = os.path.splitext(fname)[0]
            mtime = os.path.getmtime(path)

            try:
                old_mtime = self.file_list[name]['mtime']
                if old_mtime < mtime:
                    self.read_file(name, path, fname, mtime)

            except:
                self.read_file(name, path, fname, mtime)



    def read_file(self, name, path, fname, mtime):
        ctime = os.path.getctime(path)
        data = bacch.read.Read(self.config, path)

        stats = data.fetch_stats()
        stats['bytes'] = os.path.getsize(path)

        self.file_data[name] = {
                "filename": fname,
                "path": path,
                "ctime": ctime,
                "mtime": mtime,
                "data": data,
                "stats": stats
            }





