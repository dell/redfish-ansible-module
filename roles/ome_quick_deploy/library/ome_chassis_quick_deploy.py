#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 5.0.0
# Copyright © 2022 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: ome_chassis_quick_deploy
short_description: Configure quick deploy settings for a chassis using OpenManage Enterprise Modular
description: "This module configures the quick deploy settings for a chassis device using OpenManage Enterprise Modular."
version_added: "5.0.0"
author:
  - Anupam Aloke(@anupamaloke)
extends_documentation_fragment:
  - dellemc.openmanage.omem_auth_options
options:
  device_id:
    type: int
    description:
      - Target chassis device ID.
      - This option is mutually exclusive with I(device_service_tag).
  device_service_tag:
    type: str
    description:
      - Target chassis device service tag
      - This option is mutually exclusive with I(device_id).
  quick_deploy_options_type:
    type: str
    description:
      - C(Server) means that the I(quick_deploy_options) settings are for the server sleds.
      - C(IOM) means that the I(quick_deploy_options) settings are for the network IOMs.
    choices: [Server, IOM]
    default: Server
  quick_deploy_options:
    type: dict
    elements: dict
    description:
      - Quick deploy options settings for the server sleds or the network IOMs.
    suboptions:
      ipv4_enabled:
        type: bool
        description:
          - Enable or disable the IPv4 protocol.
      ipv4_network_type:
        type: str
        description:
          - IPv4 network type.
          - If C(Static), then I(ipv4_subnet_mask) and I(ipv4_gateway) must be specified. 
          - C(DHCP) means the DHCP based IPv4 address.
      ipv4_subnet_mask:
        type: str
        description:
          - IPv4 subnet mask.
          - Required if I(ipv4_network_type) is equal to C(Static).
          - This option is ignored if I(ipv4_network_type) is equal to C(DHCP).
      ipv4_gateway:
        type: str
        description:
          - IPv4 gateway.
          - Required if I(ipv4_network_type) is equal to C(Static).
          - This option is ignored if I(ipv4_network_type) is equal to C(DHCP).
      slots:
        type: list
        elements: dict
        description:
          - Slot configuration details for the server sleds or the network IOMs.
        suboptions:
          slot_id:
            type: int
            description:
              - Serial number of the slot.
          slot_ipv4_address:
            type: str
            description:
              - IPv4 address of the slot. 
          slot_ipv6_address:
            type: str
            description:
              - IPv6 address of the slot.
          vlan_id:
            type: int
            description:
              - VLAN ID of the device. The valid VLAN IDs are: 1–4094.
  requirements:
    - "python >= 3.8"
  notes:
    - "This module creates a SERVER_QUICK_DEPLOY or a IOM_QUICK_DEPLOY task to confure the quick deploy options.
    The module times out if the task takes more than 5 minutes (300 seconds) to complete. Therefore it could be
    the case that quick deploy options has successfully been configured on the chassis even though the module 
    timed out. The recommendation is to re-run the module to verify that the quick deploy options are successfully
    configured."
    - This module supports C(check_mode).
"""

EXAMPLES = """
---
- name: Configure static IPv4 address for blades' management network
  ome_chassis_quick_deploy:
    hostname: "192.168.10.10"
    username: "username"
    password: "password"
    quick_deploy_options_type: "Server"
    quick_deploy_options:
      ipv4_enabled: True
      ipv4_network_type: "Static"
      ipv4_subnet_mask: "255.255.255.0"
      ipv4_gateway: "192.168.10.1"
      slots:
        - slot_id: 1
          slot_ipv4_address: "192.168.10.20"
          vlan_id: 1
        - slot_id: 2
          slot_ipv4_address: "192.168.10.21"
          vlan_id: 1

- name: Configure DHCP IPv4 address for blades' management network
  ome_chassis_quick_deploy:
    hostname: "192.168.10.10"
    username: "username"
    password: "password"
    quick_deploy_options_type: "Server"
    quick_deploy_options:
      ipv4_enabled: True
      ipv4_network_type: "DHCP"
      slots:
        - slot_id: 1
          vlan_id: 1
        - slot_id: 2
          vlan_id: 1


# Configure static IPv4 settings for member chassis blades' management network using the lead chassis
# by passing in the member chassis device service tag
- name: Configure static IPv4 settings for member chassis blades' management network using the lead chassis
  ome_chassis_quick_deploy:
    hostname: "192.168.10.10"
    username: "username"
    password: "password"
    device_service_tag: "ABC1234"
    quick_deploy_options_type: "Server"
    quick_deploy_options:
      ipv4_enabled: True
      ipv4_network_type: "Static"
      ipv4_subnet_mask: "255.255.255.0"
      ipv4_gateway: "192.168.10.1"
      slots:
        - slot_id: 1
          slot_ipv4_address: "192.168.10.20"
          vlan_id: 1
        - slot_id: 2
          slot_ipv4_address: "192.168.10.21"
          vlan_id: 1

# Configure static IPv4 settings for member chassis blades' management network using the lead chassis
# by passing in the member chassis device ID
- name: Configure static IPv4 settings for member chassis blades' management network using the lead chassis
  ome_chassis_quick_deploy:
    hostname: "192.168.10.10"
    username: "username"
    password: "password"
    device_id: 12345
    quick_deploy_options_type: "Server"
    quick_deploy_options:
      ipv4_enabled: True
      ipv4_network_type: "Static"
      ipv4_subnet_mask: "255.255.255.0"
      ipv4_gateway: "192.168.10.1"
      slots:
        - slot_id: 1
          slot_ipv4_address: "192.168.10.20"
          vlan_id: 1
        - slot_id: 2
          slot_ipv4_address: "192.168.10.21"
          vlan_id: 1

"""

RETURN = """
---
msg:
  type: str
  description: Overall status of the quick deploy settings configuration
  returned: always
  sample: "Successfully configured the quick deploy settings."
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
        "code": "Base.1.0.GeneralError",
        "message": "A general error has occurred. See ExtendedInfo for more information.",
        "@Message.ExtendedInfo": [
            {
                "MessageId": "CGEN1014",
                "RelatedProperties": [],
                "Message": "Unable to complete the operation because an invalid value is entered for the property
                Invalid json type: STRING for Edm.Int64 property: Id .",
                "MessageArgs": [
                    "Invalid json type: STRING for Edm.Int64 property: Id"
                ],
                "Severity": "Critical",
                "Resolution": "Enter a valid value for the property and retry the operation. For more information about
                valid values, see the OpenManage Enterprise-Modular User's Guide available on the support site."
            }
        ]
    }
}
"""

import json
import copy
import ipaddress
from ssl import SSLError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import check_type_str
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError
from ansible_collections.dellemc.openmanage.plugins.module_utils.ome import RestOME

# job poll intervals and timeout
JOB_TIMEOUT_SECONDS = 300
JOB_POLL_INTERVAL_SECONDS = 5
# slots indices
SLOT_START_INDEX = 1
SLOT_END_INDEX = 8
# OME URIs
DEVICE_URI = "DeviceService/Devices"
JOBS_URI = "JobService/Jobs"
SERVER_QUICK_DEPLOY_URI = "DeviceService/Devices({0})/Settings('ServerQuickDeploy')"
IOM_QUICK_DEPLOY_URI = "DeviceService/Devices({0})/Settings('IOMQuickDeploy')"
# message strings
MSG_DEVICE_ID_FAIL = "Failed to find a chassis device with the Device ID {0}."
MSG_DEVICE_SVCTAG_FAIL = "Failed to find a chassis device with the Service Tag {0}."
MSG_CHANGES_FOUND = "Changes found to be applied."
MSG_NO_CHANGES_FOUND = "No changes found to be applied."
MSG_SUCCESS = "Successfully updated the quick deploy options settings."
MSG_FAILURE = "Failed to update the quick deploy options settings."


def _validate_inputs(module):
    """Validates the quick deploy options that have been passed
    in as module arguments.""" 
    quick_deploy = module.params.get("quick_deploy_options")
    if quick_deploy:
        # IPv4 validations
        ipv4_network_type = quick_deploy.get("ipv4_network_type")
        ipv4_subnet_mask = quick_deploy.get("ipv4_subnet_mask")
        ipv4_gateway = quick_deploy.get("ipv4_gateway")

        if (
            ipv4_network_type
            and ipv4_network_type == "Static"
            and (not all((ipv4_subnet_mask, ipv4_gateway)))
        ):
            module.fail_json(
                msg="Mandatory arguments missing: 'ipv4_subnet_mask' and "
                "'ipv4_gateway' are mandatory arguments when "
                "'ipv4_network_type' is 'Static'."
            )

        if ipv4_subnet_mask:
            if (not ipv4_network_type) or (ipv4_network_type != "Static"):
                module.fail_json(
                    msg="ValueError: 'ipv4_subnet_mask' can only be set if "
                    "'ipv4_network_type' is 'Static'."
                )

            try:
                ipaddress.ip_address(ipv4_subnet_mask)
            except ValueError as err:
                module.fail_json(
                    msg="ValueError: invalid ipv4_subnet_mask. {}".format(str(err))
                )

        if ipv4_gateway:
            if (not ipv4_network_type) or (ipv4_network_type != "Static"):
                module.fail_json(
                    msg="ValueError: 'ipv4_gateway' can only be set if "
                    "'ipv4_network_type' is 'Static'."
                )

            try:
                ipaddress.ip_address(ipv4_gateway)
            except ValueError as err:
                module.fail_json(
                    msg="ValueError: invalid ip4_gateway. {}".format(str(err))
                )

        # IPv6 validations
        ipv6_network_type = quick_deploy.get("ipv6_network_type")
        ipv6_prefix_length = quick_deploy.get("ipv6_prefix_length")
        ipv6_gateway = quick_deploy.get("ipv6_gateway")

        if (
            ipv6_network_type
            and ipv6_network_type == "Static"
            and (not all((ipv6_prefix_length, ipv6_gateway)))
        ):
            module.fail_json(
                msg="Mandatory arguments missing: 'ipv6_prefix_length' "
                "and 'ipv6_gateway' are mandatory arguments when "
                "'ipv6_network_type' is 'Static'."
            )

        ipv6_prefix_length_range = range(1, 129)
        if ipv6_prefix_length and ipv6_prefix_length not in ipv6_prefix_length_range:
            module.fail_json(
                msg="ValueError: 'ipv6_prefix_length' must be " "between 1 and 128."
            )

        if ipv6_gateway:
            if (not ipv6_network_type) or (ipv6_network_type != "Static"):
                module.fail_json(
                    msg="ValueError: 'ipv6_gateway' can only be set "
                    "if 'ipv6_network_type' is 'Static'."
                )

            try:
                ipaddress.ip_address(ipv6_gateway)
            except ValueError as err:
                module.fail_json(
                    msg="ValueError: invalid 'ip6_gateway'. " "{0}".format(str(err))
                )

        # Slots validation
        slots = quick_deploy.get("slots")
        if slots:
            for slot in slots:
                slot_id = slot.get("slot_id")
                if (not slot_id) or (
                    slot_id not in range(SLOT_START_INDEX, SLOT_END_INDEX + 1)
                ):
                    module.fail_json(
                        msg="ValueError: invalid 'slot_id'. "
                        "Valid slot_id values are [1, 8]."
                    )

                slot_ipv4_address = slot.get("slot_ipv4_address")
                if slot_ipv4_address:
                    if (not ipv4_network_type) or (ipv4_network_type != "Static"):
                        module.fail_json(
                            msg="Error: slot_ipv4_address can only be set if "
                            "'ipv4_network_type' is 'Static'."
                        )

                    try:
                        ipaddress.ip_address(slot_ipv4_address)
                    except ValueError as err:
                        module.fail_json(
                            msg="ValueError: invalid slot_ipv4_address for "
                            "Slot {0}. {1}".format(slot["slot_id"], str(err))
                        )

                slot_ipv6_address = slot.get("slot_ipv6_address")
                if slot_ipv6_address:
                    if (not ipv6_network_type) or (ipv6_network_type != "Static"):
                        module.fail_json(
                            msg="Error: 'slot_ipv6_address' can only be set if "
                            "'ipv6_network_type' is 'Static'."
                        )

                    try:
                        ipaddress.ip_address(slot_ipv6_address)
                    except ValueError as err:
                        module.fail_json(
                            msg="ValueError: invalid slot_ipv6_address for "
                            "Slot {0}. {1}".format(slot["slot_id"], str(err))
                        )

    return True


def get_default_quick_deploy_options(setting_type):
    """Returns a dict of quick deploy options with default values."""

    quick_deploy_options = {
        "DeviceId": 0,
        "Password": "",
        "ProtocolTypeV4": True,
        "NetworkTypeV4": "DHCP",
        "IpV4SubnetMask": "255.255.255.0",
        "IpV4Gateway": "0.0.0.0",
        "NetworkTypeV6": "DHCP",
        "ProtocolTypeV6": False,
        "PrefixLength": "0",
        "IpV6Gateway": "::",
        "Slots": [],
    }

    slot_type_map = {"ServerQuickDeploy": 2000, "IOMQuickDeploy": 4000}

    for index in range(SLOT_START_INDEX, SLOT_END_INDEX + 1):
        slot = {
            "SlotId": index,
            "SlotSelected": False,
            "SlotType": slot_type_map[setting_type],
            "SlotIPV4Address": "0.0.0.0",
            "SlotIPV6Address": "::",
            "VlanId": "",
        }
        quick_deploy_options["Slots"].append(slot)

    return quick_deploy_options


def get_device_quick_deploy_options(device_id, setting_type, rest_obj):
    """Returns the existing quick deploy options settings for
    the device ID."""
    quick_deploy_options = get_default_quick_deploy_options(setting_type)

    quick_deploy_uri = SERVER_QUICK_DEPLOY_URI
    if setting_type == "IOMQuickDeploy":
        quick_deploy_uri = IOM_QUICK_DEPLOY_URI

    response = rest_obj.invoke_request("GET", quick_deploy_uri.format(device_id))
    if response.status_code == 200:
        quick_deploy_response = response.json_data

        # update quick deploy attributes other than slots
        for key, _ in quick_deploy_options.items():
            if key in quick_deploy_response and key != "Slots":
                quick_deploy_options[key] = quick_deploy_response[key]

        # update slot information
        for slot in quick_deploy_options["Slots"]:
            for slot_resp in quick_deploy_response["Slots"]:
                if slot["SlotId"] == slot_resp["SlotId"]:
                    slot.update(
                        {
                            key: value
                            for (key, value) in slot_resp.items()
                            if key in slot.keys()
                        }
                    )

        # update device ID
        quick_deploy_options["DeviceId"] = device_id

    return quick_deploy_options


def get_module_quick_deploy_options(module, existing_options):
    """Returns a dict of quick deploy options that have been provided
    as module arguments."""
    try:
        target_options = copy.deepcopy(existing_options)
    except copy.Error as err:
        module.fail_json(
            msg="Failed to copy the quick deploy options. Error: {}".format(str(err))
        )

    quick_deploy_params = module.params.get("quick_deploy_options")

    if quick_deploy_params:
        # IPv4 settings
        ipv4_enabled = quick_deploy_params.get("ipv4_enabled")
        if ipv4_enabled:
            target_options["ProtocolTypeV4"] = ipv4_enabled

        ipv4_network_type = quick_deploy_params.get("ipv4_network_type")
        if ipv4_network_type:
            target_options["NetworkTypeV4"] = ipv4_network_type

        ipv4_subnet_mask = quick_deploy_params.get("ipv4_subnet_mask")
        if ipv4_subnet_mask:
            target_options["IpV4SubnetMask"] = ipv4_subnet_mask

        ipv4_gateway = quick_deploy_params.get("ipv4_gateway")
        if ipv4_gateway:
            target_options["IpV4Gateway"] = ipv4_gateway

        # IPv6 settings
        ipv6_enabled = quick_deploy_params.get("ipv6_enabled")
        if ipv6_enabled:
            target_options["ProtocolTypeV6"] = ipv6_enabled

        ipv6_network_type = quick_deploy_params.get("ipv6_network_type")
        if ipv6_network_type:
            target_options["NetworkTypeV6"] = ipv6_network_type

        ipv6_prefix_length = quick_deploy_params.get("ipv6_prefix_length")
        if ipv6_prefix_length:
            target_options["PrefixLength"] = ipv6_prefix_length

        ipv6_gateway = quick_deploy_params.get("ipv6_gateway")
        if ipv6_gateway:
            target_options["IpV6Gateway"] = ipv6_gateway

        # Slots
        slots = quick_deploy_params.get("slots", [])
        for slot in slots:
            for target_slot in target_options["Slots"]:
                if slot["slot_id"] == target_slot["SlotId"]:
                    slot_ipv4_address = slot.get("slot_ipv4_address")
                    if slot_ipv4_address:
                        target_slot["SlotIPV4Address"] = slot_ipv4_address

                    slot_ipv6_address = slot.get("slot_ipv6_address")
                    if slot_ipv6_address:
                        target_slot["SlotIPV6Address"] = slot_ipv6_address

                    vlan_id = slot.get("vlan_id")
                    if vlan_id is not None:
                        if vlan_id:
                            target_slot["VlanId"] = check_type_str(vlan_id)
                        else:
                            target_slot["VlanId"] = ""

    return target_options


def get_diff_payload_quick_deploy_options(module, new_options, old_options):
    """Returns the diff between existing quick deploy options and the new
    quick deploy options and the corresponding HTTPS payload.""" 

    payload = get_default_quick_deploy_options_payload(module.params["setting_type"])

    options_to_params_keys = get_option_names_to_payload_params_names()

    # compare and diff all attributes except slots
    equal_options = {
        key: value
        for (key, value) in new_options.items()
        if (key in set(old_options) - {"Slots"}) and (value == old_options[key])
    }
    diff_options = {
        key: value
        for (key, value) in new_options.items()
        if (key in set(old_options) - {"Slots"}) and (value != old_options[key])
    }

    # remove password from the equal options dict if present
    equal_options.pop("Password", None)

    # check for network type
    for key in ["NetworkTypeV4", "NetworkTypeV6"]:
        if diff_options.get(key) == "DHCP" and old_options.get(key) == "Dynamic":
            diff_options.pop(key)

    # merge the dicts
    try:
        merged_options = copy.deepcopy(equal_options)
    except copy.Error as err:
        module.fail_json(
            msg="Failed to copy the equal options. Error: {}".format(str(err))
        )

    merged_options.update(diff_options)

    for key, value in merged_options.items():
        payload["Params"].append(
            {"Key": options_to_params_keys[key], "Value": check_type_str(value)}
        )

    # now compare and diff Slots
    slot_diff = [
        slot for slot in new_options["Slots"] if slot not in old_options["Slots"]
    ]

    if slot_diff:
        diff_options["Slots"] = slot_diff
        for slot in slot_diff:
            slot_key = "slotId={0}".format(slot["SlotId"])
            slot_value = ";".join(
                {
                    "{0}={1}".format(value, slot[key])
                    for key, value in set(options_to_params_keys["Slots"].items())
                    - {"SlotId"}
                }
            )
            payload["Params"].append({"Key": slot_key, "Value": slot_value})

    return diff_options, payload


def get_option_names_to_payload_params_names():
    """Returns a map of Quick Deploy Options attributes names to
    their respective Quick Deploy Job Payload names."""
    return {
        "DeviceId": "deviceId",
        "Password": "rootCredential",
        "ProtocolTypeV4": "protocolTypeV4",
        "NetworkTypeV4": "networkTypeV4",
        "IpV4SubnetMask": "subnetMaskV4",
        "IpV4Gateway": "gatewayV4",
        "ProtocolTypeV6": "protocolTypeV6",
        "NetworkTypeV6": "networkTypeV6",
        "IpV6Gateway": "gatewayV6",
        "PrefixLength": "prefixLength",
        "Slots": {
            "SlotId": "slotId",
            "SlotSelected": "SlotSelected",
            "SlotType": "SlotType",
            "SlotIPV4Address": "IPV4Address",
            "SlotIPV6Address": "IPV6Address",
            "VlanId": "VlanId",
        },
    }


def get_default_quick_deploy_options_payload(setting_type):
    """Returns the default payload for the quick deploy job."""
    if setting_type == "ServerQuickDeploy":
        ops_name_param = {"Key": "operationName", "Value": "SERVER_QUICK_DEPLOY"}
    else:
        ops_name_param = {"Key": "operationName", "Value": "IOM_QUICK_DEPLOY"}

    payload = {
        "JobName": "Quick Deploy",
        "JobDescription": "New Quick Deploy Configuration for DeviceId ({0})",
        "Schedule": "startnow",
        "State": "Enabled",
        "Targets": [],
        "Params": [ops_name_param],
        "JobType": {"Id": 42, "Name": "QuickDeploy_Task"},
    }
    return payload


def update_quick_deploy_options(module, rest_obj, payload):
    """Updates the quick deploy option settings as per the payload."""
    # create the quick deploy job
    try:
        response = rest_obj.invoke_request("POST", JOBS_URI, data=payload)
        if response.status_code == 201:
            quick_deploy_job_id = response.json_data["Id"]
            job_failed, _ = rest_obj.job_tracking(
                quick_deploy_job_id,
                job_wait_sec=JOB_TIMEOUT_SECONDS,
                sleep_time=JOB_POLL_INTERVAL_SECONDS,
            )

            if job_failed:
                module.fail_json(msg=MSG_FAILURE)

    except HTTPError as err:
        module.fail_json(msg=str(err), payload=payload, error_info=json.load(err))
    except Exception as err:
        module.fail_json(msg=str(err))

    return True


def get_target_device_id_lead_chassis(module, domains):
    """Returns device ID for the lead chassis if both device ID or service tag
    are absent in the module argument. If a valid device ID or service tag
    has been provided for a member chassis, then it returns the member chassis
    device ID
    """
    target_device_id = None
    device_id = module.params.get("device_id")
    device_svctag = module.params.get("device_service_tag")
    lead_chassis_device_id = None
    lead_chassis_svctag = None
    domain_chassis_ids = []
    domain_chassis_svctags = []
    domain_chassis_svctags_ids = {}

    # get the device ID and service tag for the lead chassis
    for domain in domains:
        if domain["PublicAddress"][0] == module.params["hostname"]:
            lead_chassis_device_id = domain["DeviceId"]
            lead_chassis_svctag = domain["Identifier"].lower()

        domain_chassis_ids.append(domain["DeviceId"])
        domain_chassis_svctags.append(domain["Identifier"].lower())
        domain_chassis_svctags_ids[domain["Identifier"].lower()] = domain["DeviceId"]

    if device_id:
        if device_id not in domain_chassis_ids:
            module.fail_json(msg=MSG_DEVICE_ID_FAIL.format(device_id))
        target_device_id = device_id
    elif device_svctag:
        if device_svctag.lower() not in domain_chassis_svctags:
            module.fail_json(msg=MSG_DEVICE_SVCTAG_FAIL.format(device_svctag))

        target_device_id = domain_chassis_svctags_ids[device_svctag.lower()]
    else:
        # both device ID and service tag have not been provided as module arguments
        # use the lead chassis device ID
        target_device_id = lead_chassis_device_id

    return target_device_id


def get_target_device_id_standalone_chassis(module, domains):
    """Returns device ID for the standalone Chassis"""
    target_device_id = None
    device_id = module.params.get("device_id")
    device_svctag = module.params.get("device_service_tag")
    standalone_chassis_device_id = None
    standalone_chassis_svc_tag = None

    # get the device ID and service tag for the standalone chassis
    standalone_chassis_device_id = domains[0]["DeviceId"]
    standalone_chassis_svc_tag = domains[0]["Identifier"].lower()

    if device_id:
        if device_id != standalone_chassis_device_id:
            module.fail_json(
                msg="For a standalone chassis, the 'device_id' ({0}) should "
                "be same as the device ID ({1}) for the standalone chassis "
                "or left blank.".format(device_id, standalone_chassis_device_id)
            )
        target_device_id = device_id
    elif device_svctag:
        if device_svctag.lower() != standalone_chassis_svc_tag:
            module.fail_json(
                msg="For a standalone chassis, the 'device_service_tag' ({0}) "
                "should be same as the service tag ({1}) for the standalone "
                "chassis or left blank.".format(
                    device_svctag, standalone_chassis_svc_tag
                )
            )
        target_device_id = standalone_chassis_device_id
    else:
        # both device ID and service tag have not been provided as module arguments
        # use the standalone chassis device ID
        target_device_id = standalone_chassis_device_id

    return target_device_id


def get_chassis_domain_role(module, rest_obj):
    """Returns Chassis domain role type either STNADALONE, LEAD,or MEMBER"""
    domain_role = None

    domain_url = "ManagementDomainService/Domains"
    response = rest_obj.invoke_request("GET", domain_url)
    if response.status_code == 200:
        domains = response.json_data.get("value", [])
        for domain in domains:
            if domain["PublicAddress"][0] == module.params["hostname"]:
                domain_role = domain["DomainRoleTypeValue"]
                break

    return domain_role, domains


def run_configure_quick_deploy_options(module, rest_obj):
    """Configure the quick deploy options settings for a chassis."""
    domain_role, domains = get_chassis_domain_role(module, rest_obj)

    # get the device ID for the chassis
    if domain_role == "LEAD":
        device_id = get_target_device_id_lead_chassis(module, domains)
    elif domain_role == "STANDALONE":
        device_id = get_target_device_id_standalone_chassis(
            module, domains
        )
    elif domain_role == "MEMBER":
        module.fail_json(msg="This is not a LEAD chassis for the domain.")
    else:
        module.fail_json(msg="Failed to retrieve the domain role for the chassis.")

    # Get existing quick deploy options settings
    existing_options = get_device_quick_deploy_options(
        device_id, module.params["setting_type"], rest_obj
    )

    # Get target quick deploy options
    target_options = get_module_quick_deploy_options(module, existing_options)

    diff, payload = get_diff_payload_quick_deploy_options(
        module, target_options, existing_options
    )

    if diff:
        if module.check_mode:
            module.exit_json(changed=True, msg=MSG_CHANGES_FOUND, diff=diff)
        else:
            result = update_quick_deploy_options(module, rest_obj, payload)
            if result:
                module.exit_json(changed=True, msg=MSG_SUCCESS)
            else:
                module.fail_json(msg=MSG_FAILURE)
    else:
        module.exit_json(msg=MSG_NO_CHANGES_FOUND)


def main():
    quick_deploy_options = {
        "password": {"required": False, "type": "str", "no_log": True},
        "ipv4_enabled": {"required": False, "type": "bool"},
        "ipv4_network_type": {
            "required": False,
            "type": "str",
            "choices": ["Static", "DHCP"],
        },
        "ipv4_subnet_mask": {"required": False, "type": "str"},
        "ipv4_gateway": {"required": False, "type": "str"},
        "ipv6_enabled": {"required": False, "type": "bool"},
        "ipv6_network_type": {
            "required": False,
            "type": "str",
            "choices": ["Static", "DHCP"],
        },
        "ipv6_prefix_length": {"required": False, "type": "int"},
        "ipv6_gateway": {"required": False, "type": "str"},
        "slots": {
            "required": False,
            "type": "list",
            "elements": "dict",
            "options": {
                "slot_id": {"required": True, "type": "int"},
                "slot_ipv4_address": {"required": False, "type": "str"},
                "slot_ipv6_address": {"required": False, "type": "str"},
                "vlan_id": {"required": False, "type": "int"},
            },
        },
    }

    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": "str"},
            "username": {"required": True, "type": "str"},
            "password": {"required": True, "type": "str", "no_log": True},
            "port": {"required": False, "type": "int", "default": 443},
            "device_id": {"required": False, "type": "int"},
            "device_service_tag": {"required": False, "type": "str"},
            "setting_type": {
                "required": False,
                "type": "str",
                "choices": ["ServerQuickDeploy", "IOMQuickDeploy"],
                "default": "ServerQuickDeploy",
            },
            "quick_deploy_options": {
                "required": False,
                "type": "dict",
                "options": quick_deploy_options,
            },
        },
        mutually_exclusive=[("device_id", "device_service_tag")],
        supports_check_mode=True,
    )

    try:
        if not module.params.get("quick_deploy_options"):
            module.exit_json(
                msg="No quick deploy options found in module arguments. Nothing to do."
            )

        _validate_inputs(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            run_configure_quick_deploy_options(module, rest_obj)

    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (
        IOError,
        ValueError,
        SSLError,
        TypeError,
        ConnectionError,
        AttributeError,
        IndexError,
        KeyError,
    ) as err:
        module.fail_json(msg=str(err))


if __name__ == "__main__":
    main()
