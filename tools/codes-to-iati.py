import os
import json
import glob
import requests
import xml.etree.ElementTree as ET

## Build the list of codes
current_dir = os.path.dirname(os.path.realpath(__file__))
codes_dir = os.path.join(current_dir, '../codes')

lists = {}

id_lists = []
for prefix_file_name in glob.glob(codes_dir + '/*/*.json'):
    with open(prefix_file_name) as prefix_file:
        id_lists.append(json.load(prefix_file))


## Get a list of current IATI entries
iati_codes = []
current_iati_list = requests.get("http://iatistandard.org/202/codelists/downloads/clv3/json/en/OrganisationRegistrationAgency.json")
iati_data = current_iati_list.json()
for code in iati_data['data']:
    iati_codes.append(code['code'])

root = ET.Element("codelist")
meta = ET.SubElement(root, "metadata")
ET.SubElement(ET.SubElement(meta, "name"),"narrative").text = "Organization Identifier Lists"
ET.SubElement(ET.SubElement(meta, "description"),"narrative").text = "Organisation identifier lists and their code. These can be used as the prefix for an organisation identifier. For general guidance about constructing Organisation Identifiers, please see http://iatistandard.org/organisation-identifiers/  This list was formerly maintained by the IATI Secretariat as the Organization Registration Agency codelist. This version is maintained by the Identify-Org project, of which IATI is a member. New code requests should be made via Identify-org.net"
items = ET.SubElement(root, "codelist-items")

identify_codes = []
deprecated_codes = []

for entry in id_lists:
    if entry['code'] in iati_codes:
        iati_codes.remove(entry['code'])
        if entry['deprecated'] == True:
            # deprecated_codes.append({entry['code']:entry['description']})
            deprecated_codes.append(entry['code'])
        else:
            # We use available online to determine the value of public-database
            if entry['availableOnline']:
                publicdb = str(1)
            else:
                publicdb = str(0)

            item = ET.SubElement(items, "codelist-item",**{'public-database':publicdb})
            ET.SubElement(item, "code").text = entry['code']
            name = ET.SubElement(item, "name")
            ET.SubElement(name, "narrative").text = entry['name']
            description = ET.SubElement(item, "description")
            ET.SubElement(description, "narrative").text = entry['description']
            try:
                ET.SubElement(item, "category").text = entry['jurisdiction'][0]['countryCode']
            except:
                ET.SubElement(item, "category").text = '-'
            ET.SubElement(item, "url").text = entry['url']

    else:
        # identify_codes.append({entry['code']:entry['confirmed']})
        identify_codes.append(entry['code'])


print("IATI has the following codes missing from the Identify Org list")
print(iati_codes)
print()
print("Identify Org has the following codes missing from the IATI list")
print(identify_codes)
print("The following codes from the IATI list have been deprecated in Identify Org")
print(deprecated_codes)
print()


tree = ET.ElementTree(root)
tree.write("v3-OrganisationRegistrationAgency.xml")