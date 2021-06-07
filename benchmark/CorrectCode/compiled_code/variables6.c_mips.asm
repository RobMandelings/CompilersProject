.data

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
    sw $s1, -12($fp)
    sw $s2, -16($fp)
    sw $s3, -20($fp)
    sub $sp, $sp, 40
  main_0:
    li $t0, 10 
    la $s0,-24($fp)
    sw $t0, 0($s0)
    la $s1,-28($fp)
    sw $s0, 0($s1)
    la $s2,-32($fp)
    sw $s1, 0($s2)
    lw $t0, 0($s0)
    lw $t1, 0($s1)
    lw $t2, 0($t1)
    lw $t3, 0($s2)
    lw $t4, 0($t3)
    lw $t5, 0($t4)
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    move $a0, $t2
    li $v0, 1 
    syscall
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t5
    li $v0, 1 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    li $v0, 1 
    j main_end
  main_1:
    la $s3,-36($fp)
    lw $t6, 0($s3)
    move $v0, $t6
    j main_end
  main_end:
    lw $s3, -20($fp)
    lw $s2, -16($fp)
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


