"""info CLI command implementation."""
# dem/cli/command/info_cmd.py

from dem.core.tool_images import ToolImages
from dem.core.dev_env_setup import DevEnvLocal, DevEnvOrg, DevEnvLocalSetup, DevEnvOrgSetup
from dem.cli.console import stdout, stderr
from rich.table import Table

image_status_messages = {
    ToolImages.NOT_AVAILABLE: "[red]Error: Image is not available.[/]",
    ToolImages.LOCAL_ONLY: "Image is available locally.",
    ToolImages.REGISTRY_ONLY: "Image is available in the registry.",
    ToolImages.LOCAL_AND_REGISTRY: "Image is available locally and in the registry.",
}

def print_info(dev_env: (DevEnvLocal | DevEnvOrg)) -> None:
    tool_info_table = Table()
    tool_info_table.add_column("Type")
    tool_info_table.add_column("Image")
    tool_info_table.add_column("Status")
    for tool in dev_env.tools:
        tool_info_table.add_row(tool["type"], tool["image_name"] + ':' + tool["image_version"],
                                image_status_messages[tool["image_status"]])
    stdout.print(tool_info_table)

def execute(arg_dev_env_name: str) -> None:
    dev_env_setup = DevEnvLocalSetup()
    dev_env = dev_env_setup.get_dev_env_by_name(arg_dev_env_name)

    if dev_env is None:
        dev_env_setup = DevEnvOrgSetup()
        dev_env = dev_env_setup.get_dev_env_by_name(arg_dev_env_name)

    if dev_env is None:
        stderr.print("[red]Error: Unknown Development Environment: " + arg_dev_env_name + "[/]")
        return
    else:
        dev_env.check_image_availability(dev_env_setup.tool_images)
        print_info(dev_env)