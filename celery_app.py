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
def run_task(module, function, params, instructions={}):
    """
    Dynamically imports and executes a function from a specified module with parameters.

    Args:
        module (str): The module to import (e.g., "tasks.scraping_tasks").
        function (str): The function to call within the module.
        params (dict): A dictionary of parameters to pass to the function.
        instructions (dict): Optional instructions for Celery (e.g., task priority).
    Returns:
        dict: A dictionary containing the status and result or error details.
    """
    ntfy_fail = instructions.get("ntfy_fail", None)
    ntfy_success = instructions.get("ntfy_success", None)

    try:
        # Validate inputs
        if not isinstance(module, str) or not isinstance(function, str):
            raise ValueError("Module and function must be strings.")
        if not isinstance(params, dict):
            raise ValueError("Params must be a dictionary.")

        logger.info(f"Executing task: module={module}, function={function}, params={params}")
        if
        # Optional: Check if the module is allowed
        if ALLOWED_MODULES and module not in ALLOWED_MODULES:
            raise ImportError(f"Module '{module}' is not allowed.")

        # setup notifications for the task, if indicated in the Instructions


        # Dynamically import the module and function
        mod = importlib.import_module(module)
        func = getattr(mod, function)

        # Ensure all required parameters are provided
        required_params = func.__code__.co_varnames[:func.__code__.co_argcount]
        missing_params = [param for param in required_params if param not in params]
        if missing_params:
            if ntfy_fail:
                ntfy_fail.send(f"Missing required parameters: {missing_params}")
            raise ValueError(f"Missing required parameters: {missing_params}")

        # Execute the function
        result = func(**params)
        logger.info(f"Task succeeded: module={module}, function={function}, result={result}")
        if ntfy_success:
            ntfy_success.send(f"Task succeeded: module={module}, function={function}, result={result[:10]}")
        return {"status": "success", "module": module, "function": function, "params": params, "result": result}

    except Exception as e:
        logger.error(f"Task failed: module={module}, function={function}, error={str(e)}", exc_info=True)
        if ntfy_fail:
            ntfy_fail.send(f"Task failed: module={module}, function={function}, error={str(e)[:10]}")
        return {"status": "failed", "module": module, "function": function, "error": str(e)}
