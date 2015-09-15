# flask restufl实验项目

# use authenticate example::
    def authenticate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not getattr(func, 'authenticated', True):
                return func(*args, **kwargs)

            acct = basic_authentication()  # custom account lookup function

            if acct:
                return func(*args, **kwargs)

            restful.abort(401)
        return wrapper


    class Resource(restful.Resource):
        method_decorators = [authenticate]   # applies to all inherited resources
        
        
https://github.com/sgray10/flask-restful-auth-microservice
        
https://github.com/marchon/Flask-API-Server
https://github.com/karnikamit/RESTful-API-with-Python-and-Flask/blob/master/fun_api
https://github.com/vctandrade/flask-digest
https://github.com/inveniosoftware/flask-sso/blob/master/flask_sso/__init__.py