# coding: utf-8
from concurrent.futures import TimeoutError as FutureTaskTimeoutError
import traceback

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from aiohttp import ClientConnectionError, ClientPayloadError

from utils.enums import RequestDataReturnTypes
# from app.utils.debug import debug_print
from utils.log import get_logger

logger = get_logger(__name__)


class Spider(object):
    """爬虫基类"""

    async def fetch(self, url, *, session, method="get",
                    headers=None, params=None, data=None, json=None, proxy=None,
                    timeout=None, return_type=str, **kwargs):
        """aiohttp异步请求"""
        try:
            response = await session.request(method.lower(), url, headers=headers, params=params, data=data, json=json, proxy=proxy, timeout=timeout, **kwargs)
            if 200 <= response.status < 300:
                if return_type is dict or return_type == RequestDataReturnTypes.JSON:
                    return await response.json(content_type=None)
                elif return_type is str or return_type == RequestDataReturnTypes.TEXT:
                    return await response.text()
                elif return_type is bytes or return_type == RequestDataReturnTypes.BYTE:
                    return await response.read()
                else:
                    return response
        except FutureTaskTimeoutError as e:
            logger.warning(f"timeout{e}: {method.upper()} {url} PROXY={proxy} headers={headers} params={params} data={data} json={json}")
        except (RuntimeError, OSError, ClientConnectionError, ClientPayloadError):
            logger.warning(traceback.format_exc())
        except Exception:
            logger.exception(f"{method.upper()} {url} PROXY={proxy} headers={headers} params={params} data={data} json={json}")

        return None

    def request(self, url, *, method="get",
                headers=None, params=None, data=None, json=None, proxy=None,
                timeout=None, return_type=None, **kwargs):
        """requests同步请求"""
        try:
            response = requests.request(method.lower(), url, headers=headers, params=params, data=data, json=json, proxies=proxy, timeout=timeout, verify=False, **kwargs)
            response.encoding = response.apparent_encoding
            if 200 <= response.status_code < 300:
                if return_type is dict or return_type == RequestDataReturnTypes.JSON:
                    return response.json()
                elif return_type is str or return_type == RequestDataReturnTypes.TEXT:
                    return response.text
                elif return_type is bytes or return_type == RequestDataReturnTypes.BYTE:
                    return response.content
                else:
                    return response
        except RequestsConnectionError:
            logger.warning(traceback.format_exc())
        except Exception:
            logger.exception(f"{method.upper()} {url} PROXY={proxy} headers={headers} params={params} data={data} json={json}")

        return None
