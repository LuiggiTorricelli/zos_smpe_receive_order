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

On the scenario below, the role `zos_smpe_receive_order` is being used to receive and request, to the GLOBAL zone found in data set `SMPE.GLOBAL.CSI`, recommended PTFs (based on the latest RSU available) that are missing on the SMP/E target zone `RSU2409`, but ONLY for the FMIDs `HSQDD10` and `JSQDD1Q`.

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
              - RSU2409
          smpe_smpnts: "/usr/lpp/db2/smpnts/"
          show_output: true

## Sample Output

When this role is successfully executed, it will fail if return code of the GIMSMP program is neither 0 nor 4, otherwise it will end successfully.

A fact named `zos_smpe_receive_order_output` is registered, containing the output of the SMP/E RECEIVE ORDER execution, based on the informed variables. It will be displayed if `show_output` is set to `true`.

<details>
    <summary><b><i>Click to see the sample output</i></b></summary>

    "zos_smpe_receive_order_output": {
        "backups": [],
        "changed": true,
        "dd_names": [
            {
                "byte_count": 1621,
                "content": [
                    "\fPAGE 0001  - NOW SET TO GLOBAL ZONE          DATE 10/30/24  TIME 11:28:31  SMP/E 37.25   SMPOUT   OUTPUT",
                    "",
                    "GIM42401I    THE FOLLOWING PARAMETERS WERE SPECIFIED ON THE EXEC STATEMENT FOR GIMSMP: 'PROCESS=WAIT'.",
                    "SET BOUNDARY(GLOBAL).",
                    "GIM20501I    SET PROCESSING IS COMPLETE. THE HIGHEST RETURN CODE WAS 00.",
                    "",
                    "",
                    "RECEIVE",
                    "  LIST",
                    "  FORFMID(",
                    "    HSQDD10",
                    "    JSQDD1Q",
                    "  )",
                    "  ORDER(",
                    "    ORDERSERVER(ORDRSRVR)",
                    "    CLIENT(CLNTINFO)",
                    "    CONTENT(",
                    "      RECOMMENDED",
                    "    )",
                    "    FORTGTZONES(",
                    "      RSU2409",
                    "    )",
                    "  )",
                    ".",
                    "",
                    "GIM68700I    ORDER ORD00001 HAS BEEN SENT TO THE SERVER AT https://eccgw01.boulder.ibm.com/services/projects/ecc/ws.",
                    "GIM69144I    ORDER ORD00001 IS READY FOR DOWNLOAD.",
                    "GIM66400I    THE TRANSFER IS COMPLETE FOR FILE",
                    "             /usr/lpp/db2/smpnts/ORD00001-30October2024-11.32.35.687/GIMPAF.XML.",
                    "GIM66400I    THE TRANSFER IS COMPLETE FOR FILE",
                    "             /usr/lpp/db2/smpnts/ORD00001-30October2024-11.32.35.687/SMPPTFIN/S0001.SHOPZ.SXXXXXXX.SMPMCS.pax.Z.",
                    "GIM66400I    THE TRANSFER IS COMPLETE FOR FILE",
                    "             /usr/lpp/db2/smpnts/ORD00001-30October2024-11.32.35.687/SMPHOLD/S0002.SHOPZ.SXXXXXXX.SMPHOLD.pax.Z.",
                    "GIM66400I    THE TRANSFER IS COMPLETE FOR FILE",
                    "             /usr/lpp/db2/smpnts/ORD00001-30October2024-11.32.35.687/GIMPAF.XSL.",
                    "GIM47600I    PACKAGE ORD00001-30October2024-11.32.35.687 WAS SUCCESSFULLY STAGED TO THE SMPNTS.",
                    "",
                    "",
                    "",
                    "GIM24801W    NO SYSMODS SATISFIED THE OPERANDS SPECIFIED ON THE RECEIVE COMMAND.",
                    "GIM20501I    RECEIVE PROCESSING IS COMPLETE. THE HIGHEST RETURN CODE WAS 04.",
                    "",
                    "",
                    "GIM20502I    SMP/E PROCESSING IS COMPLETE. THE HIGHEST RETURN CODE WAS 04. SMP/E IS AT LEVEL 37.25.",
                    ""
                ],
                "dd_name": "smpout",
                "name": "IBMUSER.P0397916.T0762002.C0000000",
                "record_count": 45
            },
            {
                "byte_count": 3714,
                "content": [
                    "\fPAGE 0001  - NOW SET TO GLOBAL ZONE          DATE 10/30/24  TIME 11:28:31  SMP/E 37.25   SMPRPT   OUTPUT",
                    "",
                    "RECEIVE",
                    "  LIST",
                    "  FORFMID(",
                    "    HSQDD10",
                    "    JSQDD1Q",
                    "  )",
                    "  ORDER(",
                    "    ORDERSERVER(ORDRSRVR)",
                    "    CLIENT(CLNTINFO)",
                    "    CONTENT(",
                    "      RECOMMENDED",
                    "    )",
                    "    FORTGTZONES(",
                    "      RSU2409",
                    "    )",
                    "  )",
                    ".\fPAGE 0002  - NOW SET TO GLOBAL ZONE          DATE 10/30/24  TIME 11:32:52  SMP/E 37.25   SMPRPT   OUTPUT",
                    "",
                    "              RECEIVE  SUMMARY  REPORT",
                    "",
                    "",
                    "",
                    "SYSMOD   STATUS        TYPE      SOURCEID  FEATURE   STATUS FIELD COMMENTS",
                    "",
                    "",
                    "                                                     *SYSMODS WITH SPECIFIED FMID(S) NOT FOUND IN SMPPTFIN*\fPAGE 0003  - NOW SET TO GLOBAL ZONE          DATE 10/30/24  TIME 11:32:52  SMP/E 37.25   SMPRPT   OUTPUT",
                    "",
                    "                                        RECEIVE ++HOLD/++RELEASE SUMMARY REPORT",
                    "",
                    "                           NOTE:  SMD NF   - SYSMOD NOT RELEASED - NOT FOUND IN THE GLOBAL ZONE",
                    "                                  RSN NF   - SYSMOD NOT RELEASED - NOT HELD FOR THIS REASONID",
                    "                                  INT HLD  - SYSMOD NOT RELEASED - CANNOT RELEASE INTERNAL SYS HOLD",
                    "",
                    "SYSMOD  TYPE STATUS   REASON  FMID                                  ++HOLD MCS STATEMENTS",
                    "",
                    "HSQDD10 FIXC HELD     AH47422 HSQDD10 ++HOLD(HSQDD10) FIXCAT FMID(HSQDD10) REASON(AH47422) RESOLVER(UI81853)",
                    "                                       CATEGORY(IBM.ProductInstall-RequiredService)",
                    "                                       DATE(22276).\fPAGE 0004  - NOW SET TO GLOBAL ZONE          DATE 10/30/24  TIME 11:32:52  SMP/E 37.25   SMPRPT   OUTPUT",
                    ...
                    ...
                    ...
                    ...
                    ...
                    ...
                    ...
                ],
                "dd_name": "smprpt",
                "name": "IBMUSER.P3620681.T0830011.C0000000",
                "record_count": 70
            },
            {
                "byte_count": 0,
                "content": [
                    ""
                ],
                "dd_name": "smplist",
                "name": "IBMUSER.P6843471.T0893250.C0000000",
                "record_count": 1
            },
            {
                "byte_count": 4841,
                "content": [
                    "",
                    "--------------------------------------------------------------------------------",
                    "DATE 10/30/24  TIME 11:32:39         SMP/E GIMJVCLT OUTPUT         SMP/E 37.25",
                    "",
                    "request type=\"closeRequest\" orderid=\"H99887766\" waitTime=\"116\"",
                    "",
                    "Oct 30, 2024 6:32:39 PM com.ibm.smp.GIMJVREQ sendRequest",
                    "SEVERE: Request Document:\r",
                    "POST /services/projects/ecc/ws/UpdateOrder?orderid=H99887766\r",
                    "Content-Type: text/xml; charset=utf-8\r",
                    "Accept: application/soap+xml, application/dime, multipart/related, text/*\r",
                    "Host: null\r",
                    "Cache-Control: no-cache\r",
                    "Pragma: no-cache\r",
                    "SOAPAction: \"\"\r",
                    "Content-Length: null\r",
                    ...
                    ...
                    ...
                    ...
                    ...
                    ...
                    ...
                ],
                "dd_name": "sysprint",
                "name": "IBMUSER.P6843487.T0954493.C0000000",
                "record_count": 119
            }
        ],
        "failed": false,
        "ret_code": {
            "code": 4
        }
    }

</details>

## License

This role is licensed under licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Author Information

This role was created in 2024 by Luiggi Torricelli.
