; Test commands from UVM specification
; Stage 2: Binary encoding test

; 1. Load constant (LOAD_CONST)
; A=158, B=679, C=28
; Expected bytes: 0x9E, 0xA7, 0x02, 0x00, 0x00, 0x1C
158,679,28

; 2. Read from memory (READ_MEM)
; A=17, B=356, C=24
; Expected bytes: 0x11, 0x64, 0x01, 0x60, 0x00
17,356,24

; 3. Write to memory (WRITE_MEM)
; A=12, B=5, C=3
; Expected bytes: 0x0C, 0x65, 0x00
12,5,3

; 4. abs() command (ABS)
; A=214, B=95, C=2, D=27
; Expected bytes: 0xD6, 0x5F, 0x20, 0x38, 0x00
214,95,2,27