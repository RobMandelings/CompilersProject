.data

  ascii_word0: .asciiz "Enter the number of prime numbers required\n"
  ascii_word1: .ascii "First "
  ascii_word2: .asciiz " prime numbers are :\n"
  ascii_word3: .asciiz "2\n"
  ascii_word4: .ascii ""
  ascii_word5: .asciiz "\n"

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
    sw $s3, -20($fp)
    sw $s4, -24($fp)
    sub $sp, $sp, 112
  main_0:
    li $t0, 3 
    la $s0,-32($fp)
    sw $t0, 0($s0)
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    li $v0, 5 
    syscall
    sw $v0, -28($fp)
    j main_1
  main_1:
    la $s1,-28($fp)
    lw $t0, 0($s1)
    li $t2, 1 
    sge $t1,$t0,$t2
    bne $t1, $zero, main_3
  main_2:
    beq $t1, $zero, main_4
  main_3:
    lw $t2, 0($s1)
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    move $a0, $t2
    li $v0, 1 
    syscall
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    j main_4
  main_4:
    li $t3, 2 
    la $s2,-36($fp)
    sw $t3, 0($s2)
    j main_5
  main_5:
    lw $t3, 0($s2)
    lw $t4, 0($s1)
    sle $t5,$t3,$t4
    bne $t5, $zero, main_7
  main_6:
    beq $t5, $zero, main_21
  main_7:
    li $t6, 2 
    la $s3,-40($fp)
    sw $t6, 0($s3)
    j main_8
  main_8:
    lw $t6, 0($s3)
    lw $t7, 0($s0)
    sub $t8, $t7, 1
    sle $t9,$t6,$t8
    bne $t9, $zero, main_10
  main_9:
    beq $t9, $zero, main_16
  main_10:
    j main_11
  main_11:
    sw $t0, -48($fp)
    lw $t0, 0($s0)
    sw $t0, -52($fp)
    lw $t0, 0($s3)
    sw $t1, -56($fp)
    sw $t2, -60($fp)
    lw $t2, -52($fp)
    div $t2, $t0
    mfhi $t1
    sw $t0, -64($fp)
    sw $t2, -52($fp)
    li $t2, 0 
    seq $t0,$t1,$t2
    bne $t0, $zero, main_13
  main_12:
    beq $t0, $zero, main_15
  main_13:
    j main_16
  main_14:
    j main_15
  main_15:
    sw $t0, -68($fp)
    lw $t0, 0($s3)
    sw $t1, -72($fp)
    addi $t1, $t0, 1
    sw $t1, 0($s3)
    j main_8
  main_16:
    j main_17
  main_17:
    sw $t0, -76($fp)
    lw $t0, 0($s3)
    sw $t0, -80($fp)
    lw $t0, 0($s0)
    sw $t1, -84($fp)
    sw $t2, -52($fp)
    lw $t2, -80($fp)
    seq $t1,$t2,$t0
    bne $t1, $zero, main_19
  main_18:
    beq $t1, $zero, main_20
  main_19:
    sw $t0, -88($fp)
    lw $t0, 0($s0)
    la $a0,ascii_word4
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word5
    li $v0, 4 
    syscall
    sw $t0, -92($fp)
    lw $t0, 0($s2)
    sw $t1, -96($fp)
    addi $t1, $t0, 1
    sw $t1, 0($s2)
    j main_20
  main_20:
    sw $t0, -100($fp)
    lw $t0, 0($s0)
    sw $t1, -104($fp)
    addi $t1, $t0, 1
    sw $t1, 0($s0)
    j main_5
  main_21:
    li $v0, 0 
    j main_end
  main_22:
    sw $t0, -108($fp)
    la $s4,-44($fp)
    lw $t0, 0($s4)
    move $v0, $t0
    j main_end
  main_end:
    lw $s4, -24($fp)
    lw $s3, -20($fp)
    lw $s2, -16($fp)
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


