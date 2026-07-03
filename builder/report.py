from pathlib import Path
from datetime import datetime

def write_report(df, config):

    report_dir = Path("builder/reports")
    report_dir.mkdir(exist_ok=True)

    network = config["network"].lower()

    report = report_dir / f"{network}_validation.md"

    report.write_text(
f"""# {config['display_name']} Validation

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Knowledgebase: `{config["knowledgebase"]}`


| Check | Value |
|-------|------:|
| Stations | {len(df)} |
| Duplicate CRS | {df.duplicated('crs').sum()} |
| Missing CRS | {df['crs'].isna().sum()} |
| Missing Latitude | {df['latitude'].isna().sum()} |
| Missing Longitude | {df['longitude'].isna().sum()} |
| Missing NLC | {df['nlc'].eq('').sum()} |
| Missing Slug | {df['slug'].eq('').sum()} |
""",
        encoding="utf-8"
    )