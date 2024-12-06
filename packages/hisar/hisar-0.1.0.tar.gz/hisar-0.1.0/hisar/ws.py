# loadblast/ws_tester.py
import asyncio
import time
import random
from typing import List, Dict, Union, Optional, Callable
import websockets
from websockets.client import WebSocketClientProtocol
from rich.progress import Progress, TaskID
from rich.console import Console
from rich.table import Table
import statistics
from .plugins import get_plugin

console = Console()

class WebSocketClient:
    def __init__(self,
                 uri: str,
                 message: Union[str, bytes],
                 message_interval: float = 1.0,
                 timeout: float = 30.0,
                 on_message: Optional[Callable] = None):
        self.uri = uri
        self.message = message
        self.message_interval = message_interval
        self.timeout = timeout
        self.on_message = on_message
        self.connected = False
        self.messages_sent = 0
        self.messages_received = 0
        self.latencies: List[float] = []
        self.connection_time: Optional[float] = None
        self.last_message_time: Optional[float] = None
        self.errors: List[str] = []

    async def connect(self) -> None:
        start_time = time.time()
        try:
            self.ws = await websockets.connect(
                self.uri,
                timeout=self.timeout,
                ping_interval=20,
                ping_timeout=20
            )
            self.connection_time = time.time() - start_time
            self.connected = True
        except Exception as e:
            self.errors.append(f"Connection error: {str(e)}")
            raise

    async def send_message(self) -> None:
        if not self.connected:
            return

        try:
            start_time = time.time()
            await self.ws.send(self.message)
            self.messages_sent += 1
            self.last_message_time = start_time
        except Exception as e:
            self.errors.append(f"Send error: {str(e)}")
            self.connected = False
            raise

    async def receive_message(self) -> None:
        if not self.connected:
            return

        try:
            message = await self.ws.recv()
            if self.last_message_time is not None:
                latency = time.time() - self.last_message_time
                self.latencies.append(latency)
            self.messages_received += 1

            if self.on_message:
                await self.on_message(message)
        except Exception as e:
            self.errors.append(f"Receive error: {str(e)}")
            self.connected = False
            raise

    async def close(self) -> None:
        if self.connected:
            await self.ws.close()
            self.connected = False

class WebSocketLoadTester:
    def __init__(self,
                 uri: str,
                 num_clients: int,
                 messages_per_client: int,
                 message: Union[str, bytes] = "ping",
                 message_interval: float = 1.0,
                 timeout: float = 30.0,
                 on_message: Optional[Callable] = None):
        self.uri = uri
        self.num_clients = num_clients
        self.messages_per_client = messages_per_client
        self.message = message
        self.message_interval = message_interval
        self.timeout = timeout
        self.on_message = on_message
        self.clients: List[WebSocketClient] = []
        self.results: List[Dict] = []

    async def run_client(self, client: WebSocketClient, progress: Progress, task_id: TaskID) -> None:
        try:
            await client.connect()

            for _ in range(self.messages_per_client):
                await client.send_message()
                await client.receive_message()
                await asyncio.sleep(self.message_interval)
                progress.update(task_id, advance=1)

        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
        finally:
            await client.close()
            self.results.append({
                "connection_time": client.connection_time,
                "messages_sent": client.messages_sent,
                "messages_received": client.messages_received,
                "latencies": client.latencies,
                "errors": client.errors
            })

    async def run(self) -> None:
        total_messages = self.num_clients * self.messages_per_client

        with Progress() as progress:
            task_id = progress.add_task("[cyan]Running WebSocket tests...", total=total_messages)

            self.clients = [
                WebSocketClient(
                    self.uri,
                    self.message,
                    self.message_interval,
                    self.timeout,
                    self.on_message
                )
                for _ in range(self.num_clients)
            ]

            tasks = [self.run_client(client, progress, task_id) for client in self.clients]
            await asyncio.gather(*tasks)

    def calculate_statistics(self) -> Dict:
        all_latencies = []
        total_messages_sent = 0
        total_messages_received = 0
        connection_times = []
        total_errors = 0

        for result in self.results:
            all_latencies.extend(result["latencies"])
            total_messages_sent += result["messages_sent"]
            total_messages_received += result["messages_received"]
            if result["connection_time"]:
                connection_times.append(result["connection_time"])
            total_errors += len(result["errors"])

        if not all_latencies:
            return {
                "error": "No latency data available"
            }

        return {
            "total_clients": self.num_clients,
            "total_messages_sent": total_messages_sent,
            "total_messages_received": total_messages_received,
            "total_errors": total_errors,
            "avg_connection_time": statistics.mean(connection_times) if connection_times else 0,
            "min_latency": min(all_latencies),
            "max_latency": max(all_latencies),
            "mean_latency": statistics.mean(all_latencies),
            "median_latency": statistics.median(all_latencies),
            "stdev_latency": statistics.stdev(all_latencies) if len(all_latencies) > 1 else 0,
            "percentile_50": statistics.median(all_latencies),
            "percentile_75": statistics.quantiles(all_latencies, n=4)[2],
            "percentile_90": statistics.quantiles(all_latencies, n=10)[8],
            "percentile_95": statistics.quantiles(all_latencies, n=20)[18],
            "percentile_99": statistics.quantiles(all_latencies, n=100)[98],
        }

    def print_results(self) -> None:
        stats = self.calculate_statistics()

        if "error" in stats:
            console.print(f"\n[bold red]Error:[/bold red] {stats['error']}")
            return

        console.print("\n[bold green]WebSocket Load Test Results:[/bold green]")

        summary_table = Table(title="Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        summary_table.add_row("Total Clients", str(stats["total_clients"]))
        summary_table.add_row("Messages Sent", str(stats["total_messages_sent"]))
        summary_table.add_row("Messages Received", str(stats["total_messages_received"]))
        summary_table.add_row("Total Errors", str(stats["total_errors"]))
        summary_table.add_row("Average Connection Time", f"{stats['avg_connection_time']:.4f} seconds")

        console.print(summary_table)

        latency_table = Table(title="Latency Statistics (in seconds)", show_header=True, header_style="bold magenta")
        latency_table.add_column("Statistic", style="cyan", no_wrap=True)
        latency_table.add_column("Value", style="green")

        latency_table.add_row("Minimum", f"{stats['min_latency']:.4f}")
        latency_table.add_row("Maximum", f"{stats['max_latency']:.4f}")
        latency_table.add_row("Mean", f"{stats['mean_latency']:.4f}")
        latency_table.add_row("Median", f"{stats['median_latency']:.4f}")
        latency_table.add_row("Standard Deviation", f"{stats['stdev_latency']:.4f}")

        console.print(latency_table)

        percentile_table = Table(title="Latency Percentiles (in seconds)", show_header=True, header_style="bold magenta")
        percentile_table.add_column("Percentile", style="cyan", no_wrap=True)
        percentile_table.add_column("Value", style="green")

        percentile_table.add_row("50th (Median)", f"{stats['percentile_50']:.4f}")
        percentile_table.add_row("75th", f"{stats['percentile_75']:.4f}")
        percentile_table.add_row("90th", f"{stats['percentile_90']:.4f}")
        percentile_table.add_row("95th", f"{stats['percentile_95']:.4f}")
        percentile_table.add_row("99th", f"{stats['percentile_99']:.4f}")

        console.print(percentile_table)

    def generate_report(self, format: str, output_file: str) -> None:
        stats = self.calculate_statistics()
        plugin = get_plugin(format)
        plugin.generate(stats, self.results, output_file)
