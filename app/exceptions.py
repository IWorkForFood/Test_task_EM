from fastapi import status, HTTPException

TokenNotFound = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Токен истек, братиш")


NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')
