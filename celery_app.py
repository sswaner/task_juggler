import logging
from celery import Celery
import importlib

# Initialize the Celery app
app = Celery(
    'remote_tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0'
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional: Whitelist of allowed modules for security
ALLOWED_MODULES = {"scraping_tasks", "devops_tasks"}

@app.task
def run_task(module, function, params):
    """
    Dynamically imports and executes a function from a specified module with parameters.

    Args:
        module (str): The module to import (e.g., "tasks.scraping_tasks").
        function (str): The function to call within the module.
        params (dict): A dictionary of parameters to pass to the function.

    Returns:
        dict: A dictionary containing the status and result or error details.
    """
    try:
        # Validate inputs
        if not isinstance(module, str) or not isinstance(function, str):
            raise ValueError("Module and function must be strings.")
        if not isinstance(params, dict):
            raise ValueError("Params must be a dictionary.")

        logger.info(f"Executing task: module={module}, function={function}, params={params}")

        # Optional: Check if the module is allowed
        if ALLOWED_MODULES and module not in ALLOWED_MODULES:
            raise ImportError(f"Module '{module}' is not allowed.")

        # Dynamically import the module and function
        mod = importlib.import_module(module)
        func = getattr(mod, function)

        # Ensure all required parameters are provided
        required_params = func.__code__.co_varnames[:func.__code__.co_argcount]
        missing_params = [param for param in required_params if param not in params]
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")

        # Execute the function
        result = func(**params)
        logger.info(f"Task succeeded: module={module}, function={function}, result={result}")
        return {"status": "success", "module": module, "function": function, "params": params, "result": result}

    except Exception as e:
        logger.error(f"Task failed: module={module}, function={function}, error={str(e)}", exc_info=True)
        return {"status": "failed", "module": module, "function": function, "error": str(e)}