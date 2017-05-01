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

left_child:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, 2
	mov ecx, [ebp+8]
	imul eax, ecx
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov ecx, 1
	add eax, ecx
	mov [ebp-12], eax
	mov ecx, [ebp-12]
	mov [ebp-4], ecx
	mov eax, [ebp-4]
	add esp, 12
	pop ebp
	ret
	add esp, 12
	pop ebp
	ret
right_child:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, 2
	mov ecx, [ebp+8]
	imul eax, ecx
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov ecx, 2
	add eax, ecx
	mov [ebp-12], eax
	mov ecx, [ebp-12]
	mov [ebp-4], ecx
	mov eax, [ebp-4]
	add esp, 12
	pop ebp
	ret
	add esp, 12
	pop ebp
	ret
in_order:
	push ebp
	mov ebp, esp
	sub esp, 40
	mov eax, [ebp+8]
	mov ecx, 7
	cmp eax, ecx
	setge al
	movzx eax, al
	mov [ebp-8], eax
	mov ecx, [ebp-8]
	mov [ebp-4], ecx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-4]
	mov ecx, 0
	cmp ebx, ecx
	je L0
L1:
	mov eax, 0
	add esp, 40
	pop ebp
	ret
	jmp L0
L0:
	mov eax, [ebp+8]
	push eax
	call left_child
	pop edx
	mov [ebp-16], eax
	mov ecx, [ebp-16]
	mov [ebp-12], ecx
	mov eax, [ebp+8]
	push eax
	call right_child
	pop edx
	mov [ebp-24], eax
	mov ecx, [ebp-24]
	mov [ebp-20], ecx
	mov eax, [ebp-12]
	push eax
	call in_order
	pop edx
	mov [ebp-28], eax
	mov ecx, [ebp+8]
	mov [ebp-32], ecx
	mov eax, [ebp-32]
	push eax
	call printInt
	pop edx
	mov [ebp-36], eax
	mov eax, [ebp-20]
	push eax
	call in_order
	pop edx
	mov [ebp-40], eax
	mov eax, 0
	add esp, 40
	pop ebp
	ret
	add esp, 40
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 92
	mov eax, 0
	mov ecx, 1
	imul eax, ecx
	mov [ebp-4], eax
	mov eax, [ebp-4]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-8], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-8]
	mov [ebp-12], edx
	mov eax, [ebp-12]
	mov ecx, 5
	mov [eax], ecx
	mov eax, 1
	mov ecx, 1
	imul eax, ecx
	mov [ebp-16], eax
	mov eax, [ebp-16]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-20], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-20]
	mov [ebp-24], edx
	mov eax, [ebp-24]
	mov ecx, 3
	mov [eax], ecx
	mov eax, 2
	mov ecx, 1
	imul eax, ecx
	mov [ebp-28], eax
	mov eax, [ebp-28]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-32], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-32]
	mov [ebp-36], edx
	mov eax, [ebp-36]
	mov ecx, 6
	mov [eax], ecx
	mov eax, 3
	mov ecx, 1
	imul eax, ecx
	mov [ebp-40], eax
	mov eax, [ebp-40]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-44], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-44]
	mov [ebp-48], edx
	mov eax, [ebp-48]
	mov ecx, 1
	mov [eax], ecx
	mov eax, 4
	mov ecx, 1
	imul eax, ecx
	mov [ebp-52], eax
	mov eax, [ebp-52]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-56], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-56]
	mov [ebp-60], edx
	mov eax, [ebp-60]
	mov ecx, 2
	mov [eax], ecx
	mov eax, 5
	mov ecx, 1
	imul eax, ecx
	mov [ebp-64], eax
	mov eax, [ebp-64]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-68], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-68]
	mov [ebp-72], edx
	mov eax, [ebp-72]
	mov ecx, 4
	mov [eax], ecx
	mov eax, 6
	mov ecx, 1
	imul eax, ecx
	mov [ebp-76], eax
	mov eax, [ebp-76]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-80], eax
	mov edx, ebp
	sub edx, 40
	add edx, [ebp-80]
	mov [ebp-84], edx
	mov eax, [ebp-84]
	mov ecx, 7
	mov [eax], ecx
	mov ecx, 0
	mov [ebp-88], ecx
	mov eax, [ebp-88]
	push eax
	call in_order
	pop edx
	mov [ebp-92], eax
	mov eax, 0
	add esp, 92
	pop ebp
	ret
	add esp, 92
	pop ebp
	ret
section .data
b TIMES 10 DD 0
