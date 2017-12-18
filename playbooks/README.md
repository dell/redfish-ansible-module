
| category  | command                | playbook                   | output sample | restrictions |
|-----------|------------------------|----------------------------|-------------|--------------|
| Inventory | GetSystemInventory     | get_storage_inventory.yml  | [r740_SystemInventory_YYYYMMDD_hhmmss.json](../sample_output_files/r740_SystemInventory_YYYYMMDD_hhmmss.json) | |
|           | GetPSUInventory        | get_psu_inventory.yml      | yes         |              |
|           | GetCPUInventory        | get_cpu_inventory.yml      | yes         |              |
|           | GetNICInventory        | get_nic_inventory.yml      | yes         |              |
|           | GetFanInventory        | get_fan_inventory.yml      | yes         |              |
| Firmware  | GetInventory           | get_firmware_inventory.yml | yes         |              |
|           | UploadFirmware         | firmware_update.yml        |             | 14G only     |
|           | FirmwareCompare        | firmware_update.yml        |             | 14G only     |
|           | InstallFirmware        | firmware_update.yml        |             | 14G only     |
| Bios      | GetAttributes          | manage_bios.yml            | yes         |              |
|           | GetBootOrder           | manage_bios.yml            | yes         |              |
|           | SetOneTimeBoot         | manage_bios.yml            |             |              |
|           | SetDefaultSettings     | manage_bios.yml            |             |              |
|           | SetAttributes          | manage_bios.yml            |             |              |
|           | ConfigJob              | manage_bios.yml            |             |              |
| Power     | PowerOn                | manage_system_power.yml    |             |              |
|           | PowerOff               | manage_system_power.yml    |             |              |
|           | GracefulRestart        | manage_system_power.yml    |             |              |
|           | GracefulShutdown       | manage_system_power.yml    |             | 14G only     |
| Storage   | GetControllerInventory | get_storage_inventory.yml  | yes         |              |
|           | GetDiskInventory       | get_storage_inventory.yml  | yes         |              |
| Users     | ListUsers              | manage_idrac_users.yml     | yes         |              |
|           | AddUser                | manage_idrac_users.yml     |             |              |
|           | EnableUser             | manage_idrac_users.yml     |             |              |
|           | UpdateUserRole         | manage_idrac_users.yml     |             |              |
|           | UpdateUserPassword     | manage_idrac_users.yml     |             |              |
|           | DisableUser            | manage_idrac_users.yml     |             |              |
|           | DeleteUser             | manage_idrac_users.yml     |             |              |
| SCP       | ExportSCP              | manage_scp.yml             | yes         |              |
|           | ImportSCP              | manage_scp.yml             |             |              |
| Logs      | GetSELogs              | get_system_logs.yml        | yes         |              |
|           | GetLCLogs              | get_system_logs.yml        | yes         |              |
| Idrac     | SetDefaultSettings     | manage_idrac_power.yml     |             |              |
|           | GracefulRestart        | manage_idrac_power.yml     |             |              |
| Network   | (coming soon)          | (coming soon)              |             |              |
