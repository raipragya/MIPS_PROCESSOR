#This function is used to fetch the instructions
def IF():              
    global PC, instruction_memory
    inst = instruction_memory[PC]
    PC = PC + 4     #increment PC by 4
    return inst 
    
    
#this function decodes each instruction into different fields
def ID(inst):
    global opcode, rs, rt, rd, shamt, funct, target, imm
    #declare the different fields as empty strings
    opcode = ""
    rs = ""
    rt = ""
    rd = ""
    shamt = ""
    funct = ""
    target = ""
    imm = ""
    opcode = inst[0:6]  #first 6 bits of instruction
    control(opcode)     #function call
    
    if opcode == "000010":  # jump instruction
        target = "0000" + inst[6:32] + "00"
        return opcode, rs, rt, rd, shamt, funct, target, imm
    
    elif opcode == "000000" or opcode == "011100":  # R-type instructions 
        rs = inst[6:11]
        rt = inst[11:16]
        rd = inst[16:21]
        shamt = inst[21:26]
        funct = inst[26:32]
        return opcode, rs, rt, rd, shamt, funct, target, imm
    
    else:  # I-type instruction
        rs = inst[6:11]
        rt = inst[11:16]
        imm = inst[16:32]
        return opcode, rs, rt, rd, shamt, funct, target, imm

#This function converts a binary string to a signed integer
def bin_to_int(bin_str):   

    if bin_str[0] == '1':                               # For negative number
        if bin_str == '1' + '0' * (len(bin_str) - 1):   # Check if it's the minimum negative number
            return -2**(len(bin_str) - 1)
        bin_str = ''.join('1' if b == '0' else '0' for b in bin_str)  # Flip the bits
        return -1 * (int("0b"+bin_str, 2) + 1)          # Add 1 and then negate it
        
    else:                                               # For positive number
        return int("0b"+bin_str, 2)
    
        
        
#This function will perform the various operations based on ALUOp , funct
def EX(rs, rt, imm, funct, target, ALUOp):

    global ALUSrc , Branch, Jump, RegDst, reg, opcode,PC
    
    ALU_in1 = 0
    ALU_in2 = 0
    ALU_res = 0
    ALU_res1 = 0
    ALU_res2 = 0

    ALU_ctrl = ALU_controlUnit(ALUOp, funct) #function call
    
    # jump
    if Jump == 1:   
        PC = int("0b"+target, 2)
        return 0
    if rs != "":
        ALU_in1 = reg[int("0b"+rs, 2)]  # input1 to ALU
        
    if ALUSrc == 0:
        ALU_in2 = reg[int("0b"+rt, 2)]  # input2 to ALU
        
    else:
        ALU_in2 = bin_to_int(imm)
    
    # lui
    if ALU_ctrl == "001":  
        ALU_res = int("0b"+imm, 2) * (2**16)
        return ALU_res
        
    # ori    
    elif ALU_ctrl == "000":          
        ALU_res = ALU_in1 | ALU_in2
        return ALU_res
        
    # add    
    if ALU_ctrl == "010":                         
        ALU_res = ALU_in1 + ALU_in2
        
    # slt    
    elif ALU_ctrl == "100":                     
        ALU_res = 1 if ALU_in1 < ALU_in2 else 0
        
    # mul    
    elif ALU_ctrl == "111":  
        ALU_res = ALU_in1 * ALU_in2
    
    #div
    elif ALU_ctrl == "110": 
        ALU_res1 = ALU_in1 // ALU_in2
        ALU_res2 = ALU_in1 % ALU_in2
        return (ALU_res1,ALU_res2)
    
    # sub
    elif ALU_ctrl == "011":  
        ALU_res = ALU_in1 - ALU_in2


        
    if Branch == 1: 
        # beq
        if ALU_res==0 and opcode=="000100":
            PC = PC + (4*bin_to_int(imm))
        # bne
        elif ALU_res !=0 and opcode=="000101":  
            PC=PC+ 4*bin_to_int(imm)
        
    return ALU_res
    
    
#This function describes memory access 
def MEM(ALU_res, rt):
    global MemRd, MemWr, MemtoReg, data_memory,hi,lo

    
    # if MemRd == 1 then read from the address produced by ALU
    if MemRd == 1:  
        return data_memory[ALU_res]
        
    # if MemWr == 1 then write into the address produced by ALU
    elif MemWr == 1:  
        data_memory[ALU_res] = reg[int("0b"+rt, 2)]    
    

    if MemtoReg == 0:
        return ALU_res
        
    elif MemtoReg == 1:
        return data_memory[ALU_res]

#This function writes back to the reg
def WB(rd, rt, data):
    global reg,hi,lo, RegWr, RegDst
    
    if(RegWr == 2):      # if condition for division
        hi=data[1]
        print("hi",hi)
        lo=data[0]
        print("lo",lo)
    
    
    elif RegWr == 1:
        if RegDst == 1:
            if(funct=="010000"):
                reg[int("0b"+rd, 2)] = hi     #this hi is used in case of div,it stores remainder
            elif(funct=="010010"):
                reg[int("0b"+rd, 2)] = lo      #this lo is also used in case of div, it stores quotient
            else:
                reg[int("0b"+rd, 2)] = data
        else:
            reg[int("0b"+rt, 2)] = data

        
        
#This function sets the control signal based on the opcodes
#Control signals RegDst, Branch, MemRd , MemtoReg , ALUOp, MemWr, ALUSrc , RegWr , Jump
def control(opcode):
    global RegDst, Branch, MemRd, MemtoReg, ALUOp, MemWr, ALUSrc, RegWr, Jump
    
    if opcode == "100011":  # lw instruction
        ALUOp = "00"
        ALUSrc = 1
        Branch = 0
        MemRd = 1
        MemtoReg = 1
        MemWr = 0
        Jump = 0
        RegDst = 0
        RegWr = 1
        
    elif opcode == "101011":  # sw instruction
        ALUOp = "00"
        ALUSrc = 1
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 1 
        Jump = 0
        RegDst = 0
        RegWr = 0
    
    elif opcode == "000000":  # R-type instruction
        ALUOp = "10"
        ALUSrc = 0
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 0
        RegDst = 1
        RegWr = 1
        
    elif opcode == "011100":  # mul instruction
        ALUOp = "10"
        ALUSrc = 0 
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 0
        RegDst = 1
        RegWr = 1
         
    elif opcode == "001111":  # lui instruction
        ALUOp = "11"
        ALUSrc = 0
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 0
        RegDst = 0
        RegWr = 1
    
    elif opcode == "001101":  # ori instruction
        ALUOp = "1"
        ALUSrc = 1
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 0 
        Jump = 0
        RegDst = 0
        RegWr = 1
        
    elif opcode == "001000":  # addi instruction
        ALUOp = "00"
        ALUSrc = 1
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 0
        RegDst = 0
        RegWr = 1
        
    elif opcode == "000100":  # beq instruction
        ALUOp = "01"
        ALUSrc = 0
        Branch = 1
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 0
        RegDst = 0
        RegWr = 0
        
    elif opcode == "000101":  # bne instruction
        ALUOp = "01"
        ALUSrc = 0 
        Branch = 1
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 0 
        RegDst = 0 
        RegWr = 0

    elif opcode == "000010":  # j-type instruction
        ALUSrc = "0"
        Branch = 0
        MemRd = 0
        MemtoReg = 0
        MemWr = 0
        Jump = 1
        RegDst = 0
        RegWr = 0

#This function generates ALU control signals which decide what operation is to be done by the ALU
def ALU_controlUnit(ALUOp, funct):
    global RegWr
    # lw, sw, addi
    if ALUOp == "00":  
        return "010"
    
    # lui
    elif ALUOp == "11":   
        return "001"
        
    elif ALUOp == "10":   # R format
        # add
        if funct == "100000":  
            return "010"
        
        # slt
        elif funct == "101010":   
            return "100"
        
        # mul ; alu control is the same as add(mul is repeated add)
        elif funct == "000010":   
            return "111"   
        
        #div
        elif funct=="011010": 
            RegWr=2
            return "110"
        
        # mfhi - moves hi to rd
        elif funct=="010000": 
            return "010"
        
        #mflo - moves lo to rd
        elif funct == "010010":  
            return "010"
        
        # sub
        elif funct == "100010":   
            return "011"

        

    # beq,bne        
    elif ALUOp == "01":    
        return "011"
    
    #ori
    elif ALUOp == "1":      
        return "000"

# Now we will initialize the state of the processor
#initialise PC to point to the first instruction
PC = 4194304

#initialise the various fields of instruction with empty strings
opcode = rs = rt = rd = shamt = funct = target = imm = ""

#initialise control signals of instructions with 0
RegDst = Branch = MemRd = MemtoReg = ALUOp = MemWr = ALUSrc = RegWr = Jump = 0

#initialise reg 
reg = [0] * 32


#Controlling which program is to be run
inp=input('''Enter a letter from a,b,c which decides which program is to be run:
a.Sum of squares
b.Factorial
c.Max element of an array : ''')

print("\n")


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#for sum of squares
if (inp=="a"):

    
    reg[16]=268501088 # $s0 value is initialized to address in data memory that contains our number
    global hi
    hi=0
    global lo
    lo=0


    data_memory = {
        268500992: 0,
        268500996: 0,
        268501000: 0,
        268501004: 0,
        268501008: 0,
        268501012: 0,
        268501016: 0,
        268501020: 0,
        268501024: 0,
        268501028: 0,
        268501032: 0,
        268501036: 0,   #stores the final sum
        268501040: 0,
        268501044: 0,
        268501048: 0,
        268501052: 0,
        268501056: 0,
        268501060: 0,
        268501064: 0,
        268501068: 0,
        268501072: 0,
        268501076: 0,
        268501080: 0,
        268501084: 0,
        268501088: 31,  #number whose sum of squares of digits is to be found(give input)
        268501092: 0,
    }
    
    instruction_memory={
        4194304 : "10001110000010000000000000000000",
        4194308 : "00100000000010010000000000000000",
        4194312 : "00100000000010100000000000001010",
        4194316 : "00010001000000000000000000000110",
        4194320 : "00000001000010100000000000011010",
        4194324 : "00000000000000000101100000010000",
        4194328 : "00000000000000000100000000010010",
        4194332 : "01110001011010110101100000000010",
        4194336 : "00000001001010110100100000100000",
        4194340 : "00001000000100000000000000000011",
        4194344 : "00111100000000010001000000000001",
        4194348 : "10101100001010010000000000101100",
    }

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# for factorial
if (inp=="b"):
    data_memory = {
        268500992: 0,
        268500996: 0,
        268501000: 0,
        268501004: 0,
        268501008: 0,
        268501012: 0,
        268501016: 0,
        268501020: 0,
        268501024: 0,
        268501028: 0,
        268501032: 0,
        268501036: 0,
        268501040: 0,
        268501044: 0,
        268501048: 0,
        268501052: 0,
        268501056: 0,
        268501060: 0,
        268501064: 0,
        268501068: 0,
        268501072: 0,
        268501076: 0,
        268501080: 0,
        268501084: 0,
        268501088: 0,
        268501092: 0,
    }

    instruction_memory = {
        4194304: "00100000000010000000000000000101",    #number whose factorial is to be found(give input)
        4194308: "00111100000000010001000000000001",
        4194312: "10101100001010000000000000110000",
        4194316: "00111100000000010001000000000001",
        4194320: "10001100001010000000000000110000",
        4194324: "00100001000010000000000000000001",
        4194328: "00100000000010010000000000000001",
        4194332: "00100000000010100000000000000001",
        4194336: "00000001010010000000100000101010",
        4194340: "00010000001000000000000000000011",
        4194344: "01110001001010100100100000000010",
        4194348: "00100001010010100000000000000001",
        4194352: "00001000000100000000000000001000",
    }

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#max element of array(array can take upto 10 elements)
if (inp=="c"):
    data_memory = {
        268500992: 88,  #array elements (give input)
        268500996: 3,
        268501000: 66,
        268501004: 723,
        268501008: 9,
        268501012: 0,
        268501016: 0,
        268501020: 0,
        268501024: 0,
        268501028: 0,
        268501032: 5,  #size of array         
        268501036: 0,  #stores the final result
        268501040: 0,
        268501044: 0,
        268501048: 0,
        268501052: 0,
        268501056: 0,
        268501060: 0,
        268501064: 0,
        268501068: 0,
        268501072: 0,
        268501076: 0,
        268501080: 0,
        268501084: 0,
        268501088: 0,
        268501092: 0,
    }
    instruction_memory={
    4194304 : "00111100000000010001000000000001",
    4194308 : "00110100001010000000000000000000",
    4194312 : "00111100000000010001000000000001",
    4194316 : "10001100001010010000000000101000",
    4194320 : "00111100000000010001000000000001",
    4194324 : "10001100001010100000000000101100",
    4194328 : "10001101000010110000000000000000",
    4194332 : "00000001010010110110000000101010",
    4194336 : "00010001100000000000000000000001",
    4194340 : "00000001011000000101000000100000",
    4194344 : "00100001000010000000000000000100",
    4194348 : "00100001001010011111111111111111",
    4194352 : "00010101001000001111111111111001",
    4194356 : "00111100000000010001000000000001",
    4194360 : "10101100001010100000000000101100",
    }



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def print_result():

    print("Final result:\n")

    print("Reg : \n" , reg)
    print("\n")
    print("Data memory : \n" , data_memory)
    print("\n")
    
    if (inp=="a"):
        print("Sum of squares of digits:", data_memory[268501036])
    elif (inp=="b"):
        print("Factorial is ",reg[9])
    elif (inp=="c"):
        print("Max element of array is :",reg[10])



# Main simulation loop
while (1):
    #perform the 5 stages fetch , decode , execute , memory access and writeback
    #print value of PC at every step
    print("Current PC : " , PC)
    
    #instruction fetch
    inst = IF()
    
    #instruction decode
    opcode, rs, rt, rd, shamt, funct, target, imm = ID(inst)
    
    #instruction execute
    ALU_res = EX(rs, rt, imm, funct, target, ALUOp)  # Pass ALUOp to EX function
    
    #memory access
    mem_data = MEM(ALU_res, rt)  #function call
    
    #finally writeback
    WB(rd, rt, mem_data) #function call
    
    print("Reg : \n" , reg)
    print("\n")
    print("Data memory : \n" , data_memory)
    print("\n")
    
    print("---------------------------------------------------------------------------------------------------")
    
    if (inp=="a"):
        if PC > 4194348:
            break
    elif (inp=="b"):
        if PC > 4194352:
            break
    elif (inp=="c"):
        if PC > 4194360:
            break

print("---------------------------------------------------------------------------------------------------")
print("\n")

print_result()



