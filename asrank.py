import requests
import argparse

class ASRank:
    def __init__(self, args):
        self.file = args.file
        self.order = args.order
        self.orgs_list = self.ingest_org_list()

        self.orgs = []
        self.term_output = """
Rank\t\t Cone Size\t\t Organization Name
-----\t\t ----------\t\t -------------------"""

    def ingest_org_list(self):
        orgs_file = open(self.file, 'r')
        organizations = [org.strip().replace(' ', '') for org in orgs_file.readlines()]
        print(f"Total Organizations: {len(organizations)}")
        print(f"Sort Order: {self.order}")
        return organizations

    def fetch_highest_ranking_asn(self, org):
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

    def fetch_organization(self, org_id):
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

    def sort_orgs(self):
        for i in range(len(self.orgs)):
            swapped = False

            for j in range(0, len(self.orgs) - i - 1):
                order = 'rank' if self.order == 'rank' else 'cone'

                if self.orgs[j][order] < self.orgs[j+1][order]:
                    self.orgs[j], self.orgs[j+1] = self.orgs[j+1], self.orgs[j]
                    swapped = True

            if(swapped == False):
                break

    def present_orgs(self):
        for org in self.orgs:
            self.term_output += f"""
{org['rank']}\t\t\t {org['cone']}\t\t\t {org['name']}"""

        print(self.term_output)

    def rank(self):
        for org in self.orgs_list:
            try:
                org_id = self.fetch_highest_ranking_asn(org)

                if org_id:
                    org_details = self.fetch_organization(org_id)
                    self.orgs.append(org_details)
            except ValueError as e:
                print(e)

        if self.orgs:
            self.sort_orgs()
            self.present_orgs()

parser = argparse.ArgumentParser(prog='ASRank')
parser.add_argument('file', help='org list')
parser.add_argument('order', choices=['rank', 'cone'], help='ig')
args = parser.parse_args()
asrank = ASRank(args)
asrank.rank()
