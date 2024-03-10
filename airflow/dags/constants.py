import os
from pathlib import Path

from cosmos import ExecutionConfig, ProfileConfig, ProjectConfig

dbt_executable_path = f"{os.environ['HOME']}/.local/bin/dbt"
project_dir = Path(f"{os.environ['AIRFLOW_HOME']}/dags/warehouse")
project_config = ProjectConfig(dbt_project_path=project_dir)
execution_config = ExecutionConfig(dbt_executable_path=dbt_executable_path)

profile_config = ProfileConfig(
    profiles_yml_filepath=project_dir / "profiles.yml",
    profile_name="warehouse",
    target_name="dev",
)
