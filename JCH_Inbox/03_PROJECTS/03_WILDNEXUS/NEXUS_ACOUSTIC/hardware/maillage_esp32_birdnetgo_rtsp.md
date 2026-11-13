GitHub - stedrow/birdnetgo-m5stack-atom-echo-rtsp-mic: [[ESP32]] ...
Finished building an all-in-one BirdNET-go RPi system with a ...
Traditional [[Arduino]] microcontrollers cannot run BirdNET-Go natively because the [[BirdNET]] AI model requires significant processing power, memory, and a 64-bit architecture. [1, 2, 3, 4]
Instead, tinkerers use a hybrid ecosystem: [[ESP32]] microcontrollers (programmed via the [[Arduino]] IDE) act as remote, wireless microphones. They stream audio over the network to a central host computer—like a [[Raspberry Pi]], NAS, or server—which runs the tphakala/birdnet-go processing engine. [4, 5, 6, 7, 8]
How the Hybrid Architecture Works

The Transmitter (Microcontroller): An [[ESP32]] development board captures audio using a digital MEMS microphone. It streams this audio using the Real-Time Streaming Protocol (RTSP) over Wi-Fi.
The Receiver (Host): A [[Raspberry Pi]] or server runs BirdNET-Go, pulls the RTSP stream, and analyzes the audio via an embedded TensorFlow Lite model. [2, 4, 6, 9, 10]
Hardware Supported via the [[Arduino]] Ecosystem [5]

Instead of standard [[Arduino]] boards, deploy one of these compatible [[ESP32]] hardware configurations: [9]
M5Stack Atom Echo: A pocket-sized, fully encased unit with a built-in microphone and Wi-Fi. Requires zero soldering.
M5Stack AtomS3 Lite + PDM Mic: A modular setup utilizing a precision MEMS PDM microphone for crisp outdoor audio capture.
Custom [[ESP32]] + INMP441: A popular DIY approach pairing a generic [[ESP32]] development board with an INMP441 omnidirectional microphone module via I2S wiring. [5, 9, 11]
Open-Source Firmware Repositories

To turn your microcontroller into a streaming station for BirdNET-Go, flash it with one of these specialized firmware repositories:
For standalone [[ESP32]] setups: Use the Sukecz/birdnetgo-esp32-rtsp-mic firmware.
For M5Stack hardware: Deploy the customized thebaldgeek.net hardware repositories designed explicitly for Atom Echo and AtomS3 Lite nodes. [5, 9]
Configuration Blueprint

Once your microcontroller is flashing and streaming, add it to your BirdNET-Go configuration file (config.yaml) under the audio stream inputs section: [12, 13, 14]
streams:
  - name: "Backyard_ESP32_Node"
    uri: "rtsp://<YOUR_ESP32_IP_ADDRESS>:554/mjpeg/1"
The central server will continuously capture the stream, automatically filter species based on your coordinates, and send detections directly to your local dashboard or Home Assistant. [15, 16, 17]
If you would like to proceed, tell me:
Do you already have a specific hardware board (like an [[ESP32]] or [[Raspberry Pi]])?
Do you prefer a no-solder [[commercial]] module or a DIY component build?
I can provide the exact step-by-step flashing guide or wiring diagrams for your chosen route.

[1] https://www.reddit.com
[2] https://github.com
[3] https://pimylifeup.com
[4] https://github.com
[5] https://www.reddit.com
[6] https://www.reddit.com
[7] https://mariushosting.com
[8] https://mjrobot.org
[9] https://github.com
[10] https://toinekuiper.nl
[11] https://www.tinytronics.nl
[12] https://www.reddit.com
[13] https://github.com
[14] https://github.com
[15] https://www.reddit.com
[16] https://github.com
[17] https://ambientnode.uk