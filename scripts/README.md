# Examples

Scripts to perform some of the same tasks this Ansible module performs.

# Using curl

Sending a Redfish request to iDRAC can be done easily with curl:

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

Get power usage during last hour:

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
$ get-system-inventory.py 192.168.0.53
Model:       PowerEdge R630
Mfg:         Dell Inc.
BIOS:        2.4.2
Service tag: XXXYYXX
Serial No.:  CNYYY6XXX90XXX
Hostname:    myserver.dell.com
Power state: On
Asset tag:   123456
Memory:      128.0
CPUs:        2
CPU type:    Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz
Status:      OK

$ get-system-power.py 192.168.0.53
Power Monitoring - Historical Trends - Last Hour
Average Usage:  157 W
Max Peak:       176 W
Min Peak:       156 W

$ get-system-se-logs.py 192.168.0.53
 Log Entry 5: 2017-02-13T22:55:11-06:00
 Drive 4 is installed in disk drive bay 1.

 Log Entry 4: 2017-02-13T22:55:01-06:00
 Drive 4 in disk drive bay 1 is operating normally.

 Log Entry 3: 2017-02-13T22:55:01-06:00
 Drive 4 is removed from disk drive bay 1.

 Log Entry 2: 2017-02-11T23:01:55-06:00
 Fault detected on drive 4 in disk drive bay 1.

 Log Entry 1: 2015-10-09T12:40:30-05:00
 Log cleared.

```


