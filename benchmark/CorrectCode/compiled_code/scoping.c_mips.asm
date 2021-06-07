.data

  ascii_word0: .ascii ""
  ascii_word1: .asciiz ";"
  ascii_word2: .ascii ""
  ascii_word3: .asciiz ";"
  ascii_word4: .ascii ""
  ascii_word5: .asciiz ";"
  ascii_word6: .ascii ""
  ascii_word7: .asciiz ";"
 global0: .word 10

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
    sub $sp, $sp, 32
  main_0:
    lw $t0, global0
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    li $t1, 20 
    la $s0,-20($fp)
    sw $t1, 0($s0)
    lw $t1, 0($s0)
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t1
    li $v0, 1 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    li $t2, 30 
    sw $t2, 0($s0)
    j main_1
  main_1:
    li $t3, 1 
    li $t4, 0 
    sne $t2,$t3,$t4
    bne $t2, $zero, main_3
  main_2:
    beq $t2, $zero, main_4
  main_3:
    lw $t3, 0($s0)
    la $a0,ascii_word4
    li $v0, 4 
    syscall
    move $a0, $t3
    li $v0, 1 
    syscall
    la $a0,ascii_word5
    li $v0, 4 
    syscall
    li $t4, 40 
    la $s1,-24($fp)
    sw $t4, 0($s1)
    lw $t4, 0($s1)
    la $a0,ascii_word6
    li $v0, 4 
    syscall
    move $a0, $t4
    li $v0, 1 
    syscall
    la $a0,ascii_word7
    li $v0, 4 
    syscall
    j main_4
  main_4:
    li $v0, 1 
    j main_end
  main_5:
    la $s2,-28($fp)
    lw $t5, 0($s2)
    move $v0, $t5
    j main_end
  main_end:
    lw $s2, -16($fp)
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


