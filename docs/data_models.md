# Data models for NoSQL Pasture Management

This document summarizes the recommended data models for each NoSQL system used in the project and rationale.

MongoDB (document + geospatial)
- Collections: `farms`, `fields`, `farmer_profiles`, `treatment_events`
- Example `fields` document:

```
{
  "_id": "field_01",
  "farm_id": "farm_123",
  "name": "North Pasture",
  "boundary": { "type": "Polygon", "coordinates": [ [ [lng, lat], ... ] ] },
  "soil_type": "loam",
  "establishment_date": "2018-04-10",
  "latest_metrics": { "ndvi": 0.72, "soil_moisture": 12.3, "grass_height_cm": 8.2 },
  "notes": []
}
```

- Indexing: create a `2dsphere` index on `boundary` for geo queries. Index `farm_id` and `latest_metrics.ndvi` for queries.
- Retention: metadata kept indefinitely; events can have a TTL when appropriate.

Cassandra (wide-column for time-series)
- Table: `sensor_data_by_field`
- Example CQL:

```
CREATE TABLE IF NOT EXISTS sensor_data_by_field (
  field_id text,
  sensor_ts timestamp,
  sensor_id text,
  metric_type text,
  metric_value double,
  quality_flag int,
  PRIMARY KEY ((field_id), sensor_ts, sensor_id)
) WITH CLUSTERING ORDER BY (sensor_ts DESC);
```

- Partitioning: partition by `field_id` to keep time-series local per field. Use clustering on `sensor_ts` DESC for recent reads.
- TTL/Compaction: apply TTL on write for very high-frequency raw data (e.g., 90 days) and keep aggregated data elsewhere.

Redis (in-memory real-time)
- Use Redis Hashes for latest aggregated metrics: `field:{field_id}` HSET latest_ndvi 0.72 latest_soil_moisture 12.3
- Streams (`XADD alerts * ...`) or Pub/Sub for alert events. Sorted sets for scheduled maintenance: `maintenance:by_date` ZADD timestamp field_id

Neo4j (knowledge graph)
- Node types: `Field`, `Farm`, `Sensor`, `Farmer`, `Treatment`, `CropSpecies`, `AdvisoryRule`
- Relationship examples:
  - `(Farm)-[:OWNS]->(Field)`
  - `(Field)-[:HAS_SENSOR]->(Sensor)`
  - `(Field)-[:HAS_SPECIES]->(CropSpecies)`
  - `(AdvisoryRule)-[:APPLIES_TO]->(CropSpecies)`

- Use Neo4j for queries linking treatments, farmer networks, and historical events. Create indexes on `Field.id` and `Farm.id`.
