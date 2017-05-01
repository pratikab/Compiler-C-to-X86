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

swap:
	push ebp
	mov ebp, esp
	sub esp, 52
	mov eax, [ebp+8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-12], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-12]
	mov [ebp-16], edx
	mov edx, [ebp-16]
	mov ecx, [edx]
	mov [ebp-4], ecx
	mov eax, [ebp+8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-20], eax
	mov eax, [ebp-20]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-24], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-24]
	mov [ebp-28], edx
	mov eax, [ebp+12]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-32], eax
	mov eax, [ebp-32]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-36], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-36]
	mov [ebp-40], edx
	mov eax, [ebp-28]
	mov edx, [ebp-40]
	mov ecx, [edx]
	mov [eax], ecx
	mov eax, [ebp+12]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-44], eax
	mov eax, [ebp-44]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-48], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-48]
	mov [ebp-52], edx
	mov eax, [ebp-52]
	mov ecx, [ebp-4]
	mov [eax], ecx
	add esp, 52
	pop ebp
	ret
partition:
	push ebp
	mov ebp, esp
	sub esp, 84
	mov eax, [ebp+8]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-8], eax
	mov ecx, [ebp-8]
	mov [ebp-4], ecx
	mov ecx, [ebp+12]
	mov [ebp-12], ecx
	mov ecx, 1
	mov [ebp-16], ecx
L1:
	mov eax, [ebp-16]
	mov ecx, 1
	cmp eax, ecx
	sete al
	movzx eax, al
	mov [ebp-20], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-20]
	mov ecx, 0
	cmp ebx, ecx
	je L0
L3:
	mov eax, [ebp-4]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-24], eax
	mov eax, [ebp-24]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-28], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-28]
	mov [ebp-32], edx
	mov eax, [ebp-32]
	mov eax, [eax]
	mov ecx, [ebp+16]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-36], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-36]
	mov ecx, 0
	cmp ebx, ecx
	je L2
	mov eax, [ebp-4]
	mov ecx, 1
	add eax, ecx
	mov [ebp-40], eax
	mov ecx, [ebp-40]
	mov [ebp-4], ecx
	jmp L3
L2:
L5:
	mov eax, [ebp-12]
	mov ecx, 0
	cmp eax, ecx
	setg al
	movzx eax, al
	mov [ebp-44], eax
	mov eax, [ebp-12]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-48], eax
	mov eax, [ebp-48]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-52], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-52]
	mov [ebp-56], edx
	mov eax, [ebp-56]
	mov eax, [eax]
	mov ecx, [ebp+16]
	cmp eax, ecx
	setg al
	movzx eax, al
	mov [ebp-60], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-44]
	mov ecx, 0
	cmp ebx, ecx
	je L6
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-60]
	mov ecx, 0
	cmp ebx, ecx
	je L6
	mov eax, 1
	jmp L7
L6:
	mov eax, 0
L7:
	mov eax, [ebp-44]
	mov ecx, [ebp-60]
	movzx eax, al
	mov [ebp-64], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-64]
	mov ecx, 0
	cmp ebx, ecx
	je L4
	mov eax, [ebp-12]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-68], eax
	mov ecx, [ebp-68]
	mov [ebp-12], ecx
	jmp L5
L4:
	mov eax, [ebp-4]
	mov ecx, [ebp-12]
	cmp eax, ecx
	setge al
	movzx eax, al
	mov [ebp-76], eax
	mov ecx, [ebp-76]
	mov [ebp-72], ecx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-72]
	mov ecx, 0
	cmp ebx, ecx
	je L10
L9:
	jmp L0
	jmp L8
L10:
	mov eax, [ebp-12]
	push eax
	mov eax, [ebp-4]
	push eax
	call swap
	pop edx
	pop edx
	mov [ebp-80], eax
L8:
	jmp L1
L0:
	mov eax, [ebp+12]
	push eax
	mov eax, [ebp-4]
	push eax
	call swap
	pop edx
	pop edx
	mov [ebp-84], eax
	mov eax, [ebp-4]
	add esp, 84
	pop ebp
	ret
	add esp, 84
	pop ebp
	ret
quickSort:
	push ebp
	mov ebp, esp
	sub esp, 52
	mov eax, [ebp+12]
	mov ecx, [ebp+8]
	sub eax, ecx
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov ecx, 0
	cmp eax, ecx
	setle al
	movzx eax, al
	mov [ebp-12], eax
	mov ecx, [ebp-12]
	mov [ebp-4], ecx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-4]
	mov ecx, 0
	cmp ebx, ecx
	je L13
L12:
	mov eax, 0
	add esp, 52
	pop ebp
	ret
	jmp L11
L13:
	mov eax, [ebp+12]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-20], eax
	mov eax, [ebp-20]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-24], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-24]
	mov [ebp-28], edx
	mov edx, [ebp-28]
	mov ecx, [edx]
	mov [ebp-16], ecx
	mov eax, [ebp-16]
	push eax
	mov eax, [ebp+12]
	push eax
	mov eax, [ebp+8]
	push eax
	call partition
	pop edx
	pop edx
	pop edx
	mov [ebp-36], eax
	mov ecx, [ebp-36]
	mov [ebp-32], ecx
	mov eax, [ebp-32]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-40], eax
	mov eax, [ebp-40]
	push eax
	mov eax, [ebp+8]
	push eax
	call quickSort
	pop edx
	pop edx
	mov [ebp-44], eax
	mov eax, [ebp+12]
	push eax
	mov eax, [ebp-32]
	mov ecx, 1
	add eax, ecx
	mov [ebp-48], eax
	mov eax, [ebp-48]
	push eax
	call quickSort
	pop edx
	pop edx
	mov [ebp-52], eax
L11:
	add esp, 52
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 112
	mov ecx, 7
	mov [ebp-4], ecx
	mov eax, 0
	mov ecx, 1
	imul eax, ecx
	mov [ebp-8], eax
	mov eax, [ebp-8]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-12], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-12]
	mov [ebp-16], edx
	mov eax, [ebp-16]
	mov ecx, 4
	mov [eax], ecx
	mov eax, 1
	mov ecx, 1
	imul eax, ecx
	mov [ebp-20], eax
	mov eax, [ebp-20]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-24], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-24]
	mov [ebp-28], edx
	mov eax, [ebp-28]
	mov ecx, 6
	mov [eax], ecx
	mov eax, 2
	mov ecx, 1
	imul eax, ecx
	mov [ebp-32], eax
	mov eax, [ebp-32]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-36], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-36]
	mov [ebp-40], edx
	mov eax, [ebp-40]
	mov ecx, 3
	mov [eax], ecx
	mov eax, 3
	mov ecx, 1
	imul eax, ecx
	mov [ebp-44], eax
	mov eax, [ebp-44]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-48], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-48]
	mov [ebp-52], edx
	mov eax, [ebp-52]
	mov ecx, 2
	mov [eax], ecx
	mov eax, 4
	mov ecx, 1
	imul eax, ecx
	mov [ebp-56], eax
	mov eax, [ebp-56]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-60], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-60]
	mov [ebp-64], edx
	mov eax, [ebp-64]
	mov ecx, 1
	mov [eax], ecx
	mov eax, 5
	mov ecx, 1
	imul eax, ecx
	mov [ebp-68], eax
	mov eax, [ebp-68]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-72], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-72]
	mov [ebp-76], edx
	mov eax, [ebp-76]
	mov ecx, 9
	mov [eax], ecx
	mov eax, 6
	mov ecx, 1
	imul eax, ecx
	mov [ebp-80], eax
	mov eax, [ebp-80]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-84], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-84]
	mov [ebp-88], edx
	mov eax, [ebp-88]
	mov ecx, 7
	mov [eax], ecx
	mov eax, [ebp-4]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-92], eax
	mov eax, [ebp-92]
	push eax
	mov eax, 0
	push eax
	call quickSort
	pop edx
	pop edx
	mov [ebp-96], eax
	mov eax, 0
	mov ecx, 1
	imul eax, ecx
	mov [ebp-100], eax
	mov eax, [ebp-100]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-104], eax
	mov edx, ebp
	sub edx, 28
	add edx, [ebp-104]
	mov [ebp-108], edx
	mov eax, [ebp-108]
	mov eax, [eax]
	push eax
	call printInt
	pop edx
	mov [ebp-112], eax
	add esp, 112
	pop ebp
	ret
section .data
intArray TIMES 7 DD 0
