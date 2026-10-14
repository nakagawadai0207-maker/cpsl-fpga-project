module transmitter (input wire clk, output wire dout, output wire frame);
    reg [7:0] tx     = 0;
    reg [2:0] bitcnt = 0;
    always @(posedge clk) begin
        if (bitcnt == 3'd7) tx <= 8'b10110010;
        else                tx <= {1'b0, tx[7:1]};
        bitcnt <= bitcnt + 1;
    end
    assign dout  = tx[0];
    assign frame = (bitcnt == 3'd0);
endmodule

module receiver (input wire clk, input wire din, input wire frame, output reg [7:0] word = 0);
    reg [7:0] rx = 0;
    always @(posedge clk) begin
        if (frame) word <= rx;
        rx <= {din, rx[7:1]};
    end
endmodule
