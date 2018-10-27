CC=gcc

all :
	$(CC) -m32 srop_32.c -o srop32 -fno-stack-protector
	$(CC) srop_64.c -o srop64 -fno-stack-protector
