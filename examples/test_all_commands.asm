; Test commands from UVM specification
; Stage 1: Intermediate representation test

; 1. Load constant (LOAD_CONST)
; Format: 158,<constant>,<register_address>
; Test: A=158, B=679, C=28
158,679,28

; 2. Read from memory (READ_MEM)
; Format: 17,<memory_address>,<register_address>
; Test: A=17, B=356, C=24
17,356,24

; 3. Write to memory (WRITE_MEM)
; Format: 12,<memory_register_address>,<value_register_address>
; Test: A=12, B=5, C=3
12,5,3

; 4. abs() command (ABS)
; Format: 214,<offset>,<base_register_address>,<source_register_address>
; Test: A=214, B=95, C=2, D=27
214,95,2,27

; Additional test commands for validation
; 158,1073741824,10  ; This should cause an error (constant > 30 bits)
; 17,67108864,5      ; This should cause an error (address > 26 bits)
; 12,32,10          ; This should cause an error (register address > 31)
; 214,65536,5,10    ; This should cause an error (offset > 16 bits)