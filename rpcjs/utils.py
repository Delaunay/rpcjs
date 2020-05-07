import inspect
import importlib


def find_main_module(function):
    file = inspect.getmodule(function).__file__
    folders = file.split('/')[:-1]

    def _find_top_module():
        for idx, folder in enumerate(folders):
            try:
                importlib.import_module(folder)
                return folder
            except:
                pass

    top_module = _find_top_module()

    if top_module is None:
        return None

    start = file.rfind(top_module)

    import_path = file[start:].split('.')[0].replace('/', '.')
    return import_path


def get_import_path(function):
    module = function
    modules = []

    while not modules or module.__name__ != modules[0]:
        modules.insert(0, module.__name__)
        module = inspect.getmodule(module)

    if modules[0] == "__main__":
        # being main does not mean we are not in a module
        import_path = find_main_module(function)

        if import_path is None:
            raise RuntimeError("Cannot register functions defined in __main__")

        return import_path

    return ".".join(modules[:-1])


def make_remote_call(function, *args, **kwargs):
    """Make a remote function call"""
    module = get_import_path(function)
    function_name = function.__name__
    return {
        'module': module,
        'function': function_name,
        'args': args,
        'kwargs': kwargs
    }


def exec_remote_call(state):
    """Execute a remote call"""
    args = state.get('args', [])
    kwargs = state.get('kwargs', {})

    module_name = state['module']
    function = state['function']

    module = __import__(module_name, fromlist=[''])
    fun = getattr(module, function)

    return fun(*args, **dict(kwargs))
