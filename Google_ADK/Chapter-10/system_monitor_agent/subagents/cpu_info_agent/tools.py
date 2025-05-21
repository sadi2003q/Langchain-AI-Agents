import platform
import psutil
import time
from typing import Any, Dict


def get_cpu_info() -> Dict[str, Any]:
    """
    Gather CPU information including core count, usage, and system details.

    :returns:
        Dict[str, Any]: Dictionary with CPU information structured for ADK
    """
    try:
        cpu_info = {
            "processor": platform.processor(),
            "machine": platform.machine(),
            "architecture": platform.architecture()[0],
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "max_frequency": psutil.cpu_freq().max,
            "min_frequency": psutil.cpu_freq().min,
            "current_frequency": psutil.cpu_freq().current,
            "cpu_usage_per_core": [
                f"Core {i}: {percentage:.1f}%"
                for i, percentage in enumerate(psutil.cpu_percent(interval=1, percpu=True))
            ],
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
                "performance_concern": (
                    "High CPU usage detected" if high_usage else None
                ),
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather CPU information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }
