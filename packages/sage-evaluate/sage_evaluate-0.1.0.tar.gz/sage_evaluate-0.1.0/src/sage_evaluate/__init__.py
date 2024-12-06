import os
import evaluate

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def load(name: str):
    wer_metric_path = os.path.join(BASE_PATH, name)
    if not os.path.exists(wer_metric_path):
        raise ValueError(f"the metric {name} not found")
    return evaluate.load(wer_metric_path)

