import requests_cache
from requests_cache import timedelta
from alt_rdb_comp.utils import eprint

class ALTLinuxRDBApi:
    """
    A class to interact with the ALTLinux RDB (Repository Database) API.
    Utilizes caching to improve performance and reduce redundant API calls.
    """
    
    def __init__(self, base_url="https://rdb.altlinux.org/api") -> None:
        """
        Initializes the API instance with a cached HTTP session.

        :base_url: The base URL for the ALTLinux RDB API.
        """
        self._session = requests_cache.CachedSession(
            cache_name="rdb_altlinux_http_cache",
            # Cache is located at XDG_CACHE_HOME/{cache_name}.sqlite
            use_cache_dir=True,
            # Cache-Control header is missing, so expire_after is used
            # cache_control = True,
            expire_after=timedelta(hours=3),
        )

        self.base_url = base_url
        pass

    def _call(self, method, endpoint, params = None):
        """
        Internal method to make an HTTP request to the API and return the JSON response.
        """
        try:
            req = self._session.request(
                method, 
                f'{self.base_url}{endpoint}', 
                params=params,
            )
            return req.json()
        except requests_cache.exceptions.RequestException as e:
            eprint(f"HTTP Request failed: {e}")
            return {}
        except ValueError:
            eprint("Failed to decode JSON response")
            return {}


    def export_branch_binary_packages(self, branch = "sisyphus", arch = None) -> dict:
        """
        Retrieves binary packages for a specific branch and architecture.
        """
        # For better perfomance, possibly better
        # use cache for arch = None if it is available, 
        # because it contains information about all arches.
        # But I don't want to overcomplicate original task.
        params = None
        if arch:
            params = {'arch': arch}

        return self._call('GET', f"/export/branch_binary_packages/{branch}", params)
