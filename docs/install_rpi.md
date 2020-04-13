# Installation for raspberry-pi 4
These instructions are untested, and should be verified by someone. Please create a ticket :)


## 1. Setup required environment variables
```
export <ENV> <VALUE>
```
Make it permanent with putting it in bashrc
Refer to the list in the main readme file.

## 2. Install Depedencies
```
sudo apt-get update && sudo apt-get install git python3 python3-pip python3-venv -y
```

### Node.JS
```
curl -sL https://deb.nodesource.com/setup_13.x | sudo bash -
sudo apt-get install -y nodejs
```
### WireGuard: Ubuntu
```
sudo add-apt-repository ppa:wireguard/wireguard -y
sudo apt install wireguard wireguard-tools -y
```

### WireGuard: Debian/RPI
```
# Get signing keys to verify the new packages, otherwise they will not install
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138

# Add the Buster backport repository to apt sources.list
echo 'deb http://httpredir.debian.org/debian buster-backports main contrib non-free' | sudo tee -a /etc/apt/sources.list.d/debian-backports.list

sudo apt update
sudo apt install wireguard wireguard-tools -y
```

## 3. Building front-end
```
# Building frontend
sudo git clone https://github.com/perara/wireguard-manager.git /opt/wireguard-manager
cd /opt/wireguard-manager/wg_dashboard_frontend
sudo npm install > /dev/null && sudo npm install @angular/cli > /dev/null
sudo node_modules/@angular/cli/bin/ng build --configuration="production" > /dev/null
```

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
