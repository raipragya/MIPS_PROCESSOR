.data
    prompt:     .asciiz "Enter a number: "
    sum_msg:    .asciiz "Sum of squares of digits: "
    result:     .word 4    # Allocate 4 bytes for the result

.text
    main:
        lw $t0, 0($s0)
        # Find the sum of squares of digits
        addi $t1, $0, 0             # initialize sum to 0
        addi $t2, $0, 10            # initialize divisor to 10

    sum_of_squares_loop:
        beq $t0, $0, store_result   # if $t0 is 0, exit loop
        div $t0, $t2                # divide $t0 by 10 
        mfhi $t3                    #remainder (last digit)
        mflo $t0                    # quotient (removed last digit)
        mul $t3, $t3, $t3           # square the remainder
        add $t1, $t1, $t3           # add the squared remainder to the sum
        j sum_of_squares_loop       # jump back to the beginning of the loop

    store_result:
        # Store the sum in the result memory location
        sw $t1, result              # store the sum in the result
        # Exit program
        addi $v0,$0, 10             # syscall code for exit
        syscall







