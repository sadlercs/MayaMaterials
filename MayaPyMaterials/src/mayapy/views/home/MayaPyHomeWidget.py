# MayaPyHomeWidget.py


from PySide import QtGui
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget

from mayapy.enum.UserConfigEnum import UserConfigEnum
from mayapy.views.home.NimbleStatusElement import NimbleStatusElement

objectNum = -1

#___________________________________________________________________________________________________ MayaPyHomeWidget
class MayaPyHomeWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of MayaPyHomeWidget."""
        super(MayaPyHomeWidget, self).__init__(parent, **kwargs)
        self._firstView = True

        self.createButton.clicked.connect(self._handleCreateButton)

        self._statusBox, statusLayout = self._createElementWidget(self, QtGui.QVBoxLayout, True)
        statusLayout.addStretch()

        self._nimbleStatus = NimbleStatusElement(
            self._statusBox,
            disabled=self.mainWindow.appConfig.get(UserConfigEnum.NIMBLE_TEST_STATUS, True) )
        statusLayout.addWidget(self._nimbleStatus)
#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        if self._firstView:
            self._nimbleStatus.refresh()
            self._firstView = False

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCreateButton
    def _handleCreateButton(self):
        """
        This callback creates the Material to be used, and adds it to the object selected for import
        """
        #path = '../../apps/MayaPy/'
        path = '../assets/'
        matName = self.MaterialBox.currentText()
        objectName = self.ObjectBox.currentText()
        type = 'mayaAscii'

        #Import Object first then create shader to attach to it

        if matName == 'Ruby':
            newShader = mayaMRshader(matName, (0.614,0.041,0.041), 1.0, 1.0, (0.723,0.623,0.623), 1.0, 2.417, (0.723,0.623,0.623), (0.7,0.5,0.2), 0.5)
        if matName == 'Emerald':
            newShader = mayaMRshader(matName, (0.076,0.614,0.076), 1.0, 1.0, (0.633,0.728,0.633), 1.0, 1.6, (0.633,0.728,0.633), (0.7,0.5,0.2), 0.5)
        if matName == 'Diamond':
            newShader = mayaMRshader(matName, (0.723,0.945,1.0), 1.0, 1.0, (1.0,1.0,1.0), 1.0, 2.417, (1.0,1.0,1.0), (0.7,0.5,0.2), 0.5)
        if matName == 'Pearl':
            newShader = mayaMRshader(matName, (1.0,1.0,1.0), 1.0, 1.0, (1.0,0.829,0.829), 1.0, 2.417, (1.0,1.0,1.0), (0.7,0.5,0.2), 0.5)

        newShader.create()

        file = importFile(objectName, path, type)
        file.create()

        global objectNum
        objectNum = objectNum + 1
        cmds.select(objectName)
        cmds.rename(objectName + str(objectNum))

        cmds.hyperShade( a = matName + '1')




class mayaMRshader:
    """A Maya mental Ray shader class"""
    def __init__(self, name, diffuse, trans, refl_gloss, refl_color, refr_gloss, refr_ior, refr_color, refr_trans_color, refr_trans_weight,):
        self.name = name
        self.diffuse = diffuse
        self.trans = trans
        self.refl_gloss = refl_gloss
        self.refl_color = refl_color
        self.refr_gloss = refr_gloss
        self.refr_ior = refr_ior
        self.refr_color = refr_color
        self.refr_trans_color = refr_trans_color
        self.refr_trans_weight = refr_trans_weight

    def create(self):
        #checking if shader exists
        shadExist = 0
        allShaders = cmds.ls(mat=1)
        for shadeCheck in allShaders:
            if(shadeCheck == self.name + '1'):
                shadExist = 1

        if (shadExist == 0):

            cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=self.name)
            cmds.shadingNode('mia_material_x', asShader=True, name=self.name)

            self.name = self.name + '1'

            cmds.setAttr( self.name+".diffuse", self.diffuse[0], self.diffuse[1], self.diffuse[2])
            cmds.setAttr( self.name+".refl_color", self.refl_color[0], self.refl_color[1], self.refl_color[2])
            cmds.setAttr(self.name+".transparency", self.trans)
            cmds.setAttr( self.name+".refr_color", self.refr_color[0], self.refr_color[1], self.refr_color[2])
            cmds.setAttr( self.name+".refr_trans_color", self.refr_trans_color[0], self.refr_trans_color[1], self.refr_trans_color[2])
            cmds.setAttr(self.name+".refl_gloss", self.refl_gloss)
            cmds.setAttr(self.name+".refr_gloss", self.refr_gloss)
            cmds.setAttr(self.name+".refr_ior", self.refr_ior)
            cmds.setAttr(self.name+".refr_trans_weight", self.refr_trans_weight)


class importFile:
    """File import class"""
    def __init__(self, name, path, type,):
        self.name = name
        self.path = path
        self.type = type

    def create(self):
        cmds.file( self.path + self.name + '.ma', i=True, type=self.type)