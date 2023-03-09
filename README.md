# ASRank
This is a script to query [ASRank API](https://asrank.caida.org/) with organizations. This will return organizations:
    Organization's Name
    ASRank
    Cone Size

The organizations can be sorted by asrank or cone size based on a cli flag. Include the following organizations:
    Liquid Web
    OVH
    Hivelocity
    Hetzner
    LeaseWeb

There will be multiple ASNs for each provider. So use the highest rank ASN for each.

## Setup
`pip install -r requirements.txt`

## Usage
`python asrank.py [filename_of_orgs_list] [--order [rank][cone]]`

The file is a, one org per line, list of organizations to be queried. See organization.txt and not_asname_list.txt for examples of existing orgs and non-existing orgs.

Order is an option argument that defaults to 'rank' but will sort the organizations based on either 'rank' or 'cone size in *desending* order.

Examples
* `python asrank.py organizations.txt --order cone`
* `python asrank.py organizations.txt --order rank`

## Queries
Provided organization's names, search:
1. https://api.asrank.caida.org/v2/restful/asns/name/Hivelocity

```
count: 3
node: 0
    rank: 776
    org:
        orgId: "ee438e3f88"
node: 1
    rank: 28697
    org:
        orgId: "ee438e3f88"
node: 2
    rank: 74809
    org:
        orgId: "ee438e3f88"
```

*nodes not list in order of rank*
*each asn has the same organization*

2. https://api.asrank.caida.org/v2/restful/organizations/ee438e3f88

```
organization:
    rank:	721
    orgId:	"ee438e3f88"
    orgName:	"HIVELOCITY, Inc."
    seen:	true
    cone:
        numberAsns:	45
        numberPrefixes:	1378
        numberAddresses:	797001
    country:
        iso:	"US"
    members:
        asns:
            edges:
                0:
                    node:
                        asn:	"29802"
```


