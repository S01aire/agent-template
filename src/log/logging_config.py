import logging
from pathlib import Path

def setup_logger(
    name,
    log_file='src/log/run.log',
    level=logging.INFO,
):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(formatter)

        logger.addHandler(fh)
    
    return logger

def clean_log(log_file: str = "src/log/run.log") -> None:
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
