import importlib.metadata
import pkgutil
import inspect
import re

from process_bigraph import Process, Step, ProcessTypes

def construct_core() -> ProcessTypes:
    core = ProcessTypes()
    for name, clazz in load_local_modules():
        core.register(name, clazz)
    return core

def load_local_modules() -> list[tuple[str, Process | Step ]]:
    print("Loading local registry...")
    packages = importlib.metadata.distributions()
    classes_to_load = []
    for package in packages:
        if not does_package_require_process_bigraph(package): continue
        # If a package requires BSail, it probably has abstractions for us; worth importing.
        classes_to_load += recursive_dynamic_import(package.name)

    return classes_to_load

def does_package_require_process_bigraph(package: importlib.metadata.Distribution) -> bool:
    for key in package.metadata:
        if key != "Requires-Dist": continue
        if not re.match("process-bigraph \([=><\d.]+,?[=><\d.]+\)", package.metadata[key]): continue
        return True
    return False


def recursive_dynamic_import(package_name: str) -> list[tuple[str, Process | Step ]]:
    classes_to_import = []
    module = importlib.import_module(package_name)
    for class_name, clazz in inspect.getmembers(module, inspect.isclass):
        if not (issubclass(clazz, Process) or issubclass(clazz, Step)): continue
        importlib.import_module(package_name + "." + class_name)
        classes_to_import.append((class_name, clazz))

    for _module_loader, subname, isPkg in pkgutil.iter_modules(module.__path__):
        if not isPkg: continue
        classes_to_import += recursive_dynamic_import(f"{package_name}.{subname}")

    return classes_to_import
