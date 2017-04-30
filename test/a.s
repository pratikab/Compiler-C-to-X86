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
	sub esp, 92
	mov ecx, 1
	mov [ebp-48], ecx
	mov eax, 1
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
	mov eax, 2
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
	mov ecx, 3
	mov [eax], ecx
	mov eax, 1
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
	mov eax, [eax]
	mov ecx, 5
	add eax, ecx
	mov [ebp-88], eax
	mov ecx, [ebp-88]
	mov [ebp-44], ecx
	mov eax, [ebp-44]
	push eax
	call printInt
	pop edx
	mov [ebp-92], eax
	mov eax, 0
	add esp, 92
	pop ebp
	ret
	add esp, 92
	pop ebp
	ret
