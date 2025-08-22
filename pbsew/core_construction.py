import importlib.metadata
import pkgutil
import inspect

from process_bigraph import Process, Step, ProcessTypes, Composite


def construct_core(verbose: bool) -> ProcessTypes:
    core = ProcessTypes()
    counter = 0
    for name, clazz in load_local_modules(verbose):
        core.register_process(name, clazz)
        if verbose:
            counter += 1
            print(f'Registered `{name}` to `{clazz.__name__}`')
    if verbose:
        print(f"Registered {counter} processes...")
    return core

def load_local_modules(verbose: bool) -> list[tuple[str, Process | Step ]]:
    if verbose:
        print("Loading local registry...")
    packages = importlib.metadata.distributions()
    classes_to_load = []
    for package in packages:
        if not does_package_require_process_bigraph(package):
            continue
        # If a package requires BSail, it probably has abstractions for us; worth importing.
        if verbose:
            print(f'Relevant Processes found in `{package.name}`...')
        classes_to_load += recursive_dynamic_import(package.name, verbose)

    return classes_to_load

def does_package_require_process_bigraph(package: importlib.metadata.Distribution) -> bool:
    for entry in ([] if package.requires is None else package.requires):
        if "process-bigraph" in entry:
            return True
    return False


def recursive_dynamic_import(package_name: str, verbose: bool) -> list[tuple[str, Process | Step ]]:
    classes_to_import = []
    adjusted_package_name = package_name.replace("-", "_")
    try:
        module = importlib.import_module(adjusted_package_name)
    except ModuleNotFoundError:
        # TODO: Add code to try and find correct module name via accessing `top_level.txt`,
        #  and getting the correct module name
        # find top-level.txt
        # find correct module name
        # return recursive_dynamic_import(correct_module_name)
        raise ModuleNotFoundError(f"module {adjusted_package_name} not found")
    class_members = inspect.getmembers(module, inspect.isclass)
    if verbose:
        print(f"Processing {len(class_members)} members...")
    for class_name, clazz in class_members:
        if clazz == Process:
            if verbose:
                print(f'Process `{class_name}` skipped, because it is `Process` itself.')
            continue
        if clazz == Step:
            if verbose:
                print(f'Process `{class_name}` skipped, because it is `Step` itself.')
            continue
        if clazz == Composite:
            if verbose:
                print(f'Process `{class_name}` skipped, because it is `Composite` itself.')
            continue
        if issubclass(clazz, Process):
            if verbose:
                print(f'Process `{class_name}` added to queue!')
            classes_to_import.append((f"{package_name}.{class_name}", clazz))
        if issubclass(clazz, Step):
            if verbose:
                print(f'Step `{class_name}` added to queue!')
            classes_to_import.append((f"{package_name}.{class_name}", clazz))
        if verbose:
            print(f'Invalid `{class_name}` skipped; not a Process nor Step!')

    path = module.__path__ if hasattr(module, '__path__') else "<No `__path__` attr>"
    modules_to_check = pkgutil.iter_modules(module.__path__) if hasattr(module, '__path__') else []
    if verbose:
        print(f"Checking for modules in `{module.__name__}` [path: {path}]...")
    for _module_loader, subname, isPkg in modules_to_check:
        # if not isPkg: continue
        if verbose:
            print(f"Found: {adjusted_package_name}.{subname}")
        classes_to_import += recursive_dynamic_import(f"{adjusted_package_name}.{subname}", verbose)
    if verbose:
        print(f'Found {len(classes_to_import)} classes in `{package_name}` to import'"")
    return classes_to_import
