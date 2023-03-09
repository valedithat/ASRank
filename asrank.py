import requests
import argparse
import cowsay


def create_organizations_list(args):
    orgs_input = args.filename
    orgs_file = open(orgs_input, "r")

    organizations = [org.strip().replace(' ', '') for org in orgs_file.readlines()]
    print('==================================================================================================================')
    print(f"Organization Count: {len(organizations)}")
    print(f"Sort Order: {args.order}")
    print('==================================================================================================================')
    return organizations


def fetch_highest_ranking_asn(organization):
    asns_url = f"https://api.asrank.caida.org/v2/restful/asns/name/{organization}"
    try:
        asns_response = requests.get(asns_url)
        json_asns_response = asns_response.json()

        if json_asns_response['data']['asns']['edges']:
            highest_ranking_asn = {'rank': 0, 'asn': '', 'org_id': ''}
            # determine highest asn rank
            for asn in json_asns_response['data']['asns']['edges']:
                asn_node = asn['node']
                rank = asn_node['rank']
                org_id = org_id = asn_node['organization']['orgId']

                if rank > highest_ranking_asn['rank']:
                    highest_ranking_asn['rank'] = rank
                    highest_ranking_asn['asn'] = asn_node['asn']
                    highest_ranking_asn['org_id'] = org_id
            return highest_ranking_asn
        else:
            raise ValueError(f"No ASName found for {organization}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch ASNs for {organization}: {e}")
    except ValueError as e:
        print(e)


def fetch_organization(highest_ranking_asn):
    org_id = highest_ranking_asn['org_id']
    orgs_url = f"https://api.asrank.caida.org/v2/restful/organizations/{org_id}"
    try:
        orgs_response = requests.get(orgs_url)
        json_orgs_response = orgs_response.json()

        if json_orgs_response['data']['organization']:
            org = json_orgs_response['data']['organization']
            org_details = {
                'org_name': org['orgName'],
                'org_rank': org['rank'],
                'cone_size': org['cone']['numberAsns'],
            }
            return org_details
        else:
            raise ValueError(f"No organization found for {org_id}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch organization details for {org_id}: {e}")
    except ValueError as e:
        print(e)


def derp_sort(organization_details, args):
    length = len(organization_details)
    for i in range(length):
        swapped = False

        for j in range(0, length - i - 1):
            # order by org_rank or cone_size
            if args.order == 'rank':
                order = 'org_rank'
            elif args.order == 'cone':
                order = 'cone_size'
            # sort organization_details in descrending
            if organization_details[j][order] < organization_details[j+1][order]:
                organization_details[j], organization_details[j+1] = organization_details[j+1], organization_details[j]
                swapped = True

        if(swapped == False):
            break

def present_organizations_details(details):
    for org_detail in details:
        print(f"Organization Name: {org_detail['org_name']}")
        print(f"Organization Rank: {org_detail['org_rank']}")
        print(f"Cone Size: {org_detail['cone_size']}")
        print('==================================================================================================================')


def organizations_details(organizations, args):
    details = []
    for organization in organizations:
        try:
            # get asns by org name
            highest_ranking_asn = fetch_highest_ranking_asn(organization)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch details for {organization}: {e}")
        except ValueError as e:
            print(e)
        else:
            if highest_ranking_asn:
                # get org details by orgId
                org_details = fetch_organization(highest_ranking_asn)
                details.append(org_details)


    if details:
        # sort details by 'rank' or 'cone' size depending on arg provided in 'order'
        derp_sort(details, args)
        present_organizations_details(details)
    else:
        return 'No organizations to display'



print('==================================================================================================================')
cowsay.trex('Welcome to AZRank! Please scratch my nose')

print('==================================================================================================================')
######################################### ARG PARSE SECTION ###################################
parser = argparse.ArgumentParser(
    prog='ASRank',
    description='it ranks stuff and things',
    usage='idk',
    epilog='HEEEEEEEEELLLLPPPP IIII NEEEED HHHHEEELLLPPP'
)

# file of all orgs
parser.add_argument('filename', help='filename input of all organizations to search'
)

# sort by rank or cone size
parser.add_argument('--order', choices=['rank', 'cone'], default='rank', help='sort by rank or cone size', required=False,
)

args = parser.parse_args()

######################################### ARG PARSE SECTION ###################################


organizations = create_organizations_list(args)

organizations_details(organizations, args)

