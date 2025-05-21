import shutil
import time
from typing import Any, Dict


def get_disk_info() -> Dict[str, Any]:
    """
    Gather disk usage information for the root directory.

    :return:
        Dict[str, Any]: Dictionary with disk usage information structured for ADK
    """
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
                "data_format": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concern": (
                    "High disk usage detected" if high_usage else None
                ),
            },
        }
    except Exception as e:
        return {
            "result": {"error": f"Failed to gather disk information: {str(e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(type(e).__name__)},
        }