# Enable Log Streaming

This library provides a Python function to enable log streaming for AWS Elastic Beanstalk environments and set CloudWatch log retention.

## Installation

```bash
pip install enable-log-streaming

from enable_log_streaming.enable_log_streaming import enable_log_streaming

response = enable_log_streaming("your-environment-name", retention_days=7)
print(response)


python -m enable_log_streaming.enable_log_streaming your-environment-name --retention_days 7



---

### Step 5: Build and Publish the Package

1. **Install Build Tools**:
   ```bash
   pip install build twine
