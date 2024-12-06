<div align="center">
  <img src="./logo.png" alt="Hisar Logo" width="200">
  <h1>Hisar</h1>
  <p>A Load Testing Tool</p>
  <a href="https://github.com/walidsa3d/actions/workflows/test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/walidsa3d/hisar/test.yml?branch=main&style=flat-square" alt="Test Status">
  </a>
  <a href="https://github.com/walidsa3d/hisar/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/walidsa3d/hisar?style=flat-square" alt="License">
  </a>
</div>

Hisar is a fast Python-based load testing tool designed to test the performance and robustness of your APIs and web applications. With `Hisar`, simulate thousands of requests and evaluate system behavior under stress.

## ✨ Features

- **Easy to Use**: Simple, intuitive command-line interface for quick load tests.
- **Highly Scalable**: Test thousands of concurrent users.
- **Real-Time Metrics**: View request success rates, latency, and throughput.
- **Customizable**: Set custom headers, payloads, and authentication.
- **Multi-Protocol Support**: HTTP/HTTPS, WebSocket, gRPC, and more.
- **Integration Ready**: CI/CD integration for automated performance testing.
- **Detailed Reporting**: Generate performance reports in CSV, JSON, or HTML formats.

## 🚀 Quick Start

### Installation

You can install `Hisar` via pip:

```bash
pip install hisar
```

### Basic Usage

Run a basic load test with a specified number of users and request rate:

```bash
hisar -u 100 -n 10 --url https://example.com/api
```

- `-u`: Number of concurrent users.
- `-n`: Requests per second.
- `--url`: The target URL to test.

### Advanced Usage

Customize headers, payloads, and authentication for more complex tests:

```bash
hisar -u 500 -n 50 \
  --headers '{"Authorization": "Bearer YOUR_TOKEN"}' \
  --data '{"key": "value"}' \
  https://example.com/api
```

## 📋 Generate Reports

Generate a detailed report after the test:

```bash
hisar -r html --output report.html https://example.com/api
```

- Supported formats: `csv`, `json`, `html`.

## 🛠️ Configuration Options

`Hisar` offers a wide range of configuration options:

- **Concurrency**: Number of concurrent users.
- **Request Rate**: Number of requests per second.
- **Timeout**: Set request timeout.
- **Authentication**: Support for OAuth, Basic Auth, etc.
- **Payloads**: Support for JSON, form-data, and more.
- **Custom Headers**: Add custom request headers.

## 🧪 Example Test Scenarios

### Scenario 1: Simple API Load Test

```bash
hisar -u 200 -n 20 https://api.yourservice.com/endpoint
```

### Scenario 2: WebSocket Test

```bash
hisar -u 100 ws://yourservice.com/socket
```

### Scenario 3: gRPC Test

```bash
hisar -u 50 --grpc https://grpc.yourservice.com/Service/Method
```

## 🎯 Use Cases

- **API Performance Testing**: Test RESTful or gRPC APIs under heavy load.
- **WebSocket Testing**: Simulate real-time connections at scale.
- **Stress Testing**: Push your service to its limits and identify breaking points.
- **Automated Testing**: Integrate into CI/CD pipelines to run automated performance tests.


## 💻 Contributing

We welcome contributions from the community! If you want to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

See the [CONTRIBUTING.md](https://github.com/walidsa3d/hisar/blob/main/CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/walidsa3d/hisar/blob/main/LICENSE) file for more details.
