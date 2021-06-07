.data

  ascii_word0: .asciiz "Hello World!\n"

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
    la $a0,ascii_word0
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


