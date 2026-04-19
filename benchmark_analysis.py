import csv
import math
import multiprocessing as mp
import time
from pathlib import Path

from taylor import taylor_e_x_horner, taylor_e_x_naive, taylor_e_x_optmizada


X_VALUE = 4
N_VALUES = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
OUTPUT_CSV = Path("benchmark_results.csv")
PLOT_FILE = Path("performance_vs_n.png")
PRELIM_PLOT_FILE = Path("performance_vs_n_preliminar.png")
PRELIM_AFTER_SECONDS = 10
MAX_SECONDS_PER_CALL = 25


def _worker(func, x, n, queue):
    try:
        queue.put(("ok", func(x, n)))
    except Exception as exc:  # pylint: disable=broad-except
        queue.put(("err", repr(exc)))


def timed_call(func, x, n, timeout_seconds=None):
    start = time.perf_counter()
    if timeout_seconds is None:
        try:
            result = func(x, n)
            elapsed = time.perf_counter() - start
            return {"ok": True, "value": result, "time": elapsed, "error": None}
        except Exception as exc:  # pylint: disable=broad-except
            elapsed = time.perf_counter() - start
            return {"ok": False, "value": None, "time": elapsed, "error": repr(exc)}

    queue = mp.Queue()
    proc = mp.Process(target=_worker, args=(func, x, n, queue))
    proc.start()
    proc.join(timeout_seconds)

    elapsed = time.perf_counter() - start
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return {
            "ok": False,
            "value": None,
            "time": elapsed,
            "error": f"TimeoutError('supero {timeout_seconds:.1f}s')",
        }

    if queue.empty():
        return {"ok": False, "value": None, "time": elapsed, "error": "RuntimeError('sin resultado')"}

    status, payload = queue.get()
    if status == "ok":
        return {"ok": True, "value": payload, "time": elapsed, "error": None}
    return {"ok": False, "value": None, "time": elapsed, "error": payload}


def relative_error(approx, reference):
    return abs(approx - reference) / abs(reference)


def write_csv(rows):
    if not rows:
        return
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows):
    print("Resumen de resultados:")
    print("N | horner_time(s) | horner_rel_error | naive_time(s) | naive_rel_error | opt_time(s) | opt_rel_error | opt_status")
    for r in rows:
        t1_rel = f"{r['t1_rel_error']:.3e}" if r["t1_rel_error"] is not None else "-"
        t2_rel = f"{r['t2_rel_error']:.3e}" if r["t2_rel_error"] is not None else "-"
        t3_rel = f"{r['t3_rel_error']:.3e}" if r["t3_rel_error"] is not None else "-"
        print(
            f"{r['n']:>7} | {r['t1_time']:>10.6f} | {t1_rel:>12} | "
            f"{r['t2_time']:>10.6f} | {t2_rel:>12} | {r['t3_time']:>10.6f} | {t3_rel:>12} | {r['t3_status']}"
        )


def save_plot(rows, output_file, title):
    import matplotlib.pyplot as plt

    ns_1 = [r["n"] for r in rows if r["t1_time"] is not None]
    t1_times = [r["t1_time"] for r in rows if r["t1_time"] is not None]

    ns_2 = [r["n"] for r in rows if r["t2_status"] == "ok"]
    t2_times = [r["t2_time"] for r in rows if r["t2_status"] == "ok"]

    ns_3 = [r["n"] for r in rows if r.get("t3_status") == "ok"]
    t3_times = [r["t3_time"] for r in rows if r.get("t3_status") == "ok"]

    plt.figure(figsize=(10, 6))
    plt.plot(ns_1, t1_times, marker="o", label="horner (optimizada - Horner)")
    if ns_2:
        plt.plot(ns_2, t2_times, marker="s", label="naive (sumatoria + factorial)")
    if ns_3:
        plt.plot(ns_3, t3_times, marker="^", label="opt (iterativa optimizada)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("N (terminos)")
    plt.ylabel("Tiempo de ejecucion (s)")
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
    return output_file


def save_artifacts(rows, is_preliminary=False):
    write_csv(rows)
    if is_preliminary:
        file_path = save_plot(rows, PRELIM_PLOT_FILE, "Comparativa de rendimiento (preliminar)")
        print(f"[preliminar] CSV actualizado en: {OUTPUT_CSV}")
        print(f"[preliminar] Grafica guardada en: {file_path}")
    else:
        file_path = save_plot(rows, PLOT_FILE, "Comparativa de rendimiento: Tiempo vs N")
        print(f"Grafica guardada en: {file_path}")
        print(f"Resultados tabulares guardados en: {OUTPUT_CSV}")


def main():
    reference = math.exp(X_VALUE)
    rows = []
    total_start = time.perf_counter()

    print(f"Valor de referencia: exp({X_VALUE}) = {reference:.15f}\n")
    try:
        for idx, n in enumerate(N_VALUES, start=1):
            item_start = time.perf_counter()
            print(f"[{idx}/{len(N_VALUES)}] Iniciando N={n}...", flush=True)

            row = {
                "n": n,
                "t1_time": None,
                "t1_value": None,
                "t1_abs_error": None,
                "t1_rel_error": None,
                "t1_status": "ok",
                "t2_time": None,
                "t2_value": None,
                "t2_abs_error": None,
                "t2_rel_error": None,
                "t2_status": "ok",
                "t3_time": None,
                "t3_value": None,
                "t3_abs_error": None,
                "t3_rel_error": None,
                "t3_status": "ok",
            }

            print(f"  - Ejecutando horner (optimizada) para N={n}...", flush=True)
            t1 = timed_call(taylor_e_x_horner, X_VALUE, n, timeout_seconds=MAX_SECONDS_PER_CALL)
            row["t1_time"] = t1["time"]
            if t1["ok"]:
                row["t1_value"] = t1["value"]
                row["t1_abs_error"] = abs(t1["value"] - reference)
                row["t1_rel_error"] = relative_error(t1["value"], reference)
            else:
                row["t1_status"] = t1["error"]

            print(f"  - Ejecutando naive (sumatoria) para N={n}...", flush=True)
            t2 = timed_call(taylor_e_x_naive, X_VALUE, n, timeout_seconds=MAX_SECONDS_PER_CALL)
            row["t2_time"] = t2["time"]
            if t2["ok"]:
                row["t2_value"] = t2["value"]
                row["t2_abs_error"] = abs(t2["value"] - reference)
                row["t2_rel_error"] = relative_error(t2["value"], reference)
            else:
                row["t2_status"] = t2["error"]

            print(f"  - Ejecutando opt (iterativa optimizada) para N={n}...", flush=True)
            t3 = timed_call(taylor_e_x_optmizada, X_VALUE, n, timeout_seconds=MAX_SECONDS_PER_CALL)
            row["t3_time"] = t3["time"]
            if t3["ok"]:
                row["t3_value"] = t3["value"]
                row["t3_abs_error"] = abs(t3["value"] - reference)
                row["t3_rel_error"] = relative_error(t3["value"], reference)
            else:
                row["t3_status"] = t3["error"]

            rows.append(row)

            elapsed = time.perf_counter() - total_start
            this_n_elapsed = time.perf_counter() - item_start
            avg = elapsed / idx
            eta = avg * (len(N_VALUES) - idx)
            print(
                f"[{idx}/{len(N_VALUES)}] N={n} completado en {this_n_elapsed:.3f}s. "
                f"Tiempo total: {elapsed:.3f}s. ETA: {eta:.3f}s.",
                flush=True,
            )

            if elapsed >= PRELIM_AFTER_SECONDS:
                save_artifacts(rows, is_preliminary=True)
    except KeyboardInterrupt:
        print("\nInterrupcion detectada (Ctrl+C). Guardando resultados parciales...", flush=True)
        if rows:
            save_artifacts(rows, is_preliminary=True)
            print_summary(rows)
        else:
            print("No hay datos para guardar.")
        return

    print_summary(rows)
    save_artifacts(rows, is_preliminary=False)


if __name__ == "__main__":
    main()
