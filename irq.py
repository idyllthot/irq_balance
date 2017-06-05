#!/usr/bin/env python
# Filename irq.py

""" Standalone IRQ Balancing Script. """

__author__ = "Adam R. Dalhed"
__version__ = "0.0.1"

def set_affinity( my_irq, cpu_num ):
        my_irq_path='/proc/irq/%d/smp_affinity' %my_irq
        #my_affinity = open(my_irq_path,'w') #assumptions, needs testing
        #my_affinity.write(cpu_num + "\n")
        #my_affinity.close()

def sum_cpus(a1,a2):
        global b
        b=int(int(a1)+int(a2))


a_list=[]
cpu0_tot=0
cpu1_tot=0
cpu_tot=0
myproc=open("proc_interrupts","r")
for line in myproc:
	if line.find("eth") != -1:
		a=line.split()
		a0=int(a[0].rstrip(":"))
		sum_cpus(a[1],a[2])
		a_list.append([a0,b])
		cpu0_tot+=int(a[1])
		cpu1_tot+=int(a[2])
		cpu_tot+=b
myproc.close()	
cpu0_perc=100 * float(cpu0_tot)/float(cpu_tot)
cpu1_perc=100 * float(cpu1_tot)/float(cpu_tot)
a_list.sort(key=lambda x: x[1])
print("\n")
print(a_list)
n=1
new_cpu0_tot=0
new_cpu1_tot=0
new_cpu_tot=0
for a,b in a_list:
	if (n % 2) == 0:
		print("set affinity of %d with %d interrupts to cpu0") %(a,b)
		set_affinity(a,1)
		n=1
		new_cpu0_tot+=int(b)	
	else:
		print("set affinity of %d with %d interrupts to cpu1") %(a,b)
		set_affinity(a,2)
		n=2
		new_cpu1_tot+=int(b)	

new_cpu_tot=int(int(new_cpu0_tot)+int(new_cpu1_tot))
new_cpu0_perc=100 * float(new_cpu0_tot)/float(new_cpu_tot)
new_cpu1_perc=100 * float(new_cpu1_tot)/float(new_cpu_tot)

print("\nORIG CPU0 total  = %d (%d %%)") %(cpu0_tot,cpu0_perc)
print("ORIG CPU1 total  = %d (%d %%)") %(cpu1_tot,cpu1_perc)
print("ORIG Grand total = %d") %cpu_tot

print("\nNEW CPU0 total   = %d (%d %%)") %(new_cpu0_tot,new_cpu0_perc)
print("NEW CPU1 total   = %d (%d %%)") %(new_cpu1_tot,new_cpu1_perc)
print("NEW Grand total  = %d") %new_cpu_tot


