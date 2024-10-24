import readline
import random
import base64
import time
import sys
import os

BANNER = r"""  _    _        _______          _     
 | |  | |      |__   __|        | |    
 | |__| | _____  _| | ___   ___ | |___ 
 |  __  |/ _ \ \/ / |/ _ \ / _ \| / __|
 | |  | |  __/>  <| | (_) | (_) | \__ \
 |_|  |_|\___/_/\_\_|\___/ \___/|_|___/

          # That backslash XD


"""

class Colors:
    red = "\u001b[31;1m"
    green = "\u001b[32;1m"
    yellow = "\u001b[33;1m"
    blue = "\u001b[34;1m"
    purple = "\u001b[35;1m"
    cyan = "\u001b[36;1m"
    reset = "\u001b[0;0m"

class InvalidHexMessage(Exception):
    pass

class InvalidBase64Data(Exception):
    pass

def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform in ["linux", "linux2"]:
        os.system("clear")

def show_banner():
    terminal_columns = os.get_terminal_size().columns
    max_width = 0

    for line in BANNER.splitlines():
        if len(line) > max_width:
            max_width = len(line)
    
    spaces = int((terminal_columns - max_width) / 2)

    for line in BANNER.splitlines():
        print(f"{' ' * spaces}{line}")

def hex_encode(hex_string):
    return "".join([hex(ord(x))[2:] for x in hex_string])

def decode_hex(hex_string):
    try:
        def _to_str(num):
            try:
                return chr(eval(f"0x{num}"))
            except Exception:
                return f"{Colors.red}{num}{Colors.reset}"

        return "".join(_to_str(x2) for x2 in "".join([f"{x} " if i % 2 == 0 else x for i, x in enumerate(hex_string, start=1)]).split() )
    except SyntaxError:
        raise InvalidHexMessage("Invalid hex message data.")

tool_panels = {}

def tool_panel(tool_name: str, description: str):
    def wrapper(function):
        tool_panels[tool_name] = {
            "description": description,
            "function": function
        }

    return wrapper

@tool_panel(tool_name="Hex Encode", description="Encode plain text to hex data.")
def hex_encode_panel(text: str = None):
    if text:
        return hex_encode(text)
    
    while True:
        text = input("Text: ")
        output = hex_encode(text)
        print(f"{output}\n")

@tool_panel(tool_name="Hex Decode", description="Decode hex data to plain text.")
def hex_decode_panel(hex_data: str = None):
    if hex_data:
        return decode_hex(hex_data)
    
    while True:
        hex_data = input("Hex Data: ")
        output = decode_hex(hex_data)
        print(f"{output}\n")

@tool_panel(tool_name="Base64 Encode", description="Encode data to base64.")
def b64_encode_panel(data: str = None):
    if data:
        return base64.b64encode(data.encode()).decode()
    
    while True:
        data = input("Hex Data: ")
        output = base64.b64encode(data.encode()).decode()
        print(f"{output}\n")

@tool_panel(tool_name="Base64 Decode", description="Decode base64 data to readable text.")
def b64_decode_panel(data: str = None):
    if data:
        try:
            return base64.b64decode(data.encode()).decode()
        except Exception:
            raise InvalidBase64Data("Invalid base64 data.")

    while True:
        data = input("Hex Data: ")

        try:
            output = base64.b64decode(data.encode(), validate=True).decode()
        except Exception:
            print("Error: Invalid base64 data.\n")
            continue

        print(f"{output}\n")

def main_panel():
    while True:
        print(f"  {Colors.cyan}Select a tool:{Colors.reset}\n")

        tool_selections = {}

        for i, tool in enumerate(tool_panels, start=1):
            tool_selections[str(i)] = tool
            print(f"    {Colors.cyan}{i}{Colors.reset} . {tool} - {tool_panels[tool]['description']}")
        
        print(f"\n  Tip: You can directly encode/decode data by typing\n  it as an argument. For example: `{Colors.cyan}>{Colors.reset} 1 plain text`\n\n")

        while True:
            query = input(f"{Colors.cyan}>{Colors.reset} ").strip().split(" ", 1)
            selected_tool = query[0]

            if not selected_tool in tool_selections:
                print(f"404: tool not found.\n")
                continue
            
            tool_name = tool_selections[selected_tool]
            tool = tool_panels[tool_name]
            tool_function = tool["function"]
            tool_description = tool["description"]

            if len(query) > 1:
                try:
                    output = tool_function(query[1])
                    print(f"{output}\n")
                except Exception as e:
                    print(f"Error: {e}\n")

                continue

            print(f"Launching {Colors.blue}{tool_name}{Colors.reset}.")
            time.sleep(0.3)
            print(f"Press {Colors.blue}<CTRL + C>{Colors.reset} to go back to the main menu.\n")

            try:
                tool_function()
            except KeyboardInterrupt:
                print("\n")
                break

def main():
    #clear_console()
    show_banner()
    main_panel()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nHexTools: Cya next time! :3\n")
        exit()
