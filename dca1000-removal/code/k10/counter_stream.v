// K10: counter that streams 0, 1, 2, ... over AXI-Stream to a DMA.
// Counts up only on a handshake (tvalid && tready), so the DMA never misses a number.
// tlast marks the last word of each 1024-word packet (low 10 bits all 1s).
module counter_stream (
    input  wire        clk,
    input  wire        rstn,
    output reg  [31:0] m_axis_tdata,
    output wire        m_axis_tvalid,
    input  wire        m_axis_tready,
    output wire        m_axis_tlast
);
    assign m_axis_tvalid = rstn;

    always @(posedge clk) begin
        if (rstn == 0) m_axis_tdata <= 0;
        else if (m_axis_tvalid == 1 && m_axis_tready == 1) m_axis_tdata <= m_axis_tdata + 1;
    end

    assign m_axis_tlast = (m_axis_tdata[9:0] == 10'b1111111111);
endmodule
