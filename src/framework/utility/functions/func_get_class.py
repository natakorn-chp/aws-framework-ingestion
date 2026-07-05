
import sys
from inspect import getmembers, isclass

def get_class_by_name(module_name: str, class_name: str):

    for name, obj in getmembers(sys.modules[module_name], isclass):
        if name == class_name:
            return obj
        
    raise ValueError(f"the class name '{class_name}' not found")