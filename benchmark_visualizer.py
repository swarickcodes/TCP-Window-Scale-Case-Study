import matplotlib.pyplot as plt

def run_evaluation():
    latencies = [1, 10, 25, 50, 100, 150, 200]  # ms
    bandwidth_mbps = 1000.0                       # 1 Gbps bottleneck link
    
    legacy_throughputs = []
    novel_throughputs = []
    
    for rtt in latencies:
        rtt_sec = rtt / 1000.0
        bdp_bytes = (bandwidth_mbps * 1_000_000 / 8) * rtt_sec
        
        # Baseline TCP: capped at 65,535 bytes
        legacy_win = 65535
        legacy_tput = min(bandwidth_mbps, (legacy_win * 8) / (rtt_sec * 1_000_000))
        legacy_throughputs.append(legacy_tput)
        
        # Novel Engine: Scaled window expands to fill path BDP
        scaled_win = max(65535, bdp_bytes)
        novel_tput = min(bandwidth_mbps, (scaled_win * 8) / (rtt_sec * 1_000_000))
        novel_throughputs.append(novel_tput)

    plt.figure(figsize=(8, 5))
    plt.plot(latencies, legacy_throughputs, marker='o', color='red', linewidth=2, label='Baseline TCP (RFC 793, No Scaling)')
    plt.plot(latencies, novel_throughputs, marker='s', color='green', linewidth=2, label='Adaptive Scaled Engine (Novel)')
    
    plt.title('Throughput vs. Path Latency (1 Gbps Bottleneck Link)')
    plt.xlabel('Round Trip Time (RTT in ms)')
    plt.ylabel('Achieved Throughput (Mbps)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    print("[Evaluation] Plot generated and saved as 'performance_comparison.png'")

if __name__ == "__main__":
    run_evaluation()