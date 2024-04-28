class TestData:
    BASE_URL = 'https://stellarburgers.nomoreparties.site'
    CREATE_USER_URL = '/api/auth/register'
    LOGIN_USER_URL = '/api/auth/login'
    BASE_USER_URL = '/api/auth/user'
    ORDER_URL = '/api/orders'
    INGREDIENTS_URL = '/api/ingredients'

    ERROR_USER_EXISTS = 'User already exists'
    CREATE_USER_EXIST_ERROR = 'User already exists'
    CREATE_USER_FIELD_ERROR = 'Email, password and name are required fields'
    LOGIN_USER_FIELD_ERROR = 'email or password are incorrect'
    AUTH_ERROR = 'You should be authorised'
    NO_INGREDIENTS_ERROR = 'Ingredient ids must be provided'
