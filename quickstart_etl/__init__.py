from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from . import assets
from .sensors.github import make_github_prs_updated_sensor

# Define your job
job = define_asset_job(name="all_assets_job")


# Define your sensor
github_prs_updated_sensor = make_github_prs_updated_sensor(job)

# Add your assets, schedules, and sensors to your Definitions
defs = Definitions(
    assets=load_assets_from_package_module(assets),
    sensors=[github_prs_updated_sensor],
)
# hey lol
