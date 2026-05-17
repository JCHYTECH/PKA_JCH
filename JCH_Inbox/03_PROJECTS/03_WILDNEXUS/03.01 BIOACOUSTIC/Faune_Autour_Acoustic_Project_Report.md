# Faune Autour — Acoustic Biodiversity Sensor & Platform
[[faune-autour]]

**Document type:** Project description report  
**Project:** Faune Autour acoustic biodiversity monitoring system  
**Version:** 1.0  
**Date:** 2026-05-04  
**Prepared for:** JC / Faune Autour project  

---

## 1. Executive summary

The Faune Autour acoustic biodiversity project aims to create a connected field device and digital platform capable of listening to the surrounding environment, recognizing animal species by sound, storing detections locally, transmitting structured data to a server, and displaying biodiversity information in a map-based application.

The first technical target is a bird-focused acoustic station based on Raspberry Pi and BirdNET-Go, connected to a Faune Autour backend and dashboard. The broader strategic vision is to evolve toward a multi-taxon biodiversity radar able to detect, interpret and map biological activity around a user or fixed location.

The project should be developed progressively through three coordinated workstreams:

1. **Scientific workstream** — species, bioacoustics, validation, ecology and interpretation.
2. **Technical workstream** — Raspberry Pi, AI recognition, API, database, app and external data integrations.
3. **Hardware workstream** — microphone, power, enclosure, connectivity and outdoor robustness.

The first decisive milestone is simple and concrete:

> A Raspberry Pi listens in a real location, identifies bird vocalizations, sends structured detections to a Faune Autour server, and displays them on a map/dashboard.

Once this milestone is achieved, the project becomes scalable toward field stations, multi-site biodiversity networks, citizen-science contribution, nature reserve monitoring, photographic field assistance and ecological intelligence.

---

## 2. Project context

Faune Autour is based on the question:

> **Which species are around me now?**

A first version of such a platform can use existing biodiversity databases, geolocation, habitat maps and historical occurrence records. However, these sources mostly indicate what species are expected to be present, not what is actually active at a specific moment.

Acoustic monitoring adds a real-time observational layer. Many animals are easier to detect by sound than by sight. This is particularly true for birds, bats, amphibians, orthopterans and some mammals. A well-designed acoustic station can therefore become a permanent or mobile biological presence sensor.

The project belongs to the field of **Passive Acoustic Monitoring**. In such systems, microphones capture the soundscape, algorithms detect biological signals, and recognition models classify probable species.

Existing technologies such as BirdNET, BirdNET-Go, BirdWeather, Haikubox, AudioMoth and Wildlife Acoustics systems show that bioacoustic monitoring is technically mature enough to support a Faune Autour prototype. The opportunity is not merely to duplicate these tools, but to create a European, geospatial, field-oriented and user-friendly biodiversity interpretation layer.

---

## 3. Final product definition

### 3.1 Working product names

Possible names:

- **Faune Autour Acoustic Node**
- **Faune Autour Bioacoustic Station**
- **Faune Autour Biodiversity Radar**
- **Faune Autour Soundscape Station**

### 3.2 Product nature

The product is a connected acoustic biodiversity station linked to the Faune Autour application.

It is not only a sound recorder. It is a biological presence sensor able to:

- listen to the environment;
- identify probable species by sound;
- attach metadata to each detection;
- transmit structured observations;
- display detections on a map;
- compare detected species with expected species;
- support validation and ecological interpretation.

### 3.3 Core product function

The final product should perform the following sequence:

1. Capture environmental sound.
2. Segment audio into analysis windows.
3. Analyse sound locally using an AI recognition model.
4. Generate probable species detections with confidence scores.
5. Store detections locally.
6. Send structured detection data to the Faune Autour backend.
7. Display results in the app/dashboard.
8. Allow validation, filtering and ecological interpretation.
9. Optionally connect to external biodiversity databases and acoustic networks.

### 3.4 Main user scenarios

#### Naturalist mode

A naturalist opens the app and sees which birds or other vocal species were detected in a forest, wetland, garden or reserve.

#### Wildlife photographer mode

A photographer installs a station near a hide or observation site and receives information about species activity before or during a field session.

#### Garden / private land mode

A landowner monitors biodiversity around a garden, pond, hedge or small woodland.

#### Educational mode

A school or nature club compares soundscapes between habitats and seasons.

#### Municipality / conservation mode

A commune, park manager or reserve manager monitors biodiversity trends before and after habitat restoration, mowing, tree felling or other management interventions.

#### Scientific / expert mode

An expert user validates detections, exports data, analyses temporal patterns and contributes to structured biodiversity databases.

---

## 4. Product architecture overview

The system should be designed as a modular ecosystem composed of six layers.

### 4.1 Layer 1 — Field acoustic node

The physical device captures sound in the field.

Prototype components:

- Raspberry Pi 4 or Raspberry Pi 5;
- USB microphone or external audio interface;
- optional GPS module;
- optional 4G/LTE modem;
- optional environmental sensors;
- local storage;
- weather-resistant enclosure;
- power system: mains, battery, solar or hybrid.

### 4.2 Layer 2 — Edge AI recognition

The device analyses sound locally. For the first prototype, the recommended recognition engine is BirdNET-Go.

Initial target group:

- birds.

Later target groups:

- bats;
- amphibians;
- orthopterans/insects;
- selected mammals.

### 4.3 Layer 3 — Local data storage

The device stores detections locally before upload. This prevents data loss when the network is unavailable.

Local storage should include:

- device ID;
- timestamp;
- species name;
- scientific name;
- confidence score;
- GPS or station location;
- model version;
- optional audio clip path;
- battery/network status;
- validation status.

### 4.4 Layer 4 — Data transmission

The device sends structured observations to the backend.

Transmission options:

- Wi-Fi;
- Ethernet;
- 4G/LTE;
- MQTT;
- REST API;
- offline synchronization;
- manual export for early prototypes.

### 4.5 Layer 5 — Faune Autour backend

The backend receives, stores, validates and exposes observations.

Main backend functions:

- device registration;
- station management;
- detection ingestion;
- geospatial storage;
- species taxonomy normalization;
- audio snippet storage;
- map API;
- user permissions;
- validation workflow;
- external API integration.

### 4.6 Layer 6 — App / dashboard

The app is the user-facing interpretation layer.

It should show:

- live detections;
- species list;
- confidence score;
- map position;
- timeline;
- detected vs expected species;
- station status;
- export tools;
- validation tools.

---

## 5. Classification of specifications

## 5.1 Functional specifications

### F1 — Acoustic capture

**Objective:** capture environmental sound with sufficient quality for species recognition.

Required functions:

- continuous recording or scheduled recording;
- dawn/dusk/night/full-day modes;
- support for outdoor microphone;
- local audio buffering;
- optional short audio clips linked to detections.

Required competences:

- audio hardware selection;
- Raspberry Pi audio configuration;
- Linux sound-card configuration;
- signal-to-noise testing;
- outdoor microphone protection.

Priority: **Essential**

---

### F2 — Species recognition

**Objective:** detect and classify animal sounds.

Required functions:

- bird recognition in version 1;
- confidence scoring;
- geographic filtering;
- seasonal filtering;
- false-positive reduction;
- model version tracking;
- extension path to bats, amphibians and insects.

Required competences:

- BirdNET-Go installation;
- AI inference on edge device;
- bioacoustics;
- ornithology/species knowledge;
- model evaluation;
- false-positive management.

Priority: **Essential**

---

### F3 — Local data storage

**Objective:** avoid data loss when connectivity is absent.

Required functions:

- local detection database;
- offline queue;
- retry mechanism;
- local logs;
- local configuration file;
- diagnostic information.

Required competences:

- SQLite;
- Linux services;
- data schema design;
- error handling;
- offline-first architecture.

Priority: **Essential**

---

### F4 — Data transmission

**Objective:** send structured detection events to Faune Autour.

Required functions:

- REST API upload;
- optional MQTT event stream;
- HTTPS communication;
- device authentication;
- retry queue;
- upload of metadata first;
- optional upload of short audio clips.

Required competences:

- REST API client development;
- MQTT;
- JSON data formatting;
- secure networking;
- authentication tokens;
- network resilience.

Priority: **Essential**

---

### F5 — Backend and central database

**Objective:** receive, store and expose acoustic detections.

Required functions:

- register devices;
- receive detections;
- store geospatial data;
- normalize species names;
- manage users and stations;
- expose map data;
- manage validation status;
- export data.

Required competences:

- backend development;
- API architecture;
- PostgreSQL;
- PostGIS;
- authentication;
- cloud/server deployment;
- database administration.

Priority: **Essential**

---

### F6 — App and dashboard

**Objective:** make biodiversity detections understandable and usable.

Required functions:

- live species list;
- map view;
- timeline view;
- confidence display;
- detection filters;
- station status;
- validation screen;
- export CSV/GeoJSON.

Required competences:

- frontend development;
- PWA or mobile app development;
- map interface development;
- UX/UI design;
- API integration;
- data visualization.

Priority: **Essential**

---

### F7 — External API connections

**Objective:** enrich detections with external biodiversity and environmental data.

Potential connections:

- BirdWeather;
- GBIF;
- iNaturalist;
- eBird, depending on access and terms;
- OpenStreetMap;
- weather APIs;
- protected-area datasets;
- national biodiversity databases.

Required functions:

- import nearby observations;
- compare expected vs detected species;
- normalize taxonomy;
- cache external data;
- respect terms of use;
- optionally publish compatible detections.

Required competences:

- API integration;
- data engineering;
- taxonomy mapping;
- GIS querying;
- legal/terms-of-use review.

Priority: **Phase 2**

---

### F8 — Expert validation workflow

**Objective:** distinguish AI suggestions from validated observations.

Required functions:

- statuses: unverified, probable, validated, rejected;
- expert review screen;
- audio snippet review;
- confidence thresholds;
- validation history;
- false-positive correction.

Required competences:

- scientific data workflow;
- bioacoustic validation;
- database audit trail;
- UX for expert review;
- taxonomy standards.

Priority: **Phase 2**

---

### F9 — Energy autonomy

**Objective:** support reliable field deployment.

Required functions:

- mains power for garden version;
- battery option;
- solar option;
- power monitoring;
- low-power modes;
- scheduled recording.

Required competences:

- low-voltage electronics;
- battery sizing;
- solar sizing;
- power budgeting;
- field hardware integration.

Priority: **Phase 2 for outdoor version**

---

### F10 — Outdoor robustness

**Objective:** make the device survive real field conditions.

Required functions:

- weatherproof enclosure;
- wind/rain microphone protection;
- cable sealing;
- condensation management;
- thermal management;
- easy maintenance.

Required competences:

- mechanical prototyping;
- IP-rated enclosure design;
- outdoor cabling;
- field testing;
- maintenance planning.

Priority: **Phase 2**

---

## 5.2 Non-functional specifications

### NF1 — Reliability

Requirements:

- automatic restart after crash;
- watchdog service;
- resilient local queue;
- remote status check;
- log files;
- uptime monitoring.

Required competences:

- Linux administration;
- systemd services;
- monitoring;
- fault-tolerant software design.

---

### NF2 — Accuracy

Requirements:

- confidence threshold;
- geographic filtering;
- seasonal filtering;
- repeated detections before confirmation;
- expert validation for rare species;
- uncertainty display.

Required competences:

- bioacoustics;
- species distribution knowledge;
- statistical filtering;
- AI model evaluation.

---

### NF3 — Scalability

Requirements:

- unique device IDs;
- station groups;
- rate limiting;
- database indexing;
- geospatial queries;
- multi-user support.

Required competences:

- backend architecture;
- PostgreSQL/PostGIS optimization;
- cloud deployment;
- API security;
- DevOps.

---

### NF4 — Privacy and GDPR

Requirements:

- no continuous raw audio upload by default;
- short clips only when useful;
- user consent;
- location privacy;
- sensitive species masking;
- data deletion rules;
- privacy policy.

Required competences:

- privacy-by-design;
- GDPR-aware architecture;
- secure storage;
- legal/data governance.

---

### NF5 — Maintainability

Requirements:

- remote configuration;
- update mechanism;
- version tracking;
- installation scripts;
- technical documentation;
- support workflow.

Required competences:

- DevOps;
- Linux packaging;
- Docker;
- technical writing;
- field support design.

---

## 6. Technical competence classification

## 6.1 Bioacoustics and species expertise

Role: define biological detection logic and validate outputs.

Tasks:

- select target species groups;
- define recognition thresholds;
- evaluate false positives;
- define geographic and seasonal filters;
- create validation rules;
- design ecological interpretation.

Profile:

- zoologist;
- ornithologist;
- bioacoustics specialist;
- field naturalist.

Importance: **Critical**

---

## 6.2 Raspberry Pi / Linux edge computing

Role: build the local recognition station.

Tasks:

- install Raspberry Pi OS;
- configure microphone;
- install BirdNET-Go;
- configure startup services;
- manage logs;
- handle local storage;
- create watchdog and restart logic.

Profile:

- Linux/Raspberry Pi developer;
- embedded Linux technician.

Importance: **Critical for prototype**

---

## 6.3 Audio hardware and electronics

Role: ensure the device captures sound reliably.

Tasks:

- choose microphone;
- test gain and noise;
- select audio interface if needed;
- design enclosure;
- implement power supply;
- integrate battery/solar;
- add 4G/GPS/environmental sensors.

Profile:

- electronics prototyping engineer;
- maker/hardware technician;
- field instrumentation specialist.

Importance: **Critical for field version**

---

## 6.4 Backend/API development

Role: create the data infrastructure.

Tasks:

- design API endpoints;
- receive detections;
- authenticate devices;
- store observations;
- normalize species names;
- expose map data;
- connect external APIs.

Profile:

- backend developer;
- API developer.

Importance: **Critical**

---

## 6.5 Database and geospatial data

Role: structure and query biodiversity data.

Tasks:

- design detection schema;
- use PostgreSQL/PostGIS;
- store coordinates;
- query observations by radius;
- export GeoJSON;
- manage time-series data;
- index large tables.

Profile:

- database developer;
- GIS developer;
- data engineer.

Importance: **Critical**

---

## 6.6 Frontend / app development

Role: create the user interface.

Tasks:

- build dashboard;
- create map view;
- display detections;
- show timelines;
- create station interface;
- create validation screens;
- develop PWA or mobile app.

Profile:

- frontend developer;
- React/Next.js developer;
- Flutter or React Native developer if native app is required.

Importance: **Critical for usability**

---

## 6.7 API integration specialist

Role: connect Faune Autour to external data sources.

Tasks:

- connect BirdWeather;
- connect GBIF;
- connect weather APIs;
- connect OpenStreetMap;
- normalize taxonomies;
- cache external results;
- respect API limits.

Profile:

- integration developer;
- data engineer.

Importance: **Phase 2**

---

## 6.8 DevOps and deployment

Role: make the system robust and deployable.

Tasks:

- Dockerize services;
- deploy backend;
- configure backups;
- monitor uptime;
- manage HTTPS;
- manage logs;
- separate staging and production environments.

Profile:

- DevOps engineer;
- cloud engineer.

Importance: **Phase 2, but should be planned early**

---

## 6.9 UX/product design

Role: transform raw detections into a useful experience.

Tasks:

- define user flows;
- design clear screens;
- avoid scientific overload;
- design confidence indicators;
- create detected vs expected interface;
- design device setup flow.

Profile:

- UX/UI designer;
- product designer with scientific data sensitivity.

Importance: **Important**

---

## 6.10 Legal/privacy/data governance

Role: protect users, locations and sensitive species.

Tasks:

- define privacy policy;
- define audio retention rules;
- define user consent;
- define sensitive species masking;
- review external API terms;
- ensure GDPR compliance.

Profile:

- legal adviser;
- data protection adviser;
- biodiversity data governance specialist.

Importance: **Important before public launch**

---

## 7. Recommended team structure

## 7.1 Minimum prototype team

### Product owner / scientific lead

Potentially JC.

Responsibilities:

- define use case;
- define target species;
- validate ecological logic;
- prioritize features;
- test in real field conditions.

### Raspberry Pi / Linux developer

Responsibilities:

- install BirdNET-Go;
- configure device;
- create local connector;
- manage services and logs.

### Backend/API developer

Responsibilities:

- build Faune Autour API;
- design database;
- receive detections;
- prepare data for app.

### Frontend/PWA developer

Responsibilities:

- create dashboard;
- create map;
- create user interface.

### Hardware/electronics adviser

Can be part-time initially.

Responsibilities:

- choose microphone;
- define enclosure;
- define power system;
- prepare field reliability.

---

## 7.2 Ideal job title for key technical hire

Recommended title:

> **IoT / Full-Stack Developer for Bioacoustic Monitoring Platform**

Alternative title:

> **Full-Stack IoT Developer with API and Geospatial Data Experience**

This is more precise than “IT expert” because the person must understand connected devices, APIs, field data, maps, databases and cloud deployment.

---

## 8. Development roadmap

## Phase 0 — Product framing

Objective: define exactly what version 1 must be.

Tasks:

1. Define target user.
2. Define first taxonomic group: birds.
3. Define first environment: garden, forest edge or reserve.
4. Define first connectivity mode: Wi-Fi.
5. Define whether the station is fixed or mobile.
6. Define minimum dashboard: map + list + timeline.
7. Define success criteria.
8. Define initial budget.

Deliverables:

- product brief;
- MVP definition;
- user scenarios;
- success criteria;
- first budget.

Required competences:

- product owner;
- zoologist/bioacoustics adviser;
- technical architect.

Recommended decision:

> Start with a fixed Wi-Fi bird station, then move to outdoor autonomous version.

---

## Phase 1 — Technical proof of concept

Objective: make one Raspberry Pi identify birds and store detections.

Tasks:

1. Buy Raspberry Pi 4 or 5.
2. Buy and test USB microphone.
3. Install Raspberry Pi OS.
4. Install BirdNET-Go.
5. Configure location and species language.
6. Run a 24-hour acoustic test.
7. Check detection list.
8. Export local detections.
9. Evaluate false positives.

Deliverables:

- working Raspberry Pi recognition station;
- local detection database;
- first species detection report;
- list of hardware issues;
- list of recognition-quality issues.

Required competences:

- Raspberry Pi/Linux developer;
- audio hardware tester;
- bioacoustics evaluator.

Success criterion:

> The prototype detects real local birds and records usable detection events.

---

## Phase 2 — Local connector and data schema

Objective: transform recognition outputs into Faune Autour data.

Tasks:

1. Define detection JSON format.
2. Create device ID.
3. Create local SQLite schema.
4. Build connector script.
5. Read BirdNET-Go detections.
6. Add metadata: location, confidence, timestamp, model version.
7. Create retry queue.
8. Prepare local logs.

Deliverables:

- Faune Autour detection schema;
- connector service;
- local queue system;
- device diagnostic log.

Required competences:

- Python or Go developer;
- data architect;
- Linux service developer.

Success criterion:

> The device produces clean structured events independent of the recognition engine’s internal format.

---

## Phase 3 — Faune Autour backend API

Objective: receive and store detections centrally.

Tasks:

1. Create backend project.
2. Define API endpoints.
3. Create authentication token for device.
4. Create PostgreSQL/PostGIS database.
5. Create detection ingestion endpoint.
6. Create station table.
7. Create species table.
8. Create map query endpoint.
9. Create CSV/GeoJSON export.

Deliverables:

- backend API;
- database schema;
- API documentation;
- test detection upload;
- export function.

Required competences:

- backend developer;
- database/PostGIS developer;
- API architect.

Success criterion:

> A Raspberry Pi can send a detection to the server and the server can return it as map data.

---

## Phase 4 — First web dashboard

Objective: make detections visible and useful.

Tasks:

1. Create simple web app.
2. Display station on map.
3. Display latest detections.
4. Display species timeline.
5. Display confidence score.
6. Display station status.
7. Add filters by date, species and confidence.
8. Add export button.

Deliverables:

- PWA or web dashboard;
- map view;
- detection list;
- timeline view;
- station status panel.

Required competences:

- frontend developer;
- UX designer;
- GIS/map developer.

Success criterion:

> A user can open the dashboard and understand which species were detected, where and when.

---

## Phase 5 — Ecological intelligence layer

Objective: add interpretation beyond raw detection.

Tasks:

1. Connect external occurrence data.
2. Build expected-species list by location.
3. Compare expected species vs detected species.
4. Add seasonality.
5. Add habitat context.
6. Add rarity or unusual-detection flag.
7. Add first-detection-of-day/week/site logic.

Deliverables:

- expected species engine;
- detected vs expected dashboard;
- species probability layer;
- ecological interpretation text.

Required competences:

- data engineer;
- zoologist/ecologist;
- API integration specialist;
- GIS developer.

Success criterion:

> The application does not only say “species detected”; it says whether the detection is expected, interesting, rare or uncertain.

---

## Phase 6 — Outdoor autonomous prototype

Objective: make the system usable outside.

Tasks:

1. Choose waterproof enclosure.
2. Add microphone protection.
3. Add battery.
4. Add solar panel.
5. Add power monitoring.
6. Add 4G modem.
7. Add external antenna.
8. Add condensation control.
9. Run field test.

Deliverables:

- outdoor prototype;
- power budget;
- solar/battery sizing report;
- field test report;
- hardware bill of materials.

Required competences:

- electronics/hardware engineer;
- field technician;
- Linux developer;
- bioacoustics tester.

Success criterion:

> The device runs outdoors for several days and transmits detections reliably.

---

## Phase 7 — Validation and quality control

Objective: make the data credible.

Tasks:

1. Create validation status system.
2. Add expert review screen.
3. Store audio snippets for review.
4. Define confidence thresholds.
5. Define sensitive species treatment.
6. Define false-positive correction workflow.
7. Create quality score.

Deliverables:

- validation workflow;
- expert dashboard;
- detection quality rules;
- false-positive log;
- scientific credibility protocol.

Required competences:

- bioacoustics expert;
- frontend developer;
- backend developer;
- data governance adviser.

Success criterion:

> The system distinguishes clearly between AI suggestions and validated biodiversity observations.

---

## Phase 8 — Multi-station and network mode

Objective: scale from one device to many devices.

Tasks:

1. Create station management.
2. Create user accounts.
3. Create station groups.
4. Create public/private settings.
5. Add map of multiple stations.
6. Add aggregated statistics.
7. Add network health dashboard.

Deliverables:

- multi-device platform;
- admin dashboard;
- station owner interface;
- aggregated biodiversity map.

Required competences:

- backend developer;
- DevOps engineer;
- frontend developer;
- database architect.

Success criterion:

> Faune Autour can manage a network of acoustic stations.

---

## Phase 9 — Productization

Objective: transform prototype into a usable product.

Tasks:

1. Standardize hardware kit.
2. Create installation guide.
3. Create device setup wizard.
4. Create software update process.
5. Create support workflow.
6. Create pricing model.
7. Create packaging.
8. Review legal/privacy compliance.

Deliverables:

- product specification document;
- bill of materials;
- installation manual;
- user guide;
- maintenance guide;
- privacy policy;
- commercial positioning.

Required competences:

- product manager;
- hardware designer;
- UX designer;
- legal adviser;
- technical writer;
- support engineer.

Success criterion:

> A non-developer user can install and operate the system.

---

## 9. Dependencies between tasks

The project has strong technical dependencies. The correct sequence avoids wasted effort.

### 9.1 Main dependency chain

1. Product framing must come before hardware and software design.
2. Hardware prototype must come before outdoor enclosure design.
3. BirdNET-Go testing must come before custom connector development.
4. Detection schema must come before backend API.
5. Backend API must come before dashboard integration.
6. Dashboard must come before advanced UX optimization.
7. Basic detections must come before ecological interpretation.
8. Stable indoor prototype must come before solar/4G outdoor version.
9. Validation workflow must come before public/scientific data publication.
10. Multi-station support must come before network-scale deployment.

### 9.2 Simplified dependency table

| Task | Depends on |
|---|---|
| Define MVP | None |
| Select hardware | MVP definition |
| Install BirdNET-Go | Hardware selected |
| Test local detections | BirdNET-Go installed |
| Define detection schema | Local detection test |
| Build connector | Detection schema |
| Build backend API | Detection schema |
| Upload detections | Connector + backend API |
| Build dashboard | Backend API |
| Add map view | Dashboard + geospatial database |
| Add expected species | External API connections + location data |
| Add validation | Detections + audio snippet storage |
| Build outdoor station | Stable indoor prototype |
| Add solar/4G | Outdoor station design |
| Multi-station platform | Backend + dashboard stable |
| Productization | Field prototype validated |

---

## 10. Priority matrix

## 10.1 Must-have for first prototype

- Raspberry Pi station;
- microphone;
- BirdNET-Go;
- local detection storage;
- detection JSON schema;
- backend ingestion API;
- basic map dashboard;
- confidence score;
- manual export.

## 10.2 Should-have for field version

- 4G connectivity;
- battery/solar;
- weatherproof enclosure;
- device health monitoring;
- offline queue;
- remote configuration;
- expected vs detected species layer.

## 10.3 Could-have later

- bat detection;
- amphibian detection;
- insect detection;
- mobile app;
- push alerts;
- expert validation network;
- community-science publication;
- soundscape biodiversity index;
- camera trap integration;
- Obsidian field notebook export.

## 10.4 Not recommended for first version

- mass consumer hardware;
- custom AI model training;
- full multi-taxon recognition;
- real-time public network;
- scientific certification;
- native iOS/Android app unless PWA is insufficient.

---

## 11. Data model proposal

### 11.1 Detection object

A detection event should contain at least:

```json
{
  "device_id": "FAUNE-NODE-001",
  "station_id": "STATION-001",
  "timestamp_utc": "2026-05-04T07:30:00Z",
  "latitude": 50.000000,
  "longitude": 5.000000,
  "location_accuracy_m": 10,
  "species_scientific_name": "Turdus merula",
  "species_common_name": "Common Blackbird",
  "confidence": 0.87,
  "model_name": "BirdNET-Go",
  "model_version": "to_be_defined",
  "audio_clip_url": null,
  "validation_status": "unverified",
  "battery_level": 82,
  "network_status": "online"
}
```

### 11.2 Validation statuses

Recommended values:

- `unverified`
- `probable`
- `validated`
- `rejected`
- `needs_review`

### 11.3 Privacy levels

Recommended values:

- `private`
- `shared_with_project`
- `public_generalized_location`
- `public_precise_location`
- `restricted_sensitive_species`

---

## 12. API environment

## 12.1 Internal Faune Autour API

Suggested endpoints:

```text
POST /devices/register
POST /detections
POST /audio-clips
GET /devices/{id}/status
GET /stations/{id}/detections
GET /species/nearby
GET /map/detections
PATCH /detections/{id}/validation
GET /alerts
GET /exports/geojson
GET /exports/csv
```

## 12.2 Device-to-server communication

Recommended first version:

- HTTPS REST API;
- JSON payload;
- token-based authentication;
- local retry queue.

Recommended later version:

- MQTT for real-time events;
- REST for configuration and historical queries;
- device health telemetry;
- remote configuration.

## 12.3 External API integrations

Potential integrations:

- BirdWeather for acoustic detection network data;
- GBIF for occurrence data;
- iNaturalist for citizen observations;
- OpenStreetMap for habitat context;
- weather APIs for environmental context;
- national biodiversity databases where available.

---

## 13. Energy and connectivity specifications

## 13.1 Garden / indoor version

Recommended setup:

- mains power;
- Wi-Fi;
- Raspberry Pi;
- USB microphone;
- local storage;
- cloud upload.

Advantages:

- simple;
- low maintenance;
- ideal for first prototype;
- good for schools, gardens and fixed stations.

## 13.2 Outdoor field version

Recommended setup:

- battery;
- optional solar panel;
- 4G/LTE modem;
- external antenna;
- waterproof enclosure;
- local buffering;
- power monitoring.

Design constraints:

- continuous inference consumes energy;
- 4G transmission can consume significant power;
- solar sizing must account for winter and shade;
- condensation can damage electronics;
- microphone placement affects accuracy.

## 13.3 Power strategy

Recommended first strategy:

1. Develop mains/Wi-Fi version.
2. Measure real power consumption.
3. Design battery version using measured consumption.
4. Add solar only after real field data.
5. Add low-power scheduling if needed.

---

## 14. Innovation vision

The most interesting innovation is not only automatic species identification. It is **ecological presence intelligence**.

Most current tools answer:

> What bird is singing?

Faune Autour should answer:

> What is happening biologically around me?

### 14.1 Biodiversity radar

The app should behave like a radar of local biological activity:

- species detected now;
- species expected today;
- species absent despite being expected;
- unusual species;
- best observation time;
- trend over days and seasons.

### 14.2 Observed vs expected biodiversity

This feature should become central.

Categories:

- detected now;
- expected but not detected;
- unexpected or noteworthy;
- uncertain and requiring validation;
- new for the site;
- recurring seasonal species.

### 14.3 Photographer mode

Possible functions:

- activity alerts near a hide;
- best time of day by species;
- dawn chorus intensity;
- repeated detection zones;
- sound-triggered field notes;
- export to Obsidian photographic journal.

### 14.4 Conservation mode

Possible functions:

- before/after habitat restoration monitoring;
- hedge or pond biodiversity score;
- mowing impact analysis;
- amphibian breeding acoustic activity;
- bat activity monitoring;
- ecological evidence for land-use decisions.

### 14.5 Network effect

With multiple stations, Faune Autour can become a distributed biodiversity observatory:

- migration timing;
- first seasonal song dates;
- urban vs rural biodiversity comparison;
- soundscape health indicators;
- climate-change phenology signals.

---

## 15. Risk register

| Risk | Probability | Impact | Mitigation |
|---|---:|---:|---|
| False positive detections | High | High | Confidence thresholds, filters, expert validation |
| Poor microphone quality | Medium | High | Field testing, better microphone, wind/rain protection |
| Excessive power consumption | Medium | High | Measure first, schedule recording, optimize hardware |
| Network loss | High | Medium | Local queue and offline sync |
| Privacy concerns | Medium | High | Local processing, no raw audio upload by default |
| Sensitive species exposure | Medium | High | Location masking, restricted access |
| API dependency | Medium | Medium | Build own data model, cache external data |
| Outdoor hardware failure | Medium | High | Weatherproof enclosure, condensation management |
| Over-complex MVP | High | High | Start with bird-only fixed Wi-Fi station |
| Lack of validation credibility | Medium | High | Validation workflow and expert review |

---

## 16. Immediate next tasks

Recommended immediate sequence:

1. Freeze MVP definition:
   - fixed station;
   - birds only;
   - Wi-Fi;
   - Raspberry Pi;
   - dashboard with map/list/timeline.

2. Build first Raspberry Pi BirdNET-Go station.

3. Test microphone and detection accuracy for one week.

4. Define Faune Autour detection JSON schema.

5. Build local connector.

6. Build backend ingestion endpoint.

7. Build first dashboard.

8. Test complete chain:
   - sound capture;
   - species recognition;
   - local storage;
   - server upload;
   - map display.

9. Analyse false positives.

10. Only then design outdoor autonomous station.

---

## 17. Suggested project governance

### 17.1 Weekly review

A weekly project review should check:

- tasks completed;
- blocked tasks;
- technical risks;
- detection quality;
- hardware issues;
- next-week priorities.

### 17.2 Key performance indicators

Prototype KPIs:

- uptime;
- number of detections per day;
- percentage of plausible detections;
- false-positive rate;
- upload success rate;
- battery life if field version;
- dashboard usability;
- number of validated species.

### 17.3 Documentation to maintain

Recommended documents:

- product brief;
- hardware bill of materials;
- installation guide;
- API specification;
- detection schema;
- data privacy note;
- validation protocol;
- field test reports;
- roadmap and backlog.

---

## 18. Final operational conclusion

The project is technically realistic and strategically interesting. The strongest path is not to build a complex multi-species autonomous product immediately. The correct path is progressive:

1. prove bird detection on Raspberry Pi;
2. create a clean Faune Autour data pipeline;
3. display detections on a dashboard;
4. add ecological intelligence;
5. move toward outdoor autonomy;
6. scale into a networked biodiversity platform.

The essential product vision can be summarized as:

> **Faune Autour becomes a biodiversity radar: a system that detects, maps and interprets the living soundscape around a user or location.**

The first milestone remains the critical one:

> **One Raspberry Pi, one microphone, one real place, real bird detections, structured upload, and a map/dashboard.**

Once this works, the project can evolve into a field product, a naturalist tool, a photographic assistant, an educational platform, a municipal biodiversity monitor and eventually a European distributed acoustic biodiversity network.
