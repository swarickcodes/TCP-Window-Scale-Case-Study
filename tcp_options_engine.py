import struct

class TCPOptionEngine:
    KIND_WINDOW_SCALE = 3
    LEN_WINDOW_SCALE = 3
    
    @staticmethod
    def build_window_scale_option(shift_count: int) -> bytes:
        """
        Encodes the raw 3-byte TCP Option:
        [Kind = 3 (1 byte)] [Length = 3 (1 byte)] [Shift Count (1 byte)]
        """
        assert 0 <= shift_count <= 14, "Shift count must be in range [0, 14]"
        return struct.pack("!BBB", TCPOptionEngine.KIND_WINDOW_SCALE, TCPOptionEngine.LEN_WINDOW_SCALE, shift_count)

    @staticmethod
    def parse_options(options_bytes: bytes) -> dict:
        """
        Parses raw bytes of TCP options looking for Window Scale.
        """
        parsed = {"window_scale": 0, "supported": False}
        i = 0
        while i < len(options_bytes):
            kind = options_bytes[i]
            if kind == 0:  # End of Option List (EOL)
                break
            elif kind == 1:  # No-Operation (NOP / Padding)
                i += 1
                continue
            
            opt_len = options_bytes[i + 1]
            if kind == TCPOptionEngine.KIND_WINDOW_SCALE:
                shift = options_bytes[i + 2]
                parsed["window_scale"] = shift
                parsed["supported"] = True
            
            i += opt_len
        return parsed

if __name__ == "__main__":
    raw_opt = TCPOptionEngine.build_window_scale_option(shift_count=8)
    print(f"[Engine] Encoded Option Hex: {raw_opt.hex()}")
    
    decoded = TCPOptionEngine.parse_options(raw_opt)
    print(f"[Engine] Decoded Option: {decoded}")