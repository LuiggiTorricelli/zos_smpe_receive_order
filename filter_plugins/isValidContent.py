from __future__ import absolute_import, division, print_function
from ansible.errors import AnsibleFilterTypeError
from ansible.parsing.yaml.objects import AnsibleUnicode
from ansible.template.native_helpers import NativeJinjaText

import re

__metaclass__ = type

class FilterModule(object):
    def filters(self):
        filters = {
            "isValidContent": self.isValidContent,
        }
        return filters
    
    def isString(self, input_content):
        if type(input_content) != AnsibleUnicode and type(input_content) != str and type(input_content) != NativeJinjaText:
            return(False)
        return(True)

    def isValidOrder(self, input_content):
        possible_parms = ["content", "fortgtzones", "pending", "wait", "transferonly"]
        error_msgs = []

        input_attrs = input_content.keys()
        if "content" not in input_attrs:
            error_msgs.append("ORDER must contain the CONTENT to be received.")
        for attr in input_attrs:
            if attr not in possible_parms:
                error_msgs.append("Attribute '%s' is not a possible attribute for ORDER." % attr)
            else:
                error_msgs.append(type(input_content[attr]))
                if attr == "content" and (not self.isString(input_content[attr]) or not re.match(r"^(CRITICAL|HOLDDATA|RECOMMENDED|ALL|APARS\(.+\)|PTFS\(.+\))$", input_content[attr])):
                    error_msgs.append("Attribute '%s' must be one of the following: CRITICAL, HOLDDATA, RECOMMENDED, ALL, APARS(apar1, apar2, ...) or PTFS(ptf1, ptf2, ...)." % attr)
                elif attr == "wait" and (type(input_content[attr]) != AnsibleUnicode or type(input_content[attr]) != str) and (not re.match(r"^(\d{1,4}|NOLIMIT)$", str(input_content[attr])) or (re.match(r"^(\d{1,4})$", str(input_content[attr])) and (int(input_content[attr]) < 0 or int(input_content[attr]) > 1440))):
                    error_msgs.append("Optional attribute '%s' must be either an integer in the range 0 through 1440 or the value 'NOLIMIT'." % attr)
                elif attr == "fortgtzones" and (not isinstance(input_content[attr], list) or False in list(map(lambda x: True if (isinstance(x, str) or isinstance(x, AnsibleUnicode) or isinstance(x, NativeJinjaText)) else False, input_content[attr])) or len(input_content[attr]) == 0):
                    error_msgs.append("Optional attribute '%s' must be a list of strings." % attr)
                elif attr == "pending" and (not self.isString(input_content[attr]) or len(input_content[attr]) != 8 or not re.match(r"^(ORD\d{5})$", input_content[attr].upper())):
                    error_msgs.append("Optional attribute '%s' must be ORDnnnnn, where nnnnn in the range 00001 through 99999." % attr)
                elif attr == "transferonly" and not isinstance(input_content[attr], bool):
                    error_msgs.append("Optional attribute '%s' must be a boolean value - true or false." % attr)
        
        if len(error_msgs) > 0:
            raise AnsibleFilterTypeError("isValidOrder - %s" % "\n".join(error_msgs))
        
        return(True)
    
    def isValidOrderServer(self, input_content):
        possible_parms = {
            "url": str(),
            "certificate": str(),
            "keyring": str(),
            "inventory": ["ibm", "all"],
        }

        error_msgs = []

        input_attrs = input_content.keys()
        if "url" not in input_attrs or "certificate" not in input_attrs or "keyring" not in input_attrs:
            error_msgs.append("ORDERSERVER must contain the keys 'url', 'certificate', 'keyring' and optionally 'inventory'.")
        for attr in input_attrs:
            if attr not in possible_parms:
                error_msgs.append("Attribute '%s' is not a possible attribute for ORDERSERVER." % attr)
            else:
                if isinstance(possible_parms[attr], list):
                    if input_content[attr] not in possible_parms[attr]:
                        error_msgs.append("Attribute '%s' should have a value of: %s." % (attr, possible_parms[attr]))
                else:
                    if type(input_content[attr]) != type(possible_parms[attr]) and not (type(input_content[attr]) == AnsibleUnicode and type(possible_parms[attr]) == str):
                        error_msgs.append("Attribute '%s' must have a value of the type %s." % (attr, str(type(possible_parms[attr]))))
                    elif isinstance(input_content[attr], str) and input_content[attr].strip() == "":
                        error_msgs.append("Attribute '%s' was informed with an empty value. Either inform a correct value or do not inform this attribute." % attr)
        
        if len(error_msgs) > 0:
            raise AnsibleFilterTypeError("isValidOrderServer - %s" % "\n".join(error_msgs))
        
        return(True)

    def isValidClientInfo(self, input_content):
        optional_parms = {
            "debug": [False, True],
            "retry": int(),
            "ftpccc": [False, True],
            "javahome": str(),
            "classpath": str(),
            "javadebugoptions": str(),
            "downloadmethod": ["ftp", "http", "https"],
            "downloadkeyring": str(),
            "signaturekeyring": str(),
        }
        
        sections = ["ftpoptions", "firewall", "httpproxy", "httpsocksproxy"]

        error_msgs = []

        input_attrs = input_content.keys()
        for attr in input_attrs:
            if attr in sections:
                if attr == "ftpoptions" and (not isinstance(input_content[attr], str) or input_content[attr].strip() == ""):
                    error_msgs.append("Attribute '%s' must be a string or not be informed." % attr)

                elif attr == "firewall":
                    if not isinstance(input_content[attr], dict) or "server" not in input_content[attr] or "firecmd" not in input_content[attr]:
                        error_msgs.append("Attribute '%s' must be a dictionary with attributes 'server' and 'firecmd'." % attr)
                    else:
                        for key in input_content[attr].keys():
                            if key not in ["server", "firecmd"]:
                                error_msgs.append("Attribute '%s' is not a possible attribute for FIREWALL." % key)
                            elif key == "server":
                                if not isinstance(input_content[attr][key], dict):
                                    error_msgs.append("FIREWALL attribute '%s' must be a dictionary." % key)
                                    continue
                                elif "host" not in input_content[attr][key] or not isinstance(input_content[attr][key]["host"], str):
                                    error_msgs.append("FIREWALL attribute '%s' must contain the required string attribute 'host'." % key)
                                for server_key in input_content[attr][key]:
                                    if server_key not in ["account", "host", "user", "port", "pw"]:
                                        error_msgs.append("Attribute '%s' is not a possible attribute for SERVER." % server_key)
                                        continue
                                    elif server_key == "port" and (not isinstance(input_content[attr][key][server_key], int) or input_content[attr][key][server_key] < 1 or input_content[attr][key][server_key] > 65535):
                                        error_msgs.append("SERVER attribute '%s' must be an integer in the range 1 through 65535, or not be informed." % server_key)
                                        continue
                            elif key == "firecmd" and not isinstance(input_content[attr][key], list):
                                error_msgs.append("FIREWALL attribute '%s' must be list of strings." % key)
                                continue
                elif attr in ["httpproxy", "httpsocksproxy"]:
                    if not isinstance(input_content[attr], dict):
                        error_msgs.append("Attribute '%s' must be a dictionary." % attr)
                        continue
                    elif "host" not in input_content[attr] or not isinstance(input_content[attr]["host"], str):
                        error_msgs.append("Attribute '%s' must contain the required string attribute 'host'." % attr)
                    for key in input_content[attr]:
                        if key not in ["host", "user", "port", "pw"]:
                            error_msgs.append("Attribute '%s' is not a possible attribute for %s." % (key, attr.upper()))
                            continue
                        elif key == "port" and (not isinstance(input_content[attr][key], int) or input_content[attr][key] < 1 or input_content[attr][key] > 65535):
                            error_msgs.append("%s attribute '%s' must be an integer in the range 1 through 65535, or not be informed." % (attr.upper(), key))
                            continue

            elif attr not in optional_parms:
                error_msgs.append("Attribute '%s' is not a possible attribute for CLIENTINFO." % attr)

            else:
                if isinstance(optional_parms[attr], list):
                    if input_content[attr] not in optional_parms[attr]:
                        error_msgs.append("Attribute '%s' should have a value of: %s." % (attr, optional_parms[attr]))
                else:
                    if type(input_content[attr]) != type(optional_parms[attr]) and not (type(input_content[attr]) == AnsibleUnicode and type(optional_parms[attr]) == str):
                        error_msgs.append("Attribute '%s' must have a value of the type %s." % (attr, str(type(optional_parms[attr]))))
                    elif isinstance(input_content[attr], str) and input_content[attr].strip() == "":
                        error_msgs.append("Attribute '%s' was informed with an empty value. Either inform a correct value or do not inform this attribute." % attr)
                    elif attr == "retry" and (input_content[attr] < 0 or input_content[attr] > 9):
                        error_msgs.append("Attribute '%s' must be greater than or equal to 0 and less than or equal to 9." % attr)
        
        if len(error_msgs) > 0:
            raise AnsibleFilterTypeError("isValidClientInfo - %s" % "\n".join(error_msgs))
        
        return(True)

    def isValidContent(self, input_content, option):
        if not isinstance(input_content, dict):
            raise AnsibleFilterTypeError("isValidContent - Filter must be applied on a dictionary.")

        if not isinstance(option, str):
            raise AnsibleFilterTypeError("isValidContent - 'option' must be a string.")

        possible_options = ["ORDER", "CLIENTINFO", "ORDERSERVER"]
        option = option.upper()

        if option not in possible_options:
            raise AnsibleFilterTypeError("isValidContent - 'option' must be one of the following: %s" % str(possible_options))

        if option in ["CLIENTINFO"]:
            result = self.isValidClientInfo(input_content)
        elif option in ["ORDERSERVER"]:
            result = self.isValidOrderServer(input_content)
        elif option in ["ORDER"]:
            result = self.isValidOrder(input_content)
        
        return(result)