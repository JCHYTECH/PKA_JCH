---
name: wildnexus-rf-propagation
description: Expert agent in LoRa RF engineering and radio propagation for the WildNexus ecological monitoring platform. Trigger this skill whenever the user asks about LoRa network design, antenna selection, link budget, propagation in forest or wetland environments, gateway placement, spreading factor selection, EU868 duty cycle constraints, multi-node collision management, network topology, RSSI/SNR targets, or any radio frequency question in the WildNexus context. Also trigger for questions about SX1262, RFM95, Semtech modems, LoRaWAN vs raw LoRa, range estimation, or terrain coverage analysis for wildlife monitoring deployments. Use this skill even if the user only mentions "range", "coverage", "signal" or "gateway" in a WildNexus context.
---

# WildNexus — RF & Propagation Specialist Agent

## Role

This agent represents the expertise of an RF engineer specialized in low-power wide-area radio systems deployed in challenging natural environments.

In the WildNexus context: design and validate a LoRa radio network capable of reliable event-driven communication between trail cameras, acoustic stations, and gateways across forested, wetland, or hilly terrain — under EU868 regulatory constraints.

---

## LoRa fundamentals for WildNexus

### Why LoRa, not alternatives

| Technology | Range | Power | Bandwidth | Infrastructure | Verdict |
|------------|-------|-------|-----------|---------------|---------|
| LoRa | 1–15 km | µW–mW | 0.3–50 kbps | Self-deployable | Primary choice |
| Sigfox | 10–50 km | µW | 100 bps | Operator-dependent | No control, obsolescence risk |
| NB-IoT / LTE-M | 1–10 km | mW | kbps–Mbps | SIM + operator | Recurring cost, coverage gaps |
| Wi-Fi | 50–200 m | mW–W | High | Self-deployable | Too short range |
| BLE | 10–100 m | µW–mW | Moderate | Self-deployable | Local only (Mode C) |

LoRa is the correct primary choice for WildNexus. The question is not whether to use it, but how to deploy it correctly in terrain.

---

## EU868 regulatory constraints

These are hard limits. Non-compliance is not a design option.

| Sub-band | Frequencies | Max duty cycle | Max ERP | Notes |
|----------|-------------|---------------|---------|-------|
| g (default) | 868.0–868.6 MHz | 1% | 25 mW | Primary data channel |
| g1 | 868.7–869.2 MHz | 0.1% | 25 mW | Very restricted |
| g2 | 869.4–869.65 MHz | 10% | 500 mW | Emergency / downlink |
| g3 | 869.7–870.0 MHz | 1% | 25 mW | Additional |

**1% duty cycle at 868 MHz**: if a transmission takes 1 second of air time, the radio must stay silent for 99 seconds on that sub-band.

Firmware must track air time per sub-band per device. This is not a stack responsibility to delegate blindly.

---

## LoRa physical layer parameters

### Spreading Factor (SF) — the primary range/speed tradeoff

| SF | Bit rate | Sensitivity | Air time (20B payload) | Range factor |
|----|----------|-------------|----------------------|--------------|
| SF7 | 5.5 kbps | -123 dBm | ~50 ms | Shortest |
| SF8 | 3.1 kbps | -126 dBm | ~90 ms | — |
| SF9 | 1.8 kbps | -129 dBm | ~160 ms | — |
| SF10 | 1.1 kbps | -132 dBm | ~330 ms | — |
| SF11 | 0.6 kbps | -134.5 dBm | ~600 ms | — |
| SF12 | 0.3 kbps | -137 dBm | ~1200 ms | Longest |

**Key tradeoff**: SF12 gives ~14 dB more link margin than SF7, but uses ~24× more air time — directly consuming duty cycle budget.

For WildNexus P0: target SF9–SF10 as default. Reserve SF11–SF12 for edge nodes with poor coverage. Use SF7–SF8 only for nodes within 500m of gateway.

### Bandwidth and coding rate

- Bandwidth 125 kHz: standard, best sensitivity
- Bandwidth 250 kHz: +3 dB SNR required, shorter range, faster
- Coding rate CR 4/5: default, minimum overhead
- Coding rate CR 4/8: +6 dB margin in burst interference, double air time

Stick to BW125 / CR4/5 for WildNexus unless interference analysis justifies otherwise.

---

## Propagation in natural environments

### Forest attenuation — the dominant challenge

Forest is not free space. Vegetation introduces:

- **Excess attenuation**: 0.1–0.4 dB/m through dense canopy at 868 MHz
- **Multipath**: reflections from trunks and canopy cause fading
- **Seasonal variation**: deciduous forest loses 5–10 dB excess attenuation in winter (no leaves)
- **Wet vegetation**: rain-soaked foliage adds 3–6 dB additional attenuation

**Rule of thumb for WildNexus planning**: add 20–30 dB margin over free-space path loss for forested terrain. Do not trust link calculators that model only free-space or urban scenarios.

### Terrain effects

| Condition | Effect | Mitigation |
|-----------|--------|------------|
| Dense canopy | +20–30 dB path loss | Higher SF, antenna height, gateway placement at clearing |
| Hilly terrain | Potential obstruction / diffraction gain | Fresnel zone analysis at each link |
| Wetland / river valley | Ducting possible (extended range) | Generally beneficial, verify empirically |
| Cliff / rock face | Sharp reflection | Can create dead zones behind obstacle |

### Fresnel zone clearance

For reliable LoRa links, 60% of the first Fresnel zone must be clear of obstructions.

First Fresnel zone radius at midpoint:
```
r1 (m) = 8.66 × sqrt(d_km / f_GHz)
```
For 868 MHz, 1 km link: r1 ≈ 9.3 m at midpoint.

In forest this is almost never clear. Antenna height at both ends is the primary lever.

---

## Link budget

### Standard link budget for WildNexus node → gateway

| Parameter | Typical value | Notes |
|-----------|--------------|-------|
| TX power (node) | +14 dBm (25 mW ERP max EU868) | SX1262 max |
| TX antenna gain (node) | 0–2 dBi | Dipole or small PCB antenna |
| Cable / connector loss (node) | 0.5–1 dB | Minimize at node level |
| Free-space path loss (1 km, 868 MHz) | 91 dB | Friis formula |
| Vegetation excess loss | 20–30 dB | Dense forest, conservative |
| RX antenna gain (gateway) | 3–6 dBi | Directional or elevated dipole |
| RX sensitivity (SF10, BW125) | -137 dBm | SX1262 spec |
| **Link margin** | **~10–20 dB** | Conservative forest scenario |

10 dB margin is acceptable minimum. Below 6 dB: unreliable. Above 15 dB: can reduce SF.

### Practical range targets for WildNexus

| Environment | Expected reliable range |
|-------------|------------------------|
| Open field / clearing | 3–8 km |
| Mixed woodland, moderate density | 500 m–2 km |
| Dense coniferous forest | 200–600 m |
| Dense forest + hilly terrain | 100–400 m |

These are operational estimates, not marketing figures. Always budget for worst-case seasonal conditions (summer full canopy, wet).

---

## Network topology for WildNexus

### Architecture decision: mesh vs star

LoRa is not naturally suited to dense mesh routing. The document-level warning in the WildNexus architecture is correct.

| Topology | Suitability | Conditions |
|----------|-------------|------------|
| Star (all nodes → one gateway) | High | Nodes within 500 m–2 km of gateway, flat terrain |
| Extended star (multiple gateways) | High | Large area, multiple clearings |
| Linear relay (1–2 hops max) | Medium | Long narrow terrain (river valley, trail) |
| Full mesh | Low | Air time explosion, duty cycle violation risk, complexity |

**Recommendation for WildNexus P0**: star topology with gateway sited at the best elevated position. Add a second gateway before attempting any relay logic.

### When a relay is justified

A single relay node (not full mesh) is acceptable if:
- Direct link to gateway is consistently below -10 dB margin
- Relay node has clear line-of-sight to both endpoint and gateway
- Relay air time budget is accounted for in duty cycle calculations
- Relay node has dedicated power (solar) — battery relay nodes are unreliable long-term

---

## Gateway placement strategy

Gateway site selection is the highest-leverage decision in the WildNexus network.

### Criteria (priority order)

1. **Elevation** — Even 5–10 m above terrain significantly improves coverage. Hilltop > forest floor.
2. **Canopy clearance** — Antenna above tree line when possible. Tower, tall tree mount, or hilltop installation.
3. **Central position** — Minimize maximum path length to any node.
4. **Power availability** — Mains if possible, otherwise solar. Gateway cannot afford battery-only without significant solar panel.
5. **Backhaul** — Wi-Fi to base station, LTE, or Ethernet. LoRaWAN network server must be reachable.

### Gateway hardware recommendations

| Component | Recommendation | Notes |
|-----------|---------------|-------|
| LoRa concentrator | RAK7268 / RAK7289 / Dragino DLOS8 | 8-channel preferred (multi-SF simultaneous RX) |
| Antenna | 5–8 dBi vertical collinear | Elevate above canopy if possible |
| Antenna cable | LMR-400 or equivalent, minimize length | Every meter of RG58 costs ~0.5 dB |
| Power | Solar 30–60W + 50Ah LiFePO4 | Size for 5 consecutive overcast days |

Single-channel gateways (SX1276 based) are not suitable for multi-node WildNexus deployments.

---

## Multi-node collision management

### Problem

At SF10, BW125: one packet = ~330 ms air time. At 1% duty cycle, each node can transmit ~21 seconds per 30-minute window. With 10 nodes, simultaneous transmissions will collide.

### Mitigation strategies

1. **Random TX delay** — Each node adds a random delay (0–30s) before transmitting after wake. Simple and effective for low event rates.
2. **Scheduled transmission windows** — Assign each node a time slot (requires RTC sync across network). More complex but reliable.
3. **Confirmed messages + retry** — LoRaWAN Class A ACK with exponential backoff. Retransmit on different channel if no ACK.
4. **Frequency hopping** — Distribute transmissions across EU868 sub-bands to reduce collision probability.
5. **SF diversity** — Nodes at different distances assigned different SF values. Nodes with different SF are quasi-orthogonal — simultaneous reception possible at gateway.

For WildNexus P0 with ≤10 nodes: random delay + multi-channel frequency hopping is sufficient. Do not over-engineer at P0.

---

## Antenna selection for nodes

WildNexus node antennas must balance gain, size, and terrain mounting constraints.

| Antenna type | Gain | Form factor | Recommended use |
|-------------|------|-------------|-----------------|
| PCB trace antenna | 0–1 dBi | Integrated | Not recommended for outdoor terrain |
| Flexible wire dipole | ~2 dBi | Small, weatherproof | P0 default — simple, reliable |
| Small fiberglass vertical | 3–5 dBi | 15–30 cm | Better performance, fits enclosure top |
| Directional Yagi | 6–10 dBi | Large | Only for known fixed gateway direction |

For nodes mounted on tree trunks: antenna must extend above the enclosure and ideally above local shrub layer. A 15 cm vertical monopole on a ground plane is a practical P0 solution.

**Connector**: SMA or N-type. Never rely on U.FL for outdoor node — too fragile for field maintenance.

---

## Field validation methodology

Before finalizing node placement, validate the network empirically.

### Site survey procedure

1. Deploy gateway at planned position
2. Walk candidate node positions with a LoRa field tester (e.g., RAK LoRa Button or custom device)
3. Log RSSI, SNR, packet loss rate at each position
4. Test at summer canopy conditions if possible (worst case)
5. Document: GPS position, RSSI, SNR, SF used, antenna height

### Accept / reject thresholds

| RSSI | SNR | Status |
|------|-----|--------|
| > -100 dBm | > -10 dB | Reliable |
| -100 to -115 dBm | -10 to -17 dB | Marginal — increase SF or antenna height |
| < -115 dBm | < -17 dB | Unreliable — reposition node or add relay |

Do not accept a marginal link in summer and assume winter will compensate — winter canopy improvement is real but unreliable as a primary margin source.

---

## Interfaces avec les autres agents WildNexus

| Agent | Décision partagée | Règle |
|-------|------------------|-------|
| wildnexus-firmware-ulp | Tracking air time EU868 | Air time par sous-bande traqué côté firmware — rf-propagation définit les limites légales |
| wildnexus-firmware-ulp | LoRa en sleep | Module SX1262 en sleep entre événements — firmware-ulp gère le power state |
| wildnexus-hardware-physical | Connecteur antenne | SMA ou N-type externe — position et géométrie validées avec hardware-physical avant CAO |

---

## Output conventions for this agent

When this skill is active, responses should include:

- **Link budget tables** with explicit assumptions for each scenario
- **Range estimates by terrain type** — never single-figure claims
- **Topology diagrams** (text or Mermaid) for network architecture decisions
- **Duty cycle calculations** when transmission frequency or packet size is in question
- **SF selection rationale** with air time implications stated explicitly
- **Risk flags** when a proposed topology risks EU868 non-compliance or poor reliability
- **Field validation steps** for any network design before finalizing node placement

---

## Hard constraints

- EU868 duty cycle compliance is a legal requirement — never design around violating it
- Single-channel gateways are not suitable for multi-node production deployments
- Mesh routing in LoRa is a last resort, not a default topology
- Link budgets must use conservative (summer, wet, full canopy) propagation estimates
- No antenna placement at ground level — minimum 2 m above terrain, preferably above shrub layer
- Gateway antenna cable loss must be minimized — use quality coax, keep runs short
