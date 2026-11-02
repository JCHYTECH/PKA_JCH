# PKA_JCH — Project Mindmap

> Generated: 2026-06-23 — Dobby 🦉
> Format: Mermaid (compatible Obsidian, GitHub, mermaid.live)

```mermaid
mindmap
  root((PKA_JCH))
    WILDNEXUS_P0
      Camera Trap ESP32-S3
      LoRa Communication
      PPK2 Power Profiling
      Edge AI / FOMO
      Base Station RPi
      Budget 1000€
      Deadline 30 juin
    NEXUS_ACOUSTIC_P1
      InsectNet
        Orthoptera Classification
        Dual-Channel Spectrogram
        Xeno-Canto Dataset
        geomodel GBIF Post-Filter
        Manifold UMAP 3D
      LEAFNET
        Plant Bioelectrical Node
        AD623ANZ Amplifier
        ESP-NOW Telemetry
        MIDI Sonification
        Home Assistant Integration
      BirdNET Ecosystem
        BirdNET-Go RPi
        ecoPi Dashboard
        birdnet-stm32 Reference
      Faune_Autour
        PWA Frontend
        GBIF Data
        FROZEN
    IOT
      IoT Van
        RPi 5 12V DC-DC
        HA Autonomous
        Zigbee Sensors
        Tailscale
        PV PI Solar
      IoT Serre
        RPi 5 Esneux
        BOM 247€
        5 Phases
      IoT Maison
        Same RPi Hub
        Long Term
      Home Assistant
        M5 Docker localhost:8123
        Esneux RPi HA OS
        Van RPi HA OS
        Zigbee2MQTT
        Mosquitto
    ARTEON
      Wildlife Photography
      Shopify Store
      WildLens Ghost Blog
      WhiteWall Printing
      Step 4 of 13
    PHOTO_NATURE
      Photo Keyworder
      IPTC XMP Tagging
      Ollama Vision
      Lightroom Integration
    PHOTO_AI_JURY
      AI Critique System
      Argus MCP
      Lightroom MCP
    VETALYX
      Vita X Nesting
      IgE Allergy Tests
      Zheda Dixun Mfg
      DIAHO Distribution
      EU Regulatory
      KOL Clinical Validation
    AI_IT_TOOLS
      Dobby Orchestrator
      Graphify Knowledge Graph
      Memory Layer
      Skills System
      Team Management
    FUTURE_INVEST
      Financial Models
      Sigma Loop
    TRAVELS
      Trip Planning
```

## Connection Map

```mermaid
graph TD
    subgraph "Core Infrastructure"
        AI[AI_IT_TOOLS<br/>Dobby Orchestrator]
    end

    subgraph "Wildlife Tech"
        WN[WILDNEXUS P0<br/>Camera Trap ESP32]
        NX[NEXUS_ACOUSTIC P1<br/>Bioacoustics]
        LF[LEAFNET<br/>Plant Node]
        FA[FAUNE_AUTOUR<br/>PWA - FROZEN]
    end

    subgraph "IoT & Home"
        HA[Home Assistant<br/>Distributed]
        VAN[IoT Van<br/>RPi 5 Solar]
        SER[IoT Serre<br/>RPi 5 Esneux]
        MS[IoT Maison<br/>Long Term]
    end

    subgraph "Photography"
        ART[ARTEON<br/>Editorial Photo]
        PN[PHOTO_NATURE<br/>Keyworder]
        PJ[PHOTO_AI_JURY<br/>AI Critique]
    end

    subgraph "Business"
        VX[VETALYX<br/>Vita X Nesting]
        FI[FUTURE_INVEST<br/>Financial]
    end

    subgraph "Personal"
        TR[TRAVELS]
    end

    %% Cross-connections
    WN -->|P1 bioacoustics| NX
    WN -->|ESP32-S3 shared| VAN
    WN -->|PPK2 + power| SER
    WN -->|Edge AI| AI
    NX -->|Frontend PWA| FA
    NX -->|Parent project| LF
    NX -->|BirdNET-Go RPi| HA
    LF -->|ESP-NOW → MQTT| HA
    VAN -->|Tailscale| HA
    SER -->|RPi 5 shared| MS
    HA -->|Docker M5| AI
    ART -->|Workflow| PN
    ART -->|AI critique| PJ
    PN -->|Ollama vision| AI
    PJ -->|Argus MCP| AI
    VX -->|Regulatory| AI
    AI -->|Graphify| NX
    AI -->|Memory Layer| VX
```

## Hardware Convergence

```mermaid
graph LR
    subgraph "ESP32-S3 Family"
        WN_ESP[WildNexus<br/>Camera Trap]
        LF_ESP[LEAFNET<br/>Plant Sensor]
        VAN_ESP[IoT Van<br/>Sensors]
    end

    subgraph "Raspberry Pi Family"
        NX_RPI[NEXUS<br/>BirdNET-Go]
        HA_RPI[Home Assistant<br/>Esneux + Van]
        WN_RPI[WildNexus<br/>Base Station]
    end

    subgraph "Shared Tools"
        PPK2[PPK2<br/>Power Profiler]
        SOLAR[PV PI<br/>Solar HAT]
        ZIGBEE[Zigbee<br/>Sensors]
    end

    WN_ESP -.-> PPK2
    LF_ESP -.-> PPK2
    VAN_ESP -.-> PPK2
    NX_RPI -.-> SOLAR
    HA_RPI -.-> SOLAR
    WN_RPI -.-> SOLAR
    HA_RPI -.-> ZIGBEE
    VAN_ESP -.-> ZIGBEE
```

---

*Visualiser sur https://mermaid.live ou dans Obsidian avec le plugin Mermaid.*
