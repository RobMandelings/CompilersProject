.data

  ascii_word0: .ascii ""
  ascii_word1: .ascii "; "
  ascii_word2: .ascii "; "
  ascii_word3: .asciiz ""
  floating_point0: .float 0.5

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
    li $t0, 5 
    la $s0,-24($fp)
    sw $t0, 0($s0)
    lwc1 $f0 floating_point0
    la $s1,-28($fp)
    swc1 $f0, 0($s1)
    li $t0, 99 
    la $s2,-32($fp)
    sw $t0, 0($s2)
    lw $t0, 0($s0)
    lwc1 $f0, 0($s1)
    lw $t1, 0($s2)
    mov.s $f1, $f0
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    mov.s $f12, $f1
    li $v0, 2 
    syscall
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    move $a0, $t1
    li $v0, 11 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    la $s3,-36($fp)
    lw $t2, 0($s3)
    move $v0, $t2
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


