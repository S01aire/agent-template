
import importlib
import pkgutil

from src.model.tool import BaseTool
from src.log.logging_config import setup_logger


logger = setup_logger("tool_register")

TOOL_CLASSES: dict[str, type[BaseTool]] = {}

def register_tool(cls: type[BaseTool]):
    if cls.name in TOOL_CLASSES:
        raise ValueError(f"工具重复注册: {cls.name}")

    TOOL_CLASSES[cls.name] = cls
    logger.info(f"工具注册:{cls.name}")

    return cls

def load_tools(package_name: str = "src.tool"):
    package = importlib.import_module(package_name)

    for module_info in pkgutil.walk_packages(
        package.__path__,
        prefix=package.__name__ + '.'
    ):
        name = module_info.name

        if module_info.ispkg:
            continue

        if name.endswith(".registry"):
            continue

        importlib.import_module(name)



if __name__ == "__main__":
    load_tools()

    