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

fibonacci:
	push ebp
	mov ebp, esp
	sub esp, 28
	mov ebx, [ebp+8]
	mov ecx, 1
	cmp ebx, ecx
	sete al
	movzx edx, al
	mov [ebp-4], edx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-4]
	mov ecx, 0
	cmp ebx, ecx
	je L0
L1:
	mov eax, 1
	add esp, 28
	pop ebp
	ret
	jmp L0
L0:
	mov ebx, [ebp+8]
	mov ecx, 0
	cmp ebx, ecx
	sete al
	movzx edx, al
	mov [ebp-8], edx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-8]
	mov ecx, 0
	cmp ebx, ecx
	je L2
L3:
	mov eax, 0
	add esp, 28
	pop ebp
	ret
	jmp L2
L2:
	mov ebx, [ebp+8]
	mov ecx, 1
	sub ebx, ecx
	mov [ebp-12], ebx
	mov eax, [ebp-12]
	push eax
	call fibonacci
	pop edx
	mov [ebp-16], eax
	mov ebx, [ebp+8]
	mov ecx, 2
	sub ebx, ecx
	mov [ebp-20], ebx
	mov eax, [ebp-20]
	push eax
	call fibonacci
	pop edx
	mov [ebp-24], eax
	mov ebx, [ebp-16]
	mov ecx, [ebp-24]
	add ebx, ecx
	mov [ebp-28], ebx
	mov eax, [ebp-28]
	add esp, 28
	pop ebp
	ret
	add esp, 28
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, 4
	push eax
	call fibonacci
	pop edx
	mov [ebp-8], eax
	mov ecx, [ebp-8]
	mov [ebp-4], ecx
	mov eax, [ebp-4]
	push eax
	call printInt
	pop edx
	mov [ebp-12], eax
	add esp, 12
	pop ebp
	ret
