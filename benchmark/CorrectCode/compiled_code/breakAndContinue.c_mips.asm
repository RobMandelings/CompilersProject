.data

  ascii_word0: .ascii ""
  ascii_word1: .asciiz "\n"

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
    sub $sp, $sp, 24
  main_0:
    li $t0, 0 
    la $s0,-16($fp)
    sw $t0, 0($s0)
    j main_1
  main_1:
    lw $t0, 0($s0)
    li $t2, 10 
    slt $t1,$t0,$t2
    bne $t1, $zero, main_3
  main_2:
    beq $t1, $zero, main_11
  main_3:
    lw $t2, 0($s0)
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t2
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    j main_4
  main_4:
    lw $t3, 0($s0)
    li $t5, 5 
    seq $t4,$t3,$t5
    bne $t4, $zero, main_6
  main_5:
    beq $t4, $zero, main_8
  main_6:
    j main_11
  main_7:
    j main_10
  main_8:
    lw $t5, 0($s0)
    addi $t6, $t5, 1
    sw $t6, 0($s0)
    j main_1
  main_9:
    j main_10
  main_10:
    li $t7, 10 
    sw $t7, 0($s0)
    j main_1
  main_11:
    li $v0, 0 
    j main_end
  main_12:
    la $s1,-20($fp)
    lw $t7, 0($s1)
    move $v0, $t7
    j main_end
  main_end:
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


