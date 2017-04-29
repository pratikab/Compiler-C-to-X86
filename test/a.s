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
	sub esp, 192
	mov ecx, 1
	mov [ebp-96], ecx
	mov ecx, 1
	mov [ebp-92], ecx
	mov ecx, 1
	mov [ebp-88], ecx
	mov ecx, 1
	mov [ebp-84], ecx
	mov ecx, 1
	mov [ebp-80], ecx
	mov ecx, 1
	mov [ebp-76], ecx
	mov ecx, 1
	mov [ebp-72], ecx
	mov ecx, 1
	mov [ebp-68], ecx
	mov ecx, 1
	mov [ebp-64], ecx
	mov ecx, 1
	mov [ebp-60], ecx
	mov ecx, 1
	mov [ebp-56], ecx
	mov ecx, 1
	mov [ebp-52], ecx
	mov ecx, 1
	mov [ebp-48], ecx
	mov ecx, 1
	mov [ebp-44], ecx
	mov ecx, 1
	mov [ebp-40], ecx
	mov ecx, 1
	mov [ebp-36], ecx
	mov ecx, 1
	mov [ebp-32], ecx
	mov ecx, 1
	mov [ebp-28], ecx
	mov ecx, 1
	mov [ebp-24], ecx
	mov ecx, 1
	mov [ebp-20], ecx
	mov ecx, 1
	mov [ebp-16], ecx
	mov ecx, 1
	mov [ebp-12], ecx
	mov ecx, 1
	mov [ebp-8], ecx
	mov ecx, 1
	mov [ebp-4], ecx
	mov ebx, [ebp-52]
	mov ecx, [ebp-56]
	add ebx, ecx
	mov [ebp-104], ebx
	mov ebx, [ebp-60]
	mov ecx, [ebp-64]
	add ebx, ecx
	mov [ebp-108], ebx
	mov ebx, [ebp-104]
	mov ecx, [ebp-108]
	add ebx, ecx
	mov [ebp-112], ebx
	mov eax, [ebp-80]
	mov ecx, [ebp-84]
	imul eax, ecx
	mov [ebp-116], eax
	mov eax, [ebp-76]
	mov ecx, [ebp-116]
	imul eax, ecx
	mov [ebp-120], eax
	mov eax, [ebp-92]
	mov ecx, [ebp-96]
	imul eax, ecx
	mov [ebp-124], eax
	mov eax, [ebp-88]
	mov ecx, [ebp-124]
	imul eax, ecx
	mov [ebp-128], eax
	mov eax, [ebp-120]
	mov ecx, [ebp-128]
	imul eax, ecx
	mov [ebp-132], eax
	mov ebx, [ebp-68]
	mov ecx, [ebp-72]
	add ebx, ecx
	mov [ebp-136], ebx
	mov eax, [ebp-132]
	mov ecx, [ebp-136]
	imul eax, ecx
	mov [ebp-140], eax
	mov ebx, [ebp-112]
	mov ecx, [ebp-140]
	add ebx, ecx
	mov [ebp-144], ebx
	mov ebx, [ebp-4]
	mov ecx, [ebp-8]
	add ebx, ecx
	mov [ebp-148], ebx
	mov eax, [ebp-32]
	mov ecx, [ebp-36]
	imul eax, ecx
	mov [ebp-152], eax
	mov eax, [ebp-28]
	mov ecx, [ebp-152]
	imul eax, ecx
	mov [ebp-156], eax
	mov ebx, [ebp-24]
	mov ecx, [ebp-156]
	add ebx, ecx
	mov [ebp-160], ebx
	mov ebx, [ebp-20]
	mov ecx, [ebp-160]
	add ebx, ecx
	mov [ebp-164], ebx
	mov ebx, [ebp-16]
	mov ecx, [ebp-164]
	add ebx, ecx
	mov [ebp-168], ebx
	mov ebx, [ebp-12]
	mov ecx, [ebp-168]
	add ebx, ecx
	mov [ebp-172], ebx
	mov eax, [ebp-44]
	mov ecx, [ebp-48]
	imul eax, ecx
	mov [ebp-176], eax
	mov eax, [ebp-40]
	mov ecx, [ebp-176]
	imul eax, ecx
	mov [ebp-180], eax
	mov eax, [ebp-172]
	mov ecx, [ebp-180]
	imul eax, ecx
	mov [ebp-184], eax
	mov ebx, [ebp-148]
	mov ecx, [ebp-184]
	add ebx, ecx
	mov [ebp-188], ebx
	mov ebx, [ebp-144]
	mov ecx, [ebp-188]
	add ebx, ecx
	mov [ebp-192], ebx
	mov ecx, [ebp-192]
	mov [ebp-100], ecx
	mov eax, [ebp-100]
	push eax
	call printInt
	pop edx
	pop ebp
	ret
