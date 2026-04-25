`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // Input mapping
    wire [2:0] a = ui_in[7:5];   // 3-bit A
    wire [2:0] b = ui_in[4:2];   // 3-bit B
    wire [1:0] op = ui_in[1:0];  // 2-bit opcode

    reg [3:0] result;
    reg carry;

    always @(*) begin
        // default values (prevents latches)
        result = 4'b0000;
        carry  = 1'b0;

        case(op)
            2'b00: {carry, result} = a + b;  // ADD
            2'b01: {carry, result} = a - b;  // SUB
            2'b10: result = a & b;           // AND
            2'b11: result = a ^ b;           // XOR
        endcase
    end

    // Output mapping
    assign uo_out[3:0] = result;
    assign uo_out[4]   = carry;
    assign uo_out[7:5] = 0;

    assign uio_out = 0;
    assign uio_oe  = 0;

    wire _unused = &{ena, clk, rst_n, uio_in, 1'b0};

endmodule
