import requests
import argparse


def ingest_org_list(args):
    orgs_file = open(args.file, "r")
    organizations = [org.strip().replace(' ', '') for org in orgs_file.readlines()]
    print(f"Total Organizations: {len(organizations)}")
    print(f"Sort Order: {args.order}")
    return organizations

def fetch_highest_ranking_asn(org):
    try:
        req = requests.get(f"https://api.asrank.caida.org/v2/restful/asns/name/{org}")
        asns = req.json()

        if asns['data']['asns']['edges']:
            highest_rank = 0
            org_id = ''

            for asn in asns['data']['asns']['edges']:
                if asn['node']['rank'] > highest_rank:
                    highest_rank = asn['node']['rank']
                    org_id = asn['node']['organization']['orgId']
            return org_id
        else:
            raise ValueError(f"No ASName found for {org}")
    except ValueError as e:
        print(e)

def fetch_organization(org_id):
    req = requests.get(f"https://api.asrank.caida.org/v2/restful/organizations/{org_id}")
    orgs = req.json()

    if orgs['data']['organization']:
        org = orgs['data']['organization']
        org_details = {
            'name': org['orgName'],
            'rank': org['rank'],
            'cone': org['cone']['numberAsns'],
        }
        return org_details

def sort_orgs(orgs, order):
    for i in range(len(orgs)):
        swapped = False

        for j in range(0, len(orgs) - i - 1):
            order = 'rank' if order == 'rank' else 'cone'

            if orgs[j][order] < orgs[j+1][order]:
                orgs[j], orgs[j+1] = orgs[j+1], orgs[j]
                swapped = True

        if(swapped == False):
            break

def present_orgs(orgs):
    result = """
Rank\t\t Cone Size\t\t Organization Name
-----\t\t ----------\t\t -------------------"""

    for org in orgs:
        result += f"""
{org['rank']}\t\t {org['cone']}\t\t\t {org['name']}"""

    print(result)

def query_orgs(orgs_list, args):
    orgs = []
    for org in orgs_list:
        try:
            org_id = fetch_highest_ranking_asn(org)

            if org_id:
                org_details = fetch_organization(org_id)
                orgs.append(org_details)
        except ValueError as e:
            print(e)

    if orgs:
        sort_orgs(orgs, args)
        present_orgs(orgs)


parser = argparse.ArgumentParser(prog='ASRank')
parser.add_argument('file', help='org list')
parser.add_argument('--order', choices=['rank', 'cone'], help='rank or cone size')

args = parser.parse_args()
orgs = ingest_org_list(args)
query_orgs(orgs, args)
