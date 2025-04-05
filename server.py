# server.py
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("SumNumbersServer")

# Define a tool that calls the external web service
@mcp.tool()
async def sum_numbers(number1: int, number2: int) -> int:
    """
    Add two integers by calling an external web service.
    
    Args:
        number1 (int): First integer
        number2 (int): Second integer
    
    Returns:
        int: Sum of the two integers
    """
    # Base URL of your web service
    base_url = "https://nelsonandre.outsystemscloud.com/MCPServer/rest/MCP/SumNumbers"
    
    # Query parameters as per the Swagger spec
    params = {
        "Number1": number1,
        "Number2": number2
    }
    
    # Make an asynchronous HTTP POST request with query parameters
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # The response is plain text (e.g., "8"), convert it to an integer
            result = response.text.strip()
            return int(result)  # Return as integer
        
        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code} - {e.response.text}"
        except ValueError as e:
            return f"Error: Invalid response format - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

# Run the server directly if this script is executed
if __name__ == "__main__":
    mcp.run()