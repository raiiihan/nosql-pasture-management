from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_get_fields_returns_list():
    resp = client.get('/api/fields')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # Should have at least one field (sample fallback)
    assert len(data) >= 1
    # Each field should have expected keys
    for f in data:
        assert 'name' in f
        assert 'boundary' in f


def test_get_single_field_and_timeseries():
    # single field
    fid = 'field_1'
    resp = client.get(f'/api/fields/{fid}')
    assert resp.status_code == 200
    f = resp.json()
    assert isinstance(f, dict)
    assert f.get('name') is not None

    # timeseries
    resp2 = client.get(f'/api/fields/{fid}/timeseries?periods=12')
    assert resp2.status_code == 200
    ts = resp2.json()
    assert isinstance(ts, list)
    # entries should have metric_type and metric_value
    if len(ts) > 0:
        assert 'metric_type' in ts[0]
        assert 'metric_value' in ts[0]