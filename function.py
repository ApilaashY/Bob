import os
import importlib

class Function():
    # self.name = string
    # self.func = string
    # self.desc = string
    # self.params = list<string>
    # self.paramtypes = list<string>
    # self.function = function

    def __init__(self, name: str, func: str, desc: str, params: list[str]):
        self.name = name.strip()
        self.func = func.strip()
        self.desc = desc.strip()
        self.params = [param.strip().split(":")[0].strip() for param in params]
        self.paramtypes = [param.strip().split(":")[1].strip() for param in params]
        self.module = importlib.import_module("plugins." + ".".join(name.split(".")[:-1]) + ".tasks")
        self.function = getattr(self.module, self.func)

    def __str__(self):
        return f"{self.name} <- {': '.join([f'{param}: {paramtype}' for param, paramtype in zip(self.params, self.paramtypes)])}: {self.desc}"

    def __repr__(self):
        return self.__str__()

    def execute(self, params: list[str], delimiter: str = " "):
        expected_len = len(self.params)
        
        # If there are more parameters provided than expected, merge the excess
        if expected_len > 0 and len(params) > expected_len:
            processed_params = params[:expected_len - 1]
            processed_params.append(delimiter.join(params[expected_len - 1:]))
        else:
            processed_params = params
            
        self.function(*processed_params)

def getFunctions() -> list[Function]:
    total = []
    
    if not os.path.exists("plugins"):
        return total

    for plugin in os.listdir("plugins"):
        plugin_path = os.path.join("plugins", plugin)
        if not os.path.isdir(plugin_path):
            continue
            
        functions_file = os.path.join(plugin_path, "functions.txt")
        if not os.path.exists(functions_file):
            continue

        with open(functions_file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line == "":
                    continue
                
                try:
                    name, func, desc = line.split(",")
                    parts = func.strip().split("<")
                    func_name = parts[0].strip()
                    params = parts[1].strip().split(" ") if len(parts) > 1 else []
                    total.append(Function(f"{plugin}.{name}", func_name, desc, params))
                except (ValueError, IndexError):
                    print(f"Skipping malformed line in {functions_file}: {line}")

    return total