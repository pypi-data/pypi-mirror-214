import os
from fastapi import (
    FastAPI,
    Depends,
)
from dotenv import load_dotenv

from constants.env import *
from app.api.v1 import *
from databases.base import get_session


load_dotenv()
app = FastAPI()

# app.include_router(users.router)
# app.include_router(tasks.router)


@app.get(ROOT_ROUTE)
def home_url(session=Depends(get_session)):
    return dict(message=os.getenv(WELCOM_MESSAGE_ENV_VARIABLE_KEY, EMPTY_STRING))


if __name__ == "__main__":
    import uvicorn

    host = os.getenv(HOST_ENV_VARIABLE_KEY, HOST_DEFAULT)
    port = int(os.getenv(PORT_ENV_VARIABLE_KEY, PORT_DEFAULT))

    uvicorn.run(MAIN_KEY, host=host, port=port, reload=True)
