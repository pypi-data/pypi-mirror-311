import math
from tqdm import tqdm

class ProgressBar:
    """自定义进度条类，支持实时大小显示和动态速率更新"""
    def __init__(self, total_size, description="下载中"):
        self.total_size = total_size
        self.description = description
        self.progress = tqdm(
            desc=self.description,
            total=self.total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            bar_format="{l_bar}{bar} | 已下载: {n_fmt}/{total_fmt} [{rate_fmt}]"
        )

    def update(self, chunk_size):
        self.progress.update(chunk_size)

    def close(self):
        self.progress.close()
