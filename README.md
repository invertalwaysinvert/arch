sudo pacman -S git archiso tmux

git clone https://github.com/invertalwaysinvert/arch

sudo mkarchiso -v -w /tmp/archiso-tmp arch

python3 -m http.server

http://38.242.246.142:8000/razor-2023.06.14-x86_64.iso

# TODO:

- [ ] Passwordless sudo
- [ ] Mount drive on boot
