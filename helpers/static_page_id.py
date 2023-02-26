class static_page_id:
    def __init__(self):
        self._init_version = "0.0.0"
        self._init_version_tag = "x-version"
    @property
    def init_version(self):
        return self._init_version
    # add default filenames as this class's properties
    @property
    def init_version_tag(self):
        return self._init_version_tag
