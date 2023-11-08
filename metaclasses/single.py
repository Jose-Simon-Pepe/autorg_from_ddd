class Single(type):

    """
    Metaclass of a singleton-type class
    This implements a ingenuous-like singleton pattern (no thread-safe), which will NOT WORK under multiprocessing.
    That would require value locking on given class, throught processes.
    """


    _instances = {}

    def __call__(cls, *args, **kwargs):
 
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]
