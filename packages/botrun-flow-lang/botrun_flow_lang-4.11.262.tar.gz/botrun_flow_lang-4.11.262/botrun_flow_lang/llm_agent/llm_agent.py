from pydantic import BaseModel
from typing import Optional


class LlmAgent(BaseModel):
    name: str = ""
    print_output: bool = True
    print_plotly: bool = True
    output: Optional[str] = None
    model: str = "openai/gpt-4o-2024-08-06"
    system_prompt: str
    gen_image: bool = False
