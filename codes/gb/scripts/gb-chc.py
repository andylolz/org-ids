import csv
import requests


# An Initialisation script will get everything set-up.
# Used if a script needs to download data in order to run
def gb_chc_to_gb_coh_init(force=False):
    pass


# Map from the first to the second identifier type listed here
def gb_chc_to_gb_coh(identifier):
    download = requests.get('http://beta.charitycommission.gov.uk/charity-details/?regid=' + str(identifier) +'&subid=0&exportcsv=1')
    data = csv.DictReader(download.content.splitlines())

    for row in data:
        return "GB-COH-" +str(row['Company number'])

    return False

print gb_chc_to_gb_coh(1164883)