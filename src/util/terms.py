__author__ = "George Exarchakos, Ilker Oztelcan, Dimitris Sarakiotis"
__version__ = "0.0.4"
__email__ = "g.exarchakos@tue.nl, i.oztelcan@tue.nl, d.sarakiotis@tue.nl"
__copyright__ = "Copyright 2014, The RICH Project"
#__credits__ = ["XYZ"]
#__maintainer__ = "XYZ"
#__license__ = "GPL"
#__status__ = "Production"

uri = {
	'RPL'		: "rpl",
	'RPL_NL'	: "rpl/nd",
	# 'RPL_OL'	: "rpl/c",
	'6TP'		: "6t",
	'6TP_6'		: "6t/6",
	'6TP_SF'	: "6t/6/sf",
	'6TP_CL'	: "6t/6/cl",
	#'6TP_SV'	: "6t/6/ml",
	'6TP_SM'	: "6t/6/sm",
	'RPL_DODAG'	: "rpl/dodag"
}

keys = {
	'SM_ID': "md",
	'SF_ID': "fd",
	'CL_ID': "cd",
	'S_OFF': "so",
	'C_OFF': "co",
	'LN_OP': "lo",
	'LN_TP': "lt",
	'TNA'  : "na",
	'MTRC' : "mt",
	'WNDW' : "wi",
	'RSSI' : "RSSI",
	'PDR'  : "pdr",
	'PRR'  : "PRR",
	'LQI'  : "LQI",
	'SLT'  : 'SLOT',
	'ETX'  : 'ETX'
}

cells = {
	'broadcast',
	'unicast'
}

resources = {
	'RPL': {
		'LABEL': 'rpl',
		'DAG': {
			'LABEL': 'dag',
			'PARENT': {'LABEL': 'parent'},
			'CHILD': {'LABEL': 'child'}
		}
	},
	'6TOP': {
		'LABEL': '6top',
		'SLOTFRAME': {
			'LABEL': 'slotFrame',
			'ID': {'LABEL':'frame'},
			'SLOTS': { 'LABEL':'slots'}
		},
		'CELLLIST': {
			'LABEL': 'cellList',
			'ID': {'LABEL':'link'},
			'SLOTFRAME': {'LABEL': 'frame'},
			'CHANNELOFFSET': {'LABEL': 'channel'},
			'SLOTOFFSET': {'LABEL': 'slot'},
			'LINKOPTION': {'LABEL': 'option'},
			'LINKTYPE': {'LABEL': 'type'},
			'TARGETADDRESS': {'LABEL': 'target'}
		},
		'NEIGHBOURLIST': {
			'LABEL': 'nbrList',
			'AGE':{ 'LABEL': 'age'}
		}
	}
}

def get_resource_uri(*uri):
	path = ''
	object = resources
	first_item = 1
	for rsrc in uri:
		if rsrc in object:
			if not first_item:
				path += '/'
			first_item = 0
			path += object[rsrc]['LABEL']
			parent = object
			object = object[rsrc]
		else:
			return None
	return path

def get_resource_queries(**queries):
	query = ''
	parent = None
	first_item = 1
	for k,v in queries.iteritems():
		if not first_item:
			query += '&'
		first_item = 0
		if k in object:
			query += object[k]['LABEL']+"="+str(v)
		elif k in parent:
			query += parent[k]['LABEL']+"="+str(v)
		else:
			return None
	return query