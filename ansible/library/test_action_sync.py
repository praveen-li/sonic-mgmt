#!/usr/bin/python

from __future__ import print_function
from ansible.module_utils.basic import AnsibleModule

import shelve

DOCUMENTATION = '''
---
module: test_action_sync
version_added:
author: Praveen Chaudhary (pchaudhary@linkedin.com)

description:
    - this module will store below DB with information about topology,
    dut and server.
    - DB format: {
        current_topo: {
            name: "<topo_name>",
            "deploy-mg": "<True\False>"
        },
        actions : {
            success: [
                "add-topo <topo_name> <dut> <server>",
                "deploy-mg <topo_name> <dut> <server>",
                "run_test <test-name> <topo_name> <dut> <server>",
            ],
            failures: [
                "deploy-mg <topo_name> <dut> <server>",
                "run_test <topo_name> <dut> <server>",
                "run_test <test-name> <topo_name> <dut> <server>",
            ]
        }
    }
    - to start with current_topo will be None, or will not exist, or DB will
    not exist. All 3 will be treated as current_topo == None.
    - if action is add_topo, makes sure current_topo is None. Else fail. Fill
    new information with current_topo['deploy-mg'] is False.
    - if action is deploy-mg, makes sure current_topo['name'] == topo. Match
    dut and server too. Set current_topo['name'] == True.
    - run_test: Make Sure, deploy-mg it True.
    - remove-topo: makes sure current_topo['name'] == topo. Match
    dut and server too. Assign current_topo == None.
    - For each action, store it in either action['success'] or action['failures'].

    Note:
    - deply-mg may not ne necessary always after add topo, for that we can add
    avoid deply-mg parameter later.
'''

EXAMPLES = '''
 - name: test action sync
    test_action_sync: action={{ action }} topo={{ topo_name }} dut = {{ dut }}
        server = {{ server }} test_name={{ test_name}}
    connection: local
    register: test_action_sync
'''

class TestActionSync(object):
    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
              action=dict(required=True, type='str'),
              topo =dict(required=True, type='str'),
              dut=dict(required=True, type='str'),
              server=dict(required=True, type='str'),
              test_name=dict(required=False, type='str'),
            ),
            supports_check_mode=True)

        self.action = action
        self.topo = topo
        self.dut = dut
        self.server = server

        # class variables
        self.file = "actionDb"

        # Results
        self.result = None
        self.facts   =  {'test_action_sync': self.result}

        return

    def run(self):
        """
            Main method of the class

        """
        self.init()
        self.result = self.readFile()
        self.module.exit_json(ansible_facts=self.facts)

        return

    def readFile(self):
        """
            Function to read shelve DB file
        """
        db = None
        with shelve.open(self.file) as Db:
            db = Db;

        return db;

def main():
    testActionSync = TestActionSync()
    testActionSync.run()

    return

if __name__ == "__main__":
    main()
