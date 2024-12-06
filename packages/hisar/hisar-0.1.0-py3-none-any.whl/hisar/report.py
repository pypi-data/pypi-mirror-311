import json
import csv
from abc import ABC, abstractmethod
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from jinja2 import Template


class ReportPlugin(ABC):
    @abstractmethod
    def generate(self, stats: Dict, results: List[Dict], output_file: str) -> None:
        pass


class JSONReportPlugin(ReportPlugin):
    def generate(self, stats: Dict, results: List[Dict], output_file: str) -> None:
        data = {"statistics": stats, "results": results}
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"JSON report saved to {output_file}")


class CSVReportPlugin(ReportPlugin):
    def generate(self, stats: Dict, results: List[Dict], output_file: str) -> None:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for key, value in stats.items():
                writer.writerow([key, value])
            writer.writerow([])
            writer.writerow(["Status Code", "Elapsed Time", "Success"])
            for result in results:
                writer.writerow(
                    [
                        result.get("status_code"),
                        result.get("elapsed"),
                        result.get("success"),
                    ]
                )
        print(f"CSV report saved to {output_file}")


class HTMLReportPlugin(ReportPlugin):
    def generate(self, stats: Dict, results: List[Dict], output_file: str) -> None:
        template = Template("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Load Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                h1, h2 { color: #333; }
            </style>
        </head>
        <body>
            <h1>Load Test Report</h1>
            <h2>Statistics</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                {% for key, value in stats.items() %}
                <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
                {% endfor %}
            </table>
            <h2>Results</h2>
            <table>
                <tr><th>Status Code</th><th>Elapsed Time</th><th>Success</th></tr>
                {% for result in results %}
                <tr>
                    <td>{{ result.status_code }}</td>
                    <td>{{ result.elapsed }}</td>
                    <td>{{ result.success }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """)
        html_content = template.render(stats=stats, results=results)
        with open(output_file, "w") as f:
            f.write(html_content)
        print(f"HTML report saved to {output_file}")


def get_plugin(format: str) -> ReportPlugin:
    plugins = {
        "json": JSONReportPlugin(),
        "csv": CSVReportPlugin(),
        "html": HTMLReportPlugin(),
    }
    return plugins.get(format.lower(), JSONReportPlugin())
