"""list CLI command implementation."""
# dem/cli/list_cmd.py

from dem.core import container_engine, dev_env_setup, registry
from dem.core.tool_images import ToolImages
from dem.cli.console import stdout, stderr
from rich.table import Table

(
    DEV_ENV_ORG_NOT_IN_REGISTRY,
    DEV_ENV_ORG_INSTALLED_LOCALLY,
    DEV_ENV_ORG_REAINSTALL,
    DEV_ENV_ORG_READY,
) = range(4)

(
    DEV_ENV_LOCAL_NOT_AVAILABLE,
    DEV_ENV_LOCAL_REINSTALL,
    DEV_ENV_LOCAL_INSTALLED,
) = range(3)

dev_env_org_status_messages = {
    DEV_ENV_ORG_NOT_IN_REGISTRY: "[red]Error: Required image is not available in the registry![/]",
    DEV_ENV_ORG_INSTALLED_LOCALLY: "Installed locally.",
    DEV_ENV_ORG_REAINSTALL: "Incomplete local install. Reinstall needed.",
    DEV_ENV_ORG_READY: "Ready to be installed.",
}

dev_env_local_status_messages = {
    DEV_ENV_LOCAL_NOT_AVAILABLE: "[red]Error: Required image is not available![/]",
    DEV_ENV_LOCAL_REINSTALL: "Incopmlete local install. Reinstall needed.",
    DEV_ENV_LOCAL_INSTALLED: "Installed.",
}

def is_dev_env_org_installed_locally(dev_env_org: dev_env_setup.DevEnvOrg) -> bool:
    dev_env_local_setup_obj = dev_env_setup.DevEnvLocalSetup()
    return dev_env_org.get_local_instance(dev_env_local_setup_obj) is not None

def get_dev_env_status(dev_env: (dev_env_setup.DevEnvLocal | dev_env_setup.DevEnvOrg), 
                       tool_images: ToolImages) -> str:
    image_statuses = dev_env.check_image_availability(tool_images)
    dev_env_status = ""
    if isinstance(dev_env, dev_env_setup.DevEnvOrg):
        if (ToolImages.NOT_AVAILABLE in image_statuses) or (ToolImages.LOCAL_ONLY in image_statuses):
            dev_env_status = dev_env_org_status_messages[DEV_ENV_ORG_NOT_IN_REGISTRY]
        elif (image_statuses.count(ToolImages.LOCAL_AND_REGISTRY) == len(image_statuses)) and \
                (is_dev_env_org_installed_locally(dev_env) == True):
            dev_env_status = dev_env_org_status_messages[DEV_ENV_ORG_INSTALLED_LOCALLY]
        else:
            if (is_dev_env_org_installed_locally(dev_env) == True):
                dev_env_status = dev_env_org_status_messages[DEV_ENV_ORG_REAINSTALL]
            else:
                dev_env_status = dev_env_org_status_messages[DEV_ENV_ORG_READY]
    else:
        if (ToolImages.NOT_AVAILABLE in image_statuses):
            dev_env_status = dev_env_local_status_messages[DEV_ENV_LOCAL_NOT_AVAILABLE]
        elif (ToolImages.REGISTRY_ONLY in image_statuses):
            dev_env_status = dev_env_local_status_messages[DEV_ENV_LOCAL_REINSTALL]
        else:
            dev_env_status = dev_env_local_status_messages[DEV_ENV_LOCAL_INSTALLED]
    return dev_env_status

def list_dev_envs(local: bool, org: bool)-> None:
    dev_env_setup_obj = None
    if ((local == True) and (org == False)):
        dev_env_setup_obj = dev_env_setup.DevEnvLocalSetup()
        if not dev_env_setup_obj.dev_envs:
            stdout.print("[yellow]No installed Development Environments.[/]")
            return
    elif((local == False) and (org == True)):
        dev_env_setup_obj = dev_env_setup.DevEnvOrgSetup()
        if not dev_env_setup_obj.dev_envs:
            stdout.print("[yellow]No Development Environment in your organization.[/]")
            return
    else:
        stderr.print("[red]Error: Invalid options.[/]")
        return

    table = Table()
    table.add_column("Development Environment")
    table.add_column("Status")
    for dev_env in dev_env_setup_obj.dev_envs:
        table.add_row(dev_env.name, get_dev_env_status(dev_env, dev_env_setup_obj.tool_images))

    stdout.print(table)

def list_tool_images(local: bool, org: bool) -> None:
    container_engine_obj = container_engine.ContainerEngine()
    if (local == True) and (org == False):        
        local_images = container_engine_obj.get_local_tool_images()

        table = Table()
        table.add_column("Repository")
        for local_image in local_images:
            table.add_row(local_image)
        stdout.print(table)
    elif (local == False) and (org == True):
        registry_images = registry.list_repos(container_engine_obj)

        table = Table()
        table.add_column("Repository")
        for registry_image in registry_images:
            table.add_row(registry_image)
        stdout.print(table)

def execute(local: bool, org: bool, env: bool, tool: bool) -> None:
    if ((local == True) or (org == True)) and (env == True) and (tool == False):
        list_dev_envs(local, org)
    elif ((local == True) or (org == True)) and (env == False) and (tool == True):
        list_tool_images(local, org)
    else:
        stderr.print(\
"""Usage: dem list [OPTIONS]
Try 'dem list --help' for help.

Error: You need to set the scope and what to list!""")