sudo pacman -S git archiso tmux

git clone https://github.com/invertalwaysinvert/arch

tmux new "sudo mkarchiso -v -w /tmp/archiso-tmp arch"

python3 -m http.server

http://38.242.246.142:8000/razor-2023.06.14-x86_64.iso

# TODO:

- [ ] Passwordless sudo
- [ ] Mount drive on boot

### Delete older image

ACCESS_TOKEN=$(curl -d "client_id=$CLIENT_ID" -d "client_secret=$CLIENT_SECRET" --data-urlencode "username=$API_USER" --data-urlencode "password=$API_PASSWORD" -d 'grant_type=password' 'https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token' | jq -r '.access_token')
CUSTOM_IMAGE_ID=$(curl -X GET 'https://api.contabo.com/v1/compute/images?standardImage=false' -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213' | jq -r '.data[0].imageId')
curl -X DELETE "https://api.contabo.com/v1/compute/images/$CUSTOM_IMAGE_ID" -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213'

### Upload new image

curl -X POST 'https://api.contabo.com/v1/compute/images' -H 'Content-Type: application/json' -H "Authorization: Bearer ${ACCESS_TOKEN}" -H "x-request-id: $(uuidgen)" -H 'x-trace-id: 123213' -d '{"name": "Razor", "description": "Razor rolling", "url": "http://38.242.246.142:8000/razor-2023.06.14-x86_64.iso", "osType": "Linux", "version": "0.0.1"}'
