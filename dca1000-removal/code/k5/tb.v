module tb;
    reg clk = 0;
    always #5 clk = ~clk;
    wire       link;
    wire       frame;
    wire [7:0] word;
    transmitter t1 (.clk(clk), .dout(link), .frame(frame));
    receiver    r1 (.clk(clk), .din(link),  .frame(frame), .word(word));
    initial begin
        $dumpfile("dump.vcd"); $dumpvars(0, tb);
        #200 $display("word = %b", word);
        $finish;
    end
endmodule
