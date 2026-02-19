from fastapi import status, HTTPException

TokenNotFound = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")


NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail='Токен истёк')

NotExcistingCredentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Неверные учётные данные ')
