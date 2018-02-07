single_port_ram = """module SinglePortRam #
(
  parameter DATA_WIDTH = 8,
  parameter ADDR_WIDTH = 4,
  parameter RAM_DEPTH = 1 << ADDR_WIDTH
)
(
  input clk,
  input rst,
  input [ADDR_WIDTH-1:0] ram_addr,
  input [DATA_WIDTH-1:0] ram_d,
  input ram_we,
  output [DATA_WIDTH-1:0] ram_q
);

  reg [DATA_WIDTH-1:0] mem [0:RAM_DEPTH-1];
  reg [ADDR_WIDTH-1:0] read_addr;

  assign ram_q = mem[read_addr];
  always @ (posedge clk) begin
    if (ram_we)
      mem[ram_addr] <= ram_d;
  read_addr <= ram_addr;
  end
endmodule
"""

bidirectional_single_port_ram = """module BidirectionalSinglePortRam #
(
  parameter DATA_WIDTH = 8,
  parameter ADDR_WIDTH = 4,
  parameter RAM_LENGTH = 16,
  parameter RAM_DEPTH = 1 << (ADDR_WIDTH-1)
)
(
  input clk,
  input rst,
  input [ADDR_WIDTH-1:0] ram_addr,
  input [DATA_WIDTH-1:0] ram_d,
  input ram_we,
  output [DATA_WIDTH-1:0] ram_q,
  output [ADDR_WIDTH-1:0] ram_len
);
  reg [DATA_WIDTH-1:0] mem [0:RAM_DEPTH-1];
  reg [ADDR_WIDTH-1:0] read_addr;

  /*
  integer i;
  initial begin
    for (i = 0; i < RAM_DEPTH; i = i + 1)
      mem[i] = 0;
  end
  */
  function [ADDR_WIDTH-1:0] address (
    input [ADDR_WIDTH-1:0] in_addr
  );
  begin
    if (in_addr[ADDR_WIDTH-1] == 1'b1) begin
      address = RAM_LENGTH + in_addr;
  end else begin
      address = in_addr;
    end
  end
  endfunction // address
  wire [ADDR_WIDTH-1:0] a;
  assign a = address(ram_addr);
  assign ram_q = mem[read_addr];
  assign ram_len = RAM_LENGTH;
  always @ (posedge clk) begin
    if (ram_we)
      mem[ram_addr] <= ram_d;
  read_addr <= a;
  end
endmodule
"""

fifo = """module FIFO #
(
 parameter integer DATA_WIDTH = 32,
 parameter integer ADDR_WIDTH = 2,
 parameter integer LENGTH = 4
)
(
  input clk,
  input rst,
  input [DATA_WIDTH - 1 : 0]  din,
  input write,
  output full,
  output [DATA_WIDTH - 1 : 0] dout,
  input read,
  output empty,
  output will_full,
  output will_empty
);

reg [ADDR_WIDTH - 1 : 0] head;
reg [ADDR_WIDTH - 1 : 0] tail;
reg [ADDR_WIDTH : 0] count;
wire we;
assign we = write && !full;

reg [DATA_WIDTH - 1 : 0] mem [0 : LENGTH - 1];
initial begin : initialize_mem
  integer i;
  for (i = 0; i < LENGTH; i = i + 1) begin
      mem[i] = 0;
  end
end

always @(posedge clk) begin
  if (we) mem[head] <= din;
end
assign dout = mem[tail];

assign full = count >= LENGTH;
assign empty = count == 0;
assign will_full = write && !read && count == LENGTH-1;
assign will_empty = read && !write && count == 1;

always @(posedge clk) begin
  if (rst == 1) begin
    head <= 0;
    tail <= 0;
    count <= 0;
  end else begin
    if (write && read) begin
      if (count == LENGTH) begin
        count <= count - 1;
        tail <= (tail == (LENGTH - 1)) ? 0 : tail + 1;
      end else if (count == 0) begin
        count <= count + 1;
        head <= (head == (LENGTH - 1)) ? 0 : head + 1;
      end else begin
        count <= count;
        head <= (head == (LENGTH - 1)) ? 0 : head + 1;
        tail <= (tail == (LENGTH - 1)) ? 0 : tail + 1;
      end
    end else if (write) begin
      if (count < LENGTH) begin
        count <= count + 1;
        head <= (head == (LENGTH - 1)) ? 0 : head + 1;
      end
    end else if (read) begin
      if (count > 0) begin
        count <= count - 1;
        tail <= (tail == (LENGTH - 1)) ? 0 : tail + 1;
      end
    end
  end
end
endmodule
"""

axi_slave = """
module {module_name}
#(parameter
    C_S_AXI_ADDR_WIDTH = 6,
    C_S_AXI_DATA_WIDTH = 32
)(
    // user signals
    {custom_ports}
    // axi4 lite slave signals
    input  wire                          clk,
    input  wire                          rst,
    input  wire [C_S_AXI_ADDR_WIDTH-1:0] S_AXI_AWADDR,
    input  wire                          S_AXI_AWVALID,
    output wire                          S_AXI_AWREADY,
    input  wire [C_S_AXI_DATA_WIDTH-1:0] S_AXI_WDATA,
    input  wire [C_S_AXI_DATA_WIDTH/8-1:0] S_AXI_WSTRB,
    input  wire                          S_AXI_WVALID,
    output wire                          S_AXI_WREADY,
    output wire [1:0]                    S_AXI_BRESP,
    output wire                          S_AXI_BVALID,
    input  wire                          S_AXI_BREADY,
    input  wire [C_S_AXI_ADDR_WIDTH-1:0] S_AXI_ARADDR,
    input  wire                          S_AXI_ARVALID,
    output wire                          S_AXI_ARREADY,
    output wire [C_S_AXI_DATA_WIDTH-1:0] S_AXI_RDATA,
    output wire [1:0]                    S_AXI_RRESP,
    output wire                          S_AXI_RVALID,
    input  wire                          S_AXI_RREADY,
    output wire                          interrupt
);
//------------------------Parameter----------------------
localparam
{address_defs}

    WRIDLE            = 2'd0,
    WRDATA            = 2'd1,
    WRRESP            = 2'd2,
    RDIDLE            = 2'd0,
    RDDATA            = 2'd1,
    ADDR_BITS         = 6;

//------------------------Local signal-------------------
    reg  [1:0]                    wstate;
    reg  [1:0]                    wnext;
    reg  [ADDR_BITS-1:0]          waddr;
    wire [31:0]                   wmask;
    wire                          aw_hs;
    wire                          w_hs;
    reg  [1:0]                    rstate;
    reg  [1:0]                    rnext;
    reg  [31:0]                   rdata;
    wire                          ar_hs;
    wire [ADDR_BITS-1:0]          raddr;

    // internal registers
{register_defs}

//------------------------Instantiation------------------

//------------------------AXI write fsm------------------
assign S_AXI_AWREADY = (wstate == WRIDLE);
assign S_AXI_WREADY  = (wstate == WRDATA);
assign S_AXI_BRESP   = 2'b00;  // OKAY
assign S_AXI_BVALID  = (wstate == WRRESP);
assign wmask   = {{ {{8{{S_AXI_WSTRB[3]}}}}, {{8{{S_AXI_WSTRB[2]}}}}, {{8{{S_AXI_WSTRB[1]}}}}, {{8{{S_AXI_WSTRB[0]}}}} }};
assign aw_hs   = S_AXI_AWVALID & S_AXI_AWREADY;
assign w_hs    = S_AXI_WVALID & S_AXI_WREADY;

// wstate
always @(posedge clk) begin
    if (rst)
        wstate <= WRIDLE;
    else
        wstate <= wnext;
end

// wnext
always @(*) begin
    case (wstate)
        WRIDLE:
            if (S_AXI_AWVALID)
                wnext = WRDATA;
            else
                wnext = WRIDLE;
        WRDATA:
            if (S_AXI_WVALID)
                wnext = WRRESP;
            else
                wnext = WRDATA;
        WRRESP:
            if (S_AXI_BREADY)
                wnext = WRIDLE;
            else
                wnext = WRRESP;
        default:
            wnext = WRIDLE;
    endcase
end

// waddr
always @(posedge clk) begin
    if (aw_hs)
        waddr <= S_AXI_AWADDR[ADDR_BITS-1:0];
end

//------------------------AXI read fsm-------------------
assign S_AXI_ARREADY = (rstate == RDIDLE);
assign S_AXI_RDATA   = rdata;
assign S_AXI_RRESP   = 2'b00;  // OKAY
assign S_AXI_RVALID  = (rstate == RDDATA);
assign ar_hs   = S_AXI_ARVALID & S_AXI_ARREADY;
assign raddr   = S_AXI_ARADDR[ADDR_BITS-1:0];

// rstate
always @(posedge clk) begin
    if (rst)
        rstate <= RDIDLE;
    else
        rstate <= rnext;
end

// rnext
always @(*) begin
    case (rstate)
        RDIDLE:
            if (S_AXI_ARVALID)
                rnext = RDDATA;
            else
                rnext = RDIDLE;
        RDDATA:
            if (S_AXI_RREADY & S_AXI_RVALID)
                rnext = RDIDLE;
            else
                rnext = RDDATA;
        default:
            rnext = RDIDLE;
    endcase
end

// rdata
always @(posedge clk) begin
    if (ar_hs) begin
        rdata <= 1'b0;
        case (raddr)
{read_defs}
        endcase
    end
end


//------------------------Register logic-----------------

{assign_defs}
{write_defs}
//------------------------Memory logic-------------------

endmodule

"""
