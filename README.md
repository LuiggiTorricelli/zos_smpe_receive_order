# Ansible z/OS SMP/E RECEIVE ORDER role

The Ansible role `zos_smpe_receive_order` will perform a sequence of steps to execute the SMP/E RECEIVE ORDER command to submit an Internet Service Retrieval request to the IBM Automated Delivery Request server, considering the variables informed by the user on the specified z/OS host(s).

## Requirements

Python and Z Open Automation Utilities must be installed on the remote z/OS system, since the modules `zos_find` and `zos_mvs_raw` from the collection `ibm.ibm_zos_core` are used along the role.

## Role Variables

This role has multiple variables. The descriptions and defaults for all these variables can be found in the **[`defaults/main.yml`](/defaults/main.yml)** file and **[`meta/argument_specs.yml`](/meta/argument_specs.yml)**, together with a detailed description below:

| Variable | Description | Optional? |
| -------- | ----------- | :-------: |
| **[`show_output`](/defaults/main.yml)** | Display the output at the end | Yes<br>(default: `true`) |
| **[`smpe_csi`](/meta/argument_specs.yml)** | SMP/E GLOBAL CSI data set name to be used | No |
| **[`smpe_client`](/meta/argument_specs.yml)** | Options for the CLIENT statement with more details below | No |
| **[`smpe_options`](/defaults/main.yml)** | Options to consider on the RECEIVE statement | Yes<br>(default: `[]`) |
| **[`smpe_order`](/meta/argument_specs.yml)** | Options for the ORDER operand with more details below | No |
| **[`smpe_orderserver`](/meta/argument_specs.yml)** | Options for the ORDERSERVER statement with more details below | No |
| **[`smpe_smpnts`](/meta/argument_specs.yml)** | SMP/E SMPNTS (SMP/E Network Temporary Store) directory on z/OS Unix to be used for temporary storage | No |

On `smpe_options`, if you specify certain values, it will be ignored and not considered. The ignored values can be found in **[`smpe_ignore_options`](/vars/main.yml)**.

### Detailed structure of variable `smpe_client`, based on IBM SMP/E documentation (see **[Content of CLIENT data set](https://www.ibm.com/docs/en/zos/3.1.0?topic=processing-content-client-data-set)**):

| Variable | Attribute | Type | Optional? |
| -------- | --------- | :--: | :-------: |
| `smpe_client` | `classpath` | string | Yes |
| `smpe_client` | `debug` | boolean | Yes<br>(default: `False`) |
| `smpe_client` | `downloadkeyring` | string<br>_`keyring-name`_ or `javatruststore` | Yes |
| `smpe_client` | `downloadmethod` | string<br>`ftp`, `http` or `https` | Yes<br>(default: `ftp`) |
| `smpe_client` | `firewall` | dictionary | Yes |
| `smpe_client` | `firewall.firecmd` | list[string] | No |
| `smpe_client` | `firewall.server` | dictionary | No |
| `smpe_client` | `firewall.server.account` | string | Yes |
| `smpe_client` | `firewall.server.host` | string | No |
| `smpe_client` | `firewall.server.port` | integer (1 <= n <= 65535) | Yes |
| `smpe_client` | `firewall.server.pw` | string | Yes |
| `smpe_client` | `firewall.server.user` | string | Yes |
| `smpe_client` | `ftpccc` | boolean | Yes<br>(default: `True`) |
| `smpe_client` | `ftpoptions` | string | Yes |
| `smpe_client` | `httpproxy` | dictionary | Yes |
| `smpe_client` | `httpproxy.host` | string | No |
| `smpe_client` | `httpproxy.port` | integer (1 <= n <= 65535) | Yes |
| `smpe_client` | `httpproxy.pw` | string | Yes |
| `smpe_client` | `httpproxy.user` | string | Yes |
| `smpe_client` | `httpsocksproxy` | dictionary | Yes |
| `smpe_client` | `httpsocksproxy.host` | string | No |
| `smpe_client` | `httpsocksproxy.port` | integer (1 <= n <= 65535) | Yes |
| `smpe_client` | `httpsocksproxy.pw` | string | Yes |
| `smpe_client` | `httpsocksproxy.user` | string | Yes |
| `smpe_client` | `javadebugoptions` | string | Yes |
| `smpe_client` | `javahome` | string | Yes |
| `smpe_client` | `retry` | integer (0 <= n <= 9) | Yes<br>(default: `0`) |
| `smpe_client` | `signaturekeyring` | string<br>_`keyring-name`_ or `javatruststore` | Yes |

### Detailed structure of variable `smpe_order`, based on IBM SMP/E documentation (see **[Content of ORDER operand](https://www.ibm.com/docs/en/zos/3.1.0?topic=s-operands-10)**):

| Variable | Attribute | Type | Optional? |
| -------- | --------- | :--: | :-------: |
| `smpe_order` | `content` | string<br>`ALL`, `APARS(aaaa1, ...)`, `CRITICAL`,<br>`HOLDDATA`, `PTFS(pppp1, ...)` or `RECOMMENDED` | No |
| `smpe_order` | `fortgtzones` | list[string] | Yes |
| `smpe_order` | `pending` | string | Yes |
| `smpe_order` | `transferonly` | boolean | Yes<br>(default: `False`) |
| `smpe_order` | `wait` | integer or `NOLIMIT` | Yes<br>(default: `120`) |

### Detailed structure of variable `smpe_orderserver`, based on IBM SMP/E documentation (see **[Content of the ORDERSERVER data set](https://www.ibm.com/docs/en/zos/3.1.0?topic=processing-content-orderserver-data-set)**):

| Variable | Attribute | Type | Optional? |
| -------- | --------- | :--: | :-------: |
| `smpe_orderserver` | `url` | string | No |
| `smpe_orderserver` | `certificate` |string | No |
| `smpe_orderserver` | `keyring` | string | No |
| `smpe_orderserver` | `inventory` | string<br>`ibm` or `all` | Yes<br>(default: `ibm`) |

## Dependencies

None.

## Example Playbook

On the scenario below, the role `zos_smpe_receive_order` is being used to receive and request, to the GLOBAL zone found in data set `SMPE.GLOBAL.CSI`, recommended PTFs (based on the latest RSU available) that are missing on the SMP/E target zone `TGTZAAA`, but ONLY for the FMIDs `HSQDD10` and `JSQDD1Q`.

    - hosts: zos_server
      roles:
        - role: zos_smpe_receive_order
          smpe_csi: "SMPE.GLOBAL.CSI"
          smpe_client:
            javadebugoptions: "-Dcom.ibm.smp.debug=severe"
            javahome: "/usr/lpp/java/"
            classpath: "/usr/lpp/smp/classes"
            downloadmethod: "https"
            downloadkeyring: "javatruststore"
            httpproxy:
              host: "proxy.example.com"
              port: 1234
            firewall:
              server:
                host: "proxy.example.com"
                port: 1234
                firecmd:
                  - "&REMOTE_USER;@&REMOTE_HOST;"
                  - "&REMOTE_PW;"
          smpe_orderserver:
            url: "https://eccgw01.boulder.ibm.com/services/projects/ecc/ws"
            keyring: "IBMUSER/SHOPZKR"
            certificate: "SMPE Client Cert 2024"
          smpe_options:
            - LIST
            - FORFMID(HSQDD10,JSQDD1Q)
          smpe_order:
            content: "RECOMMENDED"
            fortgtzones:
              - TGTZAAA
          smpe_smpnts: "/usr/lpp/db2/smpnts/"
          show_output: true

## Sample Output

When this role is executed, it will execute the SMP/E RECEIVE ORDER command, failing and displaying its output if return code of the GIMSMP program is greater than 4, otherwise it will end successfully.

A fact named `zos_smpe_receive_order_details` will be set if the role runs successfully, containing details about the order that was made, such as the order ID, received SYSMODs and latest RSU and/or PUT source IDs assigned during the order. It will be displayed if `show_output` is set to `true`.

Be aware that the `latest_put` and `latest_rsu` attributes will be determined by all assignments that happened on the _RECEIVE summary report_, not only by the SYSMODs that were received. If no assignments of RSU and/or PUT source IDs are performed, the value of the attribute will be `NOT FOUND`.

    "zos_smpe_receive_order_details": {
        "latest_put": "PUT2406",
        "latest_rsu": "RSU2410",
        "order_id": "ORD00001",
        "sysmods": [
            {
                "features": [],
                "source_ids": [
                    "ORD00001",
                    "RSU2409",
                ],
                "sysmod_id": "UI11111"
            },
            {
                "features": [],
                "source_ids": [
                    "ORD00001",
                    "RSU2410",
                    "SMCCOR"
                ],
                "sysmod_id": "UI12345"
            },
            {
                "features": [],
                "source_ids": [],
                "sysmod_id": "UI98765"
            }
        ]
    }

During the execution of program GIMSMP, the output DD statements SMPLIST, SMPOUT, SMPRT and SYSPRINT will be temporarily saved on user's home directory with names `YYYYMMDDhhmmss_zos_smpe_receive_order_<dd_name>`. If the process finishes successfully, these files will be deleted.

## License

This role is licensed under licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Author Information

This role was created in 2024 by Luiggi Torricelli.
