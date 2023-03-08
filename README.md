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
