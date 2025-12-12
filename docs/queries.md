# Query examples

This file contains example queries (CQL, MongoDB, Redis, Cypher) and explanations.

MongoDB: find fields within 5 km of a point with low NDVI

```
db.fields.aggregate([
  { $geoNear: { near: { type: "Point", coordinates: [lng, lat] }, distanceField: "dist", maxDistance: 5000 } },
  { $match: { "latest_metrics.ndvi": { $lt: 0.4 } } },
  { $project: { name:1, "latest_metrics.ndvi":1 } }
])
```

Cassandra: sample time-range query for average grass_height last 30 days

```
SELECT sensor_ts, metric_value FROM sensor_data_by_field
WHERE field_id='field_01' AND metric_type='grass_height'
AND sensor_ts >= minTime AND sensor_ts <= maxTime
;
```

Redis: push alert when soil moisture low

```
HSET field:field_01 latest_soil_moisture 9.2
XADD alerts * field field_01 type moisture value 9.2
```

Neo4j: find fields sharing a farmer and same treatment in last year

```
MATCH (f1:Field)-[:OWNED_BY]->(farmer:Farmer)<-[:OWNED_BY]-(f2:Field)
MATCH (f1)-[:HAS_TREATMENT]->(t:Treatment)<-[:HAS_TREATMENT]-(f2)
WHERE t.date > date() - duration({days:365})
RETURN f1.id, f2.id, t.type
```
