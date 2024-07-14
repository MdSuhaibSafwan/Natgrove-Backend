import os
import sys
import importlib
from django.conf import settings


def get_base_model():
    module_name = (settings.BASE_MODEL).split(".")[1] + ".py"
    path = os.path.join(str(settings.PROJ_DIR), module_name)
    spec = importlib.util.spec_from_file_location("BaseModel", path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules["BaseModel"] = foo
    spec.loader.exec_module(foo)
    return foo.BaseModel
