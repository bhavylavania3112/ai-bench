import json, time, sys, psutil, torch
import torchvision.models as models

device = "cuda" if torch.cuda.is_available() else "cpu"

cpu_before = psutil.cpu_percent(interval=0.1)

x = torch.randn(1, 3, 224, 224, device=device)
model = models.resnet18(weights=None).to(device)
model.eval()

if device == "cuda":
    torch.cuda.synchronize()
start = time.time()
with torch.no_grad():
    _ = model(x)
if device == "cuda":
    torch.cuda.synchronize()
elapsed = time.time() - start

cpu_after = psutil.cpu_percent(interval=0.05)
avg_cpu = (cpu_before + cpu_after) / 2

gpu_info = {}
if device == "cuda":
    gpu_info = {
        "gpu_name": torch.cuda.get_device_name(0),
        "gpu_memory_used_mb": float(torch.cuda.memory_allocated(0)) / (1024 * 1024),
        "gpu_memory_reserved_mb": float(torch.cuda.memory_reserved(0)) / (1024 * 1024)
    }

result = {
    "device": device,
    "inference_time": elapsed,
    "avg_cpu_percent": avg_cpu,
    "gpu_info": gpu_info
}
sys.stdout.write(json.dumps(result))
sys.stdout.flush()
