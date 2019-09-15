# This screen scrapes whitepages.com.au
# Note : the WP website has a blacklist of IPs. Amazon AWS is one of them, it would seem.
# tested with 2.7
import json

def lambda_handler(event, context):
    # return lambda_handler_ptv(event, context)
    return lambda_handler_wp(event, context)


def lambda_handler_wp(event, context):
    surname   = "unknown"
    givenName = "unknown"
    postcode  = "unknown"

    # print event['Details']['Parameters']
    if 'Surname' in event['Details']['Parameters']:
        surname = event['Details']['Parameters']['Surname']

    if 'GivenName' in event['Details']['Parameters']:
        givenName = event['Details']['Parameters']['GivenName']

    if 'Postcode' in event['Details']['Parameters']:
        postcode = event['Details']['Parameters']['Postcode']

    return getDialogue(surname, givenName, postcode)

def getDialogue(theSurname, theGivenName, thePostcode):
    from botocore.vendored import requests  # this is needed for lambda
    # import requests  # this wont work in Lambda
    from requests.utils import quote
    from lxml import html

    from bs4 import BeautifulSoup


    wpURL = "https://www.whitepages.com.au/residential/results?name={name}&givenName={givenName}&location={location}"
    agent = {"User-Agent": "Mozilla/5.0"}

    url = wpURL.format(name=theSurname, givenName=theGivenName, location=quote(thePostcode))
    print(url)

    response = requests.get(url, headers=agent)
    print('done')

    root = html.fromstring(response.content)

    # response = {"Dialogue": "No results found"}  # ??? DEL ME

    # return json.dumps(response)  # ??? DEL ME

    xpath = '//*[@id="main-container-id"]/div/div[2]/div[1]/div/div[2]'  # this has num results + results
    numResults = root.xpath(xpath)

    if len(numResults) == 0:
        print("No results")
        response = {"Dialogue": "No results found"}

        return json.dumps(response)

    results = numResults[0]

    soup = BeautifulSoup(html.tostring(results), features="html.parser")

    locations = soup.find_all("span", {"class": "presence-location"})
    names = soup.find_all("span", {"class": "display-name"})

    msg = "Number of results {}. Reading up to only 3 returned results, ".format(len(names))

    for n, l in zip(names, locations):
        msg = msg + "," + n.text + ", " + l.text

    response = {"Dialogue": msg}

    return json.dumps(response)


if __name__ == '__main__':
    import sys

    surname = sys.argv[1]
    givenName = sys.argv[2]
    postcode = sys.argv[3]

    res = getDialogue(surname, givenName, postcode)

    print(res)
