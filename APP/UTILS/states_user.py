from aiogram.fsm.state import StatesGroup, State


class add_plan_user(StatesGroup):
    GET_PROJECT_NAME = State()
    GET_START_TIME = State()
    GET_END_TIME = State()
    GET_DATE = State()


class add_fact_user(StatesGroup):
    GET_PROJECT_NAME = State()
    GET_COMMENT = State()
    GET_START_TIME = State()
    GET_END_TIME = State()
    GET_DATE = State()
