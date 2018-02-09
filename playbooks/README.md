
## Organization

| category  | command                | playbook                   | sample output file |
|-----------|------------------------|----------------------------|--------------------|
| Inventory | GetSystemInventory     | get_system_inventory.yml   | [r740_SystemInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_SystemInventory_YYYYMMDD_hhmmss.json) |
|           | GetPsuInventory        | get_psu_inventory.yml      | [r740_PsuInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_PsuInventory_YYYYMMDD_hhmmss.json) |
|           | GetCpuInventory        | get_cpu_inventory.yml      | [r740_CpuInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_CpuInventory_YYYYMMDD_hhmmss.json) |
|           | GetNicInventory        | get_nic_inventory.yml      | [r740_NicInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_NicInventory_YYYYMMDD_hhmmss.json) |
|           | GetFanInventory        | get_fan_inventory.yml      | [r740_FanInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_FanInventory_YYYYMMDD_hhmmss.json) |
|           | GetStorageControllerInventory | get_stor_cont_inventory.yml | [r740_StorageControllerInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_StorageControllerInventory_YYYYMMDD_hhmmss.json) |
|           | GetDiskInventory       | get_disk_inventory.yml     | [r740_DiskInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_DiskInventory_YYYYMMDD_hhmmss.json) |
| Update    | GetFirmwareInventory   | get_firmware_inventory.yml | [r740_FirmwareInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_FirmwareInventory_YYYYMMDD_hhmmss.json) |
| System    | GetBiosAttributes      | get_bios_attributes.yml    | [r740_BiosAttributes_YYYYMMDD_hhmmss.json](../sample_output_files/r740_BiosAttributes_YYYYMMDD_hhmmss.json) |
|           | GetBiosBootOrder       | get_bios_boot_order.yml    | [r740_BiosBootOrder_YYYYMMDD_hhmmss.json](../sample_output_files/r740_BiosBootOrder_YYYYMMDD_hhmmss.json) |
|           | SetOneTimeBoot         | set_onetime_boot.yml       |                    |
|           | SetBiosDefaultSettings | set_default_bios_settings.yml |                 |
|           | SetBiosAttributes      | get_bios_attributes.yml    |                    |
|           | PowerOn                | power_on.yml               |                    |
|           | PowerForceOff          | power_force_off.yml        |                    |
|           | PowerGracefulRestart   | power_graceful_restart.ym  |                    |
|           | PowerGracefulShutdown  | power_graceful_shutdown.yml |                   |
| UserManagement | ListUsers         | list_users.yml             | [r740_Users_YYYYMMDD_hhmmss.json](../sample_output_files/r740_Users_YYYYMMDD_hhmmss.json) |
|           | AddUser                | add_user.yml               |                    |
|           | EnableUser             | enable_user.yml            |                    |
|           | UpdateUserRole         | update_user_role.yml       |                    |
|           | UpdateUserPassword     | update_user_password.yml   |                    |
|           | DisableUser            | manage_idrac_users.yml     |                    |
|           | DeleteUser             | manage_idrac_users.yml     |                    |
| Manager   | ViewLogs               | view_logs.yml              | [r740_Logs_YYYYMMDD_hhmmss.json](../sample_output_files/r740_Logs_YYYYMMDD_hhmmss.json) |
|           | ClearLogs              | clear_logs.yml             |                    |
|           | GetAttributes          | manage_idrac_settings.yml  | [r740_ManagerAttributes_YYYMMDD_hhmmss.json](../sample_output_files/r740_ManagerAttributes_YYYMMDD_hhmmss.json) |
|           | SetAttributes          | manage_idrac_settings.yml  |                    |
|           | SetDefaultSettings     | manage_idrac_settings.yml  |                    |
|           | GracefulRestart        | restart_idrac.yml          |                    |
|           | ExportSCP              | export_scp.yml             | [r740_SCP_YYYYMMDD_hhmmss.xml](../sample_output_files/r740_SCP_YYYYMMDD_hhmmss.xml) |
|           | ImportSCP              | import_scp.yml             |                    |
