from pydantic import BaseModel, validator


class Config(BaseModel):
    jx3api_key: str=""
    jx3_tuilan_ticket: str=""
    jx3wss_token: str=""
    jx3_command_header: str=""
    jx3_bot_name:str ="团团"