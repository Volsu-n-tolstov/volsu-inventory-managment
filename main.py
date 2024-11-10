import logfire

from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from models.base_model import init
from middlewares.auth import basic_auth
from schemas.graphql.query import Query
from schemas.graphql.mutation import Mutation
from configs.graphql import get_graphql_context
from configs.enviroment import get_environment_variables
from configs.database import engine

from routers.v1.item_router import router as ItemRouter
from routers.v1.transaction_router import router as TransactionRouter
from routers.v1.predict_router import router as PredictRouter

# Получаем переменные окружения
env = get_environment_variables()

# Инициализируем FastAPI приложение
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(ItemRouter)
app.include_router(TransactionRouter)
app.include_router(PredictRouter)

# Настраиваем GraphQL
schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema=schema,
    graphiql=env.DEBUG_MODE,
    context_getter=get_graphql_context
)

# Интегрируем GraphQL в основное приложение
app.include_router(
    graphql_app,
    prefix="/graphql",
    include_in_schema=False,
    dependencies=[Depends(basic_auth)]
)

# Инициализируем модели данных
init()

# Настраиваем логирование через Logfire
# logfire.configure(token=env.LOGFIRE_PROJECT_API_KEY)
# logfire.instrument_fastapi(app)
# logfire.instrument_sqlalchemy(engine=engine)

# Редирект с корневого пути на документацию
@app.get("/")
def root():
    return RedirectResponse("/docs")
