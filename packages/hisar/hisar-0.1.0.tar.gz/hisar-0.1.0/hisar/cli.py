import asyncio
import click
from rich.console import Console
from hisar.main import LoadTester
import uvloop
from .ws import WebSocketLoadTester

console = Console()


@click.command()
@click.option("--url", required=True, help="The URL to load test")
@click.option("-n", "--requests", default=100, help="Number of requests to make")
@click.option("-u", "--concurrency", default=10, help="Number of concurrent requests")
@click.option(
    "-r",
    "--report-format",
    type=click.Choice(["json", "csv", "html"], case_sensitive=False),
    help="Report format",
)
def main(url: str, requests: int, concurrency: int, report_format: str):
    """A simple load testing tool for APIs and websites."""
    console.print(f"[bold]LoadBlast[/bold] - Load Testing Tool")
    console.print(f"Target URL: {url}")
    console.print(f"Number of requests: {requests}")
    console.print(f"Concurrency: {concurrency}")

    load_tester = LoadTester(url, requests, concurrency)

    uvloop.install()
    asyncio.run(load_tester.run())

    load_tester.display()
    if report_format:
        load_tester.generate_report(report_format, "report")

@click.command()
@click.option('--url', required=True, help='The WebSocket URL to test (ws:// or wss://)')
@click.option('--clients', default=10, help='Number of WebSocket clients')
@click.option('--messages', default=10, help='Number of messages per client')
@click.option('--message', default='ping', help='Message to send')
@click.option('--interval', default=1.0, help='Interval between messages in seconds')
@click.option('--timeout', default=30.0, help='Connection timeout in seconds')
@click.option('--report-format', type=click.Choice(['json', 'csv', 'html'], case_sensitive=False), help='Report format')
@click.option('--report-output', help='Output file for the report')
def websocket(url, clients, messages, message, interval, timeout, report_format, report_output):
    """Run WebSocket load tests."""
    console.print(f"[bold]LoadBlast[/bold] - WebSocket Load Testing Tool")
    console.print(f"Target URL: {url}")
    console.print(f"Number of clients: {clients}")
    console.print(f"Messages per client: {messages}")
    console.print(f"Message interval: {interval} seconds")
    console.print(f"Timeout: {timeout} seconds")

    tester = WebSocketLoadTester(
        uri=url,
        num_clients=clients,
        messages_per_client=messages,
        message=message,
        message_interval=interval,
        timeout=timeout
    )

    uvloop.install()
    asyncio.run(tester.run())

    tester.print_results()

    if report_format and report_output:
        tester.generate_report(report_format, report_output)

if __name__ == "__main__":
    main()
