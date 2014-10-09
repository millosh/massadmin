#!/usr/bin/python

import re, os, sys

# take IP and MAC addresses
# take df output for disks
# take /proc/cpuinfo for CPU
# take /proc/meminfo for RAM
# take software from netstat -nlt
## add generic software for GNU/Linux

ma_cmd = "./massadmin.py ./servers/millosh/servers.all ./jobs/cmd.py "
ma_scp = "./massadmin.py ./servers/millosh/servers.all ./jobs/scp_from_remote.py pass "

md_cmd = "mkdir data_for_report"
ip_cmd = "ifconfig > data_for_report/ifconfig.txt"
df_cmd = "df > data_for_report/df.txt"
cu_cmd = "cat /proc/cpuinfo > data_for_report/cpuinfo.txt"
me_cmd = "cat /proc/meminfo > data_for_report/meminfo.txt"
cp_cmd = "cp /etc/redhat-release data_for_report/"
ua_cmd = "uname -a > data_for_report/uname.txt"
cmds = md_cmd + '; ' + ip_cmd + '; ' + df_cmd + '; ' + cu_cmd + '; ' + me_cmd + '; ' + cp_cmd + '; ' + ua_cmd
exec_cmd = ma_cmd + "\"" + cmds + "\""
print exec_cmd
os.system(exec_cmd)

scp_cmd = ma_scp + "data_for_report/* ./var/millosh/report"
print scp_cmd
os.system(scp_cmd)

rm_cmd = ma_cmd + "\"rm -rf data_for_report\""
print rm_cmd
os.system(rm_cmd)
