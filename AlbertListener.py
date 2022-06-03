"""
check the status of the classes with their class numbers listed in "targets.json"
The "targets.json" is formatted like this:
{
    major_name_01: [class_no_01, class_no_02, ...],
    ...
}

"""
import json
from AlbertNavigator import *

with open("targets.json", "rb") as file:
    targets = json.load(file)

with AlbertNavigator(is_text_only=True) as nav:
    nav.listen_to(targets)
