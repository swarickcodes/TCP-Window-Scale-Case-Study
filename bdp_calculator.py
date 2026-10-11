import math

def calculate_optimal_shift(bandwidth_mbps: float, rtt_ms: float, max_buffer_bytes: int = 16 * 1024 * 1024) -> int:
    """
    Computes Bandwidth-Delay Product (BDP) and the exact minimum shift exponent S.
    Formula: BDP = (Bandwidth in bps / 8) * (RTT in seconds)
    """
    bandwidth_bps = bandwidth_mbps * 1_000_000
    rtt_seconds = rtt_ms / 1000.0
    
    # Calculate BDP in bytes
    bdp_bytes = (bandwidth_bps / 8) * rtt_seconds
    
    # Target buffer has 2x headroom to avoid queue starvation
    target_buffer = min(bdp_bytes * 2, max_buffer_bytes)
    
    print(f"[Engine] Calculated BDP: {bdp_bytes / 1024:.2f} KB")
    print(f"[Engine] Target Buffer Size: {target_buffer / 1024:.2f} KB")
    
    # If buffer fits inside the standard 64 KB window, no shift needed
    if target_buffer <= 65535:
        return 0
    
    # S = ceil(log2(Target_Buffer / 65535))
    ratio = target_buffer / 65535.0
    shift = math.ceil(math.log2(ratio))
    
    # RFC 7323 restricts shift count between 0 and 14
    return min(14, max(0, shift))

if __name__ == "__main__":
    # Test case: 1 Gbps link with 100 ms latency
    bw = 1000       # 1000 Mbps = 1 Gbps
    latency = 100   # 100 ms
    s = calculate_optimal_shift(bw, latency)
    print(f"[Result] Optimal Shift Exponent S: {s} (Scale Factor: {2**s}x)")