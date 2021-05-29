"""Extremely quick and dirty module for creating a markdown file from the instances.yaml file"""
from urllib.parse import urlparse

import yaml
from mdutils.mdutils import MdUtils


def create_table(table_data, instance_data):
    rows = []
    for field, value in instance_data.items():
        if value is None:
            rows.append("")
        
        # Use markdown links for Addresses
        elif field == "url":
            url = urlparse(value).hostname
            rows.append(f"[{url}]({value})")
        
        elif field == "country" and value:
            rows.append(f"{value['flag']} {value['name']}")

        elif field == "modified":
            if value["is_modified"] is True:
                rows.append(f"[Yes]({value['source_url']})")
            else:
                rows.append("No")

        # We're going to use a markdown link here
        elif field == "privacy_policy":
            rows.append(f"[Here]({value})")

        # Handle author name
        elif field == "owner":
            # Assuming github url
            author_name = value.split("/")
            rows.append(f"[@{author_name[-1]}]({value})")
        else:
            rows.append(value)

    table_data.extend(rows)


with open("instances.yaml") as instance_yaml_file:
    data = yaml.safe_load(instance_yaml_file)

# Initial information
md_instance_list = MdUtils(file_name='Invidious-Instances.md')
md_instance_list.new_header(level=1, title='Public Instances')
md_instance_list.new_paragraph("Uptime History: [stats.uptimerobot.com/89VnzSKAn](https://stats.uptimerobot.com/89VnzSKAn)")
md_instance_list.new_paragraph("Instances API: [api.invidious.io](https://instances.invidious.io)")


# Clearnet instances
md_instance_list.new_header(level=1, title='Instances list')
table_data = ["Address", "Country", "Status", "Privacy policy", "DDos Protection / MITM", "Owner", "Modified"]
for instance_data in data["https"]:
    create_table(table_data, instance_data)

md_instance_list.new_line()
md_instance_list.new_table(columns=7, rows=len(data["https"]) + 1, text=table_data, text_align='center')


# Onion instances
md_instance_list.new_header(level=1, title='Tor onion instances list')
table_data = ["Address", "Country", "Associated clearnet instance", "Privacy policy", "Owner", "Modified"]
for instance_data in data["onion"]:
    create_table(table_data, instance_data) 

md_instance_list.new_line()
md_instance_list.new_table(columns=6, rows=len(data["onion"]) + 1, text=table_data, text_align='center')


# Instance adding directions and prerequisites
md_instance_list.new_header(level=1, title='Adding your instance')

# Prerequisites
md_instance_list.new_header(level=2, title='Prerequisites')
prerequisites = [
    "Instances must have been updated in the last month. An instance that hasn't been updated in the last month is considered unmaintained and is removed from the list",
    "Instances must have statistics (/api/v1/stats) enabled (`statistics_enabled:true` in the configuration file).",
    "Instances must be served via domain name.",
    "Instances must be served via HTTPS.",
    "Instances using any DDoS Protection / MITM are marked as such.",
    "Instances using any type of anti-bot protection are marked as such.",
    "Instances using any type of analytics are marked as such, must be GDPR compliant (if it's usable in the EU), must be CCPA compliant (if it's usable in California), and must respect the AGPL by explaining their changes and by publishing their source code. In short: instances shouldn't run analytics, because it's not worth it."
]
md_instance_list.new_list(prerequisites)
md_instance_list.new_line()

# Directions
md_instance_list.new_header(level=2, title='Directions')
directions = [
    "Fork the documentation repo.",
    "Open `instances.yaml` for editing.",
    "Append your instance to the bottom of the HTTPS (or onion) list. See the examples in the yaml file for more info",
    "Make a pull request.",
]
md_instance_list.new_list(directions, marked_with="1")

md_instance_list.create_md_file()
