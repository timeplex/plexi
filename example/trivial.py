__author__ = "George Exarchakos"
__email__ = "g.exarchakos@tue.nl"
__version__ = "0.0.12"
__copyright__ = "Copyright 2015, The RICH Project"
#__credits__ = ["XYZ"]
#__maintainer__ = "XYZ"
#__license__ = "GPL"
#__status__ = "Production"

from example import main
from core.schedule import Scheduler, logg
from core.slotframe import Slotframe
from core.interface import BlockQueue, Command
from util import terms
import sys


class TrivialScheduler(Scheduler):
	def __init__(self, net_name, lbr_ip, lbr_port, prefix, visualizer):
		super(TrivialScheduler, self).__init__(net_name, lbr_ip, lbr_port, prefix, visualizer)

	def start(self):
		f1 = Slotframe("Broadcast-Frame", 25)
		self.frames[f1.name] = f1
		q = self.set_remote_frames(self.root_id, f1)
		q.push(self.set_remote_link(1, 0, f1, self.root_id, None, self.root_id))
		self.communicate(q)

		f2 = Slotframe("Unicast-Frame", 21)
		self.frames[f2.name] = f2
		self.communicate(self.set_remote_frames(self.root_id, f2))

		self.communicate(self.set_remote_statistics(self.root_id, {"mt":"[\"PRR\",\"RSSI\"]"}))

		super(TrivialScheduler, self).start()

	def connected(self, child, parent, old_parent=None):

		commands = []

		bcq = self.set_remote_frames(child, self.frames["Broadcast-Frame"])
		for c in self.frames["Broadcast-Frame"].cell_container:
			skip = False
			for new_command in bcq:
				if new_command.uri == terms.uri['6TP_CL'] and c.slot == new_command.payload['so'] and c.channel == new_command.payload['co'] and c.option == new_command.payload['lo'] and c.owner == new_command.to and c.type == new_command.payload['lt']:
					skip = True
			if skip:
				continue
			if c.tx == parent or c.tx in self.dodag.get_children(child):
				bcq.push(self.set_remote_link(c.slot, c.channel, self.frames["Broadcast-Frame"], c.tx, None, child))
		bso, bco = self.schedule(child, None, self.frames["Broadcast-Frame"])
		if bso is not None and bco is not None:
			bcq.push(self.set_remote_link(bso, bco, self.frames["Broadcast-Frame"], child, None))
		else:
			logg.critical("INSUFFICIENT BROADCAST SLOTS: new node " + str(child) + " cannot broadcast")
		commands.append(bcq)

		ucq = self.set_remote_frames(child, self.frames["Unicast-Frame"])
		for neighbor in [parent]+self.dodag.get_children(child):
			uso, uco = self.schedule(neighbor, child, self.frames["Unicast-Frame"])
			if uso is not None and uco is not None:
				ucq.push(self.set_remote_link(uso, uco, self.frames["Unicast-Frame"], neighbor, child))
			else:
				logg.critical("INSUFFICIENT UNICAST SLOTS: new node " + str(child) + " cannot receive from " + str(neighbor))
			uso, uco = self.schedule(child, neighbor, self.frames["Unicast-Frame"])
			if uso is not None and uco is not None:
				ucq.push(self.set_remote_link(uso, uco, self.frames["Unicast-Frame"], child, neighbor))
			else:
				logg.critical("INSUFFICIENT UNICAST SLOTS: new node " + str(child) + " cannot unicast to " + str(neighbor))
		commands.append(ucq)
		return commands

	def schedule(self, tx, rx, slotframe):
		max_slots = 0
		for frame in self.frames.values():
			if max_slots < frame.slots:
				max_slots = frame.slots
		so = None
		co = None
		for slot in range(1, max_slots):
			skip = False
			free_channels = set(range(16))
			for frame in self.frames.values():
				free_channels = free_channels.difference(self.interfere(slot, tx, rx, frame))
				if len(free_channels) == 0 or self.conflict(slot, tx, rx, frame):
					skip = True
					break
			if not skip:
				so = slot
				co = list(free_channels)[0]
				break

		return so,co

	def probed(self, node, resource, value):
		q = BlockQueue()
		q.push(Command('observe', node, terms.uri['6TP_SV'] + "/" + str(value)))
		q.block()
		return q


if __name__ == '__main__':
	x = main.get_user_input(None)
	if isinstance(x, main.UserInput):
		sch = TrivialScheduler(x.network_name, x.lbr, x.port, x.prefix, x.visualizer)
		sch.start()
		sys.exit(0)
	sys.exit(x)