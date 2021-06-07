.data

 array0: .space 12
  ascii_word0: .ascii ""
  ascii_word1: .ascii "; "
  ascii_word2: .ascii "; "
  ascii_word3: .asciiz ""

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
    sub $sp, $sp, 44
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
    li $t7, 0 
    add $t8, $zero, $zero
    mul $t8, $t7, 4
    la $t5,array0($t8)
    lw $t7, 0($t5)
    sw $t0, -20($fp)
    li $t0, 1 
    sw $t1, -24($fp)
    add $t1, $zero, $zero
    mul $t1, $t0, 4
    la $t9,array0($t1)
    sw $t0, -20($fp)
    lw $t0, 0($t9)
    sw $t0, -28($fp)
    sw $t1, -32($fp)
    li $t1, 2 
    sw $t2, -36($fp)
    add $t2, $zero, $zero
    mul $t2, $t1, 4
    la $t0,array0($t2)
    sw $t1, -32($fp)
    lw $t1, 0($t0)
    sw $t0, -40($fp)
    lw $t0, -28($fp)
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t7
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t1
    li $v0, 1 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    sw $t0, -28($fp)
    la $s0,-16($fp)
    lw $t0, 0($s0)
    move $v0, $t0
    j main_end
  main_end:
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


