from maya import cmds
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as MPx

def show_my_window():

	if cmds.window('my_window', exists = True):
		cmds.deleteUI('my_window', window = True)

	win = cmds.window('my_window', title = 'Ghost', widthHeight = (640,480))
	cmds.showWindow(win)


class mainWindow(object):
	def __init__(self):
		self.window = 'base_window'
		self.title = 'Ghost'
		self.size = (512, 512)

	def create(self):
		if cmds.window(self.window, exists = True):
			cmds.deleteUI(self.window, window = True)
		self.window = cmds.window(self.window, title = self.title, widthHeight = self.size)
		self.common_menu()
		self.buttons()
		cmds.showWindow(self.window)

	def common_menu(self):
		self.edit_menu = cmds.menu(label = 'Edit')
		self.edit_menu_save = cmds.menu(label = 'Save Settings', command = self.save)

		self.help_menu = cmds.menu(label = 'Help')
		self.help_menu_item = cmds.menu(label = 'About', command = self.about)

	def buttons(self):
		self.ok_button = cmds.button(label = 'OK', command = self.ok_clicked)
		self.cancel_button = cmds.button(label = 'Cancel', command = self.cancel_clicked)

	def save(self, *args):
		print 'Save Settings'

	def about(self, *args):
		print 'About Page'

	def ok_clicked(self, *args):
		cmds.polySphere()

	def cancel_clicked(self, *args):
		cmds.deleteUI(self.window)

#QtGui and PySide

from PySide import QtGui, QtCore

class PyQtBaseWindow(QtGui.QDialog):

	def __init__(self, parent=None):
		super(PyQtBaseWindow, self).__init__(parent)
		#window set up
		self.setWindowTitle('Ghost Outliner')
		self.main_layout = QtGui.QVBoxLayout()
		self.setLayout(self.main_layout)
		#menu bar
		self.menu_bar = QtGui.QMenuBar()
		grail_menu = self.menu_bar.addMenu('Ghost It')
	
		#bottom buttons
		button_box = QtGui.QHBoxLayout()
		self.meshes_button = QtGui.QPushButton('Add Mesh')
		self.meshes_button.clicked.connect(self.meshes_clicked)
		self.ghost_button = QtGui.QPushButton('Ghost')
		self.ghost_button.clicked.connect(self.ghost_clicked)
		self.clear_button = QtGui.QPushButton('Clear')
		self.clear_button.clicked.connect(self.clear_clicked)
		self.colour_button = QtGui.QPushButton('Colour Select')
		self.colour_button.clicked.connect(self.colour_clicked)
		#layout
		self.main_layout.addWidget(self.menu_bar)
		self.main_layout.addLayout(button_box)
		self.main_layout.addWidget(self.meshes_button)
		self.main_layout.addWidget(self.ghost_button)
		self.main_layout.addWidget(self.clear_button)
		self.main_layout.addWidget(self.colour_button)
		
		
#first button will add all selected obj to the ghost outliner
	def meshes_clicked(self):
			
		print 'Mesh Added'
		
	
#second button will create the outline of the selected obj		
	def ghost_clicked(self):
		
		# create toon node
		if not cmds.objExists("bhGhostNode"):
			node = cmds.createNode( 'pfxToon', n='bhGhostNode')
			 
			# Setup toon Node
			cmds.setAttr("%s.overrideEnabled" % node, 1)
			cmds.setAttr("%s.overrideDisplayType" % node, 2)
			cmds.setAttr("%s.creaseLines" % node, 0)
			cmds.setAttr("%s.borderLines" % node, 0)
			cmds.setAttr("%s.displayPercent" % node, 100)
			
			cmds.setAttr("%s.lineWidth" % node, 0.1)
		
		items = cmds.ls()
		
		#get current selection
		selected = cmds.ls(selection=True)
		if len(selected) == 0:
			return
			
		for index in range(len(items)):	
			meshName = items[index] # selection mesh name index
			
			# check if object is selected
			if (meshName in cmds.listRelatives(selected)) == False:
				continue
			
			#Setup Connection
			cmds.duplicate(meshName, name='ghost')  
			cmds.connectAttr('%s.outMesh' % 'ghost', '%s.inputSurface[%i].surface' % ('bhGhostNode', index) )
			cmds.connectAttr('%s.worldMatrix[0]' % 'ghost', '%s.inputSurface[%i].inputWorldMatrix' % ('bhGhostNode', index) )
			cmds.setAttr("%s.visibility" % 'ghost', False )
			cmds.group(name='Ghost Group')
				
		#prevent toon shader selection  
		cmds.select( clear=True )
				
		ghostSelect()
			
		print 'Swayze'

		
#third button will delete all outlines from the screen
	def clear_clicked(self):
	
		#cmds.select(group='Ghost Group')
		#cmds.delete('Ghost Group')
		
		print 'Roadhouse'
	
	
#fourth button will allow you to select the color of the outline
	def colour_clicked(self):
		print 'Colour Wheel'


pq_ui = PyQtBaseWindow()
pq_ui.show()