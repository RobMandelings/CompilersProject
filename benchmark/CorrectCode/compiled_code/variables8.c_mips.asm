.data

 array0: .space 12
  ascii_word0: .ascii ""
  ascii_word1: .asciiz "; "

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
    sub $sp, $sp, 56
  main_0:
    li $t1, 0 
    add $t2, $zero, $zero
    mul $t2, $t1, 4
    la $t0,array0($t2)
    li $t1, 10 
    sw $t1, 0($t0)
    li $t3, 1 
    add $t4, $zero, $zero
    mul $t4, $t3, 4
    la $t1,array0($t4)
    li $t3, 20 
    sw $t3, 0($t1)
    li $t5, 2 
    add $t6, $zero, $zero
    mul $t6, $t5, 4
    la $t3,array0($t6)
    li $t5, 30 
    sw $t5, 0($t3)
    li $t5, 1 
    la $s0,-20($fp)
    sw $t5, 0($s0)
    j main_1
  main_1:
    lw $t5, 0($s0)
    slti $t7,$t5,4
    bne $t7, $zero, main_3
  main_2:
    beq $t7, $zero, main_4
  main_3:
    lw $t8, 0($s0)
    sub $t9, $t8, 1
    sw $t0, -28($fp)
    move $t0, $t9
    sw $t1, -32($fp)
    sw $t2, -36($fp)
    add $t2, $zero, $zero
    mul $t2, $t0, 4
    la $t1,array0($t2)
    sw $t0, -40($fp)
    lw $t0, 0($t1)
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    sw $t0, -44($fp)
    lw $t0, 0($s0)
    sw $t1, -48($fp)
    addi $t1, $t0, 1
    sw $t1, 0($s0)
    j main_1
  main_4:
    li $v0, 1 
    j main_end
  main_5:
    sw $t0, -52($fp)
    la $s1,-24($fp)
    lw $t0, 0($s1)
    move $v0, $t0
    j main_end
  main_end:
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


