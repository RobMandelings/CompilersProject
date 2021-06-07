.data

  ascii_word0: .ascii ""
  ascii_word1: .asciiz "; "
  ascii_word2: .ascii ""
  ascii_word3: .asciiz "; "
  ascii_word4: .ascii ""
  ascii_word5: .asciiz "; "
  ascii_word6: .ascii ""
  ascii_word7: .asciiz "; "
  ascii_word8: .ascii ""
  ascii_word9: .asciiz "; "
  ascii_word10: .ascii ""
  ascii_word11: .asciiz "; "
  ascii_word12: .ascii ""
  ascii_word13: .asciiz "; "
  ascii_word14: .ascii ""
  ascii_word15: .asciiz "; "
  floating_point0: .float 4.5
  floating_point1: .float 5.5
  floating_point2: .float 10.5
  floating_point3: .float 0.5
  floating_point4: .float 20.0
  floating_point5: .float 0.5
  floating_point6: .float 5.0
  floating_point7: .float 0.5

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
    li $t1, 5 
    li $t2, 5 
    add $t0, $t1, $t2
    la $a0,ascii_word0
    li $v0, 4 
    syscall
    move $a0, $t0
    li $v0, 1 
    syscall
    la $a0,ascii_word1
    li $v0, 4 
    syscall
    lwc1 $f1 floating_point0
    lwc1 $f2 floating_point1
    add.s $f0, $f1, $f2
    mov.s $f1, $f0
    la $a0,ascii_word2
    li $v0, 4 
    syscall
    mov.s $f12, $f1
    li $v0, 2 
    syscall
    la $a0,ascii_word3
    li $v0, 4 
    syscall
    li $t2, 15 
    li $t3, 5 
    sub $t1, $t2, $t3
    la $a0,ascii_word4
    li $v0, 4 
    syscall
    move $a0, $t1
    li $v0, 1 
    syscall
    la $a0,ascii_word5
    li $v0, 4 
    syscall
    lwc1 $f3 floating_point2
    lwc1 $f4 floating_point3
    sub.s $f2, $f3, $f4
    mov.s $f3, $f2
    la $a0,ascii_word6
    li $v0, 4 
    syscall
    mov.s $f12, $f3
    li $v0, 2 
    syscall
    la $a0,ascii_word7
    li $v0, 4 
    syscall
    li $t3, 2 
    li $t4, 5 
    mul $t2, $t3, $t4
    la $a0,ascii_word8
    li $v0, 4 
    syscall
    move $a0, $t2
    li $v0, 1 
    syscall
    la $a0,ascii_word9
    li $v0, 4 
    syscall
    lwc1 $f5 floating_point4
    lwc1 $f6 floating_point5
    mul.s $f4, $f5, $f6
    mov.s $f5, $f4
    la $a0,ascii_word10
    li $v0, 4 
    syscall
    mov.s $f12, $f5
    li $v0, 2 
    syscall
    la $a0,ascii_word11
    li $v0, 4 
    syscall
    li $t4, 20 
    li $t5, 2 
    div $t4, $t5
    mflo $t3
    la $a0,ascii_word12
    li $v0, 4 
    syscall
    move $a0, $t3
    li $v0, 1 
    syscall
    la $a0,ascii_word13
    li $v0, 4 
    syscall
    lwc1 $f7 floating_point6
    lwc1 $f8 floating_point7
    div $f7, $f8
    mflo $f6
    mov.s $f7, $f6
    la $a0,ascii_word14
    li $v0, 4 
    syscall
    mov.s $f12, $f7
    li $v0, 2 
    syscall
    la $a0,ascii_word15
    li $v0, 4 
    syscall
    li $v0, 1 
    j main_end
  main_1:
    la $s0,-12($fp)
    lw $t4, 0($s0)
    move $v0, $t4
    j main_end
  main_end:
    lw $s0, -8($fp)
    lw $ra, -4($fp)
    move $sp, $fp
    lw $fp, 0($sp)
    jr $ra


