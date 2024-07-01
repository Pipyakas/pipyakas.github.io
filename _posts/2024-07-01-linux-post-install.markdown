---
layout: post
title:  "Linux post-install"
date:   2024-07-01 16:00:00 +0700
categories: linux
---
Some useful commands for post-installation of Linux:

### Dual-boot time fix ###
```bash
timedatectl set-local-rtc 1 --adjust-system-clock
```

### Fedora GRUB ###
```bash
sudo grub2-mkconfig -o /etc/grub2.cfg
```

### zram ###
```bash
echo "zram" | sudo tee -a /etc/modules-load.d/zram.conf
echo "options zram num_devices=1" | sudo tee -a /etc/modprobe.d/zram.conf
echo 'KERNEL=="zram0", ATTR{disksize}="16G",TAG+="systemd"' | sudo tee -a /etc/udev/rules.d/99-zram.rules

sudo nano /etc/systemd/zram-generator.conf
[zram0]
zram-size = ram / 2
compression-algorithm = lz4

sudo nano /etc/sysctl.d/99-zram-tune.conf
vm.page-cluster = 0

sudo gedit /etc/systemd/system/zram.service && sudo systemctl enable --now zram.service
[Unit]
Description=Swap with zram
After=multi-user.target

[Service]
Type=oneshot 
RemainAfterExit=true
ExecStartPre=/sbin/mkswap /dev/zram0
ExecStart=/sbin/swapon /dev/zram0
ExecStop=/sbin/swapoff /dev/zram0

[Install]
WantedBy=multi-user.target
```

### amdgpu ###
```bash
sudo add-apt-repository -y ppa:oibaf/graphics-drivers
sudo apt dist-upgrade -y
sudo apt install -y mesa-vulkan-drivers mesa-vulkan-drivers:i386
echo "blacklist radeon" | sudo tee --append /etc/modprobe.d/blacklist.conf
echo "options amdgpu si_support=1 cik_support=1" | sudo tee --append /etc/modprobe.d/amdgpu.conf
sudo update-initramfs -u
```

### gdm ###
```bash
sudo cp ~/.config/monitors.xml  /var/lib/gdm3/.config/
```

### wayland ###
Edit the following file:
```bash
sudo gedit /etc/gdm3/custom.conf
```
Add the line:
```
WaylandEnable=true
```

### ntfs3 ###
```bash
uid=1000,gid=1000,rw,user,exec,umask=000,discard,noatime,x-gvfs-show
ln -s ~/.steam/steam/steamapps/compatdata /mnt/d/SteamLibrary/steamapps/
ln -s ~/.steam/steam/steamapps/compatdata /mnt/e/SteamLibrary/steamapps/
ln -s ~/.steam/steam/steamapps/shadercache /mnt/d/SteamLibrary/steamapps/
ln -s ~/.steam/steam/steamapps/shadercache /mnt/e/SteamLibrary/steamapps/
```

### Kernel arg ###
For AMD:
```bash
loglevel=0 systemd.show_status=true noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off mitigations=off amdgpu.ppfeaturemask=0xffffffff radeon.si_support=0 radeon.cik_support=0 amdgpu.si_support=1 amdgpu.cik_support=1
```
For Broadwell:
```bash
loglevel=0 systemd.show_status=true noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off mitigations=off i915.disable_power_well=0 i915.enable_fbc=1 i915.enable_dpcd_backlight=1 i915.enable_dc=2 i915.enable_guc=3
```
For Haswell:
```bash
loglevel=0 systemd.show_status=true noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off mitigations=off i915.disable_power_well=0 i915.enable_fbc=1 i915.enable_dpcd_backlight=1 i915.enable_dc=1 i915.enable_guc=-1
```

### Google Chrome/Chromium flags ###
Edit the following file:
```bash
nano ~/.config/chromium-flags.conf
```
Add the following flags:
```
--profile-directory=Default --start-maximized --force-dark-mode --enable-dom-distiller --enable-quic --enable-smooth-scrolling --ignore-gpu-blocklist --disable-gpu-driver-bug-workarounds --gpu-rasterization-msaa-sample-count=0  --enable-gpu-rasterization --enable-oop

Source: Conversation with Copilot, 7/1/2024
(1) Highlight Bash/shell code in Markdown Readme.md files. https://www.thecodebuzz.com/highlight-bash-shell-code-in-markdown-readme-md-wiki-files/.
(2) Bash script to convert a web page URL to Markdown using Pandoc.. https://gist.github.com/jonlabelle/c7d641973673698da29e3132130d6355.
(3) A Markdown interpreter using only traditional Unix tools. https://github.com/chadbraunduin/markdown.bash/.
(4) text processing - Write shell output to MS Word document - Unix & Linux .... https://unix.stackexchange.com/questions/379999/write-shell-output-to-ms-word-document.
(5) How to highlight bash/shell commands in markdown?. https://stackoverflow.com/questions/20303826/how-to-highlight-bash-shell-commands-in-markdown.
(6) github.com. https://github.com/profjulianoramos/profjulianoramos.github.io/tree/53322d8792d7f92a478d6da14474399bea235648/blog%2F_posts%2F2020-6-12-ativarzram.md.
```

### XanMod Kernel
```bash
echo 'deb http://deb.xanmod.org releases main' | sudo tee /etc/apt/sources.list.d/xanmod-kernel.list && wget -qO - https://dl.xanmod.org/gpg.key | sudo apt-key add -
sudo apt update && sudo apt install -y linux-xanmod
```

### PowerTop
Create a service file:
```bash
sudo nano /etc/systemd/system/powertop.service
```
Add the following content:
```ini
[Unit]
Description=Powertop tunings

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/sbin/powertop --auto-tune

[Install]
WantedBy=multi-user.target
```

### Docker (Ubuntu)
```bash
sudo apt-get remove -y docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

### Mouse Scrollwheel Speed
Create an imwheel configuration file:
```bash
touch imwheel.sh && gedit imwheel.sh
```
Add the following content:
```bash
#!/bin/bash
# Version 0.1 Tuesday, 07 May 2013
# Comments and complaints http://www.nicknorton.net
# GUI for mouse wheel speed using imwheel in Gnome
# imwheel needs to be installed for this script to work
# sudo apt-get install imwheel
# Pretty much hard wired to only use a mouse with
# left, right and wheel in the middle.
# If you have a mouse with complications or special needs,
# use the command xev to find what your wheel does.
#
### see if imwheel config exists, if not create it ###
if [ ! -f ~/.imwheelrc ]
then

cat >~/.imwheelrc<<EOF
".*"
None,      Up,   Button4, 5
None,      Down, Button5, 5
Control_L, Up,   Control_L|Button4
Control_L, Down, Control_L|Button5
Shift_L,   Up,   Shift_L|Button4
Shift_L,   Down, Shift_L|Button5
EOF

fi
####################################

CURRENT_VALUE=$(awk -F 'Button4,' '{print $2}' ~/.imwheelrc)

NEW_VALUE=$(zenity --scale --window-icon=info --ok-label=Apply --title="Wheelies" --text "Mouse wheel speed:" --min-value=1 --max-value=100 --value="$CURRENT_VALUE" --step 1)

if [ "$NEW_VALUE" == "" ];
then exit 0
fi

sed -i "s/\($TARGET_KEY *Button4, *\).*/\1$NEW_VALUE/" ~/.imwheelrc # find the string Button4, and write new value.
sed -i "s/\($TARGET_KEY *Button5, *\).*/\1$NEW_VALUE/" ~/.imwheelrc # find the string Button5, and write new value.

cat ~/.imwheelrc
imwheel -kill
```
Run the script and adjust the mouse wheel speed using Zenity.
To run imwhell onstart-up, create a service file:
```bash
touch ~/.config/autostart/imwheel.desktop && gedit ~/.config/autostart/imwheel.desktop
```
```desktop
[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=imwheel
Comment=imwheel
Exec=/usr/bin/imwheel
Terminal=false
```

### Docker (Fedora)
```bash
sudo dnf install -y moby-engine docker-compose
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### ibus-bamboo
```bash
sudo add-apt-repository -y ppa:bamboo-engine/ibus-bamboo
sudo apt-get update
sudo apt-get install -y ibus-bamboo
ibus restart
env DCONF_PROFILE=ibus dconf write /desktop/ibus/general/preload-engines "['xkb:us::eng', 'Bamboo']"
gsettings set org.gnome.desktop.input-sources sources "[('xkb', 'us'), ('ibus', 'Bamboo')]"
```

### Download VS Code Server
```bash
#!/bin/sh
set -e

# You can get the latest commit SHA by looking at the latest tagged commit here: https://github.com/microsoft/vscode/releases
commit_sha="08a217c4d27a02a5bcde898fd7981bda5b49391b"
archive="vscode-server-linux-x64.tar.gz"
owner='microsoft'
repo='vscode'

# Auto-Get the latest commit sha via command line.
get_latest_release() {
    tag=$(curl --silent "https://api.github.com/repos/${1}/releases/latest" | # Get latest release from GitHub API
          grep '"tag_name":'                                              | # Get tag line
          sed -E 's/.*"([^"]+)".*/\1/'                                    ) # Pluck JSON value

    tag_data=$(curl --silent "https://api.github.com/repos/${1}/git/ref/tags/${tag}")

    sha=$(echo "${tag_data}"           | # Get latest release from GitHub API
          grep '"sha":'                | # Get tag line
          sed -E 's/.*"([^"]+)".*/\1/' ) # Pluck JSON value

    sha_type=$(echo "${tag_data}"           | # Get latest release from GitHub API
          grep '"type":'                    | # Get tag line
          sed -E 's/.*"([^"]+)".*/\1/'      ) # Pluck JSON value

    if [[ "${sha_type}" != "commit" ]]; then
        combo_sha=$(curl -s "https://api.github.com/repos/${1}/git/tags/${sha}" | # Get latest release from GitHub API
              grep '"sha":'                                                     | # Get tag line
              sed -E 's/.*"([^"]+)".*/\1/'                                      ) # Pluck JSON value

        # Remove the tag sha, leaving only the commit sha;
        # this won't work if there are ever more than 2 sha,
        # and use xargs to remove whitespace/newline.
        sha=$(echo "${combo_sha}" | sed -E "s/${sha}//" | xargs)
    fi

    printf "${sha}"
}

commit_sha=$(get_latest_release "${owner}/${repo}")

echo "will attempt to download VS Code Server version = '${commit_sha}'"

# Download VS Code Server tarball to tmp directory.
curl -L "https://update.code.visualstudio.com/commit:${commit_sha}/server-linux-x64/stable" -o "/tmp/${archive}"

# Make the parent directory where the server should live.
# NOTE: Ensure VS Code will have read/write access; namely the user running VScode or container user.
mkdir -vp ~/.vscode-server/bin/"${commit_sha}"

# Extract the tarball to the right location.
tar --no-same-owner -xzv --strip-components=1 -C ~/.vscode-server/bin/"${commit_sha}" -f "/tmp/${archive}"
```

### XAMPP service ###
Create a systemd service file:
```ini
sudo nano /etc/systemd/system/xampp.service
```
Add the following content:
```ini
[Unit]
Description=XAMPP

[Service]
ExecStart=/opt/lampp/lampp start
ExecStop=/opt/lampp/lampp stop
Type=forking

[Install]
WantedBy=multi-user.target
```

### RPMFusion ###
Install RPMFusion repositories for Fedora:
```bash
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

### General environment variables ###
Set environment variables:
```bash
export RADV_PERFTEST=aco
export PROTON_FORCE_LARGE_ADDRESS_AWARE=1
export __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1
```

### Nvidia coolbits ###
Configure Nvidia coolbits:
```bash
sudo nvidia-settings -a '[gpu:0]/GPUPowerMizerMode=1' -a '[gpu:0]/GPUMemoryTransferRateOffset[2]=500'
sudo nvidia-settings -a '[gpu:0]/GPUPowerMizerMode=1' -a '[gpu:0]/GPUGraphicsClockOffset[1]=100' -a '[gpu:0]/GPUMemoryTransferRateOffset[1]=1000'

Create an Xorg configuration file:
```ini
sudo nano /etc/X11/xorg.conf.d/84-coolbits.conf
```
Add the following content:
```ini
Section "OutputClass"
    Identifier "nvidia"
    MatchDriver "nvidia-drm"
    Driver "nvidia"
    ModulePath "/usr/lib/nvidia/xorg"
    ModulePath "/usr/lib/xorg/modules"
    Option "Coolbits" "31"
EndSection
```

### Force Intel i915 driver ###
Create an Xorg configuration file:
```ini
sudo gedit /etc/X11/xorg.conf.d/99-intel.conf
```
Add the following content:
```ini
Section "OutputClass"
    Identifier "intel"
    MatchDriver "i915"
    Driver "intel"
    Option "AccelMethod" "sna"
    Option "TearFree" "true"
    Option "DRI" "3"
EndSection
```

## Create Swapfile Script

This script allows you to create a swapfile on your Linux system. You can customize the size of the swapfile based on your needs.

### Usage

1. Save the script to a file (e.g., `create_swapfile.sh`).
2. Make the script executable: `chmod +x create_swapfile.sh`.
3. Run the script: `./create_swapfile.sh`.

### Script

```bash
#!/bin/bash

# Prompt the user for the desired swapfile size (e.g., 2G, 4G, 8G)
read -p "Enter the swapfile size (e.g., 2G, 4G, 8G): " swap_size

# Create the swapfile
sudo fallocate -l "$swap_size" /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Add an entry to /etc/fstab to mount the swapfile at boot
echo "/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab

# Adjust swappiness (optional)
sudo sysctl vm.swappiness=10
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf

# Display information about the new swapfile
sudo swapon --show

echo "Swapfile created successfully!"
```

Certainly! Here's your provided information converted into a Markdown document:

---

## Mono Audio Setup

### List Available Sources

To list available audio sources and filter for output devices, use the following command:

```bash
pacmd list-sources | grep 'name:.*output'
```

### Remap Stereo to Mono

Edit the PulseAudio configuration file:

```bash
sudo gedit /etc/pulse/default.pa
```

Add the following lines to remap stereo output to mono:

```bash
load-module module-remap-sink master=alsa_output.pci-0000_00_1b.0.analog-stereo sink_name=mono_internal sink_properties="device.description='Mono Internal'" channels=2 channel_map=mono,mono
load-module module-remap-sink master=alsa_output.pci-0000_00_03.0.hdmi-stereo sink_name=mono_external sink_properties="device.description='Mono External'" channels=2 channel_map=mono,mono
# Optional: Select new remap as default
set-default-sink mono_external
```

Restart PulseAudio:

```bash
pulseaudio -k && pulseaudio --start
```

### Purge Ubuntu Snapd

Remove Snapd from Ubuntu:

```bash
sudo apt purge -y snapd
rm -vrf ~/snap
sudo rm -vrf /snap /var/snap /var/lib/snapd /var/cache/snapd /usr/lib/snapd
sudo apt-mark hold snapd
```

### Install Chromium with VAAPI Support on Fedora

Install required packages:

```bash
sudo dnf install -y libva libva-intel-driver libva-intel-hybrid-driver libva-utils libva-vdpau-driver chromium-vaapi
```

### Fix Steam Minimize Issue on Manjaro

Edit the Steam script:

```bash
sudo sed -i '8s/-0/-1/' /usr/bin/steam
```

### PRIME Render Offload Argument

Add the following argument to launch Steam games using PRIME render offload:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia %command%
```

### Optimus Manager Configuration (Arch/Manjaro)

Edit the optimus-manager configuration:

```bash
sudo gedit /etc/optimus-manager/optimus-manager.conf
```

Configure as needed:

```ini
[optimus]
switching=none
pci_power_control=yes
pci_remove=no
pci_reset=no
auto_logout=yes

[intel]
driver=intel
accel=sna
tearfree=yes
DRI=3
modeset=yes

[nvidia]
modeset=yes
PAT=yes
DPI=96
ignore_abi=yes
options=overclocking, triple_buffer
```

### Disable DualShock 4 Touchpad Input

Create a udev rule to disable the DualShock 4 touchpad:

```bash
sudo nano /etc/udev/rules.d/95-disable-ds4-tp.rules
SUBSYSTEM=="input", SUBSYSTEMS=="input", ATTRS{name}=="Wireless Controller Touchpad", ENV{LIBINPUT_IGNORE_DEVICE}="1"
```

### Build Sunshine on Fedora

Install required development tools and dependencies:

```bash
sudo dnf group install -y "Development Tools"
sudo dnf install -y openssl-devel ffmpeg-devel boost-devel boost-static.x86_64 pulseaudio-libs-devel opus-devel libXtst-devel libX11-devel libXfixes-devel libevdev-devel libxcb-devel cmake g++
git clone https://github.com/loki-47-6F-64/sunshine.git --recurse-submodules
cd sunshine && mkdir build && cd build
cmake -DCMAKE_C_COMPILER=gcc-10 -DCMAKE_CXX_COMPILER=g++-10 ..
make -j ${nproc}
```

### EnvyControl Integrated Configuration

Edit the blacklist-nvidia.conf file:

```bash
sudo nano /etc/modprobe.d/blacklist-nvidia.conf
```

Add the following lines (automatically generated by EnvyControl):

```bash
blacklist nouveau
blacklist nvidia
blacklist nvidia_drm
blacklist nvidia_uvm
blacklist nvidia_modeset
alias nouveau off
alias nvidia off
alias nvidia_drm off
alias nvidia_uvm off
alias nvidia_modeset off
```

Edit the `50-remove-nvidia.rules` file:

```bash
sudo nano /lib/udev/rules.d/50-remove-nvidia.rules
```

Add the following lines (automatically generated by EnvyControl):
```bash
# Automatically generated by EnvyControl
# Remove NVIDIA USB xHCI Host Controller devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c0330", ATTR{power/control}="auto", ATTR{remove}="1"
# Remove NVIDIA USB Type-C UCSI devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c8000", ATTR{power/control}="auto", ATTR{remove}="1"
# Remove NVIDIA Audio devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", ATTR{power/control}="auto", ATTR{remove}="1"
# Remove NVIDIA VGA/3D controller devices
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x03[0-9]*", ATTR{power/control}="auto", ATTR{remove}="1"
```

### APT proxy ###
```bash
sudo nano /etc/apt/apt.conf.d/proxy.conf
```
```ini
Acquire {
  HTTP::proxy "http://<address>:<port>";
  HTTPS::proxy "http://<address>:<port>";
}
```
```bash
sudo nano /etc/profile
```
```ini
export http_proxy=http://<address>:<port>
export https_proxy=$http_proxy
```