import time
import sys
import logging

# 1) Temel logger ayarları
logger = logging.getLogger("AstroVision")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logger.addHandler(handler)

def log(msg: str):
    # 2) Basit bir log fonksiyonu
    logger.info(msg)

def timed(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start
        prompt_snippet = getattr(args[0], "prompt", "")[:30]
        log(f"generate_scene: prompt={args[0].prompt[:30]!r}... took {duration:.2f}s")
        return result
    return wrapper