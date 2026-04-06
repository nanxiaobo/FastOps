from pydantic import BaseModel


class LogAnalyzeRequest(BaseModel):
    filename: str


class LogAskRequest(BaseModel):
    filename: str
    question: str


class LogExtractRequest(BaseModel):
    filename: str


