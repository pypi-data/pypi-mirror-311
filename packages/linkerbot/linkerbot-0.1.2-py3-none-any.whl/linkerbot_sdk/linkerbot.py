import os
import requests
from urllib.parse import urljoin
from tqdm import tqdm


class LinkerBot:
    """A simple SDK class with two utility methods."""

    def __init__(self, token=None):
        self.token = token
        self.default_cache_dir = "/Users/a1/linkerbot-sdk/test"
    
    def download_dataset(self, dataset_dir, cache_dir=None):
        """Download the dataset.
        
        Args:
            dataset_id: The ID of the dataset to download
            cache_dir: The directory to save files to. Defaults to /Users/a1/linkerbot-sdk/test
        """
        # 使用默认缓存目录如果没有指定
        cache_dir = cache_dir or self.default_cache_dir
        prefix = "graspnet"
        baseUrl = "https://columbus-robot-dev.obs.cn-north-4.myhuaweicloud.com/"
        keys = [
            {
                "key": "openData/graspnet/",
                "size": 0
            },
            {
                "key": f"openData/graspnet/dof_grasp_labels/collision_label.zip",
                "size": 1024 * 1024 * 400
            },
        ]

        # 确保基础缓存目录存在
        os.makedirs(cache_dir, exist_ok=True)

        for key in keys:
            # 构建完整的本地路径
            local_path = os.path.join(cache_dir, key['key'].lstrip('/'))
            
            if key['key'].endswith('/'):
                # 如果是目录路径，创建目录
                os.makedirs(local_path, exist_ok=True)
                print(f"Created directory: {local_path}")
            else:
                # 如果是文件，下载文件
                # 确保文件的目录存在
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # 构建完整的URL
                url = urljoin(baseUrl, key['key'])
                
                # 下载文件
                print(f"Downloading: {os.path.basename(local_path)}")
                response = requests.get(url, stream=True)
                response.raise_for_status()  # 确保请求成功
                
                # 获取文件大小
                total_size = key['size']
                downloaded_size = 0
                
                # 创建进度条
                progress_bar = tqdm(
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    desc=os.path.basename(local_path)
                )
                
                # 写入文件，同时更新进度条
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        size = f.write(chunk)
                        downloaded_size += size
                        progress_bar.update(size)
                
                progress_bar.close()

        return cache_dir
