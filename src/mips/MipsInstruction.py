import src.Instruction as Instruction
import abc

"""
Contains all mips instructions that the compiler can generate
"""


class MipsInstruction(abc.ABC, Instruction.Instruction):

    def __init__(self):
        super().__init__()
