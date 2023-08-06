'''
--------------------------------------------------------------------------------
------------------------- Mist API Python CLI Session --------------------------

    Written by: Thomas Munzer (tmunzer@juniper.net)
    Github    : https://github.com/tmunzer/mistapi_python

    This package is licensed under the MIT License.

--------------------------------------------------------------------------------
This module manages API requests with Mist Cloud. It is used to 
* generate the URL based on the provided parameters
* add the required HTTP Headers to the request
* report error if any
'''

import requests
import os
import json
from requests.exceptions import HTTPError
from mistapi.__api_response import APIResponse
from mistapi.__logger import logger


class APIRequest:

    def __init__(self):
        self._cloud_uri = ""
        self._session = requests.session()
        self.privileges = ""
        

    def _url(self, uri) -> str:
        """
        Generate the url with the host (in the object) and the uri

        PARAMS
        -----------
        :param str uri - URI where to send the request to (e.g. "/api/v1/...")

        RETURN
        -----------
        :return str url - Full URL where to send the request to (e.g. "https://api.mist.com/api/v1/...")
        """
        logger.debug(f"apirequest:in  > _url")
        return "https://" + self._cloud_uri + uri

    def _gen_query(self, query:object) -> str:
        logger.debug(f"apirequest:in  > _gen_query")
        logger.debug(f"apirequest:processing query {query}")
        html_query = "?"
        if query:
            for query_param in query:
                html_query += f"{query_param}={query[query_param]}&"
        logger.debug(f"apirequest:generated query: {html_query}")
        html_query = html_query[:-1]
        return html_query

    def mist_get(self, uri:str, query:object=None) -> APIResponse:
        """
        GET HTTP Request

        PARAMS
        -----------
        :param str uri - HTTP URI (e.g. "/api/v1/self") 
        :param object query - dict of HTTP Queries (e.g. {"page": 1, "limit":100})

        RETURN
        -----------
        :return APIResponse
        """
        try:
            url = self._url(uri) + self._gen_query(query)
            logger.info(f"apirequest:sending GET request to {url}")
            resp = self._session.get(url)
            resp.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
            logger.error(f'HTTP error description: {resp.json()}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  # Python 3.6
            logger.error("Exception occurred", exc_info=True)
        finally:
            return APIResponse(url=url, response=resp)

    def mist_post(self, uri:str,  body:object=None) -> APIResponse:
        """
        POST HTTP Request

        PARAMS
        -----------
        :param str uri - HTTP URI (e.g. "/api/v1/self") 
        :param object body 

        RETURN
        -----------
        :return APIResponse
        """
        try: 
            url = self._url(uri)
            logger.info(f"apirequest:sending POST request to {url}")
            headers = {'Content-Type': "application/json"}
            logger.debug(f"apirequest:Request body: \r\n{body}")
            if type(body) == str:
                resp = self._session.post(url, data=body, headers=headers)
            elif type(body) == list:
                resp = self._session.post(url, json=body, headers=headers)
            elif type(body) == dict:
                resp = self._session.post(url, json=body, headers=headers)
            else: 
                resp = self._session.post(url, json=body, headers=headers)
            resp.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
            logger.error(f'HTTP error description: {resp.json()}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  # Python 3.6
            logger.error("Exception occurred", exc_info=True)
        finally: 
            return APIResponse(url=url, response=resp)

    def mist_put(self, uri:str, body:object=None) -> APIResponse:
        """
        PUT HTTP Request

        PARAMS
        -----------
        :param str uri - HTTP URI (e.g. "/api/v1/self") 
        :param object body 

        RETURN
        -----------
        :return APIResponse
        """
        try:
            url = self._url(uri)
            logger.info(f"apirequest:sending PUT request to {url}")
            headers = {'Content-Type': "application/json"}
            logger.debug(f"apirequest:Request body: \r\n{body}")
            if type(body) == str:
                resp = self._session.put(url, data=body, headers=headers)
            elif type(body) == list:
                resp = self._session.put(url, json=body, headers=headers)
            elif type(body) == dict:
                resp = self._session.put(url, json=body, headers=headers)
            else: 
                resp = self._session.put(url, json=body, headers=headers)
            resp.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
            logger.error(f'HTTP error description: {resp.json()}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  # Python 3.6
            logger.error("Exception occurred", exc_info=True)
        finally: 
            return APIResponse(url=url, response=resp)

    def mist_delete(self, uri:str, query:object=None) -> APIResponse:
        """
        DELETE HTTP Request

        PARAMS
        -----------
        :param str uri - HTTP URI (e.g. "/api/v1/self") 

        RETURN
        -----------
        :return APIResponse
        """
        try: 
            url = self._url(uri) + self._gen_query(query)
            logger.info(f"apirequest:sending DELETE request to {url}")
            resp = self._session.delete(url)
            resp.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  # Python 3.6
            logger.error("Exception occurred", exc_info=True)
        else: 
            return APIResponse(url=url, response=resp)


    def mist_post_file(self, uri:str, file:str="", csv:str="", body:dict={}) -> APIResponse:
        """
        POST HTTP Request

        PARAMS
        -----------
        :param str uri - HTTP URI (e.g. "/api/v1/self") 
        :param object body 

        RETURN
        -----------
        :return APIResponse
        """
        try:                 
            url = self._url(uri)
            logger.info(f"apirequest:sending POST request to {url}")
            multipart_form_data = {}
            if file: multipart_form_data["file"] = (os.path.basename(file), open(file, 'rb'), 'application/octet-stream')
            if csv: multipart_form_data["csv"] = (os.path.basename(csv), open(file, 'rb'), 'application/octet-stream')
            if body: multipart_form_data["json"] = (None, json.dumps(body), 'application/json')
            resp = self._session.post(url, files=multipart_form_data)
            resp.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')  # Python 3.6
            logger.error(f'HTTP error description: {resp.json()}')
            return resp
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  # Python 3.6
            logger.error("Exception occurred", exc_info=True)
        else: 
            return APIResponse(url=url, response=resp)
