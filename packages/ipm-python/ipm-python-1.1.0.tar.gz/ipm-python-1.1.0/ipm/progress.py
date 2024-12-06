import requests
from tqdm import tqdm

def download_with_progress(url, destination):
    """带真实进度条的下载功能，动态调整每块大小"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    # 根据文件大小动态调整每块大小
    if total_size > 1024 * 1024 * 10:  # 超过 10MB
        block_size = 1024 * 1024  # 1MB
    elif total_size > 1024 * 1024:  # 超过 1MB
        block_size = 1024 * 100  # 100KB
    else:
        block_size = 1024  # 1KB

    with open(destination, 'wb') as file, tqdm(
        desc="下载中",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        bar_format="{l_bar}{bar} | 已下载: {n_fmt}/{total_fmt} [{rate_fmt}]"
    ) as bar:
        for data in response.iter_content(block_size):
            file.write(data)
            bar.update(len(data))
