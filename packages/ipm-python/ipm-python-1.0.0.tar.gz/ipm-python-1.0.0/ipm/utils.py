import subprocess
from tqdm import tqdm

def run_command(command, show_progress=False):
    """运行命令并显示动态进度条（可选）"""
    if show_progress:
        with tqdm(total=100, desc="处理中", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as progress:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            while process.poll() is None:
                progress.update(10)
            progress.update(100 - progress.n)
    else:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.returncode, process.stdout.read(), process.stderr.read()
