#!/usr/bin/env python

import sys
import os

sheep_frontend_path = os.path.join(os.path.dirname(__file__), "SHEEP-master", "frontend")
if os.path.exists(sheep_frontend_path):
    sys.path.insert(0, sheep_frontend_path)
    from pysheep import sheep_client
else:
    print(f"Error: SHEEP-master folder not found at {sheep_frontend_path}")
    print("Please ensure SHEEP-master folder is in the same directory as this script")
    sys.exit(1)

def create_dot_product_circuit(n):
    circuit_lines = [
        "INPUTS database selection",
        "CONST_INPUTS rotate_1",
        "OUTPUTS result",
        "database selection MULTIPLY prod_r0"
    ]
    
    for i in range(n - 1):
        circuit_lines.append(f"prod_r{i} rotate_1 ROTATE prod_r{i+1}")
        if i == 0:
            circuit_lines.append(f"prod_r0 prod_r1 ADD prod_s1")
        else:
            circuit_lines.append(f"prod_s{i} prod_r{i+1} ADD prod_s{i+1}")
    
    if n > 1:
        circuit_lines.append(f"prod_s{n-1} ALIAS result")
    else:
        circuit_lines.append(f"prod_r0 ALIAS result")
    
    return "\n".join(circuit_lines)

def main():
    database = [2, 4, 6, 8, 10, 1, 3]
    n = len(database)
    
    print(f"Database contains {n} elements: {database}\n")
 
    try:
        contexts = sheep_client.get_available_contexts()
        if contexts["status_code"] != 200:
            print("Cannot connect to SHEEP server")
            print("Make sure the server is running on http://localhost:34568/SheepServer")
            return
    except Exception as e:
        print(f"Cannot connect to SHEEP server: {e}")
        print("Make sure the server is running on http://localhost:34568/SheepServer")
        return
    
    circuit = create_dot_product_circuit(n)
    
    available_contexts = contexts["content"]
    if "SEAL_BFV" in available_contexts:
        context = "SEAL_BFV"
    elif "SEAL_CKKS" in available_contexts:
        context = "SEAL_CKKS"
    elif len(available_contexts) > 0:
        context = available_contexts[0]
    else:
        print("No encryption contexts available")
        return
    
    print("Retrieving each element from the database:\n")
    
    for i in range(n):
        sheep_client.new_job()
        sheep_client.set_context(context)
        sheep_client.set_input_type("int16_t")
        sheep_client.set_circuit_text(circuit)
        sheep_client.set_const_inputs({"rotate_1": -1})
        
        selection = [0] * n
        selection[i] = 1
        
        print(f"Retrieving element at position {i}:")
        print(f"  Selection vector: {selection}")
        
        sheep_client.set_inputs({
            "database": database,
            "selection": selection
        })
        
        run_result = sheep_client.run_job()
        if run_result["status_code"] != 200:
            print(f"  ERROR: Job execution failed - {run_result['content']}")
            continue
        
        results = sheep_client.get_results()
        if results["status_code"] != 200:
            print(f"  ERROR: Failed to get results - {results['content']}")
            continue
        
        result_content = results["content"]
        if "outputs" not in result_content:
            print(f"  ERROR: No outputs in results")
            continue
        
        output_values = result_content["outputs"]["result"]
        if isinstance(output_values[0], str):
            retrieved_value = int(output_values[0].split(',')[0])
        else:
            retrieved_value = int(output_values[0])
        
        if "cleartext check" in result_content:
            is_correct_cleartext = result_content["cleartext check"].get("is_correct", False)
            if not is_correct_cleartext:
                print(f"  WARNING: Cleartext check failed - circuit may be incorrect")
        
        expected_value = database[i]
        is_correct = (retrieved_value == expected_value)
        
        print(f"  Retrieved value: {retrieved_value}")
        print(f"  Expected value:  {expected_value}")
        if is_correct:
            print(f"  Correct!")
        else:
            print(f"  Incorrect!")
    

if __name__ == "__main__":
    main()

