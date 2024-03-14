from aiogram.fsm.state import StatesGroup, State


class add_plan_admin(StatesGroup):
    GET_ID = State()
    GET_PROJECT_NAME = State()
    GET_START_TIME = State()
    GET_END_TIME = State()
    GET_DATE = State()


class add_employer(StatesGroup):
    GET_ID = State()
    GET_NAME = State()
    GET_SURNAME = State()
    GET_PERMISSION = State()
    
    
    
class delete_employeer(StatesGroup):
    GET_ID = State()


class change_permissions(StatesGroup):
    GET_ID = State()
    GET_PERMISSION = State()
