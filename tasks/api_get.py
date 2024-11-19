from typing import Optional, Union, List, Any
from pydantic import BaseModel, HttpUrl
import requests
import json

# Define Pydantic models for the response
class APIResponseSuccess(BaseModel):
    success: bool
    status_code: int
    data: Any  # Accept any valid JSON structure (dict, list, etc.)
    error: Optional[str]

class APIResponseError(BaseModel):
    success: bool
    status_code: int
    data: Optional[Any]  # No data in case of error
    error: str

# Union type for the response
APIResponse = Union[APIResponseSuccess, APIResponseError]

# Function
def get_data_from_api(base_url: HttpUrl, uri: str) -> APIResponse:
    if not base_url.endswith("/"):
        base_url += "/"
    url = f"{base_url}{uri}"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return APIResponseError(
            success=False,
            status_code=0,  # Status code is unavailable in case of a network error
            data=None,
            error=str(e)
        ).dict()

    if response.status_code == 200:
        try:
            data = response.json()  # This can be a dict, list, or any valid JSON
            return APIResponseSuccess(
                success=True,
                status_code=response.status_code,
                data=data,
                error=None
            ).dict()
        except ValueError:
            return APIResponseError(
                success=False,
                status_code=response.status_code,
                data=None,
                error="Response is not valid JSON."
            ).dict()
    else:
        return APIResponseError(
            success=False,
            status_code=response.status_code,
            data=None,
            error=f"HTTP {response.status_code}: {response.text}"
        ).dict()

if __name__ == "__main__":
    test_data = get_data_from_api("https://435lab.com", "api/accountssdfds")
    print(json.dumps(test_data, indent=4))
    if test_data["success"]:
        print("Data fetched successfully")
        print(test_data.data)
    else:
        print(f"An error occurred: {test_data['error']}")

    print('-' * 50 )
    test_data = get_data_from_api("https://435lab.com", "api/accounts")
    if test_data["success"]:
        print("Data fetched successfully")
        print(test_data["status_code"])
    else:
        print(f"An error occurred: {test_data['status_code']}")
