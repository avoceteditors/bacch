# Module Imports
import pickle
import bacch
import os.path

def load_data(path):

    bacch.log.info("Data Handler: Initializing")
    bacch.log.debug('Checking for Saved Data')
    if os.path.exists(path) and not bacch.args.update:
        try:
            f = open(path, 'rb')
            data = pickle.load(f)
            f.close()

            bacch.log.debug('Saved Data Loaded')

            # Test for Sync
            if data.sync():
                bacch.log.debug("Updating Data")
                data.update()
                bacch.log.debug("Data Updated")

        except:
            bacch.log.debug("No Data Found, building...")
            data = bacch.DataHandler()
    else:
        bacch.log.debug("No Data Found, building...")
        data = bacch.DataHandler()

    bacch.log.info("Data Handler: Ready")
    return data

def save_data(path, data):
    bacch.log.info("Data Handler: Savng")
    try:
        f = open(path, 'wb')
        pickle.dump(data, f)
        f.close()
    except:
        bacch.log.warn("Error saving data handler")
    


