from dagster import sensor, RunRequest
from dagster.core.definitions.decorators.sensor import pipeline_failure_sensor
from dagster.core.definitions.pipeline_sensor import PipelineFailureSensorContext
from dagster.core.storage.pipeline_run import PipelineRunsFilter
from dagster.utils import merge_dicts
from dagster_github import github_resource
from dagster import repository

@sensor(pipeline_name="my_pipeline")
def my_github_sensor(context):
    github = context.resources.github

    # replace "aniltolwani/dagster-cloud-test" with your repo
    result = github.get("/repos/aniltolwani/dagster-cloud-test/pulls")

    for pr in result:
        yield RunRequest(run_key=pr["id"], run_config={})
