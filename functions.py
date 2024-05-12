import importlib.util
import inspect
import os
import traceback

FUNCTIONS_DIRECTORY = "./functions/"
FULL_FUNCTIONS_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), FUNCTIONS_DIRECTORY)

def explicitly_defined_function(func):
    return inspect.getmodule(func) is None

tools_dictionary = []

_python_types_to_chatgpt_types = {
    str: "string",
    int: "integer",
    bool: "boolean",
}

# Get all module names of .py files in functions folder
_module_names = [file[:-3] for file in os.listdir(FULL_FUNCTIONS_DIRECTORY_PATH) if file.endswith(".py")]

for module_name in _module_names:
    module_path = os.path.join(FULL_FUNCTIONS_DIRECTORY_PATH, module_name) + ".py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # for name in dir(module):
    #     if not name.startswith("__") and callable(getattr(module, name)):
    #         globals()[name] = getattr(module, name)

    functions = inspect.getmembers(module, inspect.isfunction)
    for name, func in functions:
        if not explicitly_defined_function(func):
            continue
        # Make the function global so anything importing functions.py can call it
        globals()[name] = getattr(module, name)

        try:
            # Build the info automatically for the tools dictionary that ChatGPT requires
            args_description = {}
            if "PARAMETERS DESCRIPTION:" in func.__doc__:
                function_description, args_docstring = func.__doc__.split("PARAMETERS DESCRIPTION:")
                args_docstring = args_docstring.strip()
                args_description_lines = args_docstring.split("\n")
                for arg_line in args_description_lines:
                    arg_name, arg_description = arg_line.split(" -> ")
                    args_description[arg_name.strip()] = arg_description.strip()
            else:
                function_description = func.__doc__

            function_dict = {}
            function_dict["name"] = name
            function_dict["description"] = function_description.strip()

            parameters_dict = {}
            required_parameters = []
            signature = inspect.signature(func)
            for param_name, param in signature.parameters.items():
                parameters_dict[param_name] = {
                    "type": _python_types_to_chatgpt_types[param.annotation] if param.annotation != inspect.Parameter.empty else "any",
                }
                if args_description[param_name]:
                    parameters_dict[param_name]["description"] = args_description[param_name]
                if param.default == inspect.Parameter.empty:
                    required_parameters.append(param_name)
                
            function_dict["parameters"] = {
                "type": "object",
                "properties": parameters_dict,
                "required": required_parameters
            }

            tool_dictionary = {
                "type": "function",
                "function": function_dict
            }
            tools_dictionary.append(tool_dictionary)
        
        except Exception as e:
            print(traceback.format_exc())
            print(f"Chances are the function {name}'s docstring is not in the correct format")
            raise e