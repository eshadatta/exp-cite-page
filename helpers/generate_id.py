import hashlib
import uuid
from .additional_id_formats import time_id

# start with a default id

# allow for other id schemes, must be a plugin
# allow for other configurations
   # pass by string
   # pass by length

class GenID:
    def __init__(self):
       pass

    def gen_default(self, len=10):
        return uuid.uuid4().hex[:len]

    def gen_time_based_id(self):
        return time_id.gen_time()


