import modutil


mod, __getattr__ = modutil.lazy_import(__name__,
                                       ['tests.test_data.A', '.B', '.C as still_C'])

def trigger_A():
    return mod.A

def trigger_B():
    return mod.B

def trigger_C():
    return mod.still_C
