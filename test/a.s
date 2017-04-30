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
	mov eax, [ebp+8]
	add esp, 0
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, 1
	push eax
	mov eax, 9
	push eax
	call test
	pop edx
	pop edx
	mov [ebp-8], eax
	mov ecx, [ebp-8]
	mov [ebp-4], ecx
	mov eax, [ebp-4]
	push eax
	call printInt
	pop edx
	mov [ebp-12], eax
	mov eax, 0
	add esp, 12
	pop ebp
	ret
