# server.py
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("SumNumbersServer")

# Existing tool: SumNumbers
@mcp.tool()
async def sum_numbers(number1: int, number2: int) -> int:
    """
    Add two integers by calling an external web service.

    Args:
        number1 (int): First integer
        number2 (int): Second integer

    Returns:
        int: Sum of the two integers as an integer
    """
    base_url = "https://nelsonandre.outsystemscloud.com/MCPServer/rest/MCP/SumNumbers"
    params = {"Number1": number1, "Number2": number2}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(base_url, params=params)
            response.raise_for_status()
            return int(response.text.strip())
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
        except ValueError as e:
            raise Exception(f"Invalid integer response: {str(e)}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

# New tool: EmployeeCreate
@mcp.tool()
async def create_employee(employee_name: str, nif: int = 0, date_of_birth: str = "", address: str = "") -> str:
    """
    Create an employee record by calling an external web service.

    Args:
        employee_name (str): Name of the employee (required)
        nif (int, optional): Tax identification number (defaults to 0)
        date_of_birth (str, optional): Date of birth in YYYY-MM-DD format (defaults to empty string)
        address (str, optional): Employee's address (defaults to empty string)

    Returns:
        str: Response from the web service (e.g., success message or employee ID)
    """
    base_url = "https://nelsonandre.outsystemscloud.com/MCPServer/rest/MCP/EmployeeCreate"
    
    # Prepare JSON payload as per EmployeeStructure schema
    payload = {
        "EmployeeName": employee_name,
        "NIF": nif,
        "DateOfBirth": date_of_birth,
        "Address": address
    }
    
    # Make an asynchronous HTTP POST request with JSON body
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                base_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.text.strip()  # Return plain text response
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")


if __name__ == "__main__":
    mcp.run()