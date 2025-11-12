# Terminal Archaeology 🏺

## The Journey of "Hello World"

### In Python
```python
print("Hello")
```

### What Actually Happens:

1. **Python interpreter** calls `write()` syscall
   ```c
   write(1, "Hello\n", 6)  // fd 1 = stdout
   ```

2. **Kernel receives syscall**
   - Looks up file descriptor 1
   - It points to `/dev/pts/0` (your pseudo-terminal)

3. **TTY line discipline** processes it
   - Converts `\n` to `\r\n` (carriage return + line feed)
   - Handles special characters (Ctrl+C, etc.)
   - This is why Unix works!

4. **PTY master side** receives data
   - SSH daemon is waiting here
   - Reads: "Hello\r\n"

5. **SSH protocol** encrypts it
   - Wraps in SSH packet
   - Adds headers, checksums
   - Encrypts with AES or whatever

6. **Network stack** sends it
   - TCP segments
   - IP packets  
   - Ethernet frames
   - Wireless (if WiFi)

7. **Your Windows machine** receives packets
   - Network card
   - Windows TCP/IP stack
   - SSH client (OpenSSH or built-in)

8. **SSH client** decrypts
   - Extracts terminal data
   - Sends to Windows Terminal via ConPTY

9. **Windows Terminal** interprets
   - Parses escape sequences
   - Updates DirectX framebuffer
   - Renders using GPU

10. **Your monitor** displays pixels
    - "Hello" appears on screen!

**All of this in ~20 milliseconds!** 🤯
