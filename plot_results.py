import json
import matplotlib.pyplot as plt
from pathlib import Path

# Load benchmark results
data_path = Path("benchmark_results.json")
if not data_path.exists():
    raise FileNotFoundError("benchmark_results.json not found — run your benchmark first.")

with open(data_path) as f:
    results = json.load(f)

iterations = [r["iteration"] for r in results]
times = [r["inference_time"] for r in results]
cpu = [r["avg_cpu_percent"] for r in results]
gpu_name = results[0].get("gpu_name", "Unknown GPU")

# Plot
plt.figure(figsize=(8, 4.5))
plt.plot(iterations, times, marker="o", linewidth=2, label="Inference Time (s)")
plt.title(f"AI-Bench Inference Performance — {gpu_name}", fontsize=13)
plt.xlabel("Iteration")
plt.ylabel("Seconds per inference")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Optional: add CPU usage as a secondary line
plt.twinx()
plt.plot(iterations, cpu, color="orange", linestyle="--", label="CPU Usage (%)")
plt.ylabel("CPU Usage (%)")
plt.legend(loc="upper right")

# Save figure
plt.savefig("benchmark_plot.png", dpi=300)
print("✅ Chart saved as benchmark_plot.png")
