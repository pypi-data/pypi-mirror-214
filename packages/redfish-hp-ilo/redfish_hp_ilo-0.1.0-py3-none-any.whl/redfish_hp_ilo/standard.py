class Standard:
    def software_firmware_inventory(self, select="firmware"):
        result = []
        update_service_uri = self.REDFISH_OBJ.root["UpdateService"]["@odata.id"]
        update_service_resp = self.REDFISH_OBJ.get(update_service_uri)
        if "software" in select.lower():
            inventory_uri = update_service_resp.obj["SoftwareInventory"]["@odata.id"]
        elif "firmware" in select.lower():
            inventory_uri = update_service_resp.obj["FirmwareInventory"]["@odata.id"]
        else:
            return self.response.result(response, "Invalid selection provided")
        members = self.REDFISH_OBJ.get(inventory_uri).obj["Members"]
        if not members:
            return self.response.result(response, "Inventory emptyd")
        else:
            for inventory_item in members:
                response = self.REDFISH_OBJ.get(inventory_item["@odata.id"])
                result.append(
                    {
                        "name": response.dict.get("Name"),
                        "description": response.dict.get("Description"),
                    }
                )
            return self.response.result(response, result)

    def force_restart(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        system_reboot_uri = systems_response.obj["Actions"]["#ComputerSystem.Reset"][
            "target"
        ]
        body = dict()
        body["Action"] = "ComputerSystem.Reset"
        body["ResetType"] = "ForceRestart"
        response = self.REDFISH_OBJ.post(path=system_reboot_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def power_cycle(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        system_reboot_uri = systems_response.obj["Actions"]["#ComputerSystem.Reset"][
            "target"
        ]
        body = dict()
        body["Action"] = "ComputerSystem.Reset"
        body["ResetType"] = "PowerCycle"
        response = self.REDFISH_OBJ.post(path=system_reboot_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def reset_server(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        system_reboot_uri = systems_response.obj["Actions"]["#ComputerSystem.Reset"][
            "target"
        ]
        body = dict()
        body["Action"] = "ComputerSystem.Reset"
        body["ResetType"] = "GracefulRestart"
        response = self.REDFISH_OBJ.post(path=system_reboot_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def power_down(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        system_reboot_uri = systems_response.obj["Actions"]["#ComputerSystem.Reset"][
            "target"
        ]
        body = dict()
        body["Action"] = "ComputerSystem.Reset"
        body["ResetType"] = "ForceOff"
        response = self.REDFISH_OBJ.post(path=system_reboot_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def power_up(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        system_reboot_uri = systems_response.obj["Actions"]["#ComputerSystem.Reset"][
            "target"
        ]
        body = dict()
        body["Action"] = "ComputerSystem.Reset"
        body["ResetType"] = "ForceOn"
        response = self.REDFISH_OBJ.post(path=system_reboot_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def get_bios_setting(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_members_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_members_response = self.REDFISH_OBJ.get(systems_members_uri)
        bios_uri = systems_members_response.obj["Bios"]["@odata.id"]
        bios_data = self.REDFISH_OBJ.get(bios_uri)
        return self.response.result(systems_members_response, bios_data.dict)

    def find_mac_address(self):
        ethernet_data = {}
        managers_uri = self.REDFISH_OBJ.root["Managers"]["@odata.id"]
        managers_response = self.REDFISH_OBJ.get(managers_uri)
        managers_members_uri = next(iter(managers_response.obj["Members"]))["@odata.id"]
        managers_members_response = self.REDFISH_OBJ.get(managers_members_uri)
        manager_ethernet_interfaces = managers_members_response.obj[
            "EthernetInterfaces"
        ]["@odata.id"]
        manager_ethernet_interfaces_response = self.REDFISH_OBJ.get(
            manager_ethernet_interfaces
        )
        manager_ethernet_interfaces_members = manager_ethernet_interfaces_response.obj[
            "Members"
        ]
        for member in manager_ethernet_interfaces_members:
            ethernet_data[_member["@member.id"]] = self.REDFISH_OBJ.get(
                _member["@odata.id"]
            ).obj

        for iface in ethernet_data:
            return self.response.result(
                manager_ethernet_interfaces_response,
                ethernet_data[iface].get("MACAddress"),
            )
        return None

    def computer_details(self):
        systems_response = self.REDFISH_OBJ.get(
            self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        )
        systems_members_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_members_response = self.REDFISH_OBJ.get(systems_members_uri)
        return self.response.result(
            systems_members_response, systems_members_response.dict
        )

    def change_temporary_boot_order(self, boottarget, enable="Once", mode="UEFI"):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_members_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_members_response = self.REDFISH_OBJ.get(systems_members_uri)
        body = {
            "Boot": {
                "BootSourceOverrideTarget": boottarget,
                "BootSourceOverrideEnabled": enable,
                "BootSourceOverrideMode": mode,
            }
        }
        response = self.REDFISH_OBJ.patch(path=systems_members_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def bios_revert_default(self):
        systems_uri = self.REDFISH_OBJ.root["Systems"]["@odata.id"]
        systems_response = self.REDFISH_OBJ.get(systems_uri)
        systems_members_uri = next(iter(systems_response.obj["Members"]))["@odata.id"]
        systems_members_response = self.REDFISH_OBJ.get(systems_members_uri)
        bios_uri = systems_members_response.obj["Bios"]["@odata.id"]
        bios_response = self.REDFISH_OBJ.get(bios_uri)
        bios_reset_action_uri = bios_response.obj["Actions"]["#Bios.ResetBios"][
            "target"
        ]
        body = {"Action": "Bios.ResetBios", "ResetType": "default"}
        response = self.REDFISH_OBJ.post(path=bios_reset_action_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)

    def reset_ilo(self):
        managers_uri = self.REDFISH_OBJ.root.obj["Managers"]["@odata.id"]
        managers_response = self.REDFISH_OBJ.get(managers_uri)
        managers_members_uri = next(iter(managers_response.obj["Members"]))["@odata.id"]
        managers_members_response = self.REDFISH_OBJ.get(managers_members_uri)
        reset_ilo_uri = managers_members_response.obj["Actions"]["#Manager.Reset"][
            "target"
        ]
        body = {"Action": "Manager.Reset"}
        response = self.REDFISH_OBJ.post(reset_ilo_uri, body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)


    def set_boot_mode(self, mode="Uefi"): # LegacyBios
        bios_uri = "/redfish/v1/systems/1/bios/settings"
        body = {
            "Attributes": {
                "BootMode": mode
            }
        }
        response = self.REDFISH_OBJ.patch(path=bios_uri, body=body)
        if response.status == 400:
            try:
                return self.response.result(
                    response, response.obj["error"]["@Message.ExtendedInfo"]
                )
            except Exception as e:
                return self.response.result(response, str(e))
        elif response.status < 200 or response.status > 300:
            return self.response.result(
                response,
                "An http response of '{}' was returned.".format(response.status),
            )
        else:
            return self.response.result(response, response.dict)
