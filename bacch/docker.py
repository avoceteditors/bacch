# Module Imports
import docker

from io import BytesIO

# Control Class
class Control():

    def __init__(self, args):

        client = docker.Client(base_url="unix://var/run/docker.sock")

        # Build Docker Image
        



