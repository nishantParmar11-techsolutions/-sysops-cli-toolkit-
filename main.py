# ==============================================================================
# SysOps CLI Toolkit - Enterprise Automation & Monitoring Interface
# ==============================================================================

import json
import typer
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    help="Enterprise SysOps CLI Toolkit for server monitoring and webhook automation.",
    add_completion=False,
)
console = Console()


@app.command("health-check")
def check_server_health(
    url: str = typer.Option(
        "http://localhost:8000/health",
        "--url",
        "-u",
        help="Target service health URL to audit.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output raw JSON for machine-to-machine automation pipelines.",
    ),
    timeout: int = typer.Option(
        5,
        "--timeout",
        "-t",
        help="HTTP request timeout in seconds.",
    ),
) -> None:
    """Pings a target microservice or webhook middleware to verify liveness and stability."""
    if not json_output:
        console.print(f"[bold cyan]🔍 Pinging target endpoint:[/bold cyan] {url}")
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if json_output:
            output_data = {
                "url": url,
                "status_code": response.status_code,
                "is_healthy": response.status_code == 200,
                "response": response.json() if response.content else {}
            }
            typer.echo(json.dumps(output_data, indent=2))
        else:
            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    data = {"raw_text": response.text}
                
                console.print(
                    Panel(
                        f"[bold green]✔ SUCCESS: Service is Healthy![/bold green]\n\n[dim]Status Code:[/dim] {response.status_code}\n[dim]Details:[/dim] {data}",
                        title="Health Audit Passed",
                        border_style="green",
                    )
                )
            else:
                console.print(
                    Panel(
                        f"[bold yellow]⚠️ WARNING: Received unhealthy status code {response.status_code}[/bold yellow]",
                        title="Health Audit Warning",
                        border_style="yellow",
                    )
                )
                raise typer.Exit(code=1)

    except requests.exceptions.RequestException as e:
        if json_output:
            typer.echo(json.dumps({"url": url, "error": str(e), "is_healthy": False}, indent=2))
        else:
            console.print(
                Panel(
                    f"[bold red]❌ ERROR: Connection failed to target.\n{str(e)}[/bold red]",
                    title="Health Audit Failure",
                    border_style="red",
                )
            )
        raise typer.Exit(code=1)


@app.command("system-info")
def show_system_info(
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Output telemetry in JSON format."
    )
) -> None:
    """Displays local developer environment telemetry and tool configurations."""
    telemetry = {
        "cli_engine": "Typer (v0.12.3)",
        "terminal_styling": "Rich",
        "http_client": "Requests",
        "execution_mode": "Active Production"
    }

    if json_output:
        typer.echo(json.dumps(telemetry, indent=2))
    else:
        table = Table(title="SysOps Toolkit Environment Overview", border_style="blue")
        table.add_column("Component", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")

        for key, val in telemetry.items():
            table.add_row(key.replace("_", " ").title(), val)

        console.print(table)


if __name__ == "__main__":
    app()
              
