# Django-starterkit

Starterkit for Python+Django project. There are several Django's apps as examples.


## Routing
Starterkit provides its own api for routing over models from Django Rest Framework. The routing mechanism of DRF relies on DjangoORM too much, though it provides some base classes with low coupling with DjangoORM, such classes don't provide usefull api for routing, request's argument deserialization, excepton handling and etc.   

Use api decorators for binding a controller method for a route:
- `@api.router_\[http_method\]('path/{path_param}/{?query_params=default_value}')`

For example:

```
@api.controller('orders/') <--- base path for controller
class OrderController():
    @api.router_get('path/{order_id}/{?is_paid=False}')
    def get_order(self, order_id: str, is_paid: bool ):
```
- `@api.without_authentication`- can be specified for controller class to disable authentication. For default `SessionAuthentication` for all methods.

- `@api.permissions('permission')`  - requires permission for an authenticated user, based on the Permission model from Django: e.x. `@api.permissions('market.view_product')`.

- `@api.raises(Exception, HTTPStatus)` - for binding exception for HTTP status code otherwise, an exception is handled by the base exception handler.

For example
```
    @api.router_post('login/')
    @api.raises(CustomException, HTTPStatus.BAD_REQUEST)
    def login(self):
        raise CustomException('error')
```

- You can get request payload by specification argument with name `request_body` in controller method and it automatically parsed to specified type: int, Dict, dataclass and etc. 
To obtain Django's request, just specify any argument with type `Request` :

```
@dataclass
class LoginDTO:
    username: str
    password: str
    
@dataclass
class AccountDTO:
    id: UUID
    email: str

@api.controller('')
@api.without_authentication
class AuthController:
    @inject
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    @api.router_post('login/')
    @api.raises(AuthenticationException, HTTPStatus.UNAUTHORIZED)
    def login(self, request: Request, request_body: LoginDTO):
        account = self._auth_service.authenticate(username=request_body.username, password=request_body.password)
        
        login(request, account.user)

        return AccountDTO(id=account.id, email=account.email)
````

If controller method returns dataclass (or some base type: int, bool, float and etc) it's serialized and pass as payload to Django response.


## Model

Because it's starterkit it uses DjangoORM as ORM:
- probably it should be known for all Django user
- admin panel, permission, authentication provided by Django are useful on project start.

But, if you have opportunity to change ORM, it's highly recommended to use [SQLAlchemy](https://www.sqlalchemy.org/) as ORM instead of DjangoORM. SQLAlchemy is more flexible, open to changes, has a great community.
Also, it doesn't have such problems as Django does: 
- absence of database level operations/constructions: cascade delete, join, default value and etc <- all these are handled only on python/django side.
- absence of [identity map](https://www.martinfowler.com/eaaCatalog/identityMap.html)

## Testing
[Pytest](https://docs.pytest.org/) is used for writing and running tests.

## Start project 

1. Install dependencies (pipenv creates virtualenv automatically): 
```
pipenv install
```

2. Copy `.env.example` file to `.env`
    
    2.1 Specify appropriate `DATABASE_URL` to access your database

3. Enter to shell - it runs your commands with parameters specified in `.env`
```
pipenv shell
```

Commands:
- fill database with initial data: `python manage.py runscript create_initial_data`
- create super user: `python manage.py createsuperuser`
- run server: `python runserver 0.0.0.0:8000`
- run test: `pytest`


