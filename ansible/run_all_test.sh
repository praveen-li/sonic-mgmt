#for test in acl arp continuous_reboot decap ecn_wred everflow_testbed fib lldp link_flap mem_check mtu pfc_wd port_toggle reboot repeat_harness restart_swss restart_swss_service sensors service_acl snmp syslog crm
cd /var/jenkins/sonic-mgmt/ansible/
for test in arp continuous_reboot fib mem_check reboot repeat_harness restart_swss restart_swss_service
do
    echo "TESTRUN SUITE: $test"
    ./testbed-cli.sh run_tests vms-celdx10-t1 lab $test
done
