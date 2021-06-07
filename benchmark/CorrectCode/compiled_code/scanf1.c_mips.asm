.data

  ascii_word0: .asciiz "Enter two numbers:"
  ascii_word1: .ascii ""
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
    sub $sp, $sp, 32
  main_0:
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    li $v0, 5 
    syscall
    sw $v0, -20($fp)
    li $v0, 5 
    syscall
    sw $v0, -24($fp)
    la $s0,-20($fp)
    lw $t0, 0($s0)
    la $s1,-24($fp)
    lw $t1, 0($s1)
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
    li $v0, 1 
    j main_end
  main_1:
    la $s2,-28($fp)
    lw $t2, 0($s2)
    move $v0, $t2
    j main_end
  main_end:
    lw $s2, -16($fp)
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


