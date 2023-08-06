import json
import sys

from loguru import logger

try:
    from fastapi import File, UploadFile
    from pydantic import BaseModel
except ModuleNotFoundError as inst:
    package_not_found = inst.name
    error_mod = sys.modules[__name__].__name__
    error_mod = error_mod.split(".")[-1]
    msg = f"Error when importing {error_mod} module: install '{package_not_found}' to use it."
    logger.error(msg)
    exit(1)


class ValueArgs(BaseModel):
    value: object
    args: dict



class ExtractValueArgsFastAPI:
    """
        Decorator used to extract value and args from services.
        It works with FastAPI framework.

        Example:
               >>> @app.post('/files', response_class=JSONResponse)
               >>> @ExtractValueArgsFastAPI(file=True)
               >>> def test(file, args):


        Args:
            file (bool): True if the request posts files. Default: `False`
    """
    def __init__(self, file: bool = False):
        self.file = file

    def __call__(self, f):
        def extract_file_args(file: UploadFile = File(), args: UploadFile = File()):#
            args_content = args.file.read().decode()
            args = json.loads(args_content)
            return f(file, args)

        def extract_value_args(value_args: ValueArgs):
            value = value_args.value
            args = value_args.args
            return f(value=value, args=args)

        if self.file:
            return extract_file_args
        else:
            return extract_value_args


