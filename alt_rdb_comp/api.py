import requests
import requests_cache
from requests_cache import timedelta


class HTTPError(Exception):
    def __init__(self, status_code, reason, text, json):
        self.status_code = status_code
        self.reason = reason
        self.text = text
        self.json = json


class ClientError(HTTPError):
    """(400-499)"""

    pass


class ServerError(HTTPError):
    """(500-599)"""

    pass


class ALTLinuxRDBApi(Exception):
    pass


class ArchitectureMissingError(ALTLinuxRDBApi):
    def __init__(self, arch: str, branch: str):
        self.arch = arch
        self.branch = branch
        super().__init__(f"Architecture '{arch}' is missing in branch '{branch}'.")


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

    def _call(self, method, endpoint, params=None):
        """
        Internal method to make an HTTP request to the API and return the JSON response.
        """
        try:
            res = self._session.request(
                method,
                f"{self.base_url}{endpoint}",
                params=params,
            )

            jsn = res.json()

            if 400 <= res.status_code < 500:
                raise ClientError(res.status_code, res.reason, res.text, jsn)
            elif 500 <= res.status_code < 600:
                raise ServerError(res.status_code, res.reason, res.text, jsn)

            return jsn
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP Request failed: {e}")
        except ValueError:
            raise Exception(f"Failed to decode JSON response from {endpoint}")

    def export_branch_binary_packages(self, branch="sisyphus", arch=None) -> dict:
        """
        Retrieves binary packages for a specific branch and architecture.
        """
        # For better perfomance, possibly better
        # use cache for arch = None if it is available,
        # because it contains information about all arches.
        # But I don't want to overcomplicate original task.
        params = None
        if arch:
            params = {"arch": arch}

        try:
            return self._call("GET", f"/export/branch_binary_packages/{branch}", params)
        except ClientError as e:
            errors = e.json.get("errors", {})
            arch_error = errors.get("arch", "")
            expected_prefix = "package architecture Invalid architecture name"

            if arch_error.startswith(expected_prefix):
                arch = params.get(
                    "arch", "unknown"
                )  # Assuming 'arch' is part of params
                raise ArchitectureMissingError(arch, branch) from e

            raise e
