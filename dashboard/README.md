# Dashboard mockup

This folder contains mockups and notes for a dashboard: map of fields, time-series charts, alerts table.

Widgets and data sources:
- Map: fields polygon from MongoDB (`fields` collection). Refresh: every 5 minutes.
- Time-series charts: latest metrics from Redis for near-realtime; historical from Cassandra for long-term.
- Alerts: Redis Stream `alerts` (push) and Neo4j events for resolved history.

Example Mermaid (map-level):

```mermaid
flowchart LR
  A[Ingestion] --> B[Cassandra (telemetry)]
  A --> C[MongoDB (metadata)]
  B --> D[Aggregator] --> E[Redis (latest)]
  D --> F[Neo4j (events)]
  E --> Dashboard
  C --> Dashboard
  F --> Dashboard
```
