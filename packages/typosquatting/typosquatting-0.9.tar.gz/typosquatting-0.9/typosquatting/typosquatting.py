from utility import get_elastic_client
import re
import wordninja
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch
from items import CustomerAlert
import json
from _aws_SQS import SQS
from utility import insert_in_elastic_for_monitoring



def typosquotting_enrichment_tool(ioc):
    try:
        subqueries = subquery_list(ioc['value'])
        # query_body = subqueries
        query_body = {
            "query": {
                "bool": {
                    "should": subqueries
                }
            }
        }
        check_typosquatting_of_customer_domains("companies_test", query_body, ioc['value'])
        typo_info = check_typosquatting_of_top_domains(ioc)
        # if typo_info['response']['is_typosquatting']:
        #     insert_in_elastic_for_monitoring(ioc['value'], typo_info['response']['typosquatting_of'], "top_domain")
        return typo_info
    except Exception as e:
        return {"is_typosquatting": False, "typosquatting_of": ""}
        # print(str(e))


def check_typosquatting_of_customer_domains(index_name, query_body, ioc_value):
    es = get_elastic_client()
    resp = es.search(index=index_name, body=query_body, size=20)
    if resp['hits']['total']['value'] >= 1:
        domain, extension = ioc_value.rsplit(".", 1)
        first_level_domain = domain.rsplit(".", 1)[-1]
        actual_domain = first_level_domain + "." + extension
        for res in resp['hits']['hits']:
            domain = res['_source']['domain']
            if actual_domain != domain:
                typo_result = res['_source']
                print("customer typosquatting is detected\n", typo_result)
                sqs = SQS.SQSSession.get_instance()
                queue_url = 'https://sqs.us-east-2.amazonaws.com/902621712208/customer_alert'
                alert = CustomerAlert(
                    customer_id=typo_result["companyId"],
                    type='Typosquatting',
                    source=ioc_value,
                    domain_type=typo_result["domain_type"],
                    domain_value=typo_result["domain"],
                    labels="typo-squatting"
                )
                alert = dict(alert)
                response = sqs.sqs.send_message(
                    QueueUrl=queue_url,
                    DelaySeconds=2,
                    MessageBody=json.dumps(alert)
                )
                print(response)
                insert_in_elastic_for_monitoring(ioc_value, typo_result["domain"], "customer_domain ")
                print("Message produced in queue for ", typo_result["domain"])
            else:
                print("Customer typosquatting not detected")
    else:
        print("Customer typosquatting not detected")



def check_typosquatting_of_top_domains(ioc):
    results_list = []
    es = get_elastic_client()
    # If there is an ip address in the domain then we can't find typosquatting for it
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ioc['value']):
        typo_info = {
            "is_typosquatting": False,
            "typosquatting_of": ""
        }

        # return {"status_code": 1, "response": typo_info}
        return typo_info

    # separating subdomains
    root_domain = ioc['value'].rsplit('.', 1)[0].split('.')[0:-1]
    sub_domains = clean_domain(root_domain)
    # longest_domain = None
    typo_domains = []
    longest_domain = None
    # Searching if any of subdomain matches our target domain
    for dom in sub_domains:
        query = {
            "query": {
                "term": {
                    "value.keyword": {
                        "value": dom
                    }
                }
            }
        }

        # Search for matching basic_domains
        results = es.search(index="whitelisting_v1", body=query)
        # Process the results
        for hit in results['hits']['hits']:
            matching_domains = hit['_source']['value']
            # we will get that target domain as typosquatting domain which exactly matches our artifact
            if fuzz.ratio(re.sub(r'[^a-zA-Z0-9]+', ' ', matching_domains),
                          re.sub(r'[^a-zA-Z0-9]+', ' ', dom)) == 100:
                if not longest_domain or len(matching_domains) > len(longest_domain):
                    longest_domain = matching_domains

    # we will alwasys get the longest matchig domain
    if longest_domain:
        # typo_domains = list(set(typo_domains))
        typo_info = {
            "is_typosquatting": True,
            "typosquatting_of": longest_domain
        }

        return typo_info
        # return {"status_code": 1, "response": typo_info}

    # Taking main domain + tld from domain
    ioc['value'] = '.'.join(ioc['value'].split('.')[-2:])
    subqueries = subquery_list(ioc['value'])
    # query_body = subqueries

    query_body = {
        "query": {
            "bool": {
                "should": subqueries
            }
        }
    }

    # Will take 20 matching domain from top_domains
    resp = es.search(index="whitelisting_v1", body=query_body, size=20)

    for doc in resp['hits']['hits']:
        # If we have same main_domain but different tld for our artifact and detected domain
        # then will boost its score as it is typosquatting
        # and will store the score same for other domain
        if ioc['value'].split('.')[0] == doc['_source']['value'].split('.')[0] and ioc['value'].split('.')[1] != \
                doc['_source']['value'].split('.')[1]:
            result = {
                'domain': doc['_source']['value'],
                'score': 95
                # 'score': 85
            }
        else:
            result = {
                'domain': doc['_source']['value'],
                'score': fuzz.ratio(ioc['value'], doc['_source']['value'])
            }
        results_list.append(result)
    try:
        # Taking domain with highest similarity score among all
        max_result = max(results_list, key=lambda x: x["score"])
        max_score = max_result["score"]
    except:
        pass

    # For true typosquatting firstly we will select those which score is greater than 70
    # if resp['hits']['total']['value'] >= 1 and resp['hits']['hits'][0]['_source']['domain'] != ioc['value'] and 70 < max_score < 100:
    if resp['hits']['total']['value'] >= 1 and 70 < max_score < 100:
        # if domain+tld matching score is greater than 70 then we will see if its only domain score is greater
        # than 80 then we will consider typosquatting true
        # print(fuzz.ratio(ioc['value'].split('.')[0], max_result['domain'].split('.')[0]))
        if fuzz.ratio(ioc['value'].split('.')[0], max_result['domain'].split('.')[0]) >= 70:
            typo_info = {
                "is_typosquatting": True,
                "typosquatting_of": max_result["domain"]
            }

            # return {"status_code": 1, "response": typo_info}
            return typo_info
        else:
            typo_info = {
                "is_typosquatting": False,
                "typosquatting_of": ""
            }

            # return {"status_code": 1, "response": typo_info}
            return typo_info
    else:
        typo_info = {
            "is_typosquatting": False,
            "typosquatting_of": ""
        }

    return typo_info
    # return {"status_code": 1, "response": typo_info}


def clean_domain(root_domain):
    sub_domains = []
    for domain in root_domain:
        domain = re.sub(r'[^a-zA-Z0-9]+', '.', domain)

        if '.com' not in domain:
            domain = domain + '.com'
            sub_domains.append(domain)
        else:
            sub_domains.append(domain)
        if len(domain.split('.')) > 2:
            lenght = len(domain.split('.')) - 1
            for i in range(1, lenght):
                sub_domains.append('.'.join(domain.split('.')[-lenght:]))
                lenght = lenght - 1

    sub_domains = list(set(sub_domains))
    return sub_domains


def subquery_list(value):
    value = value.lower()
    domain, extension = value.rsplit(".", 1)
    wordsList = wordninja.split(domain)
    # print(wordsList)
    subquery_list = []
    subquery_list.append(fuzzy_subquery(value))

    if wordsList == 0:
        pass
    elif wordsList == 1:
        subquery_list.append(fuzzy_subquery(domain + "." + "com"))
    else:
        subquery_list.append(fuzzy_subquery(domain + "." + "com"))
        subquery_list.append(match_subquery(domain + "." + "com"))
        count = 0
        for i in wordsList:
            if count < 2 and len(i) >= len(domain) / 2 - 1:
                subquery_list.append(fuzzy_subquery(i + "." + extension))
            count += 1

        # sorted_value = ''.join(sorted(value))
        # subquery_list.append(matchphrase_subquery(sorted_value))

    return subquery_list


def fuzzy_subquery(value):
    subquery = {
        "fuzzy": {
            "value": {
                "value": value,
                "fuzziness": "AUTO"
            }
        }
    }
    return subquery


def match_subquery(value):
    subquery = {
        "match": {
            "value": value
        }
    }
    return subquery


def matchphrase_subquery(value):
    subquery = {
        "match_phrase": {
            "sorted_domain": value
        }
    }
    return subquery

