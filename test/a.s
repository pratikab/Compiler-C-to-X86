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

test:
	push ebp
	mov ebp, esp
	sub esp, 0
	mov eax, 0
	add esp, 0
	pop ebp
	ret
	add esp, 0
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 28
	mov eax, [ebp-20]
	push eax
	call test
	pop edx
	mov [ebp-28], eax
	mov eax, 0
	add esp, 28
	pop ebp
	ret
	add esp, 28
	pop ebp
	ret
