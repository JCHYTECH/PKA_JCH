Subject: WildNexus — Edge AI hardware for stable soundscape monitoring (complementary to Tekoälyä talleille)

Dear Aki,

I came across your excellent work on the "Tekoälyä talleille" project through the Savonia Article Pro series — the soundscape monitoring pilot and the PANNs/autoencoder approach are exactly the direction we believe in.

I'm Jean-Claude, an independent researcher based in Belgium. I lead a small R&D initiative called PKA, focused on low-power edge AI for bioacoustics. Over the past year, we've developed a hardware platform called **WildNexus** — an autonomous sensor node (ESP32-S3, stereo MEMS I2S microphones, LoRa, microSD, IP67 enclosure) that captures and classifies environmental sounds entirely at the edge, running on 8×AA batteries for 60+ days without mains power.

I believe we have complementary pieces of the same puzzle:

- **You have** the AI expertise, the equine dataset, the veterinary partners, and the EU CAP funding.
- **We have** the low-power edge hardware, the MEMS microphone array, the LoRa mesh connectivity, and an outdoor-ready, battery-autonomous form factor that eliminates the need for a DGX server on-site.

Your current RPi + DGX pipeline is perfectly suited for training — our module could handle the **field deployment** side: always-on acoustic monitoring, on-device anomaly detection, and wireless alerting, with periodic uploads to your DGX for model refinement.

**I'd love to explore a collaboration.** We could provide a few WildNexus modules for you to test at Rauhalahti Riding School — plug-and-play, no wiring needed. If there's interest, I'm happy to jump on a video call to walk you through the hardware and discuss how we might adapt it to your stable monitoring use case.

I've CC'd Johannes and Heli as I understand they're deeply involved in the technical and project management sides.

Warm regards,
Jean-Claude

---

Jean-Claude Havaux
PKA Research — Bioacoustic Edge AI
Belgium
[phone number]

---

*About WildNexus: ESP32-S3 @ 240 MHz, 2× Knowles SPH0645LM4H-B I2S MEMS (16 kHz/16-bit stereo), FFT 1024 onboard, CNN TFLite INT8, LoRa SX1262, microSD 128 GB, 8×AA → 60-day autonomy, NEMA 4X IP67 enclosure. Open-source firmware, modular PCB design. Currently deployed for wildlife camera-trapping; acoustic node variant ready for adaptation.*
