# File Index Dashboard Search Design

Date: 2026-05-16
Scope: Add an elegant `file_index` search block to `JCH_Inbox/01_DASHBOARDS/hub.html`

## Goal

Expose `file_index` directly in the dashboard so JCH can:

- search files globally by keyword
- narrow results by project and component
- open the file directly as the primary action
- open the parent folder as the secondary action

The block should feel like part of the supervision hub, not a separate app.

## Recommended Approach

Embed a compact search block directly in `hub.html`, backed by a small JSON endpoint in `scripts/dashboard_server.py`.

This is preferred over a separate page or slide-out panel because:

- it minimizes navigation friction for a frequent action
- it fits the hub's role as the supervision entry point
- it keeps the UI elegant through restraint rather than extra mechanics

## User Experience

### Placement

Add the block as a first-class dashboard section in the hub, above the projects strip or between pilotage and project portfolio.

Rationale:

- important enough to be visible
- not so dominant that it competes with the core command panel

### Inputs

- Search field: `Retrouver un fichier PKA`
- Project filter: dropdown, default `Tous les projets`
- Component filter: dropdown, default `Tous les composants`

### Results

Each result row shows:

- filename
- project key
- component when available
- short readable path
- category in a subdued label

Each result row provides:

- primary action: open file
- secondary action: open parent folder

### Behavior

- No query on empty input
- Query starts only after a short minimum input length
- Project filter narrows both results and available component choices
- Component filter further narrows results
- Results sorted by backend relevance first, then stable alphabetic order
- Empty state text: `Aucun fichier correspondant`

## Data Flow

### Backend

Add an endpoint in `scripts/dashboard_server.py`, for example:

- `GET /api/file-index/search?q=<query>&project_key=<key>&component=<component>&limit=<n>`

The endpoint delegates to `scripts/rebuild_file_index.py` search functionality and returns JSON rows containing:

- `filename`
- `file_path`
- `project_key`
- `component`
- `category`

Optional helper endpoints if needed:

- `GET /api/file-index/projects`
- `GET /api/file-index/components?project_key=<key>`

But these should be avoided initially unless the UI really needs them.

### Frontend

`hub.html` adds:

- one search block section
- a small JS controller for debounced fetches
- dynamic rendering of results
- click handlers for file open and folder open actions

## Actions

### Primary Action

Open the file itself.

This is the default because the user is searching for a concrete object, not a container.

### Secondary Action

Open the parent folder.

This preserves the ability to inspect context and continue manual organization.

## Error Handling

- failed search request: show a quiet inline error state, not an alert
- no results: show empty state
- malformed rows: ignore safely and continue rendering remaining rows

## Testing

### Backend

- endpoint returns JSON with expected fields
- query filtering by `project_key` works
- query filtering by `component` works
- empty query returns no result set or empty list

### Frontend

- typing a query renders results
- selecting a project reduces result set
- selecting a component reduces result set further
- primary and secondary actions map to the correct target

## Constraints

- Keep the block visually compact
- Avoid turning the hub into a file manager
- Do not add advanced search syntax in v1
- Do not move search to a dedicated page in v1

## Out of Scope

- full-text preview inside the dashboard
- saved searches
- ranking customization UI
- multi-select bulk actions
- pagination-heavy result explorer

## Final Recommendation

Build v1 as a compact integrated block in `hub.html` with:

- keyword search first
- project and component filters second
- direct file open as primary action
- parent folder open as secondary action

This matches the dashboard's supervision role and gives the cleanest path from question to file.
