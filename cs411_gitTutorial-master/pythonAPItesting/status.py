import requests

def response():
    """Checks for live response"""
    response = requests.get("http://api.open-notify.org/astros.json")
    print(response)


def accessContent():
    """Accesses Content"""
    response = requests.get("http://api.open-notify.org/astros.json")
    print(response.json()) # This method is convenient when the API returns JSON
    print(type(response.json()))

def query():
    """Passes a query"""
    query = {'lat':'45', 'lon':'180'}
    response = requests.get('http://api.open-notify.org/iss-pass.json', params=query)
    print(response.json())


#response()
#accessContent()
#query()