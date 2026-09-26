# Frontend Design System: All Projects

One design language, every project wearing it in its own colors. This doc is the source of truth; each project doc references it and adds only what differs.

## The aesthetic in one line

Trading terminal meets Linear: information-dense like a Bloomberg screen, restrained and beautiful like a modern dev tool. Never corporate BI (no gray dashboards, no pie-chart gauges, no logo in every corner).

## Stack (identical across projects)

- Vite + React + TypeScript
- Tailwind CSS + shadcn/ui components
- TanStack Table for data grids (headless: full visual control, our code to show off)
- Recharts for charts
- react-leaflet + marker clustering where maps apply
- lucide-react for icons
- FastAPI (Python) serving SQLite over a small REST layer, one repo per project

## Shared rules

**Theme**
- Dark base always: near-black background (#0a0a0b range), elevated surfaces one step lighter
- ONE accent color per project, used sparingly: primary actions, active states, the number that matters most
- Status colors are semantic and consistent across projects (green success, amber attention, red failure, gray inactive/ghosted)
- Light mode: not a priority; dark-first

**Layout**
- Scoreboard row up top: 3-5 big numbers that answer "how are things right now" at a glance
- Below it: the working surface (grid, queue, or panels) taking most of the viewport
- Charts and trends get their own tab/section; they inform, the grid is where action happens
- Density with breathing room: tight rows in grids, generous padding between sections

**Typography**
- One sans (Inter or Geist), tabular numerals ON for every number column
- Type scale small and disciplined: big numbers earn their size, labels stay quiet

**Components every project reuses**
- StatCard: big number, small label, tiny trend indicator
- DataGrid: sortable, filterable, faceted filters in a toolbar, row click opens a detail panel
- ActionQueue: prioritized list of "do this next" items
- RunPanel: scheduled jobs view (next run, last run, success/fail, audit log, manual trigger button)
- ChartPanel: titled chart with a one-line takeaway string under the title
- DetailDrawer: slide-over for a single record, edits inline

**Icons and imagery**
- lucide-react icons everywhere for UI chrome
- Project-themed icons/imagery welcome where they stay aesthetic: an icon in the header, empty states, favicons. Theme flavors the room; it never clutters the data

## Per-project identity

| Project | Accent | Theme flavor | Doc |
|---|---|---|---|
| Job Opportunity Tracker | electric blue (or your pick) | clean, professional, zero whimsy: recruiters may see it | docs/SPEC.md |
| NHL Betting Engine | rink red or ice cyan | hockey: puck icon, subtle rink texture in empty states | nhl-dashboard-wishlist.md |
| XLNT / Ableton MCP | neon magenta or acid green | studio: waveform motifs, transport-control iconography | ableton-frontend-wishlist.md |

## Process per project

1. Wishlist doc (functionality + metrics) lives in that project
2. Layout mockup first, react to it before wiring data
3. Build on the shared component set; diverge only where the domain demands it
