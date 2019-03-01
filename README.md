SROP
---------------------

Run make to compile the binaries.

## What is SROP?
https://adamt.rocks/SROP

## 32 bit

Syscall number is 0x77.

In our frame we want to pop a shell so...

* Need to return to an int 0x80 instruction (syscall)
* Need to have a pointer to "/bin/sh" in the ebx register
* Need to have eax set to the syscall number of sys_execve
* Need edx, edi to be NULL

A few simple gadgets and we have shell.

## 64 bit

Syscall number is 0xf

In our frame we want to very similarly pop a shell.

* Need to return to a syscall instruction
* Need to have the pointer to "/bin/sh" in the rdi register
* Need to have rax set to the syscall number
* Need rsi, rdx to be NULL

