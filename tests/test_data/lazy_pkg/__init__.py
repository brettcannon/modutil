import modutil

mod, __getattr__ = modutil.lazy_import(__name__, {'..A'})

def trigger_A():
    return mod.A
