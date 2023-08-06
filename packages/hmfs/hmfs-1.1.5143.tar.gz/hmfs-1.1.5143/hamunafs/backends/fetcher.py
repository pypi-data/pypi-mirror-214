from concurrent.futures import ThreadPoolExecutor
from hamunafs.utils.singleton_wrapper import Singleton
import requests
import httpx
import shutil
import traceback
import aiofile


class FileFetcher(Singleton):
    def __init__(self, workers=10, proc_timeout=20) -> None:
        self.pool = ThreadPoolExecutor(max_workers=workers)

    def download_file(self, url, path, tries=0):
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                with open(path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        
            return path
        except Exception as e:
            traceback.print_exc()
            if tries > 3:
                return None
            return self.download_file(url, path, tries+1)

    def fetch_file(self, url, path):
        future = self.pool.submit(self.download_file, url, path, 0)
        result = future.result(timeout=60)
        return result

    async def fetch_file_async(self, url, path, tries=0):
        try:
            async with aiofile.async_open(path, 'wb') as f:
                async with httpx.AsyncClient() as client:
                    async with client.stream("GET", url) as resp:
                        async for chunk in resp.aiter_raw(1024 * 1024):
                            await f.write(chunk)
            return path
        except Exception as e:
            if tries < 3:
                return await self.fetch_file_async(url, path, tries+1)
            return None

file_fetcher = FileFetcher()