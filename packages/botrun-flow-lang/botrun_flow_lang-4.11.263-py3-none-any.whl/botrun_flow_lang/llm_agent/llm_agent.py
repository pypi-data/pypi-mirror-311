from pydantic import BaseModel
from typing import Optional


class LlmAgent(BaseModel):
    """
    @include_in_history: 是否將這次的回答加入 history
    """

    name: str = ""
    print_output: bool = True
    print_plotly: bool = True
    output: Optional[str] = None
    model: str = "openai/gpt-4o-2024-08-06"
    system_prompt: str
    gen_image: bool = False
    include_in_history: bool = True
