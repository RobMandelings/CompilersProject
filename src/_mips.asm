.data


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
    sub $sp, $sp, 24
  main_0:
    li $t0, 5 
    la $s0,-16($fp)
    sw $t0, 0($s0)
    li $v0, 1 
    j main_end
  main_1:
    la $s1,-20($fp)
    lw $t0, 0($s1)
    move $v0, $t0
    j main_end
  main_end:
    lw $s1, -12($fp)
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


