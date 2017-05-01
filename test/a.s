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

quick_sort:
	push ebp
	mov ebp, esp
	sub esp, 232
	mov eax, [ebp+8]
	mov ecx, [ebp+12]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-24], eax
	mov ecx, [ebp-24]
	mov [ebp-20], ecx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-20]
	mov ecx, 0
	cmp ebx, ecx
	je L0
L1:
	mov ecx, [ebp+8]
	mov [ebp-4], ecx
	mov ecx, [ebp+8]
	mov [ebp-16], ecx
	mov ecx, [ebp+12]
	mov [ebp-8], ecx
L3:
	mov eax, [ebp-16]
	mov ecx, [ebp-8]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-28], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-28]
	mov ecx, 0
	cmp ebx, ecx
	je L2
L5:
	mov eax, [ebp-16]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-32], eax
	mov eax, [ebp-32]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-36], eax
	mov edx, arr
	add edx, [ebp-36]
	mov [ebp-40], edx
	mov eax, [ebp-4]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-44], eax
	mov eax, [ebp-44]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-48], eax
	mov edx, arr
	add edx, [ebp-48]
	mov [ebp-52], edx
	mov eax, [ebp-40]
	mov eax, [eax]
	mov ecx, [ebp-52]
	mov ecx, [ecx]
	cmp eax, ecx
	setle al
	movzx eax, al
	mov [ebp-56], eax
	mov eax, [ebp-16]
	mov ecx, [ebp+12]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-60], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-56]
	mov ecx, 0
	cmp ebx, ecx
	je L6
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-60]
	mov ecx, 0
	cmp ebx, ecx
	je L6
	mov edx, 1
	jmp L7
L6:
	mov edx, 0
L7:
	mov eax, [ebp-56]
	mov ecx, [ebp-60]
	movzx eax, dl
	mov [ebp-64], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-64]
	mov ecx, 0
	cmp ebx, ecx
	je L4
	mov eax, [ebp-16]
	mov ecx, 1
	add eax, ecx
	mov [ebp-68], eax
	mov ecx, [ebp-68]
	mov [ebp-16], ecx
	jmp L5
L4:
L9:
	mov eax, [ebp-8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-72], eax
	mov eax, [ebp-72]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-76], eax
	mov edx, arr
	add edx, [ebp-76]
	mov [ebp-80], edx
	mov eax, [ebp-4]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-84], eax
	mov eax, [ebp-84]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-88], eax
	mov edx, arr
	add edx, [ebp-88]
	mov [ebp-92], edx
	mov eax, [ebp-80]
	mov eax, [eax]
	mov ecx, [ebp-92]
	mov ecx, [ecx]
	cmp eax, ecx
	setg al
	movzx eax, al
	mov [ebp-96], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-96]
	mov ecx, 0
	cmp ebx, ecx
	je L8
	mov eax, [ebp-8]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-100], eax
	mov ecx, [ebp-100]
	mov [ebp-8], ecx
	jmp L9
L8:
	mov eax, [ebp-16]
	mov ecx, [ebp-8]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-108], eax
	mov ecx, [ebp-108]
	mov [ebp-104], ecx
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-104]
	mov ecx, 0
	cmp ebx, ecx
	je L10
L11:
	mov eax, [ebp-16]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-112], eax
	mov eax, [ebp-112]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-116], eax
	mov edx, arr
	add edx, [ebp-116]
	mov [ebp-120], edx
	mov edx, [ebp-120]
	mov ecx, [edx]
	mov [ebp-12], ecx
	mov eax, [ebp-8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-128], eax
	mov eax, [ebp-128]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-132], eax
	mov edx, arr
	add edx, [ebp-132]
	mov [ebp-136], edx
	mov edx, [ebp-136]
	mov ecx, [edx]
	mov [ebp-124], ecx
	mov eax, [ebp-16]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-140], eax
	mov eax, [ebp-140]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-144], eax
	mov edx, arr
	add edx, [ebp-144]
	mov [ebp-148], edx
	mov eax, [ebp-148]
	mov ecx, [ebp-124]
	mov [eax], ecx
	mov eax, [ebp-8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-152], eax
	mov eax, [ebp-152]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-156], eax
	mov edx, arr
	add edx, [ebp-156]
	mov [ebp-160], edx
	mov eax, [ebp-160]
	mov ecx, [ebp-12]
	mov [eax], ecx
	jmp L10
L10:
	jmp L3
L2:
	mov eax, [ebp-4]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-164], eax
	mov eax, [ebp-164]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-168], eax
	mov edx, arr
	add edx, [ebp-168]
	mov [ebp-172], edx
	mov edx, [ebp-172]
	mov ecx, [edx]
	mov [ebp-12], ecx
	mov eax, [ebp-4]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-176], eax
	mov eax, [ebp-176]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-180], eax
	mov edx, arr
	add edx, [ebp-180]
	mov [ebp-184], edx
	mov eax, [ebp-8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-188], eax
	mov eax, [ebp-188]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-192], eax
	mov edx, arr
	add edx, [ebp-192]
	mov [ebp-196], edx
	mov eax, [ebp-184]
	mov edx, [ebp-196]
	mov ecx, [edx]
	mov [eax], ecx
	mov eax, [ebp-8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-200], eax
	mov eax, [ebp-200]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-204], eax
	mov edx, arr
	add edx, [ebp-204]
	mov [ebp-208], edx
	mov eax, [ebp-208]
	mov ecx, [ebp-12]
	mov [eax], ecx
	mov eax, [ebp-8]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-216], eax
	mov ecx, [ebp-216]
	mov [ebp-212], ecx
	mov eax, [ebp-8]
	mov ecx, 1
	add eax, ecx
	mov [ebp-224], eax
	mov ecx, [ebp-224]
	mov [ebp-220], ecx
	mov eax, [ebp-212]
	push eax
	mov eax, [ebp+8]
	push eax
	call quick_sort
	pop edx
	pop edx
	mov [ebp-228], eax
	mov eax, [ebp+12]
	push eax
	mov eax, [ebp-220]
	push eax
	call quick_sort
	pop edx
	pop edx
	mov [ebp-232], eax
	mov eax, 0
	add esp, 232
	pop ebp
	ret
	jmp L0
L0:
	add esp, 232
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 92
	mov ecx, 4
	mov [ebp-4], ecx
	mov eax, 0
	mov ecx, 1
	imul eax, ecx
	mov [ebp-12], eax
	mov eax, [ebp-12]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-16], eax
	mov edx, arr
	add edx, [ebp-16]
	mov [ebp-20], edx
	mov eax, [ebp-20]
	mov ecx, 4
	mov [eax], ecx
	mov eax, 1
	mov ecx, 1
	imul eax, ecx
	mov [ebp-24], eax
	mov eax, [ebp-24]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-28], eax
	mov edx, arr
	add edx, [ebp-28]
	mov [ebp-32], edx
	mov eax, [ebp-32]
	mov ecx, 1
	mov [eax], ecx
	mov eax, 2
	mov ecx, 1
	imul eax, ecx
	mov [ebp-36], eax
	mov eax, [ebp-36]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-40], eax
	mov edx, arr
	add edx, [ebp-40]
	mov [ebp-44], edx
	mov eax, [ebp-44]
	mov ecx, 3
	mov [eax], ecx
	mov eax, 3
	mov ecx, 1
	imul eax, ecx
	mov [ebp-48], eax
	mov eax, [ebp-48]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-52], eax
	mov edx, arr
	add edx, [ebp-52]
	mov [ebp-56], edx
	mov eax, [ebp-56]
	mov ecx, 2
	mov [eax], ecx
	mov eax, [ebp-4]
	mov ecx, 1
	sub eax, ecx
	mov [ebp-64], eax
	mov ecx, [ebp-64]
	mov [ebp-60], ecx
	mov eax, [ebp-60]
	push eax
	mov eax, 0
	push eax
	call quick_sort
	pop edx
	pop edx
	mov [ebp-68], eax
	mov ecx, 0
	mov [ebp-8], ecx
L13:
	mov eax, [ebp-8]
	mov ecx, [ebp-4]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-72], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-72]
	mov ecx, 0
	cmp ebx, ecx
	je L12
	mov eax, [ebp-8]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-76], eax
	mov eax, [ebp-76]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-80], eax
	mov edx, arr
	add edx, [ebp-80]
	mov [ebp-84], edx
	mov eax, [ebp-84]
	mov eax, [eax]
	push eax
	call printInt
	pop edx
	mov [ebp-88], eax
L14:
	mov eax, [ebp-8]
	mov ecx, 1
	add eax, ecx
	mov [ebp-92], eax
	mov ecx, [ebp-92]
	mov [ebp-8], ecx
	jmp L13
L12:
	mov eax, 0
	add esp, 92
	pop ebp
	ret
	add esp, 92
	pop ebp
	ret
section .data
arr TIMES 10 DD 0
