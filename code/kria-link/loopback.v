// K4/K7: loopback test. A jumper wire connects out_pin to in_pin on the same board.
// The LED follows the blink only while the wire is connected.
module loopback (
    input  wire clk,
    input  wire in_pin,    // jumper wire comes back in here
    output wire out_pin,   // PMOD pin that drives the jumper
    output wire led
);
    reg [26:0] count = 0;
    always @(posedge clk) begin
        count <= count + 1;
    end
    assign out_pin = count[26];   // written by Dai
    assign led     = in_pin;      // written by Dai
endmodule
