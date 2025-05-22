# 🖥️ System Monitor Agent

Welcome to the **System Monitor Agent**! This project is a Python-based application that monitors system resources and generates a comprehensive health report. Built using the `google.adk` framework, it leverages a combination of parallel and sequential agent pipelines to gather and synthesize CPU, memory, and disk information efficiently.

---

## 🚀 Project Overview

The project implements a system monitoring pipeline with the following components:

- **CPU Info Agent**: Gathers and analyzes CPU data (e.g., core count, usage).
- **Disk Info Agent**: Collects disk usage statistics (e.g., total, used, free space).
- **Memory Info Agent**: Retrieves memory usage details (e.g., total, available memory).
- **Synthesizer Agent**: Combines the data into a well-formatted system health report.

The system uses a `ParallelAgent` to collect data concurrently from the CPU, disk, and memory agents, followed by a `SequentialAgent` to synthesize the data into a final report. It highlights performance concerns and provides actionable recommendations.

---

## 📂 Project Structure

The project is organized under the `Chapter-10` directory with the following structure:

```
Chapter-10/
├── system_monitor_agent/        # Main system monitor agent module
│   ├── subagents/              # Sub-agents for specific tasks
│   │   ├── cpu_info_agent/     # CPU Info Agent module
│   │   │   ├── __init__.py     # Initializes the module
│   │   │   ├── agent.py        # Implements the agent for CPU data
│   │   │   └── tools.py        # Defines the tool for gathering CPU info
│   │   ├── disk_info_agent/    # Disk Info Agent module
│   │   │   ├── __init__.py     # Initializes the module
│   │   │   ├── agent.py        # Implements the agent for disk data
│   │   │   └── tools.py        # Defines the tool for gathering disk info
│   │   ├── memory_info_agent/  # Memory Info Agent module
│   │   │   ├── __init__.py     # Initializes the module
│   │   │   ├── agent.py        # Implements the agent for memory data
│   │   │   └── tools.py        # Defines the tool for gathering memory info
│   │   └── synthesiser_agent/  # Synthesizer Agent module
│   │       ├── __init__.py     # Initializes the module
│   │       └── agent.py        # Implements the agent for report synthesis
│   ├── .env                    # Environment variables (e.g., API keys)
│   ├── __init__.py             # Initializes the module
│   └── agent.py                # Defines the parallel and sequential agent pipeline
```

---

## 🛠️ Code Overview with Examples

### 1. CPU Info Agent
The `cpu_info_agent` collects and analyzes CPU data using the `get_cpu_info` tool.

**Example Code** (from `subagents/cpu_info_agent/tools.py`):
```python
def get_cpu_info() -> Dict[str, Any]:
    try:
        cpu_info = {
            "processor": platform.processor(),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "avg_cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%",
        }
        avg_usage = float(cpu_info["avg_cpu_usage"].strip("%"))
        high_usage = avg_usage > 80
        return {
            "result": cpu_info,
            "stats": {
                "physical_cores": cpu_info["physical_cores"],
                "logical_cores": cpu_info["logical_cores"],
                "avg_usage_percentage": avg_usage,
                "high_usage_alert": high_usage,
            },
            "additional_info": {
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": "High CPU usage detected" if high_usage else None,
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather CPU information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }
```

**Explanation**:
- `get_cpu_info`: Uses `psutil` to gather CPU data like core counts and usage percentages.
- Flags high usage (>80%) and includes metadata like collection timestamp.

**Usage Example**:
The agent might output:
```
CPU Information:
- Processor: x86_64
- Physical Cores: 4
- Logical Cores: 8
- Average CPU Usage: 85.3%
Warning: High CPU usage detected (>80%).
```

---

### 2. Disk Info Agent
The `disk_info_agent` retrieves disk usage statistics using the `get_disk_info` tool.

**Example Code** (from `subagents/disk_info_agent/tools.py`):
```python
def get_disk_info() -> Dict[str, Any]:
    try:
        total, used, free = shutil.disk_usage("/")
        usage_percent = (used / total) * 100
        high_usage = usage_percent > 85
        disk_info = {
            "total_disk_space_gb": round(total / (1024**3), 2),
            "used_disk_space_gb": round(used / (1024**3), 2),
            "free_disk_space_gb": round(free / (1024**3), 2),
            "disk_usage_percentage": f"{usage_percent:.1f}%",
        }
        return {
            "result": disk_info,
            "stats": {
                "total_gb": disk_info["total_disk_space_gb"],
                "used_gb": disk_info["used_disk_space_gb"],
                "free_gb": disk_info["free_disk_space_gb"],
                "usage_percentage": usage_percent,
                "high_usage_alert": high_usage,
            },
            "additional_info": {
                "performance_concern": "High disk usage detected" if high_usage else None,
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather disk information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }
```

**Explanation**:
- `get_disk_info`: Uses `shutil` to collect disk usage data for the root directory.
- Flags high usage (>85%) and structures the data for reporting.

**Usage Example**:
The agent might output:
```
Disk Information:
- Total Space: 500.00 GB
- Used Space: 450.00 GB
- Free Space: 50.00 GB
- Usage Percentage: 90.0%
Warning: High disk usage detected (>85%).
```

---

### 3. Memory Info Agent
The `memory_info_agent` gathers memory usage data using the `get_memory_info` tool.

**Example Code** (from `subagents/memory_info_agent/tools.py`):
```python
def get_memory_info() -> Dict[str, Any]:
    try:
        virtual_mem = psutil.virtual_memory()
        usage_percent = virtual_mem.percent
        high_usage = usage_percent > 85
        memory_info = {
            "total_memory_gb": round(virtual_mem.total / (1024**3), 2),
            "used_memory_gb": round(virtual_mem.used / (1024**3), 2),
            "available_memory_gb": round(virtual_mem.available / (1024**3), 2),
            "memory_usage_percentage": f"{usage_percent:.1f}%",
        }
        return {
            "result": memory_info,
            "stats": {
                "total_gb": memory_info["total_memory_gb"],
                "used_gb": memory_info["used_memory_gb"],
                "available_gb": memory_info["available_memory_gb"],
                "usage_percentage": usage_percent,
                "high_usage_alert": high_usage,
            },
            "additional_info": {
                "performance_concern": "High memory usage detected" if high_usage else None,
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather memory information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }
```

**Explanation**:
- `get_memory_info`: Uses `psutil` to collect memory usage stats.
- Flags high usage (>85%) and prepares data for the report.

**Usage Example**:
The agent might output:
```
Memory Information:
- Total Memory: 16.00 GB
- Used Memory: 12.00 GB
- Available Memory: 4.00 GB
- Usage Percentage: 75.0%
```

---

### 4. Synthesizer Agent
The `synthesiser_agent` combines the data into a comprehensive report.

**Example Code** (from `subagents/synthesiser_agent/agent.py`):
```python
system_report = LlmAgent(
    model='gemini-2.0-flash-001',
    name='SynthesiserAgent',
    instruction="""You are a System Report Synthesizer.

        Your task is to create a comprehensive system health report by combining information from:
        - CPU information: {cpu_info}
        - Memory information: {memory_info}
        - Disk information: {disk_info}

        Create a well-formatted report with:
        1. An executive summary at the top with overall system health status
        2. Sections for each component with their respective information
        3. Recommendations based on any concerning metrics
        """,
    description="Synthesizes all system information into a comprehensive report",
)
```

**Explanation**:
- Takes input from the CPU, disk, and memory agents.
- Formats a markdown report with an executive summary, detailed sections, and recommendations.

**Usage Example**:
The synthesized report might look like:
```
# System Health Report

## Executive Summary
The system is experiencing high disk usage (90.0%), which may impact performance. CPU and memory usage are within acceptable limits.

## CPU Information
- Physical Cores: 4
- Logical Cores: 8
- Average Usage: 85.3%
- Warning: High CPU usage detected (>80%).

## Memory Information
- Total Memory: 16.00 GB
- Used Memory: 12.00 GB
- Usage Percentage: 75.0%

## Disk Information
- Total Space: 500.00 GB
- Used Space: 450.00 GB
- Usage Percentage: 90.0%
- Warning: High disk usage detected (>85%).

## Recommendations
- Address high disk usage by freeing up space or expanding storage capacity.
- Monitor CPU usage and consider optimizing workloads.
```

---

## 📋 Sample Input

You can use the following sample input to trigger the system monitor agent pipeline. This can be used in a client application or runner to request a system health report.

**Sample Input**:
```
Generate a system health report for the current system.
```

**Expected Output**:
The agent will generate a markdown-formatted report as shown in the synthesizer example above, detailing CPU, memory, and disk information along with recommendations.

---

## 🏃 How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Install required packages:
  ```bash
  pip install python-dotenv google-adk psutil
  ```
- Set up a `.env` file in the `system_monitor_agent` directory with necessary API keys (e.g., for `google.adk`).

### Steps to Run
1. Clone the repository or navigate to the `Chapter-10` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If a `requirements.txt` is not present, use the command under Prerequisites.)
3. Navigate to the `system_monitor_agent` directory:
   ```bash
   cd system_monitor_agent
   ```
4. Ensure the `.env` file is configured with required environment variables.
5. Run the agent (requires integration with a runner or client):
   ```bash
   python agent.py
   ```
   **Note**: This project is a pipeline demo and requires a client or runner (e.g., from `google.adk`) to process requests interactively. Use the sample input above to trigger the pipeline.

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

**Built with ❤️ by the xAI Community**
