use clap::Parser;
use serde::Serialize;
use std::{fs::File, io::Write, process::Command, time::Duration};

#[derive(Parser)]
#[command(author, version, about = "AI Benchmark Logger")]
struct Args {
    #[arg(short, long, default_value = "python")]
    python: String,
    #[arg(short, long, default_value = "benchmark.py")]
    script: String,
    #[arg(short, long, default_value_t = 5)]
    iterations: u32,
}

#[derive(Serialize)]
struct BenchmarkResult {
    iteration: u32,
    inference_time: f64,
    avg_cpu_percent: f64,
    gpu_name: Option<String>,
    gpu_memory_used_mb: Option<f64>,
}

fn main() {
    let args = Args::parse();
    let mut results: Vec<BenchmarkResult> = Vec::new();
    println!("Running benchmark for {} iterations...", args.iterations);

    for i in 1..=args.iterations {
        let output = Command::new(&args.python)
            .arg(&args.script)
            .output()
            .expect("Failed to run Python benchmark script");

        let stdout = String::from_utf8_lossy(&output.stdout);
        let parsed: serde_json::Value =
            serde_json::from_str(&stdout).unwrap_or_else(|_| serde_json::json!({}));

        let entry = BenchmarkResult {
            iteration: i,
            inference_time: parsed["inference_time"].as_f64().unwrap_or(0.0),
            avg_cpu_percent: parsed["avg_cpu_percent"].as_f64().unwrap_or(0.0),
            gpu_name: parsed["gpu_info"]["gpu_name"]
                .as_str()
                .map(|s| s.to_string()),
            gpu_memory_used_mb: parsed["gpu_info"]["gpu_memory_used_mb"].as_f64(),
        };

        println!(
            "Iteration {:02} | CPU: {:.1}% | Time: {:.4}s | GPU: {}",
            i,
            entry.avg_cpu_percent,
            entry.inference_time,
            entry
                .gpu_name
                .clone()
                .unwrap_or_else(|| "None".to_string())
        );

        results.push(entry);
        std::thread::sleep(Duration::from_millis(200));
    }

    let mut file = File::create("benchmark_results.json").unwrap();
    let json = serde_json::to_string_pretty(&results).unwrap();
    file.write_all(json.as_bytes()).unwrap();
    println!("\nResults saved to benchmark_results.json");
}
