from datetime import datetime, timedelta


class Cache(dict):
    """
    Master class of cache
    Give access to models via dict notation. Ex:
    >>> cache = Cache(env)
    >>> cache['res.partner'].field_exists('name')
    >>> True
    """

    def __init__(self, env, default_expiration_time: int = 60):
        super().__init__()
        self._env = env
        self.config = {
            'expiration': {
                'default': default_expiration_time,
            }
        }

    def __str__(self):
        return f"Cache({self._env})"

    def __missing__(self, key: str):
        if not isinstance(key, str):
            raise TypeError(f"Cache key must be a string, not {type(key)} ({key})")
        self[key] = CacheModel(self, key)
        return self[key]

    @property
    def env(self):
        return self._env


class CacheModel(dict):
    """
    Basically a dict of CacheRecord
    Allows to perform operations on model level with dict notation. Ex:
    >>> cache = Cache(env)
    >>> cache_record_7 = cache['res.partner'][7]
    give access to the cache infos of res.partner(7)
    """

    def __init__(self, cache: "Cache", name: str):
        super().__init__()
        self._name = name
        self._cache = cache
        self._fields = cache.env[name].fields_get()

    def __str__(self):
        return f"CacheModel({self._name})"

    def __missing__(self, key: int):
        if not isinstance(key, int):
            raise TypeError(f"Record id must be an int, not {type(key)} ({key} on model {self.name})")
        self[key] = CacheRecord(self, key)
        return self[key]

    @property
    def api(self):
        return self._cache.env[self._name]

    @property
    def cache(self):
        return self._cache

    @property
    def name(self):
        return self._name

    def field_exists(self, field: str):
        return field in self._fields




class CacheRecord(dict):
    def __init__(self, model: "CacheModel", res_id: int):
        super().__init__()
        self._model = model
        self._env_record = model.api.browse(res_id)

    def __str__(self):
        return f"CacheRecord({self._env_record})"

    def __missing__(self, key: str):
        key = str(key)
        if not self._model.field_exists(key):
            raise KeyError(f"Field {key} does not exist on model {self._model.name}")

        self[key] = CacheField(self, key)
        return self[key]

    @property
    def env_record(self):
        return self._env_record

    @property
    def model(self):
        return self._model



class CacheField:
    def __init__(self, record: "CacheRecord", name: str, validity_duration: int = None):
        self._record = record
        self._value = None
        self.name = name
        self.validity_duration = validity_duration
        self.expiration = None


    def __str__(self):
        return f"{self.value}"


    def _read(self):
        validity_duration = self.validity_duration or self._record.model.cache.config['expiration']['default']
        self.value = self._record.env_record.read([self.name])[0].get(self.name)
        self.expiration = datetime.utcnow() + timedelta(seconds=validity_duration)

    @property
    def is_expired(self):
        return self.expiration is None or (datetime.utcnow() > self.expiration)

    def get(self):
        if self.is_expired:
            self._read()
        return self.value
