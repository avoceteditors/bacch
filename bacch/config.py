# Moduel Imports
import sys
import os.path
import json
import sysconfig
import shutil

########################################
# Configuration Functions

# Load Config
def load_config(path):
    f = open(path, 'r')
    config = json.load(f)
    f.close()

    return config


# Set Default
def set_config(path, config):
    f = open(path, 'w')
    json.dump(config, f)
    f.close()

# Configure Bacch
def configure(args):

    # Find Path to System Config
    if sys.platform == 'windows':
        base_user = os.path.join(
                sysconfig.get_path('data', 'nt_user'), 'etc', 'bacch', 'book.json')
    else:
        base_user = os.path.join(
                sysconfig.get_path('data', 'posix_user'), 'etc', 'bacch', 'book.json')

    # Update Configs
    if not os.path.exists(args.config):
        shutil.copy(base_user, 'book.json')
        config = load_config('book.json')
    elif os.path.exists(args.config) and args.update_config:
        shutil.copy(args.config, 'book-old.json')

        config_old = load_config('book-old.json')
        config_new = load_config(base_user)
        
        defaults = ["SYSTEM", "METADATA"]
        config = {"BUILDS": {}}
        for i in defaults:
            base = config_old[i].copy()
            base.update(config_new[i])
            config[i] = base
        set_config("book.json", config)
        set_config("book-default.json", config_old)
    else:
        config = load_config(args.config)


    update = {
        "ARGS": {
            "verbose": args.verbose,
            "sync": args.sync,
            "debug": args.debug
        }    
    }
    config.update(update)
    return config
