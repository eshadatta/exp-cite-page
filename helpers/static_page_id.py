class static_page_id:
    def __init__(self):
        self._init_version = "0.0.0"
        self._init_version_tag = "x-version"
        self._default_config_filename = "static.ini"
        self._default_pid_json_filename = "pid.json"
        self._default_id_types = ["doi", "uuid"]
    @property
    def init_version(self):
        return self._init_version
    @property
    def init_version_tag(self):
        return self._init_version_tag
    @property
    def default_config_filename(self):
        return self._default_config_filename
    @property
    def default_pid_json_filename(self):
        return self._default_pid_json_filename
    @property
    def default_id_types(self):
        return self._default_id_types
