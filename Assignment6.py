""" Assignment (20/02/2026)
NumPy Speed Test
Description: Compare Python lists vs NumPy arrays with 1M numbers, measure execution time, write 3 observations.
""" 

# ── NumPy Speed Test ────

import time
import numpy as np

# ── Timer Utility ────

def timer(func):
    """Decorator: measures and returns (result, elapsed_ms)."""
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000   # → milliseconds
        return result, elapsed
    return wrapper


# ── List Operations ─────

@timer
def list_sum(data):
    return sum(data)

@timer
def list_multiply(data):
    return [x * 2 for x in data]

@timer
def list_dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

@timer
def list_mean(data):
    return sum(data) / len(data)

@timer
def list_std(data):
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data)
    return (variance / len(data)) ** 0.5


# ── NumPy Operations ────

@timer
def numpy_sum(arr):
    return np.sum(arr)

@timer
def numpy_multiply(arr):
    return arr * 2

@timer
def numpy_dot_product(a, b):
    return np.dot(a, b)

@timer
def numpy_mean(arr):
    return np.mean(arr)

@timer
def numpy_std(arr):
    return np.std(arr)


# ── Benchmark Runner ────

def run_benchmark(size: int = 1_000_000) -> list[dict]:
    """Run all benchmarks and return results as a list of dicts."""

    print(f"\n  ⚙  Generating {size:,} random numbers ...")
    py_list  = [float(i) for i in range(size)]
    py_list2 = [float(size - i) for i in range(size)]
    np_arr   = np.array(py_list)
    np_arr2  = np.array(py_list2)
    print("  ✅  Data ready.\n")

    benchmarks = [
        ("Sum",          list_sum,          numpy_sum,          (py_list,),          (np_arr,)),
        ("Multiply ×2",  list_multiply,     numpy_multiply,     (py_list,),          (np_arr,)),
        ("Dot Product",  list_dot_product,  numpy_dot_product,  (py_list, py_list2), (np_arr, np_arr2)),
        ("Mean",         list_mean,         numpy_mean,         (py_list,),          (np_arr,)),
        ("Std Dev",      list_std,          numpy_std,          (py_list,),          (np_arr,)),
    ]

    results = []
    for name, list_fn, np_fn, l_args, n_args in benchmarks:
        _, list_ms = list_fn(*l_args)
        _, np_ms   = np_fn(*n_args)
        speedup    = list_ms / np_ms if np_ms > 0 else float("inf")
        results.append({
            "operation": name,
            "list_ms":   list_ms,
            "numpy_ms":  np_ms,
            "speedup":   speedup,
        })

    return results


# ── Report Printer ────

def print_report(results: list[dict]) -> None:
    """Print a formatted benchmark report with bar chart."""

    print("=" * 65)
    print("          ⚡  NumPy vs Python List — Speed Test")
    print(f"               📦  Dataset Size: 1,000,000 numbers")
    print("=" * 65)
    print(f"  {'Operation':<16} {'List (ms)':>10} {'NumPy (ms)':>11} {'Speedup':>9}  Faster?")
    print(f"  {'─'*16} {'─'*10} {'─'*11} {'─'*9}  {'─'*10}")

    for r in results:
        winner = "🚀 NumPy" if r["numpy_ms"] < r["list_ms"] else "🐍 List"
        print(f"  {r['operation']:<16} {r['list_ms']:>10.2f} {r['numpy_ms']:>11.2f} "
              f"{r['speedup']:>8.1f}x  {winner}")

    print("=" * 65)

    # ── Visual Bar Chart ────
    print("\n  📊  Speedup Bar Chart  (each █ ≈ 5×)\n")
    for r in results:
        bar   = "█" * int(r["speedup"] / 5)
        label = f"{r['speedup']:.1f}x"
        print(f"  {r['operation']:<16} {bar:<25} {label}")

    # ── Observations ────
    avg_speed  = sum(r["speedup"] for r in results) / len(results)
    total_list = sum(r["list_ms"] for r in results)
    total_np   = sum(r["numpy_ms"] for r in results)

    print("\n" + "=" * 65)
    print("  📝  Observations")
    print("=" * 65)
    print(f"""
  1. VECTORISATION WINS EVERY TIME
     NumPy was faster in all {len(results)} operations, with an average
     speedup of {avg_speed:.1f}. This is because NumPy operations run
     in compiled C/Fortran code instead of interpreted Python loops.

  2. BIGGEST GAIN — {fastest['operation'].upper()} ({fastest['speedup']:.1f}× faster)
     Operations like '{fastest['operation']}' benefit most because NumPy
     eliminates Python's per-element overhead entirely and uses
     SIMD (Single Instruction, Multiple Data) CPU instructions.

  3. TOTAL TIME SAVED
     Python lists took {total_list:.1f} ms total across all operations.
     NumPy arrays took only {total_np:.1f} ms — saving {total_list - total_np:.1f} ms
     ({((total_list - total_np) / total_list * 100):.1f}% faster overall) on 1 million numbers.
     For data science workloads, this difference is enormous.
""")
    print("=" * 65 + "\n")


# ── Main ────
def main():
    print("\n  Welcome to the NumPy Speed Test!")
    results = run_benchmark(1_000_000)
    print_report(results)

if __name__ == "__main__":
    main()