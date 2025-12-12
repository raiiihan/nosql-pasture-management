"""Data generator for pasture sensors, farmer records, and NDVI series.

This CLI produces JSON lines to stdout or a file. It's intentionally lightweight and
has a `--dry-run` style default so the rest of the scaffold can be explored without DBs.
"""
import json
import math
import random
from datetime import datetime, timedelta
import click


def generate_field(field_id="field_01", farm_id="farm_123", center=(0.0,0.0)):
    lng, lat = center
    # Simple square polygon around center
    delta = 0.01
    polygon = [ [lng-delta, lat-delta], [lng+delta, lat-delta], [lng+delta, lat+delta], [lng-delta, lat+delta], [lng-delta, lat-delta] ]
    doc = {
        "_id": field_id,
        "farm_id": farm_id,
        "name": f"Pasture {field_id}",
        "boundary": { "type":"Polygon", "coordinates": [polygon] },
        "soil_type": random.choice(["loam","sandy loam","clay"]),
        "establishment_date": "2018-04-10",
        "latest_metrics": { "ndvi": round(random.uniform(0.35,0.85),3), "soil_moisture": round(random.uniform(8,30),2), "grass_height_cm": round(random.uniform(4,30),2) },
        "notes": []
    }
    return doc


def generate_sensor_series(field_id="field_01", start=None, periods=48, freq_minutes=60):
    if start is None:
        start = datetime.utcnow()
    rows = []
    for i in range(periods):
        ts = start - timedelta(minutes=i*freq_minutes)
        for sensor in ["soil_moisture","ndvi","air_temp","grass_height"]:
            value = None
            if sensor == "soil_moisture":
                value = round(10 + 5*math.sin(i/10.0) + random.uniform(-1,1), 2)
            elif sensor == "ndvi":
                value = round(0.5 + 0.1*math.cos(i/20.0) + random.uniform(-0.05,0.05), 3)
            elif sensor == "air_temp":
                value = round(15 + 10*math.sin(i/24.0) + random.uniform(-2,2), 2)
            elif sensor == "grass_height":
                value = round(6 + 0.05*i + random.uniform(-1,1), 2)
            rows.append({
                "field_id": field_id,
                "sensor_ts": ts.isoformat(),
                "sensor_id": f"sensor_{sensor}",
                "metric_type": sensor,
                "metric_value": value,
                "quality_flag": 0
            })
    return rows


@click.group()
def cli():
    pass


@cli.command()
@click.option("--count", default=1, help="Number of fields to generate")
@click.option("--out", default=None, help="Output file (jsonl). Defaults to stdout")
def fields(count, out):
    items = [ generate_field(field_id=f"field_{i+1}", farm_id=f"farm_{(i//5)+1}", center=(0.0 + i*0.01, 0.0+i*0.005)) for i in range(count) ]
    sink = open(out, "w") if out else None
    for it in items:
        text = json.dumps(it)
        if sink:
            sink.write(text + "\n")
        else:
            click.echo(text)
    if sink:
        sink.close()


@cli.command()
@click.option("--field-id", default="field_1")
@click.option("--periods", default=48)
@click.option("--out", default=None)
def sensors(field_id, periods, out):
    rows = generate_sensor_series(field_id=field_id, periods=periods)
    sink = open(out, "w") if out else None
    for r in rows:
        text = json.dumps(r)
        if sink:
            sink.write(text + "\n")
        else:
            click.echo(text)
    if sink:
        sink.close()


if __name__ == '__main__':
    cli()
