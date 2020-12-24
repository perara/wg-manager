# Installation for Linux (Ubuntu, Debian, Raspberry Pi)
These instructions are tested working on:\
:heavy_check_mark: Ubuntu 20.04\
:heavy_check_mark: Ubuntu 18.04\
:x: Ubuntu 16.04 (fails when starting the http server `uvicorn main:app --host=0.0.0.0`)\
:x: Debian 10\
&nbsp;&nbsp;(fails when starting the wg0 interface`[#] ip link add wg0 type wireguard\nRTNETLINK answers: Operation not supported\nUnable to access interface: Protocol not supported\n[#] ip link delete dev wg0\nCannot find device "wg0"\n'`)\
:x: Debian 9
&nbsp;&nbsp;(fails at `pip install -r requirements.txt` error: `Could not find a version that satisfies the requirement fastapi (from -r requirements.txt (line 2)) (from versions: `)

## 1. Setup required environment variables
```
export <ENV>=<VALUE>
```
You will need the following:
```
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=admin
```
Make it permanent with putting it in bashrc
Refer to the list in the main readme file.

## 2. Install Depedencies

### Python
```
sudo apt-get update && sudo apt-get install git python3 python3-pip python3-venv -y
```

### Node.JS: Ubuntu
```
curl -sL https://deb.nodesource.com/setup_13.x | sudo bash -
sudo apt-get install -y nodejs
```

### Node.JS: Debian
```
sudo apt install curl
curl -sL https://deb.nodesource.com/setup_13.x | sudo bash -
sudo apt-get install -y nodejs
```
### WireGuard: Ubuntu
#### 18.04 and later
```
sudo apt update
sudo apt install wireguard wireguard-tools -y
```
#### 16.04 and earlier
```
sudo add-apt-repository ppa:wireguard/wireguard -y
sudo apt install wireguard wireguard-tools -y
```

### WireGuard: Debian 10/Raspberry Pi (with Raspbian 10)
```
# Get signing keys to verify the new packages, otherwise they will not install
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138

# Add the Buster backport repository to apt sources.list
echo 'deb http://httpredir.debian.org/debian buster-backports main contrib non-free' | sudo tee -a /etc/apt/sources.list.d/debian-backports.list

sudo apt update
sudo apt install wireguard wireguard-tools -y
```

### WireGuard: Debian 9/Raspberry Pi (with Raspbian 9)
```
# Get signing keys to verify the new packages, otherwise they will not install
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138

echo "deb http://deb.debian.org/debian/ unstable main" | sudo tee -a /etc/apt/sources.list.d/unstable.list

sudo apt update
sudo apt install wireguard wireguard-tools -y
```

## 3. Building front-end
```
# Building frontend
sudo git clone https://github.com/perara/wg-manager.git /opt/wg-manager
cd /opt/wg-manager/wg_dashboard_frontend
sudo npm install > /dev/null && sudo npm install @angular/cli > /dev/null
sudo node_modules/@angular/cli/bin/ng build --configuration="production"
```
One thing to be aware of is that when issuing the `sudo node_modules/@angular/cli/bin/ng build --configuration="production"` command, if you do not have enough memory on your server, the process will get "Killed". This happens when trying to compile on the lowest tier DIgital Ocean droplet. To get around this you can either add more memory or create a swap file. Here is a great guide on [creating a swap file](https://linuxize.com/post/create-a-linux-swap-file/).

## 4. Setup back-end
```
sudo mv dist ../wg_dashboard_backend/build
cd ../wg_dashboard_backend/
sudo python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install uvicorn
uvicorn main:app --host=0.0.0.0
```

## 5. Complete
You should now see the following
```
#INFO:     Started server process [259296]
#INFO:     Waiting for application startup.
#INFO:     Application startup complete.
#INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit) 
``` 

## 6. Default routing not working?
Try these.

PostUp `iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE; ip6tables -A FORWARD -i %i -j ACCEPT; ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`

PostDown `iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE; ip6tables -D FORWARD -i %i -j ACCEPT; ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE`
