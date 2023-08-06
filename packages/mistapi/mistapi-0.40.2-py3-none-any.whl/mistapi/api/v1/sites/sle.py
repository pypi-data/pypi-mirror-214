'''
--------------------------------------------------------------------------------
------------------------- Mist API Python CLI Session --------------------------

    Written by: Thomas Munzer (tmunzer@juniper.net)
    Github    : https://github.com/tmunzer/mistapi_python

    This package is licensed under the MIT License.

--------------------------------------------------------------------------------
'''

from mistapi import APISession as _APISession
from mistapi.__api_response import APIResponse as _APIResponse
import deprecation

def getSiteSleClassifierDetails(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, classifier:str, start:int=None, end:int=None, duration:str="1d") -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleClassifierDetails
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics
    :param str classifier        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/classifier/{classifier}/summary"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleMetricClassifiers(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleMetricClassifiers
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric -  values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/classifiers"
    query_params={}
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleHistogram(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d") -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleHistogram
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/histogram"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactSummary(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", fields:str=None, classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactSummary
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str fields(wlan, device_type, device_os, band, ap, server, mxedge, switch, client, vlan, interface, chassis, gateway, peer_path, gateway_zones)
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impact-summary"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if fields: query_params["fields"]=fields
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedApplications(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedApplications
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-applications"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedAps(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedAps
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-aps"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedChassis(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedChassis
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-chassis"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedWiredClients(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedWiredClients
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-clients"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedGateways(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedGateways
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-gateways"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedInterfaces(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedInterfaces
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-interfaces"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedSwitches(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedSwitches
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-switches"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleImpactedWirelessClients(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d", classifier:str=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleImpactedWirelessClients
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration
    :param str classifier        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/impacted-users"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    if classifier: query_params["classifier"]=classifier
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleSummary(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, start:int=None, end:int=None, duration:str="1d") -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleSummary
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    QUERY PARAMS
    ------------
    :param int start
    :param int end
    :param str duration        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/summary"
    query_params={}
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def getSiteSleThreshold(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSleThreshold
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/threshold"
    query_params={}
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def replaceSiteSleThreshold(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, body:object) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/replaceSiteSleThreshold
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    BODY PARAMS
    -----------
    :param dict body - JSON object to send to Mist Cloud (see API doc above for more details)
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/threshold"
    resp = mist_session.mist_post(uri=uri, body=body)
    return resp
    
def updateSiteSleThreshold(mist_session:_APISession, site_id:str, scope:str, scope_id:str, metric:str, body:object) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/updateSiteSleThreshold
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`
    :param str metric - values from /api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics        
    
    BODY PARAMS
    -----------
    :param dict body - JSON object to send to Mist Cloud (see API doc above for more details)
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metric/{metric}/threshold"
    resp = mist_session.mist_put(uri=uri, body=body)
    return resp
    
def getSiteSlesMetrics(mist_session:_APISession, site_id:str, scope:str, scope_id:str) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getSiteSlesMetrics
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str site_id
    :param str scope
    :param str scope_id - * site_id if `scope`==`site`
* device_id if `scope`==`ap`, `scope`==`switch` or `scope`==`gateway`
* mac if `scope`==`client`        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/sle/{scope}/{scope_id}/metrics"
    query_params={}
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    