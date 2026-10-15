module testbench;

  reg clk;
  reg rstn;
  reg tready;

  wire [31:0] tdata;
  wire tvalid;
  wire tlast;

  counter_stream a (
    .clk(clk),
    .rstn(rstn),
    .m_axis_tdata(tdata),
    .m_axis_tvalid(tvalid),
    .m_axis_tready(tready),
    .m_axis_tlast(tlast)
  );

  always begin
    #5 clk = ~clk;
  end

  initial begin
    clk = 0;
    rstn = 0;
    tready = 1;

    #20 rstn = 1;
    #80 tready = 0;   // DMA busy from 100 ns
    #30 tready = 1;   // ready again at 130 ns
  end

  always @(posedge clk) begin
    if (tvalid == 1 && tready == 1) begin
      $display("%0t %0d %0b", $time, tdata, tlast);
      if (tlast == 1) $finish;
    end
  end

endmodule
