#!/usr/bin/env python3
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")

SHEEP_PATH = os.path.join(os.path.dirname(__file__), "SHEEP-master", "frontend")

if not os.path.exists(SHEEP_PATH):
    print(f"Error: SHEEP frontend not found at: {SHEEP_PATH}")
    sys.exit(1)

sys.path.insert(0, SHEEP_PATH)
from pysheep import sheep_client


def build_dotprod_circuit(size: int) -> str:
    lines = [
        "INPUTS db sel",
        "CONST_INPUTS rot",
        "OUTPUTS out",
        "db sel MULTIPLY temp0"
    ]
    for i in range(size - 1):
        lines.append(f"temp{i} rot ROTATE temp{i+1}")
        prev_sum = "temp0" if i == 0 else f"sum{i}"
        lines.append(f"{prev_sum} temp{i+1} ADD sum{i+1}")
    lines.append(f"{'sum' + str(size - 1) if size > 1 else 'temp0'} ALIAS out")
    return "\n".join(lines)


def get_encryption_context() -> str:
    try:
        response = sheep_client.get_available_contexts()
        if response["status_code"] != 200:
            raise ConnectionError("Failed to reach SHEEP server")
        available = response["content"]
        for ctx in ("SEAL_BFV", "SEAL_CKKS"):
            if ctx in available:
                return ctx
        if available:
            return available[0]
        raise RuntimeError("No available encryption contexts found")
    except Exception as err:
        print(f"Error: Connection to SHEEP server failed: {err}")
        sys.exit(1)


def run_pir_retrieval(database):
    n = len(database)
    circuit_text = build_dotprod_circuit(n)
    context = get_encryption_context()
    print(f"\nUsing encryption context: {context}")
    print(f"Database: {database}\n")
    for idx in range(n):
        sheep_client.new_job()
        sheep_client.set_context(context)
        sheep_client.set_input_type("int16_t")
        sheep_client.set_circuit_text(circuit_text)
        sheep_client.set_const_inputs({"rot": -1})
        selection = [1 if j == idx else 0 for j in range(n)]
        print(f"Retrieving index {idx} with selection {selection}")
        sheep_client.set_inputs({"db": database, "sel": selection})
        time.sleep(0.1)
        run_result = None
        for _ in range(3):
            run_result = sheep_client.run_job()
            if run_result["status_code"] == 200:
                break
            time.sleep(0.3)
        if run_result is None or run_result["status_code"] != 200:
            print(f"Execution error: {run_result['content'] if run_result else 'No response'}")
            continue
        output_result = sheep_client.get_results()
        if output_result["status_code"] != 200:
            print(f"Result fetch error: {output_result['content']}")
            continue
        result_data = output_result["content"].get("outputs", {}).get("out", [])
        if not result_data:
            print("No output received.")
            continue
        value = int(result_data[0].split(',')[0]) if isinstance(result_data[0], str) else int(result_data[0])
        expected = database[idx]
        print(f"Retrieved: {value} | Expected: {expected}")
        print("Correct" if value == expected else "Incorrect")


def main():
    db_values = [2, 4, 6, 8, 10, 1, 3]
    run_pir_retrieval(db_values)


if __name__ == "__main__":
    main()
