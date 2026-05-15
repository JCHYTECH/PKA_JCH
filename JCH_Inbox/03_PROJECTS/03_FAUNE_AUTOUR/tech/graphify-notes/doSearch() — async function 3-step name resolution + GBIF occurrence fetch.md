---
source_file: "git/faune-autour_13.html"
type: "document"
community: "Species Search & Geolocation Logic"
tags:
  - graphify/document
  - graphify/EXTRACTED
  - community/Species_Search_&_Geolocation_Logic
---

# doSearch() — async function: 3-step name resolution + GBIF occurrence fetch

## Connections
- [[DICT_INDEX — bidirectional JS index (lowercase key → species entry)]] - `calls` [EXTRACTED]
- [[GBIF Occurrence Search API (api.gbif.orgv1occurrencesearch)]] - `calls` [EXTRACTED]
- [[GBIF Species Match API (api.gbif.orgv1speciesmatch and speciessearch)]] - `calls` [EXTRACTED]
- [[Mode Par Espèce — search observations by species name (FR or Latin)]] - `implements` [INFERRED]
- [[Rationale 3-step species name resolution — GBIF speciesmatch poor at French vernacular names; local dict + vernacularName endpoint + strict fallback]] - `rationale_for` [EXTRACTED]
- [[bboxWkt() — WKT polygon from latlon + radius (km)]] - `calls` [EXTRACTED]
- [[gpsInit() — CoreLocation GPS via navigator.geolocation, fallback Brussels simulation]] - `shares_data_with` [EXTRACTED]

#graphify/document #graphify/EXTRACTED #community/Species_Search_&_Geolocation_Logic