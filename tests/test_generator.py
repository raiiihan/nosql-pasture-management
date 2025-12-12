from src.generator import generate_field, generate_sensor_series


def test_generate_field():
    f = generate_field('field_test', 'farm_test', (10.0, 55.0))
    assert f['_id'] == 'field_test'
    assert 'boundary' in f


def test_generate_series_length():
    rows = generate_sensor_series(field_id='field_test', periods=10, freq_minutes=60)
    # 4 sensors per timestamp
    assert len(rows) == 10 * 4
