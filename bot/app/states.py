"""FSM states for the lead intake flow."""
from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    description = State()
    email = State()
