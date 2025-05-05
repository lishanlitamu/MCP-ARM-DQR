import requests
import json
from pathlib import Path
import yaml
from typing import Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP
import os
import sys

# Initialize FastMCP server
mcp = FastMCP("dqr")

# Constants
DQR_API_BASE = "https://dqr-web-service.svcs.arm.gov"
USER_AGENT = "dqr-app/1.0"

@mcp.tool()
async def query_dqr(
    datastream: str,
    quality_category: Optional[str] = None,
    startdate: Optional[str] = None,
    enddate: Optional[str] = None
) -> Dict:
    """Query the ARM Data Quality Report (DQR) API for data quality information.
    
    Args:
        datastream: The datastream to query (required)
        quality_category: Quality category filter (optional)
        startdate: Start date for filtering (optional)
        enddate: End date for filtering (optional)
        
    Returns:
        Dict containing the DQR data
    """
    try:
        # Construct URL based on parameters
        if all([datastream, quality_category, startdate, enddate]):
            url = f"{DQR_API_BASE}/dqr_full/{datastream}/{startdate}/{enddate}/{quality_category.lower()}"
        elif quality_category is None and startdate is None and enddate is None:
            url = f"{DQR_API_BASE}/dqr_ds/{datastream}"
        elif quality_category is not None and startdate is None and enddate is None:
            url = f"{DQR_API_BASE}/dqr_qc/{datastream}/{quality_category.lower()}"
        elif not (startdate and enddate):
            raise ValueError(f"Invalid dates: Startdate:{startdate}; Enddate:{enddate}.")
        else:
            url = f"{DQR_API_BASE}/dqr_se/{datastream}/{startdate}/{enddate}"

        # Make API request
        headers = {
            "accept": "application/json",
            "User-Agent": USER_AGENT
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching DQR data: {response.status_code}, {response.text}")

    except Exception as e:
        raise Exception(f"Error querying DQR API: {str(e)}")

def main():
    """Start the MCP server."""
    mcp.run("stdio") 

if __name__ == '__main__':
    main()