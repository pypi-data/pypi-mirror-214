import os


class Envvar:
    """Class which covers environment variables, with default values."""

    def __init__(self, name, **kwargs):

        environ = kwargs.get("environ")

        if environ is None:
            environ = os.environ

        self.name = name
        self.is_set = False
        self.value = None

        if name in environ:
            self.is_set = True
            self.value = environ[name]
        else:
            if "default" in kwargs:
                self.is_set = True
                self.value = kwargs["default"]
            else:
                self.is_set = False
                self.value = None
