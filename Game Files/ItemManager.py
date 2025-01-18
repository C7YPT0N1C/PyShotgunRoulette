from Items import *

def UseItem(Item):
    module_name = f"{Item}Item"  # Construct the module name
    if module_name in globals():
        item_module = globals()[module_name]
        if hasattr(item_module, "Use"):
            item_module.Use()
        else:
            print(f"Error: {module_name} does not have a 'Use' function.")
    else:
        print(f"Error: Item '{Item}' not found.")

# Example usage
UseItem("Handsaw")
UseItem("NonExistent")  # Test error handling
