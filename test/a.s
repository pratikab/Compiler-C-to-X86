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
	push ebp
	mov ebp, esp
	sub esp, 20
	mov ecx, 7
	mov [ebp-4], ecx
	mov ecx, 4
	mov [ebp-8], ecx
	mov ecx, 2
	mov [ebp-12], ecx
L1:
	mov ebx, [ebp-12]
	mov ecx, 8
	cmp ebx, ecx
	sete al
	mov [ebp-16], al
	mov ebx, [ebp-16]
	mov ecx, 0
	cmp ebx, ecx
	je L0
	mov eax, [ebp-12]
	push eax
	call printInt
	pop edx
	mov ebx, [ebp-12]
	mov ecx, 1
	add ebx, ecx
	mov [ebp-20], ebx
	mov ecx, [ebp-20]
	mov [ebp-12], ecx
	jmp L1
L0:
	mov eax, [ebp-12]
	push eax
	call printInt
	pop edx
	pop ebp
	ret
