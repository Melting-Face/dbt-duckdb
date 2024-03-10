import os
from pathlib import Path

from cosmos import ExecutionConfig, ProfileConfig, ProjectConfig

profile_config = ProfileConfig(
    profile_name="warehouse",
    target_name="dev",
)
dbt_executable_path = f"{os.environ['HOME']}/.local/bin/dbt"
project_dir = Path(f"{os.environ['HOME']}/dags/dbt/warehouse")
project_config = ProjectConfig(project_dir)
execution_config = ExecutionConfig(dbt_executable_path)
