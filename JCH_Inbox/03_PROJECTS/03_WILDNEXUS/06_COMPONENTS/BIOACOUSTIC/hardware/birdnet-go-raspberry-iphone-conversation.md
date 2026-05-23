# BirdNET-Go + Raspberry Pi 5 + iPhone — Conversation Summary

Date: 2026-05-14

## Objective

Create a bioacoustic wildlife monitoring platform based on:

- Raspberry Pi 5
- BirdNET-Go
- Outdoor microphones
- Future iPhone application
- GPS / species recognition / mapping
- Potential future AI extensions

---

# Recommended Hardware Architecture

## Main SBC

Recommended:

- Raspberry Pi 5
- 8 GB RAM version

Reason:
- Excellent compromise
- Enough for BirdNET-Go
- Good Docker support
- Large community
- Stable Linux ecosystem

16 GB version considered unnecessary for V1.

---

# Starter Kit Selected

User currently owns:

- iRasptek Raspberry Pi 5 Starter Kit
- 8 GB RAM
- 64 GB Bookworm microSD
- Active cooling
- Official PSU

Assessment:
- Good choice for V1
- Replace SD card later with higher-end Samsung PRO Plus or SanDisk Extreme

---

# Microphone Discussion

## Initial USB Mini Microphone

User owns:
- Mini USB microphone

Conclusion:
- Good for initial testing
- Plug-and-play
- Limited naturalist performance

---

## Better Existing Microphone

User discovered:

- BOYA BY-MM1 shotgun microphone

Assessment:
- Much better than mini USB mic
- Directional
- Better bird detection potential
- Suitable for V1 outdoor tests

Architecture:

BOYA BY-MM1
→ UGREEN USB Audio Adapter
→ Raspberry Pi 5
→ BirdNET-Go

---

# Recommended USB Audio Adapter

Recommended model:

- UGREEN USB Sound Card with separate microphone input

Reasons:
- Excellent Linux compatibility
- Stable ALSA behavior
- Better microphone handling
- Ideal for Raspberry Pi + BirdNET-Go

Avoid:
- Smartphone-only TRRS adapters
- Bluetooth audio
- USB-C mobile dongles

---

# Future Professional Microphone Upgrade

Recommended later:

- EM272 / Clippy EM272Z1

Reasons:
- Very popular in BirdNET community
- Excellent sensitivity
- Low noise
- Better long-distance bird detection

Not required initially.

---

# Outdoor Casing Recommendations

## Community Best Practice

Do NOT place:
- Raspberry Pi
- Fan
- Microphone

inside the same tiny enclosure.

Recommended approach:

- IP67 electrical enclosure
- Microphone separated from Raspberry Pi
- Silica gel against condensation
- Cable glands
- Light ventilation

Recommended structure:

[Microphone]
    ↓
[cable]
    ↓
[IP67 enclosure]
    ├── Raspberry Pi 5
    ├── UGREEN audio
    ├── cooling
    └── power

---

# BirdNET-Go Installation Process

## Operating System

Required:
- Raspberry Pi OS Bookworm 64-bit

Verify:

```bash
uname -m
```

Expected result:

```bash
aarch64
```

---

# System Update

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

---

# Audio Detection

Verify microphone:

```bash
arecord -l
```

Test recording:

```bash
arecord -D plughw:1,0 -f cd -d 5 test.wav
aplay test.wav
```

---

# Install BirdNET-Go

Download installer:

```bash
cd ~
curl -fsSL https://github.com/tphakala/birdnet-go/raw/main/install.sh -o install.sh
```

Run installer:

```bash
bash ./install.sh
```

---

# BirdNET-Go Service Commands

Check status:

```bash
sudo systemctl status birdnet-go.service
```

View logs:

```bash
journalctl -u birdnet-go.service -f
```

Restart service:

```bash
sudo systemctl restart birdnet-go.service
```

---

# Access BirdNET-Go Web Interface

Find Raspberry Pi IP:

```bash
hostname -I
```

Open in browser:

```text
http://YOUR_PI_IP:8080
```

---

# Recommended V1 Architecture

## Hardware

- Raspberry Pi 5 8 GB
- BOYA BY-MM1
- UGREEN USB Audio Adapter
- IP67 enclosure
- Raspberry Pi OS Bookworm 64-bit

## Software

- Docker
- BirdNET-Go
- Future REST API
- Future iPhone SwiftUI application

---

# Recommended Development Strategy

## Phase 1

- Install BirdNET-Go
- Validate audio
- Test species detection

## Phase 2

- Improve outdoor deployment
- Add GPS/location metadata
- Structure data storage

## Phase 3

- Build iPhone application
- Add mapping
- Add species filtering

## Phase 4

- Advanced AI
- Multiple stations
- Solar power
- Networked bioacoustic system

---

# Key Technical Advice

Main priority is NOT:
- excessive hardware optimization
- advanced AI too early

Main priorities are:
- good audio capture
- stable workflow
- clean architecture
- reliable outdoor deployment
- good UX for future mobile app

