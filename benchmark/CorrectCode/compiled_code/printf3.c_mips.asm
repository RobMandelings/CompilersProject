.data

  ascii_word0: .ascii ""
  ascii_word1: .ascii ""
  ascii_word2: .ascii ""
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
    sub $sp, $sp, 16
  main_0:
    lwc1 $f1 floating_point0
    mov.s $f0, $f1
    li $t0, 10 
    li $t1, 37 
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    mov.s $f12, $f0
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


