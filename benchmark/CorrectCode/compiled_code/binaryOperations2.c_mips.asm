.data

  ascii_word0: .ascii ""
  ascii_word1: .asciiz "; "
  ascii_word2: .ascii ""
  ascii_word3: .asciiz "; "
  ascii_word4: .ascii ""
  ascii_word5: .asciiz "; "
  ascii_word6: .ascii ""
  ascii_word7: .asciiz "; "

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
    sub $sp, $sp, 28
  main_0:
    li $t1, 2 
    li $t2, 3 
    add $t0, $t1, $t2
    mul $t1, $t0, 2
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t1
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    li $t3, 2 
    li $t4, 4 
    mul $t2, $t3, $t4
    addi $t3, $t2, 2
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t3
    li $v0, 1 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    li $t5, 10 
    li $t6, 2 
    div $t5, $t6
    mflo $t4
    li $t6, 10 
    li $t7, 2 
    div $t6, $t7
    mflo $t5
    add $t6, $t4, $t5
    la $a0,ascii_word4
    li $v0, 4 
    syscall
    move $a0, $t6
    li $v0, 1 
    syscall
    la $a0,ascii_word5
    li $v0, 4 
    syscall
    li $t8, 100 
    li $t9, 80 
    sub $t7, $t8, $t9
    li $t9, 2 
    div $t7, $t9
    mflo $t8
    sw $t0, -16($fp)
    li $t0, 5 
    sw $t1, -20($fp)
    li $t1, 5 
    sub $t9, $t0, $t1
    sw $t0, -16($fp)
    add $t0, $t8, $t9
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
    sw $t0, -24($fp)
    la $s0,-12($fp)
    lw $t0, 0($s0)
    move $v0, $t0
    j main_end
  main_end:
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


