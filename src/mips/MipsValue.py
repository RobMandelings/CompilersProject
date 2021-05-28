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
    def is_temporary_register(mips_register):
        assert isinstance(mips_register, MipsRegister)
        return mips_register in MipsRegister.get_temporary_registers()

    @staticmethod
    def is_saved_temporary_register(mips_register):
        assert isinstance(mips_register, MipsRegister)
        return mips_register in MipsRegister.get_saved_temporary_registers()

    def get_name(self):
        return self.content


class MipsLiteral(MipsValue):
    def __init__(self, value):
        super().__init__(value)

    def get_value(self):
        return self.content
