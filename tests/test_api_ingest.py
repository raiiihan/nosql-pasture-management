from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_ingest_field_and_sensors():
    # Ingest field
    field = {
        "_id": "field_test",
        "farm_id": "farm_test",
        "name": "Test Field",
        "boundary": {"type": "Polygon", "coordinates": [[[0,0],[0,1],[1,1],[1,0],[0,0]]]},
        "latest_metrics": {"ndvi": 0.5}
    }
    resp = client.post('/api/fields', json=field)
    assert resp.status_code in (200, 201)

    # Ingest sensors
    rows = [
        {
            "field_id": "field_test",
            "sensor_ts": "2025-12-10T12:00:00Z",
            "sensor_id": "sensor_sm",
            "metric_type": "soil_moisture",
            "metric_value": 15.0,
            "quality_flag": 0
        }
    ]
    resp2 = client.post('/api/fields/field_test/ingest-sensors', json=rows)
    assert resp2.status_code == 200
    data = resp2.json()
    assert data.get('status') == 'accepted'
    assert data.get('rows') == 1
