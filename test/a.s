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
	sub esp, 16
	mov ecx, 0
	mov [ebp-4], ecx
	mov ecx, 5
	mov [ebp-8], ecx
	mov ecx, 0
	mov [ebp-4], ecx
L1:
	mov ebx, [ebp-4]
	mov ecx, 8
	cmp ebx, ecx
	setl al
	movzx edx, al
	mov [ebp-12], edx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-12]
	mov ecx, 0
	cmp ebx, ecx
	je L0
	mov eax, [ebp-4]
	push eax
	call printInt
	pop edx
L2:
	mov ebx, [ebp-4]
	mov ecx, 1
	add ebx, ecx
	mov [ebp-16], ebx
	mov ecx, [ebp-16]
	mov [ebp-4], ecx
	jmp L1
L0:
	pop ebp
	ret
