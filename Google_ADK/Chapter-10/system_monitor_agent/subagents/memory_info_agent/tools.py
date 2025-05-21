

import time
from typing import Any, Dict
import psutil

def get_memory_info() -> Dict[str, Any]:
    """
    Gather memory (RAM) usage information.

    Returns:
        Dict[str, Any]: Dictionary with memory information structured for ADK
    """
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
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": (
                    "High memory usage detected" if high_usage else None
                ),
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather memory information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }