import abc
import enum


class MipsValue(abc.ABC):
    """
    Abstract class which is used as a general interface for both mips
    """

    def __init__(self, content):
        self.content = content

    def get_content(self):
        return self.content


class MipsRegister(enum.Enum, MipsValue):
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

    def get_name(self):
        return self.content


class MipsLiteral(MipsValue):
    def __init__(self, value):
        super().__init__(value)

    def get_value(self):
        return self.content
