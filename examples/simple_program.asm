; Simple test program
; Load constants into registers

158,100,0    ; Load 100 into register 0
158,200,1    ; Load 200 into register 1
158,300,2    ; Load 300 into register 2

; Read from memory (assume there is a value at address 500)
17,500,3     ; Read from memory at address 500 into register 3

; Write value from register 1 to memory at address from register 0
12,0,1       ; Write value from register 1 to memory at address from register 0

; abs() command
214,10,2,1   ; Calculate abs(register1) and save to memory at address (register2 + 10)