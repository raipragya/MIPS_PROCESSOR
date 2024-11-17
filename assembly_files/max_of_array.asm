.data
array: .word 32,3,66,723,9  # example array
array_size: .word 10  # size of the array
max: .word 0  # initialize max to the smallest possible integer

.text
main:

    la $t0, array  # load address of array into $t0
    lw $t1, array_size  # load array size into $t1
    lw $t2, max  # load max into $t2

    # loop through the array
loop:

    lw $t3, 0($t0)  # load word from array into $t3
    slt $t4, $t2, $t3   # set $t4 to 1 if $t2 < $t3, else 0
    beq $t4,$0, not_max  # if $t4 is 0, then $t3 is not the max
    add $t2, $t3, $0      # update max to $t3
not_max:

    addi $t0, $t0, 4  # move to next array element
    addi $t1, $t1, -1  # decrement array size
    bne $t1,$0, loop  # if array size is not zero, loop again

    sw $t2, max  # store the max value in max

    # print max value

    add $v0, $0, 1
    add $a0, $t2, $0
    syscall

    # exit program
    addi $v0, $0, 10
    syscall
    
    
    
