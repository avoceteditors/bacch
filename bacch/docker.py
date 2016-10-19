# Module Imports
import docker

# Control Class
class Control():

    def __init__(self, args):

        client = docker.Client(base_url="unix://var/run/docker.sock")
        odb_passwd = "testing"
        dfile = dockerfile(odb_passwd)


def dockerfile(passwd):

    image = """
    FROM orientdb:latest
    MAINTAINER Avocet Editors <kenneth@avoceteditors.com>

    ENV ORIENTDB_ROOT_PASSWORD %s
    
    RUN mkdir /data
    RUN mkdir /document

    VOLUME ["/data", "/document"]
    """ % passwd

    return image
