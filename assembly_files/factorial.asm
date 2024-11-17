.data
    prompt:      .asciiz "Enter a non-negative integer: "
    result_msg:  .asciiz "Factorial is: "
    user_input:  .word 0  # space for storing user input

.text
    main:
        # Read user input (set user input to 5)
        addi $t0,$0, 6                          # set user input to 5
        sw $t0, user_input                 # store user input in memory
        lw $t0, user_input                 # load user input from memory into $t0
        addi $t0, $t0, 1                  # for comparison purposes

        # Calculate factorial
        addi $t1, $0, 1                   # initialize result to 1
        addi $t2, $0, 1                   # initialize loop counter to 1

    factorial_loop:
        slt $at, $t2, $t0
        beq $at, $0, end_factorial        # if loop counter equals user input, exit loop

        mul $t1, $t1, $t2                 # multiply result by loop counter
        addi $t2, $t2, 1                  # increment loop counter
        j factorial_loop                  # jump back to the beginning of the loop

    end_factorial:
        # Display the result
        addi $v0, $0, 4                   # syscall code for print_str
        la $a0, result_msg                # load address of result message string
        syscall

        addi $v0, $0, 1                   # syscall code for print_int
        add $a0, $t1, $0                   # load the result into $a0
        syscall

        # Exit program
        addi $v0, $0, 10                  # syscall code for exit
        syscall




