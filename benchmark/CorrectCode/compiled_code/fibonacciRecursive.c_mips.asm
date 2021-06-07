.data

  ascii_word0: .asciiz "Enter a number:"
  ascii_word1: .ascii "fib("
  ascii_word2: .ascii ")\t= "
  ascii_word3: .asciiz ";\n"

.text

  entry_0:
    jal main_entry
  entry_1:
    li $v0, 10 
    syscall


  f_entry:
    sw $fp, 0($sp)
    move $fp, $sp
    sw $ra, -4($fp)
    sw $s0, -8($fp)
    sw $s1, -12($fp)
    sub $sp, $sp, 88
  f_0:
    la $s0,-16($fp)
    sw $a0, 0($s0)
    j f_1
  f_1:
    lw $t0, 0($s0)
    li $t2, 2 
    slt $t1,$t0,$t2
    bne $t1, $zero, f_3
  f_2:
    beq $t1, $zero, f_5
  f_3:
    lw $t2, 0($s0)
    move $v0, $t2
    j f_end
  f_4:
    j f_7
  f_5:
    lw $t2, 0($s0)
    sub $t3, $t2, 1
    sw $a0, -24($fp)
    sw $a0, -24($fp)
    move $a0, $t3
    sub $sp, $sp, 20
    sw $t0, -28($fp)
    sw $t1, -32($fp)
    sw $t2, -36($fp)
    sw $t3, -40($fp)
    sw $t4, -44($fp)
    jal f_entry
    lw $t4, -44($fp)
    lw $t3, -40($fp)
    lw $t2, -36($fp)
    lw $t1, -32($fp)
    lw $t0, -28($fp)
    addi $sp, $sp, 20
    move $t4, $v0
    lw $t5, 0($s0)
    sub $t6, $t5, 2
    sw $a0, -24($fp)
    sw $a0, -24($fp)
    move $a0, $t6
    sub $sp, $sp, 32
    sw $t0, -28($fp)
    sw $t1, -32($fp)
    sw $t2, -36($fp)
    sw $t3, -40($fp)
    sw $t4, -44($fp)
    sw $t5, -48($fp)
    sw $t6, -52($fp)
    sw $t7, -56($fp)
    jal f_entry
    lw $t7, -56($fp)
    lw $t6, -52($fp)
    lw $t5, -48($fp)
    lw $t4, -44($fp)
    lw $t3, -40($fp)
    lw $t2, -36($fp)
    lw $t1, -32($fp)
    lw $t0, -28($fp)
    addi $sp, $sp, 32
    move $t7, $v0
    add $t8, $t4, $t7
    sw $v0, -28($fp)
    move $v0, $t8
    j f_end
  f_6:
    j f_7
  f_7:
    la $s1,-20($fp)
    lw $t8, 0($s1)
    sw $v0, -32($fp)
    move $v0, $t8
    j f_end
  f_end:
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


  main_entry:
    sw $fp, 0($sp)
    move $fp, $sp
    sw $ra, -4($fp)
    sw $s0, -8($fp)
    sw $s1, -12($fp)
    sw $s2, -16($fp)
    sub $sp, $sp, 64
  main_0:
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    li $v0, 5 
    syscall
    sw $v0, -20($fp)
    li $t0, 1 
    la $s0,-24($fp)
    sw $t0, 0($s0)
    j main_1
  main_1:
    lw $t0, 0($s0)
    la $s1,-20($fp)
    lw $t1, 0($s1)
    sle $t2,$t0,$t1
    bne $t2, $zero, main_3
  main_2:
    beq $t2, $zero, main_4
  main_3:
    lw $t3, 0($s0)
    addi $t4, $t3, 1
    sw $t4, 0($s0)
    lw $t5, 0($s0)
    lw $t6, 0($s0)
    move $a0, $t6
    sub $sp, $sp, 32
    sw $t0, -32($fp)
    sw $t1, -36($fp)
    sw $t2, -40($fp)
    sw $t3, -44($fp)
    sw $t4, -48($fp)
    sw $t5, -52($fp)
    sw $t6, -56($fp)
    sw $t7, -60($fp)
    jal f_entry
    lw $t7, -60($fp)
    lw $t6, -56($fp)
    lw $t5, -52($fp)
    lw $t4, -48($fp)
    lw $t3, -44($fp)
    lw $t2, -40($fp)
    lw $t1, -36($fp)
    lw $t0, -32($fp)
    addi $sp, $sp, 32
    move $t7, $v0
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    move $a0, $t5
    li $v0, 1 
    syscall
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t7
    li $v0, 1 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    j main_1
  main_4:
    li $v0, 0 
    j main_end
  main_5:
    la $s2,-28($fp)
    lw $t8, 0($s2)
    move $v0, $t8
    j main_end
  main_end:
    lw $s2, -16($fp)
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


