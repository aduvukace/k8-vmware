from pprint import pprint

import pyVmomi

from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Create import VM_Create
from k8_vmware.vsphere.VM_Task import VM_Task


class test_VM_Task(TestCase_VM):
    vm_name = f"tests__unit__" + __name__

    def setUp(self):
        self.vm_name = test_VM_Task.vm_name
        self.vm_task = VM_Task(vm=self.vm)

    def test__init__(self):
        assert type(self.vm_task.sdk) is Sdk
        assert self.vm_task.vm  == self.vm
        assert self.vm.name()   == self.vm_name

    def test_power_on__power_off(self):
        task_power_on  = self.vm_task.power_on()
        assert task_power_on.info.entityName     == self.vm_name
        assert task_power_on.info.state          == "success"
        assert task_power_on.info.name           == pyVmomi.vim.VirtualMachine.PowerOn
        assert task_power_on.info.descriptionId  == 'VirtualMachine.powerOn'
        assert str(task_power_on.info.entity)    == f"'vim.VirtualMachine:{self.vm.moid()}'"

        task_power_off = self.vm_task.power_off()
        assert task_power_off.info.entityName    == self.vm_name
        assert task_power_off.info.state         == "success"
        assert task_power_off.info.name          == pyVmomi.vim.VirtualMachine.PowerOff
        assert task_power_off.info.descriptionId == 'VirtualMachine.powerOff'

    def test_that_powered_on_vms_can_be_deleted(self):
        test_vm = VM_Create().create()
        test_vm.task().power_on()
        test_vm.task().delete()

        ### todo: re-add one self.sdk.tasks_recent() is faster (at the moment it can add 3 secs to the test execution
        ### test below shows the power of recent_tasks, but at the moment that method is highly inefficient
        ### so skipping this
        # vm_moid = test_vm.moid()
        # recent_tasks = self.sdk.tasks_recent()
        # last_task      = recent_tasks.pop()
        # event_chain_id = last_task['EventChainId']
        #
        # assert last_task == {'DescriptionId': 'ManagedEntity.destroy',
        #                      'Entity'       : f"vim.VirtualMachine:{vm_moid}",
        #                      'EventChainId' : event_chain_id,
        #                      'Key'          : f"haTask-{vm_moid}-vim.ManagedEntity.destroy-{event_chain_id}",
        #                      'State'        : 'success'}
