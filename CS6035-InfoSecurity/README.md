# CS6035-Assignments
Assignments for CS-6035: Introduction to Info Security

**Useful Commands**

**system():** f7e0e040 (print system)

**/bin/sh:** f7f55338 (find &system,+9999999,"/bin/sh")

**exit:** f7e00990 (print exit)


**Check ASLR status:**

cat /proc/sys/kernel/randomize_va_space


**Turn off ASLR:**

echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
