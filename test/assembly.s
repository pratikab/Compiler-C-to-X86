section .text
	global main 
printInt:
	push ebp
	mov ebp, esp
	mov eax, [esp+8] 	
	xor esi, esi
	cmp eax, 0
	jge loop
	neg eax
	push eax
	pop eax
loop:
	mov edx, 0
	mov ebx, 10
	div ebx
	add edx, 48
	push edx
	inc esi
	cmp eax, 0
	jz   next
	jmp loop
next:
	cmp esi, 0
	jz   exit
	dec esi
	mov eax, 4
	mov ecx, esp
	mov ebx, 1
	mov edx, 1
	int  0x80
	add esp, 4
	jmp  next
exit:
	pop ebp
	ret
main:
	mov eax , 45
	push eax
	call printInt
	mov eax, 1
	mov ebx, 0
	int 0x80
