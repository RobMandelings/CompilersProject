.data

  ascii_word0: .asciiz "Hello "
  ascii_word1: .asciiz "World\n"
  ascii_word2: .asciiz "World\n"

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
    sub $sp, $sp, 8
  f_0:
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    j f_end
  f_1:
    j f_end
  f_end:
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


  g_entry:
    sw $fp, 0($sp)
    move $fp, $sp
    sw $ra, -4($fp)
    sub $sp, $sp, 8
  g_0:
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    jal f_entry
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    j g_end
  g_end:
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


  main_entry:
    sw $fp, 0($sp)
    move $fp, $sp
    sw $ra, -4($fp)
    sw $s0, -8($fp)
    sub $sp, $sp, 16
  main_0:
    jal f_entry
    jal g_entry
    li $v0, 1 
    j main_end
  main_1:
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


