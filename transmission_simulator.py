from bdp_calculator import calculate_optimal_shift
from tcp_options_engine import TCPOptionEngine

class TCPConnectionSession:
    def __init__(self, bandwidth_mbps: float, rtt_ms: float, peer_supports_scaling: bool = True):
        self.bw = bandwidth_mbps
        self.rtt = rtt_ms
        self.peer_supports_scaling = peer_supports_scaling
        self.local_shift = calculate_optimal_shift(self.bw, self.rtt)
        self.effective_shift = 0
        self.right_edge = 0

    def perform_handshake(self):
        """Simulate the 3-Way Handshake with Middlebox/Legacy Fallback"""
        print(f"[Handshake] Client sends SYN with Window Scale Option = {self.local_shift}")
        
        if self.peer_supports_scaling:
            syn_ack_option = TCPOptionEngine.build_window_scale_option(self.local_shift)
            parsed = TCPOptionEngine.parse_options(syn_ack_option)
            self.effective_shift = parsed["window_scale"]
            print(f"[Handshake] Server echoed Option Kind 3. Scaling enabled with Shift = {self.effective_shift}")
        else:
            # Fallback Guard: remote endpoint or firewall stripped Option Kind 3
            self.effective_shift = 0
            print("[Handshake] WARNING: Remote peer omitted Option Kind 3. Fallback to S = 0 activated.")

    def compute_transmission_window(self, advertised_16bit_window: int, current_ack: int) -> int:
        """
        Applies bitwise shift and Right-Edge Monotonicity Guard (Anti-Retraction).
        """
        raw_effective_window = advertised_16bit_window << self.effective_shift
        new_right_edge = current_ack + raw_effective_window
        
        # Enforce right-edge monotonicity
        if new_right_edge < self.right_edge:
            effective_window = max(0, self.right_edge - current_ack)
            print("[Guard] Prevented Window Retraction!")
        else:
            effective_window = raw_effective_window
            self.right_edge = new_right_edge
            
        return effective_window

if __name__ == "__main__":
    print("=== Scenario 1: Scaled High-BDP Link ===")
    session1 = TCPConnectionSession(bandwidth_mbps=1000, rtt_ms=100, peer_supports_scaling=True)
    session1.perform_handshake()
    win1 = session1.compute_transmission_window(advertised_16bit_window=65535, current_ack=0)
    print(f"Effective Window: {win1 / (1024 * 1024):.2f} MB\n")
    
    print("=== Scenario 2: Legacy Endpoint (Fallback Guard) ===")
    session2 = TCPConnectionSession(bandwidth_mbps=1000, rtt_ms=100, peer_supports_scaling=False)
    session2.perform_handshake()
    win2 = session2.compute_transmission_window(advertised_16bit_window=65535, current_ack=0)
    print(f"Effective Window: {win2 / 1024:.2f} KB")