# Examples

Scripts to perform some of the same tasks this Ansible module performs. For reference only (but you can try them if you want).

# Using curl

Sending a Redfish request to iDRAC can be done easily with a web browser or using curl:

Get system health:

```
$ curl –s https://<idrac-ip>/redfish/v1/Systems/System.Embedded.1 -k -u root:password | python -m json.tool | jq .Status
{
  "Health": "OK",
  "HealthRollUp": "OK",
  "State": "Enabled"
}
```

Get storage controller health:
 
```
$ curl –s https://<idrac-ip>/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/RAID.Slot.8-1 -k -u root:password | python -m json.tool | jq .Name
"PERC H730 Adapter"
$ curl –s https://<idrac-ip>/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/RAID.Slot.8-1 -k -u root:password | python -m json.tool | jq .Status
{
  "Health": "OK",
  "HealthRollUp": "OK"
}
```

Get power consumption during last hour:

```$ curl –s https://<idrac-ip>/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl -k -u root:password | python -m json.tool | jq .PowerMetrics
{
  "AverageConsumedWatts": 152,
  "IntervalInMin": 60,
  "MaxConsumedWatts": 168,
  "MinConsumedWatts": 148
}
```

# Using provided scripts

```
$ view-system-power.py 192.168.0.53
ip=192.168.0.53, id=root, pw=calvin
uri=https://192.168.0.53/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl
Power Monitoring - Historical Trends - Last Hour
Average Usage:  157 W
Max Peak:       176 W
Min Peak:       156 W
```


