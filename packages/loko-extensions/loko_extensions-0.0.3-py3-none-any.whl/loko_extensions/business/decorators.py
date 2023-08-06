import functools
import json


def extract_value_args(_request=None, file=False):
    """
            Decorator used to extract value and args from services.
            It works with Flask and Sanic frameworks.

            Example:
                >>> # using Flask
                >>> @app.route("/files", methods=["POST"])
                >>> @extract_value_args(_request=request, file=True)
                >>> def test(file, args):

                >>> # using Sanic
                >>> @bp.post('/files')
                >>> @extract_value_args(file=True)
                >>> async def test(file, args):

            Args:
                _request (werkzeug.local.LocalProxy): Flask request. Default: `None`
                file (bool): True if the request posts files. Default: `False`
                """
    def get_value_args(f):
        @functools.wraps(f)
        def tmp(*args, **kwargs):
            request = _request or args[0]
            value = request.files['file'] if file else request.json.get('value')
            args = request.files['args'] if file else request.json.get('args')
            if file:
                ### flask ###
                if _request:
                    args = args.read().decode()
                ### sanic ###
                else:
                    args = args[0].body.decode()
                args = json.loads(args)
            return f(value, args)
        return tmp
    return get_value_args
