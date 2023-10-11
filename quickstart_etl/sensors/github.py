
import json
import os
from dagster import (
    AssetKey,
    DagsterEventType,
    EventRecordsFilter,
    RunRequest,
    SensorDefinition,
    sensor,
)

def make_github_prs_updated_sensor(job) -> SensorDefinition:
    """Returns a sensor that launches the given job when the GitHub "pull requests" have been updated."""

    @sensor(name=f"{job.name}_on_github_prs_updated", job=job)
    def github_prs_updated_sensor(context):
        cursor = context.cursor if context.cursor else None

        pr_event_records = context.instance.get_event_records(
            EventRecordsFilter(
                event_type=DagsterEventType.ASSET_MATERIALIZATION,
                Asset_key=AssetKey(["github", "core", "pull_requests", os.getenv['REPO_NAME']]),
                after_cursor=cursor,
            ),
            ascending=False,
            limit=1,
        )

        if not pr_event_records:
            return

        yield RunRequest(run_key=None)

        # update the sensor cursor with the latest event cursor
        context.update_cursor(json.dumps({"pull_requests": pr_event_records[0].storage_id}))

    return github_prs_updated_sensor