import psutil
from datetime import datetime

def check_health():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    
    print(f"\n{'='*50}")
    print(f"ATLAS SYSTEM HEALTH - {datetime.now()}")
    print(f"{'='*50}")
    print(f"CPU:  {cpu:.1f}%")
    print(f"RAM:  {mem.used/(1024**3):.2f}GB / {mem.total/(1024**3):.2f}GB ({mem.percent:.1f}%)")
    print(f"Free: {mem.available/(1024**3):.2f}GB")
    print(f"{'='*50}\n")

check_health()
