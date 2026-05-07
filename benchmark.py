import random
import time
import psutil
import logging
import pandas as pd

# налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("experiment.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def generate_data(size, data_type="random"):
    random.seed(42)
    if data_type == "random":
        return [random.randint(0, 1_000_000) for _ in range(size)]
    elif data_type == "nearly_sorted":
        arr = list(range(size))
        swaps = int(size * 0.05)
        for _ in range(swaps):
            idx1, idx2 = random.randint(0, size-1), random.randint(0, size-1)
            arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
        return arr

def measure_performance(algo_func, algo_name, size, data_type, runs=30):
    results = []
    logging.info(f"тестування: {algo_name} | розмір: {size} | тип: {data_type}")
    
    for i in range(runs):
        try:
            data = generate_data(size, data_type)
            process = psutil.Process()
            psutil.cpu_percent(interval=None)
            mem_before = process.memory_info().rss
            
            start = time.perf_counter()
            algo_func(data)
            duration = time.perf_counter() - start
            
            mem_after = process.memory_info().rss
            cpu_usage = psutil.cpu_percent(interval=None)
            memory_used = max(0, (mem_after - mem_before) / 1024 / 1024)
            
            results.append({
                "run": i + 1, "algorithm": algo_name, "size": size,
                "type": data_type, "time_sec": duration,
                "memory_mb": memory_used, "cpu_percent": cpu_usage
            })
        except Exception as e:
            logging.error(f"помилка у {algo_name} (запуск {i+1}): {str(e)}")
            
    return results