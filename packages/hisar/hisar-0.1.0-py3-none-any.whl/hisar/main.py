import asyncio
import time
from typing import List, Dict
import httpx
from rich.progress import Progress, TaskID
from rich.console import Console
from rich.table import Table
import statistics
from hisar.utils import USER_AGENTS
import random

console = Console()


class LoadTester:
    def __init__(self, url: str, num_requests: int, concurrency: int):
        self.url = url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.results: List[Dict] = []

    async def make_request(
        self, client: httpx.AsyncClient, progress: Progress, task_id: TaskID
    ) -> None:
        """Make a GET request

        Args:
            client (httpx.AsyncClient): HTTP client instance.
            progress (Progress): progress percent.
            task_id (TaskID): task id
        """
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        start_time = time.time()
        try:
            response = await client.get(
                self.url, headers=headers, timeout=20, follow_redirects=True
            )
            elapsed = time.time() - start_time
            self.results.append(
                {
                    "status_code": response.status_code,
                    "elapsed": elapsed,
                    "success": response.is_success,
                }
            )
        except Exception as e:
            elapsed = time.time() - start_time
            self.results.append(
                {
                    "status_code": None,
                    "elapsed": elapsed,
                    "success": False,
                    "error": str(e),
                }
            )
        progress.update(task_id, advance=1)

    async def run(self) -> None:
        """Run All Tasks."""
        async with httpx.AsyncClient() as client:
            with Progress() as progress:
                task_id = progress.add_task(
                    "[cyan]Making requests...", total=self.num_requests
                )
                tasks = [
                    self.make_request(client, progress, task_id)
                    for _ in range(self.num_requests)
                ]
                await asyncio.gather(*tasks)

    def stats(self) -> Dict:
        """Calculate Statistics

        Returns:
            Dict: Stats Dictionary.
        """
        response_times = [r["elapsed"] for r in self.results]
        successful_requests = sum(1 for r in self.results if r["success"])
        failed_requests = self.num_requests - successful_requests

        return {
            "total_requests": self.num_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "total_time": sum(response_times),
            "min_time": min(response_times),
            "max_time": max(response_times),
            "mean_time": statistics.mean(response_times),
            "median_time": statistics.median(response_times),
            "stdev_time": statistics.stdev(response_times)
            if len(response_times) > 1
            else 0,
            "percentile_50": statistics.median(response_times),
            "percentile_75": statistics.quantiles(response_times, n=4)[2],
            "percentile_90": statistics.quantiles(response_times, n=10)[8],
            "percentile_95": statistics.quantiles(response_times, n=20)[18],
            "percentile_99": statistics.quantiles(response_times, n=100)[98],
        }

    def display(self) -> None:
        """Display Results"""
        stats = self.stats()

        console.print("\n[bold green]Results:[/bold green]")

        summary_table = Table(
            title="Summary", show_header=False, header_style="bold magenta"
        )
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="green")

        summary_table.add_row("Total Requests", str(stats["total_requests"]))
        summary_table.add_row("Successful Requests", str(stats["successful_requests"]))
        summary_table.add_row("Failed Requests", str(stats["failed_requests"]))
        summary_table.add_row("Total Test Time", f"{stats['total_time']:.2f} seconds")

        console.print(summary_table)

        stats_table = Table(
            title="Response Time Stats (in seconds)",
            show_header=True,
            header_style="bold magenta",
        )
        stats_table.add_column("Statistic", style="cyan", no_wrap=True)
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Minimum", f"{stats['min_time']:.4f}")
        stats_table.add_row("Maximum", f"{stats['max_time']:.4f}")
        stats_table.add_row("Mean", f"{stats['mean_time']:.4f}")
        stats_table.add_row("Median", f"{stats['median_time']:.4f}")
        stats_table.add_row("Standard Deviation", f"{stats['stdev_time']:.4f}")

        console.print(stats_table)

        percentile_table = Table(
            title="Response Time Percentiles (in seconds)",
            show_header=True,
            header_style="bold magenta",
        )
        percentile_table.add_column("Percentile", style="cyan", no_wrap=True)
        percentile_table.add_column("Value", style="green")

        percentile_table.add_row("50th (Median)", f"{stats['percentile_50']:.4f}")
        percentile_table.add_row("75th", f"{stats['percentile_75']:.4f}")
        percentile_table.add_row("90th", f"{stats['percentile_90']:.4f}")
        percentile_table.add_row("95th", f"{stats['percentile_95']:.4f}")
        percentile_table.add_row("99th", f"{stats['percentile_99']:.4f}")

        console.print(percentile_table)
