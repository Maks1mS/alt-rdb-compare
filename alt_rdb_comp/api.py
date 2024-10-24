import requests_cache
from requests_cache import timedelta

class ALTLinuxRDBApi:
    def __init__(self, base_url="https://rdb.altlinux.org/api") -> None:
        self._session = requests_cache.CachedSession(
            cache_name="rdb_altlinux_http_cache",
            use_cache_dir=True,
            # Cache-Control header is missing, so expire_after is used
            # cache_control = True,
            expire_after=timedelta(hours=3),
        )

        self.base_url = base_url
        pass

    def _call(self, method, endpoint, params = None):
        req = self._session.request(
            method, 
            f'{self.base_url}{endpoint}', 
            params,
        )
        json = req.json()
        return json


    def export_branch_binary_packages(self, branch = "sisyphus", arch = None) -> dict:
        params = None
        if arch:
            params = {'arch': arch}

        return self._call('GET', f"/export/branch_binary_packages/{branch}", params)
