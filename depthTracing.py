#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
from ghidra.program.model.listing import FunctionManager
from ghidra.program.model.symbol import RefType
from ghidra.program.model.pcode import PcodeOp

# Get the current program and function manager
program = currentProgram
function_manager = program.getFunctionManager()
listing = program.getListing()

# Dictionaries to store valid edges and computed calls
valid_edges = {}
computed_calls = {}

# Set to track visited functions for recursion
visited_functions = set()

# Helper function to resolve computed call targets (with full overestimation)
def resolve_computed_call(instruction):
    """Handles computed calls and overestimates targets."""
    potential_targets = set()  # Use a set to avoid duplicates

    # Check p-code operations for CALLIND (indirect calls)
    pcode_ops = instruction.getPcode()
    for op in pcode_ops:
        if op.getOpcode() == PcodeOp.CALLIND:
            # Gather all references from the instruction's address
            references = currentProgram.getReferenceManager().getReferencesFrom(instruction.getAddress())
            for ref in references:
                target_function = getFunctionAt(ref.getToAddress())
                if target_function:
                    potential_targets.add(target_function.getName())
                else:
                    potential_targets.add("Unresolved at {}".format(ref.getToAddress()))

    # Add all functions as overestimated targets if no specific references exist
    if not potential_targets:
        for function in function_manager.getFunctions(True):
            potential_targets.add(function.getName())

    return list(potential_targets)

# Helper function to determine if a function's address is stored in memory
def is_address_taken(function):
    references = getReferencesTo(function.getEntryPoint())
    for ref in references:
        if ref.getReferenceType() == RefType.DATA:
            return True
    return False

# Step 1: List all functions in the program
print("Listing all functions in the program:\n")
for function in function_manager.getFunctions(True):
    function_name = function.getName()
    function_address = function.getEntryPoint()
    print("Function: {} at Address: {}".format(function_name, function_address))

# Step 2: Separate computed and valid edges for all functions
for function in function_manager.getFunctions(True):
    function_name = function.getName()
    
    # Initialize lists for valid and computed calls
    valid_edges[function_name] = []
    computed_calls[function_name] = []
    
    # Get instructions in the function's address range
    instructions = listing.getInstructions(function.getBody(), True)
    for instruction in instructions:
        if instruction.getFlowType().isCall():
            if instruction.getFlowType().isComputed():
                # Handle computed calls by trying to resolve the target
                potential_targets = resolve_computed_call(instruction)
                computed_calls[function_name].extend(potential_targets)
            else:
                # Handle direct calls
                references = currentProgram.getReferenceManager().getReferencesFrom(instruction.getAddress())
                for ref in references:
                    if ref.getReferenceType() == RefType.UNCONDITIONAL_CALL:
                        called_function = getFunctionAt(ref.getToAddress())
                        if called_function:
                            valid_edges[function_name].append(called_function.getName())

# Print separated lists of direct and computed calls
print("\nCaptured Function Call Graph - Valid Edges:")
for caller, callees in valid_edges.items():
    if callees:
        for callee in callees:
            print("Function '{}' directly calls '{}'".format(caller, callee))

print("\nCaptured Function Call Graph - Computed Calls:")
for caller, targets in computed_calls.items():
    if targets:
        print("Function '{}' has computed calls to:".format(caller))
        for target in targets:
            print("  - {}".format(target))

# Step 3: Ask the user for a specific function and depth
try:
    user_function_name = askString("Function Selection", "Enter the name of the function you'd like to trace:")
    max_depth = askInt("Depth Limit", "Enter the maximum depth for tracing (0 for no limit):")
except CancelledException:
    print("Operation cancelled by the user.")
    exit()

# Step 4: Find all functions with the specified name
matching_functions = []
for function in function_manager.getFunctions(True):
    if function.getName() == user_function_name:
        matching_functions.append(function)

if not matching_functions:
    print("Function '{}' not found in the program.".format(user_function_name))
    exit()

# Recursive function to trace edges with depth control and address tracking
def trace_callers(function, depth=0):
    if max_depth > 0 and depth >= max_depth:
        return
    if function in visited_functions:
        return  # Avoid infinite recursion for recursive calls

    visited_functions.add(function)
    function_name = function.getName()
    indent = '  ' * depth

    print("{}Function '{}' at depth {}".format(indent, function_name, depth))

    # Check if the function's address is taken
    if is_address_taken(function):
        print("{}Function '{}' has its address stored in memory.".format(indent, function_name))

    # Get references to the target function (calls to it)
    references = getReferencesTo(function.getEntryPoint())
    for ref in references:
        ref_type = ref.getReferenceType()
        if ref_type.isCall():
            calling_function = getFunctionContaining(ref.getFromAddress())
            if calling_function:
                print("{}Direct Call: {} -> {}".format(indent, calling_function.getName(), function_name))
                # Recursive call for further depth
                trace_callers(calling_function, depth + 1)
        elif ref_type == RefType.DATA:
            print("{}Potential Overestimated Call: Reference to '{}' from data at {}".format(
                indent, function_name, ref.getFromAddress()))

# Step 5: Trace the selected function(s)
for function in matching_functions:
    print("\nStarting trace for function '{}' at address {}:\n".format(function.getName(), function.getEntryPoint()))
    trace_callers(function)
