---
type: community
cohesion: 0.25
members: 9
---

# Species Search & Geolocation Logic

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[DICT_INDEX — bidirectional JS index (lowercase key → species entry)]] - document - [[Git]]/faune-autour_13.html
- [[Mode Explorer Autour — list all animal observations in GPS radius by period]] - document - faune-autour.md
- [[Mode Par Espèce — search observations by species name (FR or Latin)]] - document - faune-autour.md
- [[Rationale 3-step species name resolution — GBIF speciesmatch poor at French vernacular names; local dict + vernacularName endpoint + strict fallback]] - document - API_pour_observations_be.md
- [[Rationale WKT bounding box used instead of geoDistance — geoDistance only available for GBIF download API, not real-time search]] - document - API_pour_observations_be.md
- [[bboxWkt() — WKT polygon from latlon + radius (km)]] - document - [[Git]]/faune-autour_13.html
- [[doExplore() — async function GBIF kingdom Animalia query by WKT bbox + period]] - document - [[Git]]/faune-autour_13.html
- [[doSearch() — async function 3-step name resolution + GBIF occurrence fetch]] - document - [[Git]]/faune-autour_13.html
- [[gpsInit() — CoreLocation GPS via navigator.geolocation, fallback Brussels simulation]] - document - [[Git]]/faune-autour_13.html

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Species_Search_&_Geolocation_Logic
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_GBIF Data Sources & APIs]]
- 3 edges to [[_COMMUNITY_PWA App & Deployment]]

## Top bridge nodes
- [[doSearch() — async function 3-step name resolution + GBIF occurrence fetch]] - degree 7, connects to 1 community
- [[doExplore() — async function GBIF kingdom Animalia query by WKT bbox + period]] - degree 4, connects to 1 community
- [[DICT_INDEX — bidirectional JS index (lowercase key → species entry)]] - degree 2, connects to 1 community
- [[Mode Explorer Autour — list all animal observations in GPS radius by period]] - degree 2, connects to 1 community
- [[Mode Par Espèce — search observations by species name (FR or Latin)]] - degree 2, connects to 1 community