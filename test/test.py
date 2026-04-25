import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    dut._log.info("Testing ALU")

    # Test all operations and inputs
    for op in range(4):          # 2-bit opcode
        for a in range(8):       # 3-bit A
            for b in range(8):   # 3-bit B

                # Pack inputs
                ui_val = (a << 5) | (b << 2) | op
                dut.ui_in.value = ui_val

                await ClockCycles(dut.clk, 1)

                val = dut.uo_out.value.integer
                result = val & 0xF
                carry  = (val >> 4) & 1

                # Expected behavior
                if op == 0:   # ADD
                    expected = a + b
                elif op == 1: # SUB
                    expected = (a - b) & 0xF
                elif op == 2: # AND
                    expected = a & b
                elif op == 3: # XOR
                    expected = a ^ b

                assert result == (expected & 0xF), \
                    f"FAIL: op={op}, a={a}, b={b}, got={result}, exp={expected}"
