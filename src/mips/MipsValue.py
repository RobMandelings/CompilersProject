import enum


class MipsValue:
    """
    Abstract class which is used as a general interface for both mips
    """

    def __init__(self, content):
        self.content = content

    def get_content(self):
        return self.content


class MipsRegister(MipsValue, enum.Enum):
    # Constant 0
    ZERO = '$zero'

    # Expression eval. and function call results
    V0 = '$v0'
    V1 = '$v1'

    # Procedure call arguments
    A0 = '$a0'
    A1 = '$a1'
    A2 = '$a2'
    A3 = '$a3'

    # Temporary (not preserved across calls)
    T0 = '$t0'
    T1 = '$t1'
    T2 = '$t2'
    T3 = '$t3'
    T4 = '$t4'
    T5 = '$t5'
    T6 = '$t6'
    T7 = '$t7'
    T8 = '$t8'
    T9 = '$t9'

    # Saved temporary (preserved across calls)
    S0 = '$s0'
    S1 = '$s1'
    S2 = '$s2'
    S3 = '$s3'
    S4 = '$s4'
    S5 = '$s5'
    S6 = '$s6'
    S7 = '$s7'

    # Floating point
    F0 = '$f0'
    F1 = '$f1'
    F2 = '$f2'
    F3 = '$f3'
    F4 = '$f4'
    F5 = '$f5'
    F6 = '$f6'
    F7 = '$f7'
    F8 = '$f8'
    F9 = '$f9'
    F10 = '$f10'
    F11 = '$f11'
    F12 = '$f12'
    F13 = '$f13'
    F14 = '$f14'
    F15 = '$f15'
    F16 = '$f16'
    F17 = '$f17'
    F18 = '$f18'
    F19 = '$f19'
    F20 = '$f20'
    F21 = '$f21'
    F22 = '$f22'
    F23 = '$f23'
    F24 = '$f24'
    F25 = '$f25'
    F26 = '$f26'
    F27 = '$f27'
    F28 = '$f28'
    F29 = '$f29'
    F30 = '$f30'
    F31 = '$f31'

    # Special registers
    STACK_POINTER = '$sp'
    FRAME_POINTER = '$fp'
    RETURN_ADDRESS = '$ra'

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.value

    @staticmethod
    def get_arg_registers():
        return [MipsRegister.A0, MipsRegister.A1, MipsRegister.A2, MipsRegister.A3]

    @staticmethod
    def get_saved_temporary_registers():
        return [MipsRegister.S0, MipsRegister.S1, MipsRegister.S2, MipsRegister.S3, MipsRegister.S4, MipsRegister.S4,
                MipsRegister.S5, MipsRegister.S6, MipsRegister.S7]

    @staticmethod
    def get_temporary_registers():
        return [MipsRegister.T0, MipsRegister.T1, MipsRegister.T2, MipsRegister.T3, MipsRegister.T4, MipsRegister.T5,
                MipsRegister.T6, MipsRegister.T7, MipsRegister.T8, MipsRegister.T9]

    @staticmethod
    def get_floating_point_registers():
        return [MipsRegister.F0, MipsRegister.F1, MipsRegister.F2, MipsRegister.F3, MipsRegister.F4, MipsRegister.F5,
                MipsRegister.F6, MipsRegister.F7, MipsRegister.F8, MipsRegister.F9, MipsRegister.F10, MipsRegister.F11,
                MipsRegister.F12,
                MipsRegister.F13, MipsRegister.F14, MipsRegister.F15, MipsRegister.F16, MipsRegister.F17,
                MipsRegister.F18,
                MipsRegister.F19,
                MipsRegister.F20, MipsRegister.F21, MipsRegister.F22, MipsRegister.F23, MipsRegister.F24,
                MipsRegister.F25,
                MipsRegister.F26,
                MipsRegister.F27, MipsRegister.F28, MipsRegister.F29, MipsRegister.F30, MipsRegister.F31]

    @staticmethod
    def is_temporary_register(mips_register):
        assert isinstance(mips_register, MipsRegister)
        return mips_register in MipsRegister.get_temporary_registers()

    @staticmethod
    def is_saved_temporary_register(mips_register):
        assert isinstance(mips_register, MipsRegister)
        return mips_register in MipsRegister.get_saved_temporary_registers()

    @staticmethod
    def is_floating_point_register(mips_register):
        assert isinstance(mips_register, MipsRegister)
        return mips_register in MipsRegister.get_floating_point_registers()

    def get_name(self):
        return self.content


class MipsLiteral(MipsValue):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"{self.content}"

    def get_value(self):
        return self.content
