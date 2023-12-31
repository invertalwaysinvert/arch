sudo pacman-key --init
sudo pacman -Sy

sudo pacman -S --noconfirm git archiso tmux
&&
git clone https://github.com/invertalwaysinvert/arch
&&
tmux new "sudo mkarchiso -v -w /tmp/archiso-tmp arch && cd out && python3 -m http.server"

archinstall --config https://raw.githubusercontent.com/invertalwaysinvert/arch/main/airootfs/etc/skel/config.json --creds https://raw.githubusercontent.com/invertalwaysinvert/arch/main/airootfs/etc/skel/creds.json --disk_layouts https://raw.githubusercontent.com/invertalwaysinvert/arch/main/airootfs/etc/skel/disks.json --silent

mount -o remount,size=2G /run/archiso/cowspace

sudo mkfs.btrfs /dev/sda1
sudo mount /dev/sda1 /mnt
sudo mkdir /mnt/{upper,work,os}
sudo mount overlay -t overlay -o lowerdir=/run/archiso/airootfs,upperdir=/mnt/upper,workdir=/mnt/work /mnt/os

# Cloud Init

sudo parted /dev/sda resizepart 3 100%
sudo btrfs filesystem resize max /

# TODO:

- [ ] Passwordless sudo
- [ ] Mount drive on boot

### Delete older image

ACCESS_TOKEN=$(curl -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" --data-urlencode "username=$API_USER" --data-urlencode "password=$API_PASSWORD" -d 'grant_type=password' 'https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token' | jq -r '.access_token')
CUSTOM_IMAGE_ID=$(curl -X GET 'https://api.contabo.com/v1/compute/images?standardImage=false' -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213' | jq -r '.data[0].imageId')
curl -X DELETE "https://api.contabo.com/v1/compute/images/$CUSTOM_IMAGE_ID" -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213'

### Upload new image

ACCESS_TOKEN=$(curl -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" --data-urlencode "username=$API_USER" --data-urlencode "password=$API_PASSWORD" -d 'grant_type=password' 'https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token' | jq -r '.access_token')
curl -X POST 'https://api.contabo.com/v1/compute/images' -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213' -d '{"name": "Razor", "description": "Razor rolling", "url": "http://38.242.246.142:8000/razor-2023.06.15-x86_64.iso", "osType": "Linux", "version": "0.0.1"}'

### Reinstall

ACCESS_TOKEN=$(curl -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" --data-urlencode "username=$API_USER" --data-urlencode "password=$API_PASSWORD" -d 'grant_type=password' 'https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token' | jq -r '.access_token')
curl -X PUT 'https://api.contabo.com/v1/compute/instances/201332848' -H "Content-Type: application/json" -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H "x-trace-id: 123213" -d '{"imageId": "69b52ee3-2fda-4f44-b8de-69e480d87c7d", "sshKeys": [73745], "rootPassword": 73742}'

### Reinstall custom

ACCESS_TOKEN=$(curl -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" --data-urlencode "username=$API_USER" --data-urlencode "password=$API_PASSWORD" -d 'grant_type=password' 'https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token' | jq -r '.access_token')
CUSTOM_IMAGE_ID=$(curl -X GET 'https://api.contabo.com/v1/compute/images?standardImage=false' -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213' | jq -r '.data[0].imageId')
curl -X PUT 'https://api.contabo.com/v1/compute/instances/201332848' -H "Content-Type: application/json" -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H "x-trace-id: 123213" --binary-data "{\"imageId\": \"$CUSTOM_IMAGE_ID\", \"userData\": \"$(<cloud-init.yml)\", "sshKeys": [73745]}"
