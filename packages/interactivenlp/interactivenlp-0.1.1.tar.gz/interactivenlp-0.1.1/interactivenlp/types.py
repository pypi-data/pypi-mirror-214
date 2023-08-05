from enum import Enum
from typing import List, Optional, Callable


class BlockTypeEnum(Enum):
    NormalText = "normal"
    BoldText = "bold"
    ItalicText = "italic"
    UnderlineText = "underline"
    LightText = "light"
    Title = "title"
    Custom = "custom"

    def __str__(self):
        return self.value


class BlockLevelEnum(Enum):
    Paragraph = "paragraph"
    Sentence = "sentence"
    Word = "word"

    def __str__(self):
        return self.value


class Block:
    def __init__(self,  level: BlockLevelEnum, type: BlockTypeEnum, content: Optional[str],  subBlocks: Optional[List['Block']]):
        self.content = content
        self.type = type
        self.level = level
        self.subBlocks = subBlocks

    def __dict__(self):
        subBlocks = []
        if self.subBlocks is not None:
            subBlocks = [subBlock.__dict__ for subBlock in self.subBlocks]

        return {
            "content": self.content,
            "type": self.type.value,
            "level": self.level.value,
            "subBlocks": subBlocks
        }


class InteractiveRssType:
    def __init__(self, article: str, paragraphs: list[str]):
        self.article = article
        self.paragraphs = paragraphs


InteractiveFunctionType = Callable[[InteractiveRssType], List[Block]]

class InteractiveFunctionConfigurationType:
    def __init__(self, function: InteractiveFunctionType, name: str, description: str = None):
        self.name = name
        self.function = function
        self.description = description

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description
        }

class ModelConfigurationType:
    def __init__(self, name: str, description: str, functions: List[InteractiveFunctionConfigurationType],):
        self.name = name
        self.description = description
        self.functions = functions

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "functions": [function.__dict__() for function in self.functions]
        }
