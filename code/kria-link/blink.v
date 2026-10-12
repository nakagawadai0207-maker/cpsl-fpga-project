// K4: blink an LED from a 27-bit counter.
// At 100 MHz, bit 26 flips every 2^26 edges = ~0.67 s.
module blink (
    input  wire clk,   // the clock comes in
    output wire led    // goes out to an LED pin
);
    reg [26:0] count = 0;        // 27 flip-flops, start at 0

    always @(posedge clk) begin
        count <= count + 1;      // at every rising edge: +1
    end

    assign led = count[26];      // the LED is wired to bit 26
endmodule
