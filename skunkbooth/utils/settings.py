from collections.abc import MutableMapping

from yaml import dump, safe_load

from skunkbooth.data.defaults import _settings


class _makesettings(MutableMapping):
    """Metaclass for settings"""

    def __init__(self, *args):
        try:
            with open(_settings["SETTINGS_FILE"]) as f:
                self.store = safe_load(f)
                if self.store is None:
                    self.store = {}
        except FileNotFoundError:
            self.store = {}

        # Load default values if unset
        for i in _settings:
            if i not in self.store:
                self.store[i] = _settings[i]

        with open(_settings["SETTINGS_FILE"], "w") as f:
            f.write(dump(self.store))

    def __getitem__(self, key: str):
        return self.store[self._keytransform(key)]

    def __setitem__(self, key: str, val: str):
        self.store[self._keytransform(key)] = val
        with open(self["SETTINGS_FILE"], "w") as f:
            f.write(dump(self.store))

    def __delitem__(self, key: str):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key: str) -> str:
        return key


class settings(metaclass=_makesettings):
    """Produced by _makesettings"""

    pass
