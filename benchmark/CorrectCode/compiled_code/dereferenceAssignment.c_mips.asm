.data

  ascii_word0: .ascii ""
  ascii_word1: .asciiz "; "
  ascii_word2: .ascii ""
  ascii_word3: .asciiz "\n"
  ascii_word4: .ascii ""
  ascii_word5: .asciiz "; "
  ascii_word6: .ascii ""
  ascii_word7: .asciiz "\n"

.text

  entry_0:
    jal main_entry
  entry_1:
    li $v0, 10 
    syscall


  main_entry:
    sw $fp, 0($sp)
    move $fp, $sp
    sw $ra, -4($fp)
    sw $s0, -8($fp)
    sw $s1, -12($fp)
    sw $s2, -16($fp)
    sub $sp, $sp, 40
  main_0:
    li $t0, 0 
    la $s0,-20($fp)
    sw $t0, 0($s0)
    la $s1,-24($fp)
    sw $s0, 0($s1)
    lw $t0, 0($s1)
    li $t1, 10 
    sw $t1, 0($t0)
    lw $t1, 0($s0)
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t1
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    lw $t2, 0($s1)
    lw $t3, 0($t2)
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t3
    li $v0, 1 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    lw $t4, 0($s1)
    lw $t5, 0($s1)
    lw $t6, 0($t5)
    addi $t7, $t6, 1
    sw $t7, 0($t4)
    lw $t8, 0($s0)
    la $a0,ascii_word4
    li $v0, 4 
    syscall
    move $a0, $t8
    li $v0, 1 
    syscall
    la $a0,ascii_word5
    li $v0, 4 
    syscall
    lw $t9, 0($s1)
    sw $t0, -32($fp)
    lw $t0, 0($t9)
    la $a0,ascii_word6
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word7
    li $v0, 4 
    syscall
    li $v0, 1 
    j main_end
  main_1:
    sw $t0, -36($fp)
    la $s2,-28($fp)
    lw $t0, 0($s2)
    move $v0, $t0
    j main_end
  main_end:
    lw $s2, -16($fp)
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


