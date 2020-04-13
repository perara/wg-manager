# Importing existing configuration
It is not unusual to have existing WireGuard configurations in production, and for this reason, we support to import these in full or partial form.

It is possible to:
1. Import server configuration only
    * Peer export will not work due to impartial information, such as missing private-key
2. Import peer configuration only,
    * Server configuration will only be partial. e.g private-key must be manually entered
3. Import server **and** peer configuration.
    * Given compliant configuration (see assumptions), everything should be fully imported.

## Configuration assumptions
There are a few assumptions made for the configuration to be successfully imported.
1. Generally, any file that **does not contain** **Endpoint** key in the Peer sections are servers. The import will fail 
if multiple files is without Endpoint
2. All files that **have Endpoint defined** are considered peers of the server
3. All files should be imported at the **same time**

### Server
The format of the server should look similar to this:
```
[Interface]
Address = 10.0.92.1/24
PrivateKey = 0MHXsC4zJrDZA5MpZZKQiS/j5srAvSC9bJx7Igtq1FE=
ListenPort = 56944
PostUp = 
PostDown = 

[Peer]
PublicKey = XNRPEweV3guSis3YRHDBldizn6xivv+2Tug0G/BM6gE=
AllowedIPs = 10.0.92.2/32

[Peer]
PublicKey = XNRPEweV3guSis3YRHDBldizn6xivv+2Tug0G/BM6gE=
AllowedIPs = 10.0.92.3/32
```

### Peer
```
[Interface]
Address = 10.0.92.2/24
PrivateKey = aN08xqUVOEAoc74e2yzvN/yOtXJgtISru7mjrPFhlUY
DNS="8.8.8.8"

[Peer]
PublicKey = gybMBZBfwsmsXBl8bG2ZobGiG77aGdxOoyQsjTzrKkY=
AllowedIPs = 0.0.0.0/0
Endpoint = my-address.com:5455

<! THIS IS INVALID !> <! THIS WONT WORK !>
[Peer]
PublicKey = gybMBZBfwsmsXBl8bG2ZobGiG77aGdxOoyQsjTzrKkY=
AllowedIPs = 0.0.0.0/0
Endpoint = my-address.com:5455
```
Note that we do **not** support importing peers with multiple peer sections.

## How to
1. Click the **Import Configuration** button in the right pane
2. Select all relevant server and client files and submit.
3. If successfully, the server configuration should now be filled and a indicator on how many peers added is shown at the bottom of the form.
