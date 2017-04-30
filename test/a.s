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
	sub esp, 308
	mov ecx, 0
	mov [ebp-32], ecx
	mov ecx, 2
	mov [ebp-4], ecx
	mov ecx, 2
	mov [ebp-8], ecx
	mov ecx, 2
	mov [ebp-12], ecx
	mov ecx, 2
	mov [ebp-16], ecx
	mov ecx, 0
	mov [ebp-20], ecx
L1:
	mov eax, [ebp-20]
	mov ecx, [ebp-4]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-84], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-84]
	mov ecx, 0
	cmp ebx, ecx
	je L0
	mov ecx, 0
	mov [ebp-24], ecx
L4:
	mov eax, [ebp-24]
	mov ecx, [ebp-8]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-88], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-88]
	mov ecx, 0
	cmp ebx, ecx
	je L3
	mov eax, [ebp-20]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-92], eax
	mov eax, [ebp-24]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-96], eax
	mov eax, [ebp-92]
	mov ecx, [ebp-96]
	add eax, ecx
	mov [ebp-100], eax
	mov eax, [ebp-100]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-104], eax
	mov edx, ebp
	sub edx, 48
	add edx, [ebp-104]
	mov [ebp-108], edx
	mov eax, [ebp-108]
	mov ecx, 1
	mov [eax], ecx
L5:
	mov eax, [ebp-24]
	mov ecx, 1
	add eax, ecx
	mov [ebp-112], eax
	mov ecx, [ebp-112]
	mov [ebp-24], ecx
	jmp L4
L3:
L2:
	mov eax, [ebp-20]
	mov ecx, 1
	add eax, ecx
	mov [ebp-116], eax
	mov ecx, [ebp-116]
	mov [ebp-20], ecx
	jmp L1
L0:
	mov ecx, 0
	mov [ebp-20], ecx
L7:
	mov eax, [ebp-20]
	mov ecx, [ebp-12]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-120], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-120]
	mov ecx, 0
	cmp ebx, ecx
	je L6
	mov ecx, 0
	mov [ebp-24], ecx
L10:
	mov eax, [ebp-24]
	mov ecx, [ebp-16]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-124], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-124]
	mov ecx, 0
	cmp ebx, ecx
	je L9
	mov eax, [ebp-20]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-128], eax
	mov eax, [ebp-24]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-132], eax
	mov eax, [ebp-128]
	mov ecx, [ebp-132]
	add eax, ecx
	mov [ebp-136], eax
	mov eax, [ebp-136]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-140], eax
	mov edx, ebp
	sub edx, 64
	add edx, [ebp-140]
	mov [ebp-144], edx
	mov eax, [ebp-144]
	mov ecx, 2
	mov [eax], ecx
L11:
	mov eax, [ebp-24]
	mov ecx, 1
	add eax, ecx
	mov [ebp-148], eax
	mov ecx, [ebp-148]
	mov [ebp-24], ecx
	jmp L10
L9:
L8:
	mov eax, [ebp-20]
	mov ecx, 1
	add eax, ecx
	mov [ebp-152], eax
	mov ecx, [ebp-152]
	mov [ebp-20], ecx
	jmp L7
L6:
	mov ecx, 0
	mov [ebp-20], ecx
L13:
	mov eax, [ebp-20]
	mov ecx, [ebp-4]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-156], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-156]
	mov ecx, 0
	cmp ebx, ecx
	je L12
	mov ecx, 0
	mov [ebp-24], ecx
L16:
	mov eax, [ebp-24]
	mov ecx, [ebp-16]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-160], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-160]
	mov ecx, 0
	cmp ebx, ecx
	je L15
	mov ecx, 0
	mov [ebp-28], ecx
L19:
	mov eax, [ebp-28]
	mov ecx, [ebp-12]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-164], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-164]
	mov ecx, 0
	cmp ebx, ecx
	je L18
	mov eax, [ebp-20]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-168], eax
	mov eax, [ebp-28]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-172], eax
	mov eax, [ebp-168]
	mov ecx, [ebp-172]
	add eax, ecx
	mov [ebp-176], eax
	mov eax, [ebp-176]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-180], eax
	mov edx, ebp
	sub edx, 48
	add edx, [ebp-180]
	mov [ebp-184], edx
	mov eax, [ebp-28]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-188], eax
	mov eax, [ebp-24]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-192], eax
	mov eax, [ebp-188]
	mov ecx, [ebp-192]
	add eax, ecx
	mov [ebp-196], eax
	mov eax, [ebp-196]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-200], eax
	mov edx, ebp
	sub edx, 64
	add edx, [ebp-200]
	mov [ebp-204], edx
	mov eax, [ebp-184]
	mov eax, [eax]
	mov ecx, [ebp-204]
	mov ecx, [ecx]
	imul eax, ecx
	mov [ebp-208], eax
	mov eax, [ebp-32]
	mov ecx, [ebp-208]
	add eax, ecx
	mov [ebp-212], eax
	mov ecx, [ebp-212]
	mov [ebp-32], ecx
L20:
	mov eax, [ebp-28]
	mov ecx, 1
	add eax, ecx
	mov [ebp-216], eax
	mov ecx, [ebp-216]
	mov [ebp-28], ecx
	jmp L19
L18:
	mov eax, [ebp-20]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-220], eax
	mov eax, [ebp-24]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-224], eax
	mov eax, [ebp-220]
	mov ecx, [ebp-224]
	add eax, ecx
	mov [ebp-228], eax
	mov eax, [ebp-228]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-232], eax
	mov edx, ebp
	sub edx, 80
	add edx, [ebp-232]
	mov [ebp-236], edx
	mov eax, [ebp-236]
	mov ecx, [ebp-32]
	mov [eax], ecx
	mov ecx, 0
	mov [ebp-32], ecx
L17:
	mov eax, [ebp-24]
	mov ecx, 1
	add eax, ecx
	mov [ebp-240], eax
	mov ecx, [ebp-240]
	mov [ebp-24], ecx
	jmp L16
L15:
L14:
	mov eax, [ebp-20]
	mov ecx, 1
	add eax, ecx
	mov [ebp-244], eax
	mov ecx, [ebp-244]
	mov [ebp-20], ecx
	jmp L13
L12:
	mov ecx, 0
	mov [ebp-20], ecx
L22:
	mov eax, [ebp-20]
	mov ecx, [ebp-4]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-248], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-248]
	mov ecx, 0
	cmp ebx, ecx
	je L21
	mov ecx, 0
	mov [ebp-24], ecx
L25:
	mov eax, [ebp-24]
	mov ecx, [ebp-16]
	cmp eax, ecx
	setl al
	movzx eax, al
	mov [ebp-252], eax
	xor ebx, ebx
	xor ecx, ecx
	mov ebx, [ebp-252]
	mov ecx, 0
	cmp ebx, ecx
	je L24
	mov eax, [ebp-20]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-260], eax
	mov eax, [ebp-24]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-264], eax
	mov eax, [ebp-260]
	mov ecx, [ebp-264]
	add eax, ecx
	mov [ebp-268], eax
	mov eax, [ebp-268]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-272], eax
	mov edx, ebp
	sub edx, 80
	add edx, [ebp-272]
	mov [ebp-276], edx
	mov edx, [ebp-276]
	mov ecx, [edx]
	mov [ebp-256], ecx
	mov eax, [ebp-20]
	mov ecx, 2
	imul eax, ecx
	mov [ebp-280], eax
	mov eax, [ebp-24]
	mov ecx, 1
	imul eax, ecx
	mov [ebp-284], eax
	mov eax, [ebp-280]
	mov ecx, [ebp-284]
	add eax, ecx
	mov [ebp-288], eax
	mov eax, [ebp-288]
	mov ecx, 4
	imul eax, ecx
	mov [ebp-292], eax
	mov edx, ebp
	sub edx, 80
	add edx, [ebp-292]
	mov [ebp-296], edx
	mov eax, [ebp-296]
	mov eax, [eax]
	push eax
	call printInt
	pop edx
	mov [ebp-300], eax
L26:
	mov eax, [ebp-24]
	mov ecx, 1
	add eax, ecx
	mov [ebp-304], eax
	mov ecx, [ebp-304]
	mov [ebp-24], ecx
	jmp L25
L24:
L23:
	mov eax, [ebp-20]
	mov ecx, 1
	add eax, ecx
	mov [ebp-308], eax
	mov ecx, [ebp-308]
	mov [ebp-20], ecx
	jmp L22
L21:
	mov eax, 0
	add esp, 308
	pop ebp
	ret
	add esp, 308
	pop ebp
	ret
