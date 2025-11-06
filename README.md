# ai-bench
Lightweight Rust + PyTorch CLI to benchmark real-world AI inference performance — logs CPU, GPU, and latency metrics in JSON.
AI-Bench is a hybrid Rust + Python benchmarking CLI that measures true inference performance for AI models.
It runs models locally via PyTorch, records per-iteration latency, CPU usage, and GPU memory, and saves all results in structured JSON.

Tech Stack:
Rust (Orchestration + CLI) · PyTorch (Model runtime) · CUDA 12.1 · Matplotlib (Visualization)

Why:
Traditional benchmarks focus on theoretical FLOPS — AI-Bench captures how your CPU, GPU, and memory actually behave during inference.

Features:

GPU and CPU metric logging

Per-iteration latency measurement

JSON export for reproducibility

Matplotlib visualization (optional dark theme)

 Usage:

cargo run -- --iterations 5
python plot_results.py

 Example Output:

Iteration 01 | CPU: 12.3% | Time: 0.021 s | GPU: NVIDIA RTX 3060


📁 Results:
Saved automatically to benchmark_results.json.
