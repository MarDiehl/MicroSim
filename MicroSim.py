#!usr/bin/python3
#!/bin/bash

print("Importing Files.......")
import sys
import os
import glob
from pathlib import Path
from xml.dom import minidom
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#from vtk.util import numpy_support


#importing PP tools
from resources.PP_tools.pptcount import *
from resources.PP_tools.frontvelocity import *
from resources.PP_tools.tipradius import *
from resources.PP_tools.front_undercooling import *

from resources.PP_tools.triple_point import *


print("Done")

validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[0-9.]+'))
validator2 = QtGui.QRegExpValidator(QtCore.QRegExp('^\d[0-9,.]+$'))
validator2e = QtGui.QRegExpValidator(QtCore.QRegExp('^\d[0-9,.e-+]+$'))
validatorName = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[A-Za-z0-9_-.]*$'))
validator2fill = QtGui.QRegExpValidator(QtCore.QRegExp(r'^\d{0-9}(\,\d{0-9})?$'))



class StartScreen(QDialog):
    def __init__(self):
        super(StartScreen,self).__init__()
        loadUi("resources/maincsreen.ui",self)
        self.setWindowTitle("NSM - MLab")
        self.logo.setStyleSheet("background-image : url(resources/img/MicroSim2.png)")
        self.logo_2.setStyleSheet("background-image : url(resources/img/MicroSim2.png)")

        #icons for MainFrame
        self.sideBtn1.setIcon(QtGui.QIcon('resources/img/favicon.png'))
        self.sideBtn2.setIcon(QtGui.QIcon('resources/img/phases.png'))
        self.sideBtn3.setIcon(QtGui.QIcon('resources/img/time.png'))
        self.sideBtn4.setIcon(QtGui.QIcon('resources/img/nacl.png'))
        self.sideBtn5.setIcon(QtGui.QIcon('resources/img/shape.png'))
        self.sideBtn6.setIcon(QtGui.QIcon('resources/img/domain.png'))
        self.sideBtn7.setIcon(QtGui.QIcon('resources/img/pngegg.png'))
        self.sideInfileBtn.setIcon(QtGui.QIcon('resources/img/previous.png'))
        self.createN.setIcon(QtGui.QIcon('resources/img/createnew2.png'))
        self.importF.setIcon(QtGui.QIcon('resources/img/import3.png'))
        self.continueF.setIcon(QtGui.QIcon('resources/img/edit.png'))
        self.postProcessingF.setIcon(QtGui.QIcon('resources/img/postProcessing.png'))
        
        
        #post Processing Hide And Show
    
        self.SimulationDetail.hide()
        self.imgShow.hide()
        self.pptPlot.hide()
        self.PPpause.hide()
        self.pptRadius.hide()
        self.table_plot_widget.hide()
        self.drawLineWidget.hide()
        self.velocity_DrawLineWidget.hide()
        self.h5tovtk_Screen.hide()
        self.PPimage_widge.hide()
        self.PPexport_widge.hide()
        self.triple_point_widget.hide()
        
        self.ppToolwidget.setEnabled(False)
        
        #icons for post processing
        self.PPhome.setIcon(QtGui.QIcon('resources/img/Mlogo.png'))
        self.PPimport.setIcon(QtGui.QIcon('resources/img/file.png'))
        self.PPimage.setIcon(QtGui.QIcon('resources/img/picture.png'))
        self.PPexport.setIcon(QtGui.QIcon('resources/img/export.png'))
        self.PPimportData.setIcon(QtGui.QIcon('resources/img/import.png'))
        self.PP_clear.setIcon(QtGui.QIcon('resources/img/remove.png'))
        self.pptarea.setIcon(QtGui.QIcon('resources/img/area.png'))
        self.pptcount.setIcon(QtGui.QIcon('resources/img/abacus.png'))
        self.pptsize.setIcon(QtGui.QIcon('resources/img/pptsize.png'))
        self.fastNext.setIcon(QtGui.QIcon('resources/img/fastNext.png'))
        self.nextView.setIcon(QtGui.QIcon('resources/img/nextView.png'))
        self.preView.setIcon(QtGui.QIcon('resources/img/preView.png'))
        self.fastPre.setIcon(QtGui.QIcon('resources/img/fastPre.png'))
        self.PPplay.setIcon(QtGui.QIcon('resources/img/play.png'))
        self.PPreload.setIcon(QtGui.QIcon('resources/img/reload.png'))
        self.xyPLane.setIcon(QtGui.QIcon('resources/img/xyPlane.png'))
        self.yzPlane.setIcon(QtGui.QIcon('resources/img/yzPlane.png'))
        self.xzPlane.setIcon(QtGui.QIcon('resources/img/xzPlane.png'))
        
        self.tip_radiusbtn.setIcon(QtGui.QIcon('resources/img/tipradius.png'))
        self.pptplot_import.setIcon(QtGui.QIcon('resources/img/down.png'))
        self.surfaceAreabtn.setIcon(QtGui.QIcon('resources/img/particle.png'))
        self.total_vol_btn.setIcon(QtGui.QIcon('resources/img/3dvolume.png'))
        self.phase_frac_btn.setIcon(QtGui.QIcon('resources/img/Phasefrac.png'))
        self.draw_Line.setIcon(QtGui.QIcon('resources/img/resize.png'))
        self.velocity_OverLine.setIcon(QtGui.QIcon('resources/img/zigzag-line.png'))
        self.fVelocitybtn.setIcon(QtGui.QIcon('resources/img/zigzag.png'))
        self.front_undercoolbtn.setIcon(QtGui.QIcon('resources/img/layers.png'))
        
        #post processing Animation
        
        self.anim_h5toVTK = QtCore.QPropertyAnimation(self.h5tovtk_Screen, b"pos")
        self.anim_h5toVTK.setStartValue(QtCore.QPoint(230, 30))
        self.anim_h5toVTK.setEndValue(QtCore.QPoint(230,0))
        self.anim_h5toVTK.setDuration(200)
        
        self.anim_PPimage = QtCore.QPropertyAnimation(self.PPimage_widge, b"pos")
        self.anim_PPimage.setStartValue(QtCore.QPoint(360, 30))
        self.anim_PPimage.setEndValue(QtCore.QPoint(360,0))
        self.anim_PPimage.setDuration(200)
        
        
        self.anim_PPexport = QtCore.QPropertyAnimation(self.PPexport_widge, b"pos")
        self.anim_PPexport.setStartValue(QtCore.QPoint(360, 30))
        self.anim_PPexport.setEndValue(QtCore.QPoint(360,0))
        self.anim_PPexport.setDuration(200)
        
        
        #all graph declaration
        
        self.fig_ppt = plt.figure(facecolor='#77767B')
        self.canvas_ppt = FigureCanvas(self.fig_ppt)
        self.toolbar_ppt = NavigationToolbar(self.canvas_ppt, self)
        self.verticalLayout_ppt2.addWidget(self.toolbar_ppt)
        self.verticalLayout_ppt.addWidget(self.canvas_ppt)
        
        
        self.fig_table = plt.figure()  #For Post processing 77767B
        self.fig_table.tight_layout()
        self.canvas_table = FigureCanvas(self.fig_table)
        # adding canvas to the layout
        self.toolbar_table = NavigationToolbar(self.canvas_table, self)
        self.table_plot2.addWidget(self.toolbar_table)
        self.table_plot.addWidget(self.canvas_table)
        
        
        
        self.figure = plt.figure(facecolor='#77767B')  #For Post processing 77767B
        self.canvas = FigureCanvas(self.figure)
        # adding canvas to the layout
        self.verticalLayout.addWidget(self.canvas)
        #self.canvas.mpl_connect('button_press_event',onclick)
        
        
        self.ppt_Count_Plot_flag = 0;
        self.ppt_size_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.infileLoad_Flag = 0
        self.vtkLoad_flag = 0
        
        
        #for 3D ploting
        self.data_3D_flag = 0
        self.yzplane_flag = 0
        self.xyplane_flag = 0
        self.xzplane_flag = 0


        #post processing click action
        self.PPimport.clicked.connect(self.PPimportClicked)
        self.PPimportData.clicked.connect(self.PPimportDataClicked)
        self.h5tovtkbtn.clicked.connect(self.h5tovtkbtnClicked)
        self.h5tovtkClose.clicked.connect(self.h5tovtkCloseClicked)
        self.h5tovtk_infilebtn.clicked.connect(self.h5tovtk_infilebtnClicked)
        self.h5tovtk_outputbtn.clicked.connect(self.h5tovtk_outputbtnClicked)
        self.h5tovtk_vtkoutputbtn.clicked.connect(self.h5tovtk_vtkoutputbtnClicked)
        self.h5tovtk_convert.clicked.connect(self.h5tovtk_convertClicked)
        
        self.PPimage.clicked.connect(self.PPimageClicked)
        self.PPimageClose.clicked.connect(self.PPimageCloseClicked)        
        self.PPimageLocbtn.clicked.connect(self.PPimageLocbtnClicked)
        self.PPimageConvert.clicked.connect(self.PPimageConvertClicked)
        
        self.PPexport.clicked.connect(self.PPexportClicked)
        self.PPexportClose.clicked.connect(self.PPexportCloseClicked)        
        self.PPexportLocbtn.clicked.connect(self.PPexportLocbtnClicked)
        self.PPexportConvert.clicked.connect(self.PPexportConvertClicked)
        
        self.PP_clear.clicked.connect(self.PP_clearClicked)


        self.fastNext.clicked.connect(self.fastNextClicked)
        self.fastPre.clicked.connect(self.fastPreClicked)
        self.nextView.clicked.connect(self.nextViewClicked)
        self.preView.clicked.connect(self.preViewClicked)
        self.PPreload.clicked.connect(self.PPreloadClicked)
        self.PPplay.clicked.connect(self.PPplayClicked)
        self.PPpause.clicked.connect(self.PPpauseClicked)
        self.draw_Line.clicked.connect(self.draw_LineClicked)
        self.plot_over_lineBtn.clicked.connect(self.plot_over_lineClicked)
        self.pptplot_import.clicked.connect(self.pptplot_importClicked)
        self.xyPLane.clicked.connect(self.xyPLaneClicked)
        self.yzPlane.clicked.connect(self.yzPlaneClicked)
        self.xzPlane.clicked.connect(self.xzPlaneClicked)

        
        self.pptcount.clicked.connect(self.pptcountClicked)
        self.pptsize.clicked.connect(self.pptsizeClicked)
        self.pptarea.clicked.connect(self.pptareaClicked)
        self.fVelocitybtn.clicked.connect(self.fVelocitybtnClicked)
        self.velocity_OverLine.clicked.connect(self.velocity_OverLineClicked)
        self.tip_radiusbtn.clicked.connect(self.tip_radiusbtnClicked)
        self.front_undercoolbtn.clicked.connect(self.front_undercoolbtnClicked)
        self.triple_pointbtn.clicked.connect(self.triple_pointbtnClicked)
        
        
        self.exportToCSV.clicked.connect(self.exportToCSVClicked)
        self.plotwrtTime.clicked.connect(self.plotwrtTimeClicked)
        self.plotwrtTimeAll.clicked.connect(self.plotwrtTimeAllClicked)
        self.table_close.clicked.connect(self.table_closeClicked)
        self.velocity_Plot_over_lineBtn.clicked.connect(self.velocity_Plot_over_lineBtnClicked)
        
        self.phase_frac_btn.clicked.connect(self.phasefracClicked)
        self.surfaceAreabtn.clicked.connect(self.surfaceAreabtnClicked)
        self.total_vol_btn.clicked.connect(self.total_vol_btnClicked)

        self.iteration_step.valueChanged.connect(self.plotfig)
        self.depth_plot.valueChanged.connect(self.plotFig_3d)
        #self.POL_start.textChanged.connect(self.draw_line_on_Sim)
        #self.POL_end.textChanged.connect(self.draw_line_on_Sim)
        
        self.scalerValue.currentIndexChanged.connect(self.plotfig)


        #disabling esc key
        QtWidgets.QShortcut(QtGui.QKeySequence("Escape"), self, activated=self.on_Escape)

        #RESTRICTING STRING INPUT
        self.mesh_x.setValidator(validator)
        self.mesh_y.setValidator(validator)
        self.mesh_z.setValidator(validator)
        self.dx.setValidator(validator2e)
        self.dy.setValidator(validator2e)
        self.dz.setValidator(validator2e)
        self.dt.setValidator(validator2e)
        self.timeSteps.setValidator(validator)
        self.saveAt.setValidator(validator)
        self.Nsmooth.setValidator(validator)
        self.startTime.setValidator(validator)
        self.numWorkers.setValidator(validator)
        self.R_Value.setValidator(validator2e)
        self.V_Value.setValidator(validator2e)
        self.BC_1.setValidator(validator)
        self.BC_2.setValidator(validator)
        self.BC_3.setValidator(validator)
        self.BC_4.setValidator(validator)
        self.diffInput.setValidator(validator2e)
        self.Estrain.setValidator(validator2)
        self.Econstant.setValidator(validator2)
        self.gammaInput.setValidator(validator2e)
        
        ##Post Processing validator
        self.POL_start.setValidator(validator2)
        self.POL_end.setValidator(validator2)
        self.h5tovtk_sTime.setValidator(validator)
        self.h5tovtk_eTime.setValidator(validator)
        self.PPimagedir.setValidator(validator)
        self.PPexportdir.setValidator(validator)

        #for DomainFilling

        self.cube_end.setValidator(validator2)
        self.cube_start.setValidator(validator2)
        self.cylinder_center.setValidator(validator2)
        self.cylinder_radius.setValidator(validator)
        self.cylinder_zend.setValidator(validator)
        self.cylinder_zstart.setValidator(validator)
        self.ellipse_center.setValidator(validator2)
        self.ellipse_eccentric.setValidator(validator)
        self.ellipse_majorAxis.setValidator(validator)
        self.ellipse_rotation.setValidator(validator)
        self.sphere_center.setValidator(validator2)
        self.sphere_radius.setValidator(validator)


        ##GP Validator
        self.trackProgressGP.setValidator(validator)
        self.epsilonGP.setValidator(validator2e)
        self.tauGP.setValidator(validator2e)
        self.FanisotropyGP.setValidator(validator2e)
        self.anisotropyTypeGP.setValidator(validator)
        self.funcWGP.setValidator(validator)
        self.shiftJGP.setValidator(validator2e)
        self.equTGP.setValidator(validator2e)
        self.fillingTGP.setValidator(validator2e)
        self.TGP.setValidator(validator2e)
        self.ampNoiseGP.setValidator(validator)
        self.writecompGP.setValidator(validator)


        self.TauGP.setValidator(validator2)
        self.debGP.setValidator(validator2)
        self.gammaABCGP.setValidator(validator2)
        self.tempgradyGP.setValidator(validator2)


        #CH Validator
        self.trackProgressCH.setValidator(validator)

        self.lPhiCH.setValidator(validator2)
        self.kappaPhiCH.setValidator(validator2)
        self.kappaCCH.setValidator(validator2)
        self.afmCH.setValidator(validator2)
        self.bfpCH.setValidator(validator2)

        self.infile.setValidator(validatorName)
        self.filling.setValidator(validatorName)
        self.output.setValidator(validatorName)

        #hinding Widget and Frames
        self.frame_2.hide()
        self.pwidget.hide()
        self.pwidget_2.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.hide()
        self.widgetGamma.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        self.Func2.hide()
        self.shapeUpdate.hide()
        self.w1.hide()
        self.continueTab.hide()
        self.continueF.hide()
        self.paraviewError.hide()

        self.widgetGammaABC.hide()

        self.postProcessingScreen.hide()
       

        #start ScreenFrame
        self.openFile.clicked.connect(self.openFileDir)
        self.startNew.clicked.connect(self.startNewClicked)
        self.createN.clicked.connect(self.startNewClicked)
        self.continueTab.clicked.connect(self.continueTabClicked)
        self.continueF.clicked.connect(self.continueTabClicked)
        self.importFile.clicked.connect(self.importFileClicked)
        self.importF.clicked.connect(self.importFileClicked)
        self.close_btn.clicked.connect(self.close_btnClicked)
        self.sideInfileBtn.clicked.connect(self.sideInfileBtnClicked)
        self.postProcessing.clicked.connect(self.postProcessingClicked)
        self.postProcessingF.clicked.connect(self.postProcessingClicked)
        self.PPhome.clicked.connect(self.PPhomeClicked)


        #shape frame
        self.shapeframe.hide()
    
        #Btn click action
        self.btn1.clicked.connect(self.clickedBtn1)
        self.sideBtn1.clicked.connect(self.clickedBtn1)
        self.btn2.clicked.connect(self.clickedBtn2)


        self.next1.clicked.connect(self.NextBtn1)
        self.sideBtn2.clicked.connect(self.NextBtn1)


        self.next2.clicked.connect(self.NextBtn2)
        self.sideBtn3.clicked.connect(self.NextBtn2)


        self.next3.clicked.connect(self.NextBtn3)
        self.sideBtn4.clicked.connect(self.NextBtn3)

        self.btn3.clicked.connect(self.clickedBtn3)
        self.btn4.clicked.connect(self.clickedBtn4)
        self.btn41.clicked.connect(self.clickedBtn41)
        self.btn42.clicked.connect(self.clickedBtn42)

        self.next4.clicked.connect(self.NextBtn4)
        self.sideBtn5.clicked.connect(self.NextBtn4)

        self.next5.clicked.connect(self.NextBtn5)
        self.sideBtn6.clicked.connect(self.NextBtn5)

        self.next6.clicked.connect(self.NextBtn6)
        self.sideBtn7.clicked.connect(self.NextBtn6)

        self.btn5.clicked.connect(self.clickedBtn5)
        self.next7.clicked.connect(self.clickedBtn6)
        self.btn6.clicked.connect(self.clickedBtn6)
        self.btn7.clicked.connect(self.clickedBtn7)


        #action on mesh change4
        self.mesh_x.textChanged.connect(self.drawMesh)

        #action on mesh change
        self.mesh_y.textChanged.connect(self.drawMesh)

        #action on mesh change
        self.dx.textChanged.connect(self.draw_dx)

        #action on mesh change
        self.dy.textChanged.connect(self.draw_dy)
  

        #Changing Phases
        self.phasebtn.clicked.connect(self.phaseBtnClicked)
        self.phasesavebtn.clicked.connect(self.phaseSaveBtnClicked)

        #Changing Components
        self.componentbtn.clicked.connect(self.componentBtnClicked)
        self.comsavebtn.clicked.connect(self.componentSaveBtnClicked)

        self.GP_next.clicked.connect(self.GPnextClicked)
        self.GP_pre.clicked.connect(self.GPpreClicked)
        self.saveGP.clicked.connect(self.saveGPClicked)
        self.saveGP.hide()

        self.KKS_next.clicked.connect(self.KKSnextClicked)
        self.KKS_pre.clicked.connect(self.KKSpreClicked)
        self.saveKKS.clicked.connect(self.saveKKSClicked)
        #self.saveKKS.show()

        self.KKS2_next.clicked.connect(self.KKS2nextClicked)
        self.KKS2_pre.clicked.connect(self.KKS2preClicked)
        self.saveKKS2.clicked.connect(self.saveKKS2Clicked)
        self.saveKKS2.hide()

        self.CH_next.clicked.connect(self.CHnextClicked)
        self.CH_pre.clicked.connect(self.CHpreClicked)
        self.saveCH.clicked.connect(self.saveCHClicked)

        self.tableWidgetCHA.itemClicked.connect(self.tableItemClickedCHA)
        self.saveCH.hide()

        self.finish.clicked.connect(self.clickedfinish)
        self.runBtn.clicked.connect(self.clickedrunBtn)
        self.preview.clicked.connect(self.clickedpreview)
        self.paraviewErrorClose.clicked.connect(self.paraviewErrorCloseClicked)
        self.paraviewCancel.clicked.connect(self.paraviewErrorCloseClicked)
        self.paraviewBrowse.clicked.connect(self.paraviewBrowseClicked)
        self.paraviewOpen.clicked.connect(self.paraviewOpenClicked)
        self.PPbutton.clicked.connect(self.PPbuttonClicked)

        #Boundary Conditions
        self.BCV_1.cursorPositionChanged.connect(self.BCV1fill)
        self.BCV_2.cursorPositionChanged.connect(self.BCV2fill)
        self.BCV_3.cursorPositionChanged.connect(self.BCV3fill)
        self.BCV_4.cursorPositionChanged.connect(self.BCV4fill)

        #shadow
        shadow = QtWidgets.QGraphicsDropShadowEffect(self,
                                                     blurRadius=10.0,
                                                     color=QtGui.QColor (63, 63, 63, 180),
                                                     offset=QtCore.QPointF(3.0, 3.0)
                                                     )
        self.frame_1.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_2.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_4.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_5.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_6.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_61.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_62.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_7.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_8.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_9.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_10.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.frame_11.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 4.0)))
        self.ShapeList.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 3.0)))
        self.shapeframe.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(3.0, 3.0)))
        self.startNew.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.continueTab.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.importFile.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.postProcessing.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.w1.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 3.0)))
        self.paraviewError.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 3.0)))
        self.createN.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(6.0, 6.0)))
        self.continueF.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(6.0, 6.0)))
        self.importF.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(6.0, 6.0)))
        self.postProcessingF.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(6.0, 6.0)))
        self.pwidget.setGraphicsEffect(shadow)
        self.pwidget_2.setGraphicsEffect(shadow)
        self.Qbox.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=10.0,color=QtGui.QColor (76,35,45, 180),offset=QtCore.QPointF(2.0, -2.0)))
        self.table_plot_widget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.h5tovtk_Screen.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.PPimage_widge.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))
        self.PPexport_widge.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(self,blurRadius=14.0,color=QtGui.QColor (63, 63, 63, 180),offset=QtCore.QPointF(4.0, 4.0)))


        #Animations
        #self.anim1 = QPropertyAnimation(self.StartFrame, b"pos")
        #self.anim1.setEndValue(QPoint(0, 600))
        #self.anim1.setDuration(400)

        #self.anim2 = QPropertyAnimation(self.w1, b"geometry")
        #self.anim2.setEndValue(QRect(240, 150, 530, 300))
        #self.anim2.setDuration(200)

        self.anim12 = QtCore.QPropertyAnimation(self.w1, b"pos")
        self.anim12.setStartValue(QtCore.QPoint(280, 160))
        self.anim12.setEndValue(QtCore.QPoint(280,180))
        self.anim12.setDuration(300)

        
        #VALUE CHANGE ACTION
        self.dim.valueChanged.connect(self.updateDim)
        self.Qbox.hide()
        self.reStart.valueChanged.connect(self.reStartFun)

        self.noP.valueChanged.connect(self.updateNoP)
        self.noP.lineEdit().setReadOnly(True)
        self.noC.valueChanged.connect(self.updateNoC)
        self.shiftGP.valueChanged.connect(self.updateshiftGP)
        self.shiftKKS2.valueChanged.connect(self.updateshiftKKS2)
        self.tdbflagCH.valueChanged.connect(self.updatetdbflag)
        self.funcF.valueChanged.connect(self.funcFflag)

        self.noiseGP.valueChanged.connect(self.updatenoiseGPflag)
        #self.noiseKKS.valueChanged.connect(self.updatenoiseKKSflag)
        self.noiseKKS2.valueChanged.connect(self.updatenoiseKKS2flag)


        self.diffInput.textChanged.connect(self.FillDiffMat)
        self.gammaInput.textChanged.connect(self.FillGammaMat)
        self.gammaABCGP.textChanged.connect(self.FillGammaABC)
        self.pDropdown.currentIndexChanged.connect(self.phaseChange)
        self.pDropdown_2.currentIndexChanged.connect(self.phaseChange_BC)

        #for boundary condition
        self.BC_1.highlighted.connect(self.BCV1fill)
        self.BC_2.highlighted.connect(self.BCV2fill)
        self.BC_3.highlighted.connect(self.BCV3fill)
        self.BC_4.highlighted.connect(self.BCV4fill)


        self.BC_1.currentIndexChanged.connect(self.BCV1Change)
        self.BC_2.currentIndexChanged.connect(self.BCV2Change)
        self.BC_3.currentIndexChanged.connect(self.BCV3Change)
        self.BC_4.currentIndexChanged.connect(self.BCV4Change)

        self.BC_1.model().item(0).setEnabled(False)
        self.BC_1.model().item(2).setEnabled(False)
        self.BC_1.model().item(4).setEnabled(False)

        self.BC_2.model().item(0).setEnabled(False)
        self.BC_2.model().item(2).setEnabled(False)
        self.BC_2.model().item(4).setEnabled(False)

        self.BC_3.model().item(0).setEnabled(False)
        self.BC_3.model().item(2).setEnabled(False)
        self.BC_3.model().item(4).setEnabled(False)

        self.BC_4.model().item(0).setEnabled(False)
        self.BC_4.model().item(2).setEnabled(False)
        self.BC_4.model().item(4).setEnabled(False)
        self.startTime.setEnabled(False) ## ReStart Parameter

        self.allCheck_2.hide()

        #DOmain Filling
        self.shape.currentIndexChanged.connect(self.domainShapeChange)
        self.pDropdown_3.currentIndexChanged.connect(self.domainPhaseChange)
        self.addShape.clicked.connect(self.shapeframeToggle)
        self.shapeCancel.clicked.connect(self.shapeCancelClicked)
        self.shapeframeclose.clicked.connect(self.shapeCancelClicked)
        self.shapeSave.clicked.connect(self.shapeSaveClicked)
        self.shapeUpdate.clicked.connect(self.shapeUpdateClicked)
        self.shapeedit.clicked.connect(self.shapeeditClicked)
        self.shapedelete.clicked.connect(self.shapedeleteClicked)
        self.addShapeFile.clicked.connect(self.addShapeFileClicked)


        self.cubeIcon.setPixmap(QtGui.QPixmap("resources/img/cube.JPG"))
        self.cylinderIcon.setPixmap(QtGui.QPixmap("resources/img/cylinder.JPG"))
        self.ellipseIcon.setPixmap(QtGui.QPixmap("resources/img/ellipse.png"))
        self.sphereIcon.setPixmap(QtGui.QPixmap("resources/img/sphere.png"))
        self.RsphereIcon.setPixmap(QtGui.QPixmap("resources/img/RandomS.png"))
        self.RcylinderIcon.setPixmap(QtGui.QPixmap("resources/img/corsening.png"))
        self.ashokchakra.setPixmap(QtGui.QPixmap("resources/img/ashokchakra.png"))
        self.background.setPixmap(QtGui.QPixmap("resources/img/backImage.png"))
        self.background2.setPixmap(QtGui.QPixmap("resources/img/back2.png"))

        #radio toggled
        self.diffR.toggled.connect(self.fMatrixToggled)
        self.diffR_2.toggled.connect(self.dMatrixToggled)
        self.allCheck.toggled.connect(self.allCheckFunc)

        self.radio_GP.toggled.connect(self.radio_GPToggled)
        self.radio_CH.toggled.connect(self.radio_CHToggled)
        self.radio_KKR.toggled.connect(self.radio_KKRToggled)
        self.radio_KKS2.toggled.connect(self.radio_KKS2Toggled)
        self.thermalYGP.toggled.connect(self.radio_thermalYGPToggled)
        self.thermalNGP.toggled.connect(self.radio_thermalNGPToggled)
        self.thermalYKKS2.toggled.connect(self.radio_thermalYKKS2Toggled)
        self.thermalNKKS2.toggled.connect(self.radio_thermalNKKS2Toggled)


        self.es.clicked.connect(self.esToggled)
        self.es_2.clicked.connect(self.es2Toggled)
        self.es_3.clicked.connect(self.es3Toggled)

        self.allCheck_2.toggled.connect(self.allCheckBC)
        self.allCheck_BC.toggled.connect(self.allCheckBCV)


        #important Initializations
        grid = QGridLayout()
        self.diffMat.setLayout(grid)

        self.Diffusivity = []
        self.DiffusivityType = []
        self.eigenStrain = []
        self.elasticConstant = []
        self.elasticType = []

        self.Bcnd = [""]*4
        self.BconV = [""]*4
        self.ShapeFlag = 0

        self.domainType = []
        self.domainValue =[]

        if self.noP.value() == 1:
            self.pDropdown.addItem("alpha")
            self.Diffusivity.append("")
            self.DiffusivityType.append("")
            self.eigenStrain.append("")
            self.elasticConstant.append("")
            self.elasticType.append("")

            self.pDropdown_3.addItem("alpha")
            self.domainType.append("")
            self.domainValue.append("")

        header = self.tableWidgetGP.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidgetGP.setColumnHidden(5,True)
        '''
        headerKKS = self.tableWidgetKKS.horizontalHeader()
        headerKKS.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        headerKKS.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        headerKKS2 = self.tableWidgetKKS2.horizontalHeader()
        headerKKS2.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        headerKKS2.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        headerCH = self.tableWidgetCH.horizontalHeader()
        headerCH.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        headerCH.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        '''

        headerCHA = self.tableWidgetCHA.horizontalHeader()
        headerCHA.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        headerCHA.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        
        
        #setting table column names
        self.tableWidgetGPA.setHorizontalHeaderLabels(['Phases', 'A'])
        
        
        ##post processing
        self.table_ppt_size.setColumnHidden(1, True)
        headerPPT = self.table_ppt_size.horizontalHeader()
        headerPPT.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) 
        


    @QtCore.pyqtSlot()
    def on_Escape(self):
        return

    def importFileClicked(self):
        self.model_CH.setChecked(False)
        self.model_GP.setChecked(False)
        self.model_KKS.setChecked(False)
        self.model_KKS2.setChecked(False)
        self.w1.show()
        self.anim12.start()

    def close_btnClicked(self):
        self.w1.hide()

    def sideInfileBtnClicked(self):
        self.StartFrame.show()
        self.continueTab.show()
        self.continueF.show()
        self.createN.setGeometry(260,250,110,110)
        self.startNew.setGeometry(260,360,110,61)
        self.importF.setGeometry(510,250,110,110)
        self.importFile.setGeometry(510,360,110,60)
        self.postProcessingF.setGeometry(630,250,110,110)
        self.postProcessing.setGeometry(630,360,101,60)
        self.w1.hide()

    def postProcessingClicked(self):
        self.postProcessingScreen.show()

    def PPhomeClicked(self):
        self.postProcessingScreen.hide()


    ##____________________________Post processing Func ________________#

    def PPimportClicked(self):
        self.PPinfileDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath() , 'InFile(*.in)')
        self.PPimportRun()
        self.infileLoad_Flag = 1
        if self.vtkLoad_flag ==1:
            self.ppToolwidget.setEnabled(True)

    def PPimportRun(self):
        try:
            PPfileDir = open(self.PPinfileDir, 'r')
            PPfileLines = PPfileDir.readlines()

            for i in PPfileLines:

                if "#" in i:
                    pass

                elif "=" in i :
                    i = i.replace(" ", "")
                    i = i.replace(";", "")
                    i = i.replace("\n", "")
                    entries = i.split("=")

                    if entries[0] == "NUMPHASES":
                        self.PP_NoP = entries[1]

                    elif entries[0] == "NUMCOMPONENTS":
                        self.PP_NoC = entries[1]

                    elif entries[0] == "NTIMESTEPS":
                        self.PP_timeSteps = entries[1]

                    elif entries[0] == "SAVET":
                        self.PP_savet = entries[1]

                    elif entries[0] == "COMPONENTS":
                        entries[1] = entries[1].replace("{","")
                        entries[1] = entries[1].replace("}","")
                        self.PP_Cnames = entries[1].split(",")

                    elif entries[0] == "PHASES":
                        entries[1] = entries[1].replace("{","")
                        entries[1] = entries[1].replace("}","")
                        self.PP_Pnames = entries[1].split(",")
                        
                    elif entries[0] == "DELTA_X":
                        self.PP_dx = entries[1]
                        
                    elif entries[0] == "DELTA_t":
                        self.PP_dt = entries[1]
                        
                
                        

            self.SimulationDetail.show()
            self.PP_fileData.setText("Number of components : "+  self.PP_NoC  + "\nComponents : " + (",").join(self.PP_Cnames) + "\nNumber of phases  : " + self.PP_NoP + "\n Phases : " + (",").join(self.PP_Pnames) )

        except IOError:
            print("could not read")

        except UnicodeDecodeError:
            print("could not read")

    def PPimportDataClicked(self):
        try:
            self.PPdataDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath() , 'VTK(*.vtk)' )
            self.PPdataRun()
            self.vtkLoad_flag = 1
            if self.infileLoad_Flag == 1:
                self.ppToolwidget.setEnabled(True)
            

        except IOError:
            print("could not read")
            return

        except UnicodeDecodeError:
            print("could not read")
            return
        
    # PPimage Func
        
    def PPimageClicked(self):
        self.PPimage_widge.setGeometry(360,0,461,161)
        self.PPimage_error.setText("")
        self.PPimagedir.setText("")
        
        self.widget_5.setEnabled(False)
        self.ppToolwidget.setEnabled(False)
        self.Screen1.setEnabled(False)
        self.PPimage_widge.show()
        self.anim_PPimage.start()
        
    def PPimageCloseClicked(self):
        self.PPimage_error.setText("")
        self.PPimage_widge.setGeometry(360,0,0,0)
        self.widget_5.setEnabled(True)
        self.ppToolwidget.setEnabled(True)
        self.Screen1.setEnabled(True)
        self.PPimage_widge.hide()
        
    
    def PPimageLocbtnClicked(self):
        self.PPimage_error.setText("")
        
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        if dlg.exec_():
            self.PPimage_outputdir =  ''.join(dlg.selectedFiles())
            self.PPimagedir.setText(self.PPimage_outputdir)
            
    
    def PPimageConvertClicked(self):
        
        if self.PPimagedir.text() != "":
            if  os.path.isdir(self.PPimagedir.text()):
                
                PPimage_outhead, PPimage_outtail = os.path.split(self.PPdataDir)
                saveimagedir = self.PPimagedir.text() + "/"+PPimage_outtail[:-5]
            else:
                self.PPimage_error.setText("Wrong path")
        else:
            saveimagedir = self.PPdataDir[:-5]

        
        if self.PPimage_allcheck.isChecked():
            
            self.iteration_step.setValue(0)
            
            for i in range(self.iteration_step.maximum()):
                
                finalDir = saveimagedir  + str(i) + ".png"
                plt.savefig(finalDir)
                self.iteration_step.setValue(self.iteration_step.value() + 1)
                self.PPimage_error.setText("Saving "+ str(i) +". Please wait...")
                self.PPimage_error.repaint()
                
            
            self.PPimageCloseClicked()
            Submitmsg = QMessageBox()
            Submitmsg.setWindowTitle("File Created")
            Submitmsg.setText("\n Sucessfully created png files at :\n\n      "+ saveimagedir )
            Submitmsg.exec_()
            
        
        else:
            finalDir = saveimagedir + "_" + self.showTime.text() + ".png"
            plt.savefig(finalDir)
            self.PPimageCloseClicked()
            Submitmsg = QMessageBox()
            Submitmsg.setWindowTitle("File Created")
            Submitmsg.setText("\n Sucessfully created png file at :\n\n      "+ finalDir )
            Submitmsg.exec_()
    
    # PPexort func
    
    def PPexportClicked(self):
        self.PPexport_widge.setGeometry(360,0,461,161)
        self.PPexport_error.setText("")
        self.PPexportdir.setText("")
        
        self.widget_5.setEnabled(False)
        self.ppToolwidget.setEnabled(False)
        self.Screen1.setEnabled(False)
        self.PPexport_widge.show()
        self.anim_PPexport.start()
        
    def PPexportCloseClicked(self):
        self.PPexport_error.setText("")
        self.PPexport_widge.setGeometry(360,0,0,0)
        self.widget_5.setEnabled(True)
        self.ppToolwidget.setEnabled(True)
        self.Screen1.setEnabled(True)
        self.PPexport_widge.hide()
        
    
    def PPexportLocbtnClicked(self):
        self.PPexport_error.setText("")
        
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        if dlg.exec_():
            self.PPexport_outputdir =  ''.join(dlg.selectedFiles())
            self.PPexportdir.setText(self.PPexport_outputdir)
            
    
    def PPexportConvertClicked(self):
        
        if self.PPexportdir.text() != "":
            if  os.path.isdir(self.PPexportdir.text()):
                
                PPexport_outhead, PPexport_outtail = os.path.split(self.PPdataDir)
                saveimagedir = self.PPexportdir.text() + "/"+PPexport_outtail[:-5]
            else:
                self.PPexport_error.setText("Wrong path")
        else:
            saveimagedir = self.PPdataDir[:-5]

        
        if self.PPexport_allcheck.isChecked():
            
            self.iteration_step.setValue(0)
            
            for i in range(self.iteration_step.maximum()):
                iteration_value_plot = self.iteration_step.value()
                scalar_name_plot = self.scalerValue.currentText()
            
                # plot data
                
                if self.data_3D_flag == 0:
                
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    pf = np.copy(np.reshape(vtkPointData, self.grid_reshape))
                    
                elif self.data_3D_flag == 1:
                    if self.xyplane_flag == 1 :
                        vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                        
                        grid_shape = self.vtkData[0].GetDimensions()
                        

                        pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                        
                        pf = pf[self.depth_plot.value(),:,:]
                        
        
                    
                    elif self.yzplane_flag == 1 :
                        vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                        
                        grid_shape = self.vtkData[0].GetDimensions()
                        

                        pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                        
                        pf = pf[:,self.depth_plot.value(),:]
                        
                    
                    elif self.xzplane_flag == 1 :
                        vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                        
                        grid_shape = self.vtkData[0].GetDimensions()
                        

                        pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                        
                        pf = pf[:,:,self.depth_plot.value()]
                        
                #Saving File
                finalDir = saveimagedir  + str(i) + ".csv"
                np.savetxt(finalDir, pf, delimiter=",")
                
                self.PPexport_error.setText("Saving "+ str(i) +". Please wait...")
                self.PPexport_error.repaint()
                self.iteration_step.setValue(self.iteration_step.value() + 1)
                
            
            self.PPexportCloseClicked()
            Submitmsg = QMessageBox()
            Submitmsg.setWindowTitle("File Created")
            Submitmsg.setText("\n Sucessfully created png files at :\n\n      "+ saveimagedir )
            Submitmsg.exec_()
            
        
        else:
            iteration_value_plot = self.iteration_step.value()
            scalar_name_plot = self.scalerValue.currentText()
        
            # plot data
            
            if self.data_3D_flag == 0:
            
                vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                
                pf = np.copy(np.reshape(vtkPointData, self.grid_reshape))
                
            elif self.data_3D_flag == 1:
                if self.xyplane_flag == 1 :
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    grid_shape = self.vtkData[0].GetDimensions()
                    

                    pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                    
                    pf = pf[self.depth_plot.value(),:,:]
                    
    
                
                elif self.yzplane_flag == 1 :
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    grid_shape = self.vtkData[0].GetDimensions()
                    

                    pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                    
                    pf = pf[:,self.depth_plot.value(),:]
                    
                
                elif self.xzplane_flag == 1 :
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    grid_shape = self.vtkData[0].GetDimensions()
                    

                    pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                    
                    pf = pf[:,:,self.depth_plot.value()]
            
            finalDir = saveimagedir + "_" + self.showTime.text() + ".csv"
            np.savetxt(finalDir, pf, delimiter=",")
            
            
            self.PPexportCloseClicked()
            Submitmsg = QMessageBox()
            Submitmsg.setWindowTitle("File Created")
            Submitmsg.setText("\n Sucessfully created png file at :\n\n      "+ finalDir )
            Submitmsg.exec_()
            
    def PP_clearClicked(self):
        self.figure.clear()
        self.imgShow.hide()
        self.fig_ppt.clear()
        self.canvas_ppt.draw()
        self.SimulationDetail.hide()
        self.pptPlot.hide()
        self.triple_point_widget.hide()

        self.ppToolwidget.setEnabled(False)
        
        self.ppt_Count_Plot_flag = 0;
        self.ppt_size_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.infileLoad_Flag = 0
        self.vtkLoad_flag = 0
        
        
        #for 3D ploting
        self.data_3D_flag = 0
        self.yzplane_flag = 0
        self.xyplane_flag = 0
        self.xzplane_flag = 0
        
        self.PPdataDir = ""
        self.PPinfileDir = ""
        
        
        self.scalerValue.clear()
        self.iteration_step.setValue(0)
        self.showTime.setText("")
        
        
        return
        
        
    def h5tovtkbtnClicked(self):
        self.h5tovtk_Screen.setGeometry(230,0,601,351)
        
        self.widget_5.setEnabled(False)
        self.ppToolwidget.setEnabled(False)
        self.Screen1.setEnabled(False)
        self.h5tovtk_Screen.show()
        self.anim_h5toVTK.start()
        
    def h5tovtkCloseClicked(self):
        self.h5tovtk_Screen.setGeometry(230,0,0,351)
        self.widget_5.setEnabled(True)
        self.ppToolwidget.setEnabled(True)
        self.Screen1.setEnabled(True)
        self.h5tovtk_Screen.hide()
        
    
    def h5tovtk_infilebtnClicked(self):
        self.h5tovtk_error.setText("")
        
        try:
            self.h5tovtk_infileDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath() , 'Infile(*.in)' )
            
            self.h5tovtk_infileLoc.setText(self.h5tovtk_infileDir)
        
        except IOError:
            print("could not read")
            return

        except UnicodeDecodeError:
            print("could not read")
            return
        
    def h5tovtk_outputbtnClicked(self):
        self.h5tovtk_error.setText("")
        
        if self.h5tovtk_h5radio.isChecked():
            try:
                self.h5tovtk_outputDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath() , 'H5(*.h5)' )
                
                self.h5tovtk_outputloc.setText(self.h5tovtk_outputDir)
                
            except IOError:
                print("could not read")
                return

            except UnicodeDecodeError:
                print("could not read")
                return
            
        elif self.h5tovtk_xmfradio.isChecked():
            try:
                self.h5tovtk_outputDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Multiple File', QtCore.QDir.currentPath() , 'XMF(*.xmf)' )
                
                self.h5tovtk_outputloc.setText(self.h5tovtk_outputDir)
                
            except IOError:
                print("could not read")
                return

            except UnicodeDecodeError:
                print("could not read")
                return
            
    def h5tovtk_vtkoutputbtnClicked(self):
        self.h5tovtk_error.setText("")
        
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        if dlg.exec_():
            self.h5tovtk_vtkoutputdir =  ''.join(dlg.selectedFiles())
            self.h5tovtk_vtkoutput.setText(self.h5tovtk_vtkoutputdir)
            
 
    
    def h5tovtk_convertClicked(self):
        
        if self.h5tovtk_infileLoc.text() == "":
            self.h5tovtk_error.setText("Infile location not found")
            return False
            
        elif self.h5tovtk_outputloc.text() == "":
            self.h5tovtk_error.setText("output file location not found")
            return False
        
        elif self.h5tovtk_sTime.text() =="":
            self.h5tovtk_error.setText("Please input Start Time")
            return False
        
        elif self.h5tovtk_eTime.text() =="":
            self.h5tovtk_error.setText("Please input End Time")
            return False
        else:
            self.h5tovtk_error.setText("")
            
            
        
        if self.h5tovtk_h5radio.isChecked():
            
            h5_outhead, h5_outtail = os.path.split(self.h5tovtk_outputloc.text())
            
            split_text = "_" + self.h5tovtk_sTime.text()+".h5"
            
            h5_outputfilename = h5_outtail.split(split_text)
            
            #reading vtk output file dir
            
            if self.h5tovtk_vtkoutput.text() == "":
                vtk_output_fname = h5_outhead + "/" + h5_outputfilename[0]+ ".vtk"
            
            elif os.path.isdir(self.h5tovtk_vtkoutput.text()):
                vtk_output_fname = self.h5tovtk_vtkoutput.text() + "/" + h5_outputfilename[0]+ ".vtk"
                
            else:
                return False
                
            
            h5toxmf_cmd = "cd " +h5_outhead + "; cd ..;" + "cp ~/MicroSim/Grand_potential_Finite_difference_2D_MPI/write_xdmf write_xdmf ; ./write_xdmf " + self.h5tovtk_infileLoc.text() + " "+ h5_outputfilename[0] + " " +  self.h5tovtk_sTime.text() + " "+ self.h5tovtk_eTime.text() 
            

            os.system("gnome-terminal -e 'bash -c \""+h5toxmf_cmd+";\"'")
            
            
            xmlfile = minidom.parse( h5_outhead +"/" + h5_outputfilename[0] +"_" +self.h5tovtk_sTime.text() + ".xmf")
            models = xmlfile.getElementsByTagName('Attribute')
            scalar_names_xml = []
            
            for elem in models:
                scalar_names_xml.append(elem.attributes['Name'].value)
                
                
            source_files = glob.glob(h5_outhead +"/"+ h5_outputfilename[0] +'*.xmf')
            xmf_names = []
            for files in source_files:
                xmf_names.append(str(files))
                
            xmf_names = sorted(xmf_names,key=lambda x: int(x.split('_')[-1].split('.')[0]))
                
                
            python_script_for_vtk = "from paraview.simple import *\nparaview.simple._DisableFirstRenderCameraReset()\noutput = XDMFReader(FileNames=" +str(xmf_names) +")\noutput.PointArrayStatus = " +str(scalar_names_xml) + "\nanimationScene1 = GetAnimationScene()\nanimationScene1.UpdateAnimationUsingDataTimeSteps()\nprint('Converting to vtk. Please wait...')\nSaveData('" + vtk_output_fname + "', proxy=output, Writetimestepsasfileseries=1,Firsttimestep=0, Lasttimestep=-1,Timestepstride="+  str(int(self.h5tovtk_eskip.text()) + 1) +")\nprint('Done')"
            
            fileName = h5_outhead + "/h5tovtk.py"
            f = open(fileName, "w")
            f.write( python_script_for_vtk )
            f.close()
            
            xmftovtk_cmd = "cd " +h5_outhead + ";pvpython h5tovtk.py;rm h5tovtk.py;cd ..;rm write_xdmf"
            os.system("gnome-terminal -e 'bash -c \""+xmftovtk_cmd+";\"'")
            
        elif self.h5tovtk_xmfradio.isChecked():
            
            h5_outhead, h5_outtail = os.path.split(self.h5tovtk_outputloc.text())
            
            split_text = "_"+self.h5tovtk_sTime.text()+".xmf"
            
            h5_outputfilename = h5_outtail.split(split_text)
            
            #reading vtk output file dir
            
            if self.h5tovtk_vtkoutput.text() == "":
                vtk_output_fname = h5_outhead + "/" + h5_outputfilename[0]+ "_.vtk"
            
            elif os.path.isdir(self.h5tovtk_vtkoutput.text()):
                vtk_output_fname = self.h5tovtk_vtkoutput.text() + "/" + h5_outputfilename[0]+ "_.vtk"
                
            else:
                return False
            
            
            xmlfile = minidom.parse( h5_outhead +"/" + h5_outputfilename[0] + "_" +self.h5tovtk_sTime.text() + ".xmf")
            models = xmlfile.getElementsByTagName('Attribute')
            scalar_names_xml = []
            
            for elem in models:
                scalar_names_xml.append(elem.attributes['Name'].value)
            
            source_files = glob.glob(h5_outhead +"/"+ h5_outputfilename[0] +'*.xmf')
            xmf_names = []
            for files in source_files:
                xmf_names.append(str(files))
                
            xmf_names = sorted(xmf_names,key=lambda x: int(x.split('_')[-1].split('.')[0]))
            
            python_script_for_vtk = "from paraview.simple import *\nparaview.simple._DisableFirstRenderCameraReset()\noutput = XDMFReader(FileNames=" +str(xmf_names) +")\noutput.PointArrayStatus = " +str(scalar_names_xml) + "\nanimationScene1 = GetAnimationScene()\nanimationScene1.UpdateAnimationUsingDataTimeSteps()\nprint('Converting to vtk. Please wait...')\nSaveData('" + vtk_output_fname + "', proxy=output, Writetimestepsasfileseries=1,Firsttimestep=0, Lasttimestep=-1,Timestepstride="+  str(int(self.h5tovtk_eskip.text()) + 1) +")\nprint('Done')"
            
            fileName = h5_outhead + "/h5tovtk.py"
            f = open(fileName, "w")
            f.write( python_script_for_vtk )
            f.close()
            
            xmftovtk_cmd = "cd " +h5_outhead + ";pvpython h5tovtk.py;rm h5tovtk.py;cd ..;rm write_xdmf"
            os.system("gnome-terminal -e 'bash -c \""+xmftovtk_cmd+";\"'")
        
       
        

    def plotfig(self):
        if self.scalerValue.currentIndex() >= 0:
            
            self.showTime.setText(str(self.timeItretion[self.iteration_step.value()]))

            iteration_value_plot = self.iteration_step.value()
            scalar_name_plot = self.scalerValue.currentText()

            self.figure.clear()
            self.ax = self.figure.add_subplot(111)
            self.ax.axis('off')

            # plot data
            
            if self.data_3D_flag == 0:
            
                vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                
                pf = np.copy(np.reshape(vtkPointData, self.grid_reshape))
                
            elif self.data_3D_flag == 1:
                if self.xyplane_flag == 1 :
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    grid_shape = self.vtkData[0].GetDimensions()
                    

                    pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                    
                    pf = pf[self.depth_plot.value(),:,:]
                    
       
                
                elif self.yzplane_flag == 1 :
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    grid_shape = self.vtkData[0].GetDimensions()
                    

                    pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                    
                    pf = pf[:,self.depth_plot.value(),:]
                    
                
                elif self.xzplane_flag == 1 :
                    vtkPointData = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
                    
                    grid_shape = self.vtkData[0].GetDimensions()
                    

                    pf = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                    
                    pf = pf[:,:,self.depth_plot.value()]
                    
                    
            c = self.ax.imshow(pf, origin='lower', cmap='coolwarm')
            #plt.colorbar(c, shrink=0.55)
            plt.tight_layout()
            # refresh canvas
            self.canvas.draw()
            
        if self.ppt_Count_Plot_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)

            self.ax_ppt.plot(self.timeItretion,self.ppt_count)
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.ppt_count[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("PPT Count = " + str(self.ppt_count[self.iteration_step.value()]), loc='center')
            self.ax_ppt.set_xlabel('Iteration')
            self.ax_ppt.set_ylabel('Precipitate Count')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
            
        elif self.ppt_size_flag == 1:
            self.pptPlot.show()
            k = int(self.iteration_step.value())
            self.table_ppt_size.setRowCount(self.ppt_count[k])
            
            for t in range(int(self.ppt_count[k])):
                self.table_ppt_size.setItem(t,0,QTableWidgetItem(str(round(self.ppt_coords[k][t][0],2)) + " , " + str(round(self.ppt_coords[k][t][1],2))  ))#+ " , " + str(round(self.ppt_coords[k][t][2],2))
                self.table_ppt_size.setItem(t,1,QTableWidgetItem( str(  round(self.ppt_area[k][t],3 )) ) )
                self.table_ppt_size.setItem(t,2,QTableWidgetItem( str(  round(np.sqrt(self.ppt_area[k][t]/np.pi ),3 )) ) )
                self.table_ppt_size.setItem(t,3,QTableWidgetItem(str(self.ppt_major_axis[k][t])))
                self.table_ppt_size.setItem(t,4,QTableWidgetItem(str(self.ppt_minor_axis[k][t])))
                self.table_ppt_size.setItem(t,5,QTableWidgetItem(str(  round(self.ppt_major_axis[k][t]/self.ppt_minor_axis[k][t] , 2)   )))
                
        elif self.velocity_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)

            self.ax_ppt.plot(self.timeItretion,self.arr_velocity)
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.arr_velocity[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Velocity = " + str( round(self.arr_velocity[self.iteration_step.value()],3)), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Average Front Velocity')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
        
        elif self.volume_SA_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            
            self.ax_ppt.plot(self.timeItretion,self.volume_fraction)
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.volume_fraction[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Volume Fraction = " + str(round(self.volume_fraction[self.iteration_step.value()], 3)), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Volume Fraction')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
            
        elif self.volume_SA_flag == 2:
            self.pptPlot.show()
            self.fig_ppt.clear()
            
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            
            self.ax_ppt.plot(self.timeItretion,self.total_SA)
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.total_SA[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Surface Area = " + str(round(self.total_SA[self.iteration_step.value()], 3)), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Surface Area')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
            
        elif self.volume_SA_flag == 3:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            self.ax_ppt.plot(self.timeItretion,self.total_volume)
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.total_volume[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Total Volume = " + str(round(self.total_volume[self.iteration_step.value()], 3)), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Total Volume')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            self.canvas_ppt.draw()
        
        elif self.velocity_over_line_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            self.ax_ppt.plot(self.timeItretion, self.velocity_OL)
            
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.velocity_OL[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Velocity =  " + str(self.velocity_OL[self.iteration_step.value()]), loc='center')
            self.ax_ppt.set_xlabel('Iterations')
            self.ax_ppt.set_ylabel('Velocity')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
            
        elif self.velocity_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            
            self.ax_ppt.plot(self.timeItretion,self.arr_velocity)
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.arr_velocity[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Velocity = " + str(round(self.arr_velocity[self.iteration_step.value()], 3)), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Average Front Velocity')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            
            self.canvas_ppt.draw()
            
        elif self.tip_radius_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            
            self.ax_ppt.plot(self.timeItretion[1:],self.tip_radius_data[1:])
            
            if self.iteration_step.value() != 0:
                self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.tip_radius_data[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("Tip Radius = " + str(self.tip_radius_data[self.iteration_step.value()]), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Tip Radius')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
            
        elif self.front_undercool_flag == 1:
            self.pptPlot.show()
            self.fig_ppt.clear()
            self.ax_ppt = self.fig_ppt.add_subplot(111)
            
            self.ax_ppt.plot(self.timeItretion[1:],self.front_undercooling[1:])
            
            if self.iteration_step.value() != 0:
                self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.front_undercooling[self.iteration_step.value()], marker ='o')
            self.ax_ppt.set_title("T_front = " + str(self.front_undercooling[self.iteration_step.value()]), loc='center')
            self.ax_ppt.set_xlabel('Timesteps')
            self.ax_ppt.set_ylabel('Front Temperature')
            self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
            #self.ax_ppt.grid()
            
            self.canvas_ppt.draw()
            
        elif self.triple_point_flag ==1:
            
            k = int(self.iteration_step.value())
            self.table_triplePoint.setRowCount(len(self.triple_point_value[k]))
            
            for t in range(len(self.triple_point_value[k])):
                self.table_triplePoint.setItem(t,0,QTableWidgetItem( str(t)))
                self.table_triplePoint.setItem(t,1,QTableWidgetItem( str( self.triple_point_value[k][t]) ))
                
            
            for i in self.triple_point_value[self.iteration_step.value()]:
                self.ax.scatter(i[1],i[0],marker='o')
            self.canvas.draw()
  
            
    
    def plotFig_3d(self):
        
        self.plotfig()
        return
            
    def pptplot_importClicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV(*.csv)", options=options)
        
        if fileName != "":
            fileName = fileName + ".csv"
            f = open(fileName, "w")
            
            if self.ppt_Count_Plot_flag == 1:
                
                f.write( "Timesteps , Ppt Count \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.ppt_count[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
            
                return
            
                    
            elif self.velocity_flag == 1:
                
                f.write( "Timesteps, Front Velocity \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.arr_velocity[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                
                return
             
            
            elif self.volume_SA_flag == 1:
                f.write( "Timesteps, Volume Fraction \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.volume_fraction[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                
                return
               
                
            elif self.volume_SA_flag == 2:
                
                f.write( "Timesteps, Surface Area \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.total_SA[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                return
                
              
            elif self.volume_SA_flag == 3:
                
                f.write( "Timesteps, Total Volume \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.total_volume[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                return
            
            elif self.velocity_over_line_flag ==1:
                f.write( "Timesteps, Velocity \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.velocity_OL[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                return
            
            elif self.tip_radius_flag == 1:
                f.write( "Timesteps, Tip Radius \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.tip_radius_data[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                return
            
            elif self.front_undercool_flag == 1:
                f.write( "Timesteps, Front Temperature \n" )
            
                for rowNumber in range(len(self.timeItretion)):
              
                    f.write( str(self.timeItretion[rowNumber]) + "," + str(self.front_undercooling[rowNumber]) )
                   
                    f.write("\n")
                f.close()
                
                Submitmsg = QMessageBox()
                Submitmsg.setWindowTitle("File Created")
                Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
                Submitmsg.exec_()
                return
            
            
                
            
        
    def fastNextClicked(self):
        self.iteration_step.setValue(len(self.timeItretion)-1)

    def fastPreClicked(self):
        self.iteration_step.setValue(0)

    def nextViewClicked(self):
        self.iteration_step.setValue(self.iteration_step.value() + 1)

    def preViewClicked(self):
        if self.iteration_step.value() != 0:
            self.iteration_step.setValue(self.iteration_step.value() - 1)

    def PPreloadClicked(self):

        DatafilePath = self.PPdataDir[:-5]

        self.timeItretion = []
        for files in glob.glob(DatafilePath + '*.vtk'):
            itretionV = files.split("_")
            self.timeItretion.append(int(itretionV[len(itretionV) - 1].replace(".vtk","")))

        self.timeItretion =  sorted(self.timeItretion)

        self.vtkData = np.empty(len(self.timeItretion) , dtype = object)
        count=0
        for n in self.timeItretion:

            vtk_read = DatafilePath + str(n) + ".vtk"
            reader = vtkDataSetReader()
            reader.SetFileName(vtk_read)
            reader.ReadAllScalarsOn()  # Activate the reading of all scalars
            reader.Update()
            self.vtkData[count] = reader.GetOutput()
            count = count + 1


        Number_of_Scalers = self.vtkData[0].GetPointData().GetNumberOfArrays()
        scalar_names = [self.vtkData[0].GetPointData().GetArrayName(i) for i in range(0, Number_of_Scalers)]
        self.scalerValue.clear()
        self.scalerValue.addItems(scalar_names)

        self.iteration_step.setMaximum(len(self.timeItretion)-1)

        
        
    def PPplayClicked(self):
        self.iteration_step.setValue(0)
        self.PPplay.hide()
        self.PPpause.show()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Runanimation)
        self.timer.start(1)
    
    
    def Runanimation(self):
        self.iteration_step.setValue(self.iteration_step.value() + 1)
        
        if (self.iteration_step.value() == self.iteration_step.maximum()):
            self.timer.stop()
            self.PPplay.show()
            self.PPpause.hide()
            return
    
    def PPpauseClicked(self):
        self.timer.stop()
        self.PPplay.show()
        self.PPpause.hide()
                
    def draw_LineClicked(self):
        self.drawLineWidget.show()
        #self.draw_line_on_Sim()
        
    def draw_line_on_Sim(self):
        
        startPoints = self.POL_start.text().split(",")
        endPoints = self.POL_end.text().split(",")
        iteration_value_plot = self.iteration_step.value()
        
        if len(startPoints) != 2 or len(endPoints) != 2:
            return
        
        if startPoints[0] == "" or startPoints[1] == "" or endPoints[0] == "" or endPoints[1] == "":
            return
        
        x1 , y1 = int(startPoints[0]) , int(startPoints[1])
        x2 , y2 = int(endPoints[0]) , int(endPoints[1])
        

        
        if int(startPoints[0]) >= self.grid_reshape[0] or int(startPoints[1]) >= self.grid_reshape[1] or int(endPoints[0]) >= self.grid_reshape[0] or int(endPoints[1]) >= self.grid_reshape[1]:
            print("out of bound")
            return
        
        scat, = plt.plot([],[],  marker='o')
        
        scat.set_data([x1 , x2],[y1 , y2])
        # scat.set_ydata([y1 , y2])
        self.canvas.draw()
    
    def plot_over_lineClicked(self):

        startPoints = self.POL_start.text().split(",")
        endPoints = self.POL_end.text().split(",")
        iteration_value_plot = self.iteration_step.value()
        
        if len(startPoints) != 2 or len(endPoints) != 2:
            return
        
        if startPoints[0] == "" or startPoints[1] == "" or endPoints[0] == "" or endPoints[1] == "":
            return
        

        if int(startPoints[0]) >= self.grid_reshape[0] or int(startPoints[1]) >= self.grid_reshape[1] or int(endPoints[0]) >= self.grid_reshape[0] or int(endPoints[1]) >= self.grid_reshape[1]:
            print("out of bound")
            return
       
        
        x1 , y1 = int(startPoints[0]) , int(startPoints[1])
        x2 , y2 = int(endPoints[0]) , int(endPoints[1])
        
        points = []
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        
        
        phi_Value = []
        iteration_value_plot = self.iteration_step.value()
        scalar_name_plot = self.scalerValue.currentText()
        Phi_data = self.vtkData[iteration_value_plot].GetPointData().GetArray(scalar_name_plot)
            

        Phi_data = np.copy(np.reshape(Phi_data, self.grid_reshape))
            
        for i in range(len(points)):
            phi_loc = points[i]
            phi_Value.append(Phi_data[phi_loc[1]][phi_loc[0]])
            
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_Count_Plot_flag = 0
        self.ppt_size_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 1
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0

        self.pptPlot.show()
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)

        self.ax_ppt.plot(np.arange(1, len(phi_Value)+1) , phi_Value)
        
        self.ax_ppt.set_title("Plot Over Line ", loc='center')
        self.ax_ppt.set_xlabel('')
        self.ax_ppt.set_ylabel('phi')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        self.drawLineWidget.hide()
        
    def PPbuttonClicked(self):
        if os.path.isdir(self.runDir + "/DATA/") and os.path.isdir(self.runDir):  ##checking data file status

            self.PPdataDir = self.runDir + "/DATA/" +self.output.text() + "_0.vtk"
            self.PPinfileDir = self.runDir + "/" + self.infile.text()

            self.PPdataRun()
            self.PPimportRun()
            self.postProcessingScreen.show()
            self.vtkLoad_flag = 1
            self.infileLoad_Flag == 1
            self.ppToolwidget.setEnabled(True)

        else:
            self.finish_error.setText("Sorry, DATA or Infile directory not found.")


    def PPdataRun(self):
        
        if os.path.isfile(self.PPdataDir):
            DatafilePath = self.PPdataDir[:-5]

            self.timeItretion = []
            for files in glob.glob(DatafilePath + '*.vtk'):
                itretionV = files.split("_")
                self.timeItretion.append(int(itretionV[len(itretionV) - 1].replace(".vtk","")))

            self.timeItretion =  sorted(self.timeItretion)

            self.vtkData = np.empty(len(self.timeItretion) , dtype = object)
            count=0
            

            for n in self.timeItretion:

                vtk_read = DatafilePath + str(n) + ".vtk"
                datahead, datatail = os.path.split(vtk_read)
                self.loding_label.setText("Loading : " + datatail )
                self.loding_label.repaint()
                
                reader = vtkDataSetReader()
                reader.SetFileName(vtk_read)
                reader.ReadAllVectorsOn()
                reader.ReadAllScalarsOn()  # Activate the reading of all scalars
                reader.Update()
                self.vtkData[count] = reader.GetOutput()
                
                count = count + 1
            
            self.loding_label.setText("")
            self.loding_label.repaint()
                
            Number_of_Scalers = self.vtkData[0].GetPointData().GetNumberOfArrays()
            scalar_names = [self.vtkData[0].GetPointData().GetArrayName(i) for i in range(0, Number_of_Scalers)]
            
            
            
            grid_shape = self.vtkData[0].GetDimensions()
          
            if grid_shape[0] == 1:
                self.data_3D_flag = 0
                self.grid_reshape = ( grid_shape[2], grid_shape[1]  )  #have some doubt here
                self.widget_3d.setEnabled(False)               
                

            elif grid_shape[1] == 1:
                self.data_3D_flag = 0
                self.grid_reshape = ( grid_shape[0], grid_shape[2]  )
                self.widget_3d.setEnabled(False)
                

            elif grid_shape[2] == 1:
                self.data_3D_flag = 0
                self.grid_reshape = ( grid_shape[1], grid_shape[0]  )
                self.widget_3d.setEnabled(False)
                
                
            else:
                self.data_3D_flag = 1 
                self.depth_plot.setRange(0,(grid_shape[2]-1))
                self.grid_reshape = ( grid_shape[0], grid_shape[1]  )
                
                self.widget_3d.setEnabled(True)
                
                
                self.yzplane_flag = 0
                self.xyplane_flag = 1
                self.xzplane_flag = 0
                self.xyPLane.setStyleSheet("border : 1px solid rgb(186, 189, 182);")
                self.yzPlane.setStyleSheet("border : none;")
                self.xzPlane.setStyleSheet("border : none;")
            
            
            self.scalerValue.clear()
            self.scalerValue.addItems(scalar_names)

            self.iteration_step.setMaximum(len(self.timeItretion)-1)

            self.plotfig()
            self.imgShow.show()
            
            #self.ppt_area, self.ppt_radius, self.ppt_coords, self.ppt_major_axis , self.ppt_minor_axis , self.ppt_count , self.ppt_perimeter = load_ppt_property(self.timeItretion, self.vtkData ,self.scalerValue.currentText())
        
        else:
            print("No file Selected")
            return
        
    def xyPLaneClicked(self):
        grid_shape = self.vtkData[0].GetDimensions()
  
        self.depth_plot.setRange(0,(grid_shape[2]-1))
        self.grid_reshape = ( grid_shape[0], grid_shape[1]  )
        
        
        self.yzplane_flag = 0
        self.xyplane_flag = 1
        self.xzplane_flag = 0
        self.xyPLane.setStyleSheet("border : 1px solid rgb(186, 189, 182);")
        self.yzPlane.setStyleSheet("border : none;")
        self.xzPlane.setStyleSheet("border : none;")
        self.plotfig()
        
        return
    
    def yzPlaneClicked(self):
        grid_shape = self.vtkData[0].GetDimensions()
  
        self.depth_plot.setRange(0,(grid_shape[0]-1))
        self.grid_reshape = ( grid_shape[1], grid_shape[2]  )
        
        
        self.yzplane_flag = 1
        self.xyplane_flag = 0
        self.xzplane_flag = 0
        self.xyPLane.setStyleSheet("border : none;")
        self.yzPlane.setStyleSheet("border : 1px solid rgb(186, 189, 182);")
        self.xzPlane.setStyleSheet("border : none;")
        self.plotfig()
    
        return
    
    def xzPlaneClicked(self):
        grid_shape = self.vtkData[0].GetDimensions()
  
        self.depth_plot.setRange(0,(grid_shape[1]-1))
        self.grid_reshape = ( grid_shape[0], grid_shape[2]  )
        
        self.yzplane_flag = 0
        self.xyplane_flag = 0
        self.xzplane_flag = 1
        self.xyPLane.setStyleSheet("border : none;")
        self.yzPlane.setStyleSheet("border : none;")
        self.xzPlane.setStyleSheet("border : 1px solid rgb(186, 189, 182);")
        self.plotfig()
        return
    
    
        

#_______________________PPT Action____________________________________#

    def pptcountClicked(self):
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_Count_Plot_flag = 1
        self.ppt_size_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
       
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        
        self.ppt_area, self.ppt_radius, self.ppt_coords, self.ppt_major_axis , self.ppt_minor_axis , self.ppt_count , self.ppt_perimeter = load_ppt_property(self.timeItretion, self.vtkData ,self.scalerValue.currentText(), Is3d, self.depth_plot.value())
        self.pptPlot.show()
        
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)

        self.ax_ppt.plot(self.timeItretion,self.ppt_count)
        self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.ppt_count[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("PPT Count = " + str(self.ppt_count[self.iteration_step.value()]), loc='center')
        self.ax_ppt.set_xlabel('Iteration')
        self.ax_ppt.set_ylabel('Precipitate Count')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        
    def pptsizeClicked(self):
        self.pptRadius.show()
        self.SimulationDetail.hide()
        self.pptPlot.hide()
        self.triple_point_widget.hide()
        
        self.table_ppt_size.setColumnHidden(1, True)
        self.ppt_size_flag = 1
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        
        self.ppt_area, self.ppt_radius, self.ppt_coords, self.ppt_major_axis , self.ppt_minor_axis , self.ppt_count , self.ppt_perimeter = load_ppt_property(self.timeItretion, self.vtkData ,self.scalerValue.currentText(), Is3d, self.depth_plot.value())
        
        k = int(self.iteration_step.value())
        self.table_ppt_size.setRowCount(self.ppt_count[k])
        
        for t in range(int(self.ppt_count[k])):
            self.table_ppt_size.setItem(t,0,QTableWidgetItem(str(round(self.ppt_coords[k][t][0],2)) + " , " + str(round(self.ppt_coords[k][t][1],2))  )) #+ " , " + str(round(self.ppt_coords[k][t][2],2))
            self.table_ppt_size.setItem(t,1,QTableWidgetItem( str(  round(self.ppt_area[k][t],3 )) ) )
            self.table_ppt_size.setItem(t,2,QTableWidgetItem( str(  round(self.ppt_radius[k][t],3 )) ) )
            self.table_ppt_size.setItem(t,3,QTableWidgetItem(str(self.ppt_major_axis[k][t])))
            self.table_ppt_size.setItem(t,4,QTableWidgetItem(str(self.ppt_minor_axis[k][t])))
            self.table_ppt_size.setItem(t,5,QTableWidgetItem(str(  round(self.ppt_major_axis[k][t]/self.ppt_minor_axis[k][t] , 2)   )))
            
    
    def pptareaClicked(self):
        
        if self.ppt_size_flag == 1:
            self.table_ppt_size.setColumnHidden(1, False)
        
        else:
            self.pptsizeClicked()
            self.table_ppt_size.setColumnHidden(1, False)
            
    def exportToCSVClicked(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV(*.csv)", options=options)
        
        if fileName != "":
            fileName = fileName + ".csv"
            f = open(fileName, "w")
            
            f.write( "x,y,z,area,radius,major-axis,minor-axis,AR \n" )
            
            for rowNumber in range(self.table_ppt_size.rowCount()):
                for colNumber in range(self.table_ppt_size.columnCount()):
                    f.write(self.table_ppt_size.item(rowNumber, colNumber).text()  )
                    f.write(",")
                f.write("\n")
            
            Submitmsg = QMessageBox()
            Submitmsg.setWindowTitle("File Created")
            Submitmsg.setText("\n Sucessfully created csv file at :\n\n      "+fileName  )
            Submitmsg.exec_()
            
    def plotwrtTimeClicked(self):
        self.table_plot_widget.show()
        self.table_plot_widget.setGeometry(60,90,741,421)
        
        self.fig_table.clear()
        self.ax_table = self.fig_table.add_subplot(111)
            
        
        for i in self.table_ppt_size.selectionModel().selectedColumns():
            
            if self.table_ppt_size.selectionModel().selectedColumns() == 0 or i.column() == 0:
                self.table_closeClicked()
                self.table_plot_widget.hide()
                #self.error_table_plot.setText("Please select a parameter to plot")
                return
                
            if i.column() == 1:
                arr_area = np.empty(len(self.timeItretion))
                for k in range(len(self.timeItretion)):
                    arealist = self.ppt_area[k]
                    arr_area[k] = np.mean(arealist)
                    print(sum(arealist))
                    
                self.ax_table.plot(self.timeItretion,arr_area ,  label="Area")
                
            if i.column() == 2:
                arr_radius = np.empty(len(self.timeItretion))
                for k in range(len(self.timeItretion)):
                    radiuslist = self.ppt_radius[k]
                    arr_radius[k] = np.mean(radiuslist)
                    
                self.ax_table.plot(self.timeItretion,arr_radius , label="Radius")
                
            if i.column() == 3:
                arr_major_axis = np.empty(len(self.timeItretion))
                for k in range(len(self.timeItretion)):
                    major_axislist = self.ppt_major_axis[k]
                    arr_major_axis[k] = np.mean(major_axislist)
                    
                self.ax_table.plot(self.timeItretion,arr_major_axis , label="Major Axis")
                
            if i.column() == 4:
                arr_minor_axis = np.empty(len(self.timeItretion))
                for k in range(len(self.timeItretion)):
                    minor_axislist = self.ppt_minor_axis[k]
                    arr_minor_axis[k] = np.mean(minor_axislist)
                    
                self.ax_table.plot(self.timeItretion,arr_minor_axis , label="Minor Axis")
                
            if i.column() == 5:
                arr_AR = np.empty(len(self.timeItretion))
                for k in range(len(self.timeItretion)):
                    major_axislist = self.ppt_major_axis[k]
                    arr_major = np.mean(major_axislist)
                    minor_axislist = self.ppt_minor_axis[k]
                    arr_minor = np.mean(minor_axislist)
                
                    arr_AR[k] = arr_major/arr_minor
            
                    
                self.ax_table.plot(self.timeItretion,arr_AR , label="Aspect Ratio")
                

        self.ax_table.set_ylabel('Property')
        #self.ax_ppt.grid()
        
        self.ax_table.legend()
        
        self.canvas_table.draw()
        
    def plotwrtTimeAllClicked(self):
        
        arr_area = np.empty(len(self.timeItretion))
        arr_radius = np.empty(len(self.timeItretion))
        arr_major_axis = np.empty(len(self.timeItretion))
        arr_minor_axis = np.empty(len(self.timeItretion))
        arr_AR = np.empty(len(self.timeItretion))
        
        
        for k in range(len(self.timeItretion)):
            arealist = self.ppt_area[k]
            arr_area[k] = np.mean(arealist)
       
            radiuslist = self.ppt_radius[k]
            arr_radius[k] = np.mean(radiuslist)
       
            major_axislist = self.ppt_major_axis[k]
            arr_major_axis[k] = np.mean(major_axislist)
            minor_axislist = self.ppt_minor_axis[k]
            arr_minor_axis[k] = np.mean(minor_axislist)
           
            arr_AR[k] = arr_major_axis[k]/arr_minor_axis[k]
            
        
        
        self.table_plot_widget.show()
        self.table_plot_widget.setGeometry(60,90,741,421)
        
        self.fig_table.clear()
        
        self.ax_table1 = self.fig_table.add_subplot(221)
        self.ax_table1.set_title('Area')
        self.ax_table1.tick_params(labelbottom=False)
        
        self.ax_table2 = self.fig_table.add_subplot(222)
        self.ax_table2.set_title('Radius')
        self.ax_table2.tick_params(labelbottom=False)
        
        self.ax_table3 = self.fig_table.add_subplot(223 , sharex=self.ax_table1)
        self.ax_table3.set_title('Major Axis')
      
        self.ax_table4 = self.fig_table.add_subplot(224 , sharex=self.ax_table2)
        self.ax_table4.set_title('Aspect Ratio')
      
    
        self.ax_table1.plot(self.timeItretion,arr_area)
        self.ax_table2.plot(self.timeItretion,arr_radius,'tab:orange')
        self.ax_table3.plot(self.timeItretion,arr_major_axis,'tab:green')
        self.ax_table4.plot(self.timeItretion,arr_AR,'tab:red')
        
        self.canvas_table.draw()
            
            
    def table_closeClicked(self):
        self.table_plot_widget.hide()
        self.table_plot_widget.setGeometry(0,0,0,0)
        
        
    def fVelocitybtnClicked(self):
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        self.front_velocity_data = front_Velocity(len(self.timeItretion), self.vtkData ,self.scalerValue.currentText(), self.PP_dt, self.PP_savet, self.PP_dx, Is3d, self.depth_plot.value())
        self.front_velocity_data[0] = [0]
        
        self.arr_velocity = np.empty(len(self.timeItretion))
        
        for k in range(len(self.timeItretion)):
            velocitylist = self.front_velocity_data[k]
            self.arr_velocity[k] = np.mean(velocitylist)
            
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.volume_SA_flag = 0
        self.velocity_flag = 1
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)
        
        self.ax_ppt.plot(self.timeItretion,self.arr_velocity)
        self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.arr_velocity[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("Velocity = " + str(self.arr_velocity[self.iteration_step.value()]), loc='center')
        self.ax_ppt.set_xlabel('Timesteps')
        self.ax_ppt.set_ylabel('Average Front Velocity')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        
    def velocity_OverLineClicked(self):
        self.velocity_DrawLineWidget.show()
        
    def velocity_Plot_over_lineBtnClicked(self):
        
        startPoints = self.POL_start_Velocity.text().split(",")
        endPoints = self.POL_end_Velocity.text().split(",")
        
        if len(startPoints) != 2 or len(endPoints) != 2:
            return
        
        x1 , y1 = int(startPoints[0]) , int(startPoints[1])
        x2 , y2 = int(endPoints[0]) , int(endPoints[1])
        
        points = []
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        
        grid_shape = self.vtkData[0].GetDimensions()
        
        if grid_shape[0] == 1:
            grid_reshape = ( grid_shape[1], grid_shape[2]  )
            
        elif grid_shape[1] == 1:
            grid_reshape = ( grid_shape[0], grid_shape[2]  )
            
        elif grid_shape[2] == 1:
            grid_reshape = ( grid_shape[1], grid_shape[0]  )
            
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
            
        
        Phi_sum = []
        
        for n in range(len(self.timeItretion)):
            phi_Value = []
 
            scalar_name_plot = self.scalerValue.currentText()
            
            vtkPointData = self.vtkData[n].GetPointData().GetArray(scalar_name_plot)
            
            if Is3d == 0:
                Phi_data = np.copy(np.reshape(vtkPointData, grid_reshape))
                
        
            elif Is3d == 1 :
                Phi_data = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                Phi_data = Phi_data[depth_plot,:,:]

            
            elif Is3d == 2 :
                Phi_data = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                Phi_data = Phi_data[:,depth_plot,:]
                
            
            elif Is3d == 3 :
                Phi_data = np.copy(np.reshape(vtkPointData,  (grid_shape[2], grid_shape[1], grid_shape[0])))
                Phi_data = Phi_data[:,:,depth_plot]
                
            for i in range(len(points)):
                phi_loc = points[i]
                phi_Value.append(Phi_data[phi_loc[1]][phi_loc[0]])
                
            Phi_sum.append(sum(phi_Value))
        
        self.velocity_OL =  np.empty(len(self.timeItretion) ,  dtype = float)
        self.velocity_OL[0] = 0

        for i in range(1,len(self.timeItretion) ):
            self.velocity_OL[i] = float(self.PP_dx)*((Phi_sum[i] - Phi_sum[i-1])/(float(self.PP_dt)*float(self.PP_savet)))
            
       
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_Count_Plot_flag = 0
        self.ppt_size_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 1
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)

        self.ax_ppt.plot(self.timeItretion, self.velocity_OL)
        
        self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.velocity_OL[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("Velocity =  " + str(self.velocity_OL[self.iteration_step.value()]), loc='center')
        self.ax_ppt.set_xlabel('Iterations')
        self.ax_ppt.set_ylabel('Velocity')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        self.velocity_DrawLineWidget.hide()
        
    def tip_radiusbtnClicked(self):
        
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        self.tip_radius_data= tip_radius_calculate( self.vtkData ,self.timeItretion,self.scalerValue.currentText(), self.PP_dx, Is3d, self.depth_plot.value())
        
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 1
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)
        
        self.ax_ppt.plot(self.timeItretion[1:],self.tip_radius_data[1:])
        
        if self.iteration_step.value() != 0:
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.tip_radius_data[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("Tip Radius = " + str(self.tip_radius_data[self.iteration_step.value()]), loc='center')
        self.ax_ppt.set_xlabel('Timesteps')
        self.ax_ppt.set_ylabel('Tip Radius')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        
    
    def front_undercoolbtnClicked(self):
        
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
                
        AllItems = [self.scalerValue.itemText(i) for i in range(self.scalerValue.count())]
        
        self.front_undercooling= front_undercooling_cal( self.vtkData ,self.timeItretion,self.scalerValue.currentText(),AllItems,  Is3d, self.depth_plot.value())
        
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 1
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)
        
        self.ax_ppt.plot(self.timeItretion[1:],self.front_undercooling[1:])
        
        if self.iteration_step.value() != 0:
            self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.front_undercooling[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("T_front = " + str(self.front_undercooling[self.iteration_step.value()]), loc='center')
        self.ax_ppt.set_xlabel('Timesteps')
        self.ax_ppt.set_ylabel('Front Temperature')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        
    def triple_pointbtnClicked(self):
        
        self.triple_point_value= triple_point( self.vtkData ,self.timeItretion,self.scalerValue.currentText())
        
        self.triple_point_widget.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        
        
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 0
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 1
        
        k = int(self.iteration_step.value())
        self.table_triplePoint.setRowCount(len(self.triple_point_value[k]))
        
        for t in range(len(self.triple_point_value[k])):
            self.table_triplePoint.setItem(t,0,QTableWidgetItem( str(t)))
            self.table_triplePoint.setItem(t,1,QTableWidgetItem( str( self.triple_point_value[k][t]) ))
            
        
        
        for i in self.triple_point_value[k]:
            self.ax.scatter(i[1],i[0],marker='o')
        self.canvas.draw()
            

    
    def phasefracClicked(self):
        
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        self.total_volume, self.volume_fraction , self.total_SA = volFrac_SA_Vol(self.timeItretion, self.vtkData ,self.scalerValue.currentText(), Is3d, self.depth_plot.value())
        
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 1
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)
        
        self.ax_ppt.plot(self.timeItretion,self.volume_fraction)
        self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.volume_fraction[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("Volume Fraction = " + str(round(self.volume_fraction[self.iteration_step.value()], 3)), loc='center')
        self.ax_ppt.set_xlabel('Timesteps')
        self.ax_ppt.set_ylabel('Volume Fraction')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
       
       
    def surfaceAreabtnClicked(self):
        
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        self.total_volume, self.volume_fraction , self.total_SA = volFrac_SA_Vol(self.timeItretion, self.vtkData ,self.scalerValue.currentText(), Is3d, self.depth_plot.value())
        
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 2
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)
        
        self.ax_ppt.plot(self.timeItretion,self.total_SA)
        self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.total_SA[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("Surface Area = " + str(round(self.total_SA[self.iteration_step.value()], 3)), loc='center')
        self.ax_ppt.set_xlabel('Timesteps')
        self.ax_ppt.set_ylabel('Surface Area')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        
        self.canvas_ppt.draw()
        
    def total_vol_btnClicked(self):
        if self.data_3D_flag == 0:
            
            Is3d = 0
            
        elif self.data_3D_flag == 1:
            if self.xyplane_flag == 1 :
                
                Is3d = 1
            
            elif self.yzplane_flag == 1 :
                
                Is3d = 2
                
            
            elif self.xzplane_flag == 1 :
                
                Is3d = 3
        
        self.total_volume, self.volume_fraction , self.total_SA = volFrac_SA_Vol(self.timeItretion, self.vtkData ,self.scalerValue.currentText(), Is3d, self.depth_plot.value())
        
        self.pptPlot.show()
        self.SimulationDetail.hide()
        self.pptRadius.hide()
        self.triple_point_widget.hide()
        
        self.ppt_size_flag = 0
        self.ppt_Count_Plot_flag = 0
        self.velocity_flag = 0
        self.volume_SA_flag = 3
        self.plot_over_line_flag = 0
        self.velocity_over_line_flag = 0
        self.tip_radius_flag = 0
        self.front_undercool_flag = 0
        self.triple_point_flag = 0
        
        self.pptPlot.show()
        self.fig_ppt.clear()
        self.ax_ppt = self.fig_ppt.add_subplot(111)
        self.ax_ppt.plot(self.timeItretion,self.total_volume)
        self.ax_ppt.scatter(self.timeItretion[self.iteration_step.value()], self.total_volume[self.iteration_step.value()], marker ='o')
        self.ax_ppt.set_title("Total Volume = " + str(round(self.total_volume[self.iteration_step.value()], 3)), loc='center')
        self.ax_ppt.set_xlabel('Timesteps')
        self.ax_ppt.set_ylabel('Total Volume')
        self.fig_ppt.subplots_adjust(top=0.905,bottom=0.149,left=0.209,right=0.955,hspace=0.2,wspace=0.2)
        #self.ax_ppt.grid()
        self.canvas_ppt.draw()

        
        

    ##______________________Reset All Func__________________________#

    def resetAll(self):
        self.First_widget.show()
        self.frame_1.show()
        self.frame_2.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        

        self.sideBtn1.setEnabled(True)
        self.sideBtn2.setEnabled(False)
        self.sideBtn3.setEnabled(False)
        self.sideBtn4.setEnabled(False)
        self.sideBtn5.setEnabled(False)
        self.sideBtn6.setEnabled(False)
        self.sideBtn7.setEnabled(False)

        self.sideBtn2.setGeometry(0,185,211,65)
        self.sideBtn3.setGeometry(0,250,211,65)
        self.sideBtn4.setGeometry(0,315,211,65)
        self.sideBtn5.setGeometry(0,380,211,65)
        self.sideBtn6.setGeometry(0,445,211,65)
        self.sideBtn7.setGeometry(0,510,211,65)

        self.btn1.setGeometry(60, 20, 325, 70)
        self.btn2.setGeometry(385, 30, 325, 60)
        self.btn1.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn2.setStyleSheet("background-color: rgb(238, 238, 236)")

        self.btn3.setGeometry(60, 20, 162, 70)
        self.btn4.setGeometry(222, 30, 163, 60)
        self.btn41.setGeometry(385, 30, 162, 60)
        self.btn42.setGeometry(547, 30, 163, 60)
        self.btn3.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn4.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn41.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn42.setStyleSheet("background-color: rgb(238, 238, 236)")

        self.btn5.setGeometry(60, 20, 217, 70)
        self.btn6.setGeometry(277, 30, 216, 60)
        self.btn7.setGeometry(493, 30, 217, 60)
        self.btn5.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn7.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn7.setEnabled(False)

        self.dim.setValue(2)
        self.mesh_x.setText("")
        self.mesh_y.setText("")
        self.mesh_z.setText("1")
        self.mesh_z.setEnabled(False)
        self.dx.setText("")
        self.dy.setText("")
        self.dz.setText("")
        self.dt.setText("")
        self.noP.setValue(1)
        self.noC.setValue(2)
        self.ctext.setPlainText("C1\nC2")
        self.ptext.setPlainText("alpha")
        self.updateNoP()
        self.updateNoC()
        self.timeSteps.setText("")
        self.Nsmooth.setText("")
        self.saveAt.setText("")
        self.reStart.setValue(0)
        self.startTime.setText("0")
        self.startTime.setEnabled(False)
        self.numWorkers.setText("")
        self.gammaInput.setText("")
        self.R_Value.setText("1.0")
        self.V_Value.setText("1.0")
        self.diffR.setChecked(False)
        self.diffR_2.setChecked(True)
        self.diffInput.setText("")
        self.Estrain.setText("0.01,0.01,0.0,0.0,0.0,0.0")
        self.es.setChecked(True)
        self.es_2.setChecked(False)
        self.es_3.setChecked(False)
        self.Econstant.setText("")
        self.gammaInput.setText("")
        self.pDropdown_2.setCurrentIndex(0)
        self.BC_1.setCurrentIndex(1)
        self.BCV_1.setText("0")
        self.BC_2.setCurrentIndex(1)
        self.BCV_2.setText("0")
        self.BC_3.setCurrentIndex(1)
        self.BCV_3.setText("0")
        self.BC_4.setCurrentIndex(1)
        self.BCV_4.setText("0")
        for i in range(4):
            self.Bcnd[i] = "1,1,1,1"
            self.BconV[i] = "0,0,0,0"
        self.ShapeList.clear()

        self.radio_CH.setChecked(False)
        self.radio_GP.setChecked(False)
        self.radio_KKR.setChecked(False)
        self.radio_KKS2.setChecked(False)
        
        self.Qbox.setGeometry(360,260,0,0)
        self.Qbox.hide()

        #Model sepecific parameters

        #GP
        try:
            self.tableWidgetGPA.clearContents()
            self.tableWidgetGP.clearContents()
        except AttributeError:
            pass


        self.thermalYGP.setChecked(True)
        self.thermalNGP.setChecked(False)

        self.simTypeGP.setCurrentIndex(0)
        self.writeFormatGP.setCurrentIndex(0)
        self.writehdfGP.setValue(0)
        self.trackProgressGP.setText("")
        self.epsilonGP.setText("")
        self.tauGP.setText("")
        self.TauGP.setText("")
        self.FanisotropyGP.setText("")
        self.anisotropyTypeGP.setText("")
        self.debGP.setText("")
        self.funcWGP.setText("")
        self.gammaABCGP.setText("")
        self.shiftGP.setValue(0)
        self.shiftJGP.setText("0")
        self.shiftJGP.setEnabled(False)
        self.writecompGP.setText("")
        self.noiseGP.setValue(0)
        self.ampNoiseGP.setText("")
        self.ampNoiseGP.setEnabled(False)
        self.equTGP.setText("")
        self.TGP.setText("")
        self.fillingTGP.setText("")
        self.tempgradyGP.setText("0.96,0.06,800.0,0,0.016")
        self.tempgradyGP.setEnabled(False)
        self.funcF.setValue(1)


        ##CH
        try:
            self.tableWidgetCHA.clearContents()
            #self.tableWidgetCH.clear()
        except AttributeError:
            pass

        self.writeFormatCH.setCurrentIndex(0)
        self.trackProgressCH.setText("")
        self.lPhiCH.setText("")
        self.kappaPhiCH.setText("")
        self.kappaCCH.setText("")
        self.afmCH.setText("")
        self.bfpCH.setText("")
        self.spinodalCH.setValue(0)
        self.tdbflagCH.setValue(0)
        self.tdbfnameCH.setText("")
        self.tdbfnameCH.setEnabled(False)

        #KKS
       

        self.writeFormatKKS.setCurrentIndex(0)
        self.trackprogressKKS.setText("")
        #self.elastIntKKS.setText("")
        self.temperatureKKS.setText("")
        self.TauKKS.setText("")
        self.epsilonKKS.setText("")
        #self.SeedKKS.setText("")
        self.equTKKS.setText("")
    

        #KKS2
        '''
        try:
            self.tableWidgetKKS2.clearContents()
        except AttributeError:
            pass
        '''

        self.thermalYKKS2.setChecked(True)
        self.thermalNKKS2.setChecked(False)
        self.simTypeKKS2.setCurrentIndex(0)
        self.writeFormatKKS2.setCurrentIndex(0)
        self.trackProgressKKS2.setText("")
        self.epsilonKKS2.setText("")
        self.FanisotropyKKS2.setText("")
        self.debKKS2.setText("")
        self.temperatureKKS2.setText("")
        self.noiseKKS2.setValue(0)
        self.ampNoiseKKS2.setText("0")
        self.ampNoiseKKS2.setEnabled(False)
        self.tempGradyKKS2.setText("0.96,0.06,800.0,0,0.016")
        self.tempGradyKKS2.setEnabled(False)
        self.tNoiseStartKKS2.setText("")
        self.TLKKS2.setText("")
        self.atrKKS2.setText("")
        self.CLPidKKS2.setText("")
        self.CLDidKKS2.setText("")
        self.shiftKKS2.setValue(0)
        self.ShiftJKKS2.setText("")
        self.fillingTKKS.setText("")


        ##deleting all Error
        self.error1.setText("")
        self.error2.setText("")
        self.error3.setText("")
        self.error4.setText("")
        self.error5.setText("")
        self.error6.setText("")
        self.error7.setText("")
        self.error8.setText("")
        self.error10.setText("")
        self.finish_error.setText("")
        self.errorCH.setText("")
        self.errorGP.setText("")
        self.errorKKS.setText("")
        self.errorKKS2.setText("")

        self.ShapeList.clear()
        
        #GOING TO FIRST PAGE
        self.clickedBtn1()

        return


    def addShapeFileClicked(self):
        self.ShapefileDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath() )
        try:
                shapeFileDir = open(self.ShapefileDir, 'r')
                ShapeLines = shapeFileDir.readlines()
                self.StartFrame.hide()
                self.ShapeFlag = 1

                for i in ShapeLines:

                    if "#" in i:
                        pass

                    elif "=" in i and "FILL" in i:
                        i = i.replace(" ","")
                        i = i.replace(";","")
                        i = i.replace("="," ")
                        i = i.replace("\n","")
                        i = i.replace("FILL","")
                        self.ShapeList.addItem(i)

        except IOError:
            print("could not read")

        except UnicodeDecodeError:
            print("could not read")
        


    def openFileDir(self):
        if self.model_GP.isChecked() or self.model_CH.isChecked() or self.model_KKS.isChecked() or self.model_KKS2.isChecked() :
            self.errorStartScreen.setText("")
            self.fileNameDir, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath() , 'InFile(*.in)')
            self.fileLabel.setText(self.fileNameDir)
            self.ReadfromFile()
        else:
            self.errorStartScreen.setText("Please selct the Model")
            return


    def drawMesh(self):

        if self.mesh_x.text() !="":
            self.Qbox.setGeometry(380,350,200,4)
            self.Qbox.show()
            self.error1.setText("")
        else:
            self.Qbox.hide()

        if self.mesh_y.text() !="" and self.mesh_x.text() !="":

            try:
                x_dim = float(self.mesh_x.text())
                self.error1.setText("")

            except ValueError:
                self.error1.setText("Please enter valid Mesh X")
                return

            try:
                y_dim = float(self.mesh_y.text())
                self.error1.setText("")

            except ValueError:
                self.error1.setText("Please enter valid Mesh Y")
                return

            if x_dim > y_dim:
                self.Qbox.setGeometry(380,370 - round((y_dim/x_dim)*90),200,round((y_dim/x_dim)*200))
            elif x_dim < y_dim:
                self.Qbox.setGeometry(490 - round((x_dim/y_dim)*90) ,270,  round((x_dim/y_dim)*200),200)
            else:
                self.Qbox.setGeometry(380,270,200,200)

            self.Qbox.show()

        if self.dx.text() !="" and self.dy.text() !="":
            self.draw_dx()
            self.draw_dy()


    def draw_dx(self):
        v = [self.v_0,self.v_1,self.v_2,self.v_3,self.v_4,self.v_5,self.v_6,self.v_7,self.v_8,self.v_9]
        if self.dx.text() !="" and float(self.dx.text()) > 0:

            Qwidth = self.Qbox.frameGeometry().width()
            Qheight = self.Qbox.frameGeometry().height()
            for i in range(9):
                v[i].setGeometry(round((Qwidth/10)*(i+1)),1,1,Qheight-1)

        else:
            for i in range(9):
                v[i].setGeometry(0,0,0,0)


    def draw_dy(self):
        h = [self.h_0,self.h_1,self.h_2,self.h_3,self.h_4,self.h_5,self.h_6,self.h_7,self.h_8,self.h_9,self.h_10,self.h_11,self.h_12,self.h_13,self.h_14,self.h_15,self.h_16,self.h_17,self.h_18,self.h_19,self.h_20,self.h_21,self.h_22,self.h_23,self.h_24,self.h_25,self.h_26,self.h_27,self.h_28,self.h_29,self.h_30,self.h_31,self.h_32,self.h_33,self.h_34,self.h_35,self.h_36,self.h_37,self.h_38,self.h_39,self.h_40,self.h_41,self.h_42,self.h_43,self.h_44,self.h_45,self.h_46,self.h_47,self.h_48,self.h_49,self.h_50]
        for i in range(51):
            h[i].setGeometry(0,0,0,0)

        #error Handling
        try:
            dx_value = float(self.dx.text())
            self.error2.setText("")

        except ValueError:
            self.error2.setText("dx : Value Error ")
            return

        try:
            dy_value = float(self.dy.text())
            self.error2.setText("")

        except ValueError:
            self.error2.setText("dy : Value Error ")
            return

        if dx_value == 0:
            self.error2.setText("dx cannot be equal to 0")
            return
        if dy_value == 0:
            self.error2.setText("dy cannot be equal to 0")
            return

        if self.dy.text() !="" and float(self.dy.text()) > 0:

            Qwidth = self.Qbox.frameGeometry().width()
            Qheight = self.Qbox.frameGeometry().height()

            dy_dx = dy_value/dx_value
            no_hl = round((dy_dx)*(Qwidth/10))

            if  dy_dx> 2 or dy_dx < 0.5:
                no_hl = 2*(Qwidth/10)

            try:
                num_lines = round(Qheight/no_hl)
            except ZeroDivisionError:
                return

            if len(h) < num_lines:
                num_lines = len(h)
                no_hl = 2*(Qwidth/10)
                
            for i in range(num_lines):
                h[i].setGeometry(1 , round(no_hl*(i+1)), Qwidth-1 , 1  )

        return

## All Value Change Function (Flags)
    def updateDim(self):
        if(self.dim.value() == 2):
            self.mesh_z.setText("1")
            self.mesh_z.setEnabled(False)
        else:
            self.mesh_z.setEnabled(True)

    def reStartFun(self):
        if(self.reStart.value() == 1):
            self.startTime.setEnabled(True)
        elif(self.reStart.value() == 0):
            self.startTime.setEnabled(False)

    def updateshiftGP(self):
        if(self.shiftGP.value() == 1):
            self.shiftJGP.setEnabled(True)
        elif(self.shiftGP.value() == 0):
            self.shiftJGP.setEnabled(False)

    def radio_thermalYGPToggled(self):
        if self.thermalYGP.isChecked():
            self.tempgradyGP.setEnabled(False)
        else:
            self.tempgradyGP.setEnabled(True)


    def radio_thermalNGPToggled(self):
        if self.thermalNGP.isChecked():
            self.tempgradyGP.setEnabled(True)
        else:
            self.tempgradyGP.setEnabled(False)
            
    def updateshiftKKS2(self):
        if(self.shiftKKS2.value() == 1):
            self.ShiftJKKS2.setEnabled(True)
        elif(self.shiftKKS2.value() == 0):
            self.ShiftJKKS2.setEnabled(False)

    def radio_thermalYKKS2Toggled(self):
        if self.thermalYKKS2.isChecked():
            self.tempGradyKKS2.setEnabled(False)
        else:
            self.tempGradyKKS2.setEnabled(True)


    def radio_thermalNKKS2Toggled(self):
        if self.thermalNKKS2.isChecked():
            self.tempGradyKKS2.setEnabled(True)
        else:
            self.tempGradyKKS2.setEnabled(False)

#Noise Flag
    def updatenoiseGPflag(self):
        if self.noiseGP.value() == 0:
            self.ampNoiseGP.setEnabled(False)

        elif self.noiseGP.value() == 1:
            self.ampNoiseGP.setEnabled(True)

    def updatenoiseKKSflag(self):
        if self.noiseKKS.value() == 0:
            self.ampNoiseKKS.setEnabled(False)

        elif self.noiseKKS.value() == 1:
            self.ampNoiseKKS.setEnabled(True)

    def updatenoiseKKS2flag(self):
        if self.noiseKKS2.value() == 0:
            self.ampNoiseKKS2.setEnabled(False)

        elif self.noiseKKS2.value() == 1:
            self.ampNoiseKKS2.setEnabled(True)


    def phaseBtnClicked(self):
        self.pwidget.show()
        self.next2.setEnabled(False)
        self.componentbtn.setEnabled(False)
        self.phasebtn.setEnabled(False)


    def phaseSaveBtnClicked(self):

        Pnames = self.ptext.toPlainText().splitlines()

        if len(Pnames) != self.noP.value():
            self.perror.setText( str(self.noP.value()) + " phase names required" )
        else:
            for i in range(len(Pnames)):
                self.pDropdown.setItemText(i,Pnames[i])
                self.pDropdown_3.setItemText(i,Pnames[i])

            self.pwidget.hide()
            self.next2.setEnabled(True)
            self.componentbtn.setEnabled(True)
            self.phasebtn.setEnabled(True)
            self.perror.setText("")


    def updateNoP(self):
        noP_value = self.noP.value()
        if(noP_value == 2):
            self.ptext.setPlainText("alpha\nbeta")
            self.gammaABCGP.setEnabled(False)


        elif (noP_value == 3):
            self.ptext.setPlainText("alpha\nbeta\ngamma")
            self.gammaABCGP.setEnabled(True)


        elif(noP_value == 1):
            self.ptext.setPlainText("alpha")
            self.gammaABCGP.setEnabled(False)


        elif (noP_value > 3 ):
            self.gammaABCGP.setEnabled(True)
            Pnames = self.ptext.toPlainText().splitlines()

            if len(Pnames) < noP_value :
                Phase_text2 = self.ptext.toPlainText()

                for i in range(noP_value - len(Pnames) ):
                    Phase_text2 = Phase_text2 +"\nP" +str(len(Pnames)+1+i)

                self.ptext.setPlainText(Phase_text2)

            if len(Pnames) > noP_value:
                Phase_text2 = Pnames[0]
                for i in range(1,noP_value,1):
                    Phase_text2 = Phase_text2 + "\n" + Pnames[i]

                self.ptext.setPlainText(Phase_text2)

        #function start
        Pnames = self.ptext.toPlainText().splitlines()
        Ndropdown = self.pDropdown.count()

        if Ndropdown < noP_value:
            for i in range(noP_value - Ndropdown):
                self.pDropdown.addItem(Pnames[Ndropdown +i])
                self.Diffusivity.append("")
                self.DiffusivityType.append("")
                self.eigenStrain.append("")
                self.elasticConstant.append("")
                self.elasticType.append("")

                self.pDropdown_3.addItem(Pnames[Ndropdown +i])
                self.domainType.append("")
                self.domainValue.append("")

        elif Ndropdown > noP_value:
            for i in range(Ndropdown - noP_value):
                self.pDropdown.removeItem(self.pDropdown.count() -1)
                self.Diffusivity.pop()
                self.DiffusivityType.pop()
                self.eigenStrain.pop()
                self.elasticConstant.pop()
                self.elasticType.pop()

                self.pDropdown_3.removeItem(self.pDropdown_3.count() -1)
                self.domainType.pop()
                self.domainValue.pop()

        #GP model
        self.tableWidgetGP.setRowCount(noP_value**2)
        self.tableWidgetGPA.setRowCount(noP_value)

        #self.tableWidgetKKS.setRowCount(noP_value**2)
        #self.tableWidgetKKS2.setRowCount(noP_value**2)
        #self.tableWidgetKKSF.setRowCount(noP_value)

        #self.tableWidgetCH.setRowCount(noP_value**2)
        self.tableWidgetCHA.setRowCount(noP_value)
        #self.tableWidgetGP.setItem((noP_value*noP_value)-1,4, QTableWidgetItem(str("-")))  ## filling last column of slope

        rcount =0

        for i in range(noP_value):

            self.tableWidgetGPA.setItem(i,0, QTableWidgetItem(str(i)))
            self.tableWidgetGPA.item(i,0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidgetGPA.item(i,0).setFlags(self.tableWidgetGPA.item(i,0).flags() & ~QtCore.Qt.ItemIsEditable)

            #self.tableWidgetKKSF.setItem(i,0, QTableWidgetItem(str(i)))
            #self.tableWidgetKKSF.item(i,0).setTextAlignment(QtCore.Qt.AlignCenter)
            #self.tableWidgetKKSF.item(i,0).setFlags(self.tableWidgetKKSF.item(i,0).flags() & ~QtCore.Qt.ItemIsEditable)

            self.tableWidgetCHA.setItem(i,0, QTableWidgetItem(str(i)))
            self.tableWidgetCHA.item(i,0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidgetCHA.item(i,0).setFlags(self.tableWidgetCHA.item(i,0).flags() & ~QtCore.Qt.ItemIsEditable)

            self.tableWidgetCHA.setItem(i,1, QTableWidgetItem(str("DM")))
            self.tableWidgetCHA.item(i,1).setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidgetCHA.item(i,1).setFlags(self.tableWidgetCHA.item(i,0).flags() & ~QtCore.Qt.ItemIsEditable)



            for j in range(noP_value):
                #Phase-composition Table 
                self.tableWidgetGP.setItem(rcount,0, QTableWidgetItem(str(i)))
                self.tableWidgetGP.setItem(rcount,1, QTableWidgetItem(str(j)))
                self.tableWidgetGP.item(rcount,0).setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidgetGP.item(rcount,1).setTextAlignment(QtCore.Qt.AlignCenter)

                self.tableWidgetGP.item(rcount,0).setFlags(self.tableWidgetGP.item(rcount,0).flags() & ~QtCore.Qt.ItemIsEditable)
                self.tableWidgetGP.item(rcount,1).setFlags(self.tableWidgetGP.item(rcount,1).flags() & ~QtCore.Qt.ItemIsEditable)

                
                
                if j==i or j<i:
                    self.tableWidgetGP.setItem(rcount,6, QTableWidgetItem(str("-"))) #Rotation 
                    #self.tableWidgetKKS2.setItem(rcount,4, QTableWidgetItem(str("-")))

                else:
                    self.tableWidgetGP.setItem(rcount,6, QTableWidgetItem(str("")))
                    #self.tableWidgetKKS2.setItem(rcount,4, QTableWidgetItem(str("")))

                if j!= (noP_value-1) and i!=j:
                    #GP Ceq Cfil Cslope
                    self.tableWidgetGP.setItem(rcount,2, QTableWidgetItem(str("-")))
                    self.tableWidgetGP.setItem(rcount,3, QTableWidgetItem(str("-")))
                    self.tableWidgetGP.setItem(rcount,4, QTableWidgetItem(str("-")))
                    self.tableWidgetGP.setItem(rcount,5, QTableWidgetItem(str("-")))
                else:
                    self.tableWidgetGP.setItem(rcount,2, QTableWidgetItem(str("")))
                    self.tableWidgetGP.setItem(rcount,3, QTableWidgetItem(str("")))
                    self.tableWidgetGP.setItem(rcount,4, QTableWidgetItem(str("")))
                    self.tableWidgetGP.setItem(rcount,5, QTableWidgetItem(str("")))
                    

          
                rcount = rcount +1


    def componentBtnClicked(self):
        self.pwidget_2.show()  #component Widget
        self.next2.setEnabled(False)
        self.componentbtn.setEnabled(False)
        self.phasebtn.setEnabled(False)



    def componentSaveBtnClicked(self):
        Cnames = self.ctext.toPlainText().splitlines()

        if len(Cnames) != self.noC.value():
            self.cerror.setText( str(self.noC.value()) + " Components required" )
        else:
            self.pwidget_2.hide()
            self.next2.setEnabled(True)
            self.componentbtn.setEnabled(True)
            self.phasebtn.setEnabled(True)
            self.cerror.setText( "" )


    def updateNoC(self):
        noC_value = self.noC.value()
        Cnames = self.ctext.toPlainText().splitlines()

        if len(Cnames) < noC_value :
            Com_text2 = self.ctext.toPlainText()

            for i in range(noC_value - len(Cnames) ):
                Com_text2 = Com_text2 +"\nC" +str(len(Cnames)+1+i)

            self.ctext.setPlainText(Com_text2)

        if len(Cnames) > noC_value:
            Com_text2 = Cnames[0]
            for i in range(1,noC_value,1):
                Com_text2 = Com_text2 + "\n" + Cnames[i]

            self.ctext.setPlainText(Com_text2)

        #Changing input length of Diffusion

        diffData = str(self.diffInput.text())
        matData = diffData.split(",")

        k=self.noC.value()-1

        if len(matData) > k and self.diffR_2.isChecked():
            ReducedText = matData[0]
            for i in range(1,k ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.diffInput.setText(ReducedText)

        if len(matData) > k*k and self.diffR.isChecked():
            ReducedText = matData[0]
            for i in range(1,k*k ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.diffInput.setText(ReducedText)


    def clickedBtn1(self):

        #frame Hide/Show
        self.frame_1.show()
        self.frame_2.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        self.First_widget.show()

        #Btn Animation
        self.btn1.setGeometry(60, 20, 325, 70)
        self.btn2.setGeometry(385, 30, 325, 60)


        self.btn1.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn2.setStyleSheet("background-color: rgb(238, 238, 236)")

        self.Qbox.show()
        self.Qbox.setStyleSheet("background-color: rgb(218, 218, 218); border: 1px solid rgb(77, 77, 77);")

    def clickedBtn2(self):

        if(self.dim.value() <= 1 or self.dim.value() > 3 ):
            self.error1.setText("Dimension should be 2D or 3D")
            return

        elif (self.mesh_x.text() == "" or int(self.mesh_x.text()) < 1):
            self.error1.setText("Please Fill valid MESH - X")
            return

        elif (self.mesh_y.text() == "" or int(self.mesh_x.text()) < 1):
            self.error1.setText("Please Fill valid MESH - Y")
            return

        elif (self.mesh_z.text() == "" or int(self.mesh_x.text()) < 1):
            self.error1.setText("Please Fill valid MESH - Z")
            return

        else:
            self.error1.setText("")

        self.frame_2.show()
        self.frame_1.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        self.First_widget.show()

        self.btn1.setGeometry(60, 30, 325, 60)
        self.btn2.setGeometry(385, 20, 325, 70)

        self.btn2.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn1.setStyleSheet("background-color: rgb(238, 238, 236)")

        self.Qbox.show()


    def clickedBtn3(self):

        #frame Hide/Show
        self.frame_6.hide()
        self.frame_61.hide()
        self.frame_62.hide()
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()

        self.Qbox.hide()

        self.Four_widget.show()
        self.frame_5.show()
        
        
        #Btn Animation
        self.btn3.setGeometry(60, 20, 162, 70)
        self.btn4.setGeometry(222, 30, 163, 60)
        self.btn41.setGeometry(385, 30, 162, 60)
        self.btn42.setGeometry(547, 30, 163, 60)
        self.btn3.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn4.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn41.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn42.setStyleSheet("background-color: rgb(238, 238, 236)")


    def clickedBtn4(self):

        if self.phaseSave():

            k = self.noP.value()
            l = self.noC.value() -1

            for i in range(k):
                if self.DiffusivityType[i] == "0" and len(self.Diffusivity[i].split(",")) != l*l:
                    return

                if self.DiffusivityType[i] == "1" and ( len(self.Diffusivity[i].split(",")) < l or len(self.Diffusivity[i].split(",")) > l*l )  :
                    return

                if len(self.eigenStrain[i].split(",")) != 6:
                    return

                if self.elasticType == "0" and len(self.elasticConstant[i].split(",")) != 3:
                    return

                if self.elasticType == "1" and len(self.elasticConstant[i].split(",")) != 3:
                    return

                if self.elasticType == "2" and len(self.elasticConstant[i].split(",")) != 6:
                    return
        else:
            return

        self.error6.setText("")

        #frame Hide/Show
        self.frame_5.hide()
        self.frame_61.hide()
        self.frame_62.hide()
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()

        self.Qbox.hide()

        self.Four_widget.show()
        self.frame_6.show()


        #Btn Animation
        self.btn3.setGeometry(60, 30, 162, 60)
        self.btn4.setGeometry(222, 20, 163, 70)
        self.btn41.setGeometry(385, 30, 162, 60)
        self.btn42.setGeometry(547, 30, 163, 60)
        self.btn3.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn4.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn41.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn42.setStyleSheet("background-color: rgb(238, 238, 236)")


    def clickedBtn41(self):

        gammaData = self.gammaInput.text().split(",")

        k=self.noP.value()
        max_len = k*((k -1 )/2)


        if self.gammaInput.text() == "":
            self.error6.setText("Please fill Gamma Value")
            return

        elif len(gammaData) != max_len:
            self.error6.setText("Invalid Gamma tuple length")
            return

        elif self.R_Value.text()=="":
            self.error6.setText("Please fill R Value")
            return

        elif self.V_Value.text()=="":
            self.error6.setText("Please fill V Value")
            return

        else:
            self.error6.setText("")

        #frame Hide/Show
        self.frame_5.hide()
        self.frame_6.hide()
        self.frame_62.hide()
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()

        self.Qbox.hide()

        self.Four_widget.show()
        self.frame_61.show()


        #Btn Animation
        self.btn3.setGeometry(60, 30, 162, 60)
        self.btn4.setGeometry(222, 30, 163, 60)
        self.btn41.setGeometry(385, 20, 162, 70)
        self.btn42.setGeometry(547, 30, 163, 60)
        self.btn3.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn41.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn4.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn42.setStyleSheet("background-color: rgb(238, 238, 236)")
        
    def clickedBtn42(self):

        noP_value = self.noP.value()
        
        if self.funcF.value() == 1:
            for i in range(noP_value):
                if self.tableWidgetGPA.item(i,1) is None or self.tableWidgetGPA.item(i,1).text() == '':
                    self.error62.setText("Fill All values of A. If not required then put '-'")
                    return 
                
        elif self.funcF.value() == 2 or self.funcF.value() == 3 or self.funcF.value() == 4 :
            if self.num_thermo_phases.value() == 0 :
                self.error62.setText("Incorrect num_thermo_phases")
                return 
            elif self.tdbfname.text() == "":
                self.error62.setText("Please fill tdbfname")
                return 
            
            elif self.tdbphases.text() == "":
                self.error62.setText("Please fill Tdb Phases")
                return 
            
            elif len(self.tdbphases.text().split(",")) != self.num_thermo_phases.value() :
                self.error62.setText("Required " + str(self.num_thermo_phases.value()) + " values for Tdb Phases" )
                return 
        
            elif self.phasemap.text() == "":
                self.error62.setText("Please fill Phase Map")
                return 
            
            elif len(self.phasemap.text().split(",")) != noP_value:
                self.error62.setText("Required " + str(noP_value) + " values for Phase Map" )
                return 
        self.error62.setText("")

        #frame Hide/Show
        self.frame_5.hide()
        self.frame_6.hide()
        self.frame_61.hide()
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()

        self.Qbox.hide()

        self.Four_widget.show()
        self.frame_62.show()


        #Btn Animation
        self.btn3.setGeometry(60, 30, 162, 60)
        self.btn4.setGeometry(222, 30, 163, 60)
        self.btn41.setGeometry(385, 30, 162, 60)
        self.btn42.setGeometry(547, 20, 163, 70)
        self.btn4.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn3.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn42.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn41.setStyleSheet("background-color: rgb(238, 238, 236)")
        

    def clickedBtn5(self):

        #frame Hide/Show
        self.frame_8.show()
        self.frame_9.hide()
        self.frame_11.hide()
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.show()

        self.Qbox.hide()

        #Btn Animation
        self.btn5.setGeometry(60, 20, 217, 70)
        self.btn6.setGeometry(277, 30, 216, 60)
        self.btn7.setGeometry(493, 30, 217, 60)


        self.btn5.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn7.setStyleSheet("background-color: rgb(238, 238, 236)")


    def clickedBtn6(self):


        if self.radio_GP.isChecked() == False and self.radio_CH.isChecked() == False and self.radio_KKR.isChecked() == False and self.radio_KKS2.isChecked() == False:
            self.error8.setText("Please select a model")
            return

        self.error8.setText("")

        #frame Hide/Show
        self.frame_8.hide()
        self.frame_11.hide()
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.show()


        self.Qbox.hide()
        self.frame_9.show()


        #Btn Animation
        self.btn5.setGeometry(60, 30, 217, 60)
        self.btn6.setGeometry(277, 20, 216, 70)
        self.btn7.setGeometry(493, 30, 217, 60)


        self.btn6.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn5.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn7.setStyleSheet("background-color: rgb(238, 238, 236)")


    def clickedBtn7(self):

        if self.radio_GP.isChecked() and self.saveGPChack() or self.radio_KKR.isChecked() and self.saveKKSCheck() or self.radio_KKS2.isChecked() and self.saveKKS2Check() or self.radio_CH.isChecked() and self.saveGPChack():

            self.frame_8.hide()
            self.frame_9.hide()
            self.First_widget.hide()
            self.Second_widget.hide()
            self.Third_widget.hide()
            self.Four_widget.hide()
            self.Fifth_widget.hide()
            self.Sixth_widget.hide()
            self.Seven_widget.show()


            self.Qbox.hide()
            self.frame_11.show()


            #Btn Animation
            self.btn5.setGeometry(60, 30, 217, 60)
            self.btn6.setGeometry(277, 30, 216, 60)
            self.btn7.setGeometry(493, 20, 217, 70)


            self.btn7.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
            self.btn5.setStyleSheet("background-color: rgb(238, 238, 236)")
            self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")



    def NextBtn1(self):

        if (self.dx.text() == ""):
            self.error2.setText("Please Fill valid dx")
            return

        elif (self.dy.text() == ""):
            self.error2.setText("Please Fill valid Dy")
            return

        elif (self.dz.text() == ""):
            self.error2.setText("Please Fill valid dz")
            return

        elif (self.dt.text() == ""):
            self.error2.setText("Please Fill valid Dt")
            return

        else:
            self.error2.setText("")

        self.First_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        self.Third_widget.hide()
        self.Qbox.hide()
        self.Second_widget.show()

        self.sideBtn2.setGeometry(0,185,231,65)
        self.sideBtn2.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
        self.sideBtn2.setEnabled(True)


    def NextBtn2(self):
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Four_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        self.Third_widget.show()

        self.sideBtn3.setGeometry(0,250,231,65)
        self.sideBtn3.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
        self.sideBtn3.setEnabled(True)
        self.Qbox.hide()


    def NextBtn3(self):
        if (self.timeSteps.text() == ""):
            self.error4.setText("Please Fill valid TimeSteps")
            return

        elif (self.Nsmooth.text() == ""):
            self.error4.setText("Please Fill valid Nsmooth")
            return

        elif (self.saveAt.text() == ""):
            self.error4.setText("Please Fill valid Save Interval")
            return

        elif (self.startTime.text() == ""):
            self.error4.setText("Please Fill valid Start Time")
            return

        else:
            self.error4.setText("")
        
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Third_widget.hide()
        self.Four_widget.show()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()

        self.sideBtn4.setGeometry(0,315,231,65)
        self.sideBtn4.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
        self.sideBtn4.setEnabled(True)
        self.Qbox.hide()

        k = self.noC.value()-1

        if k<5:
            self.diffMat.setGeometry(160-(28*k), 150-(23*k), 56*k, 46*k)
            self.line_2.setGeometry(0,46*k-2,10,2)
            self.line_3.setGeometry(56*k-10,0,10,2)
            self.line_4.setGeometry(56*k-10,46*k-2,10,2)
        else:
            self.diffMat.setGeometry(48, 58, 224, 184)
            self.line_2.setGeometry(0,182,10,2)
            self.line_3.setGeometry(214,0,10,2)
            self.line_4.setGeometry(214,182,10,2)


        Wlen = (len(self.diffMat.children()) - 5)**0.5

        if Wlen == 0:
            self.diffMatIn = [[0 for x in range(20)] for y in range(20)]

            for i in range(k):
                for j in range(k):
                    self.diffMatIn[i][j] = QLabel()
                    self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))
                    self.diffMatIn[i][j].setAlignment(QtCore.Qt.AlignCenter)
                    self.diffMatIn[i][j].setStyleSheet("color : #fff ; font: 75 11pt 'Ubuntu';")
                    if k<5:
                        self.diffMatIn[i][j].setFixedHeight(40)
                        self.diffMatIn[i][j].setStyleSheet("color : #fff ; font: 75 10pt 'Ubuntu';")

                    self.diffMat.layout().addWidget(self.diffMatIn[i][j], i,j)

        elif k < Wlen:
            for i in range(int(Wlen)):
                for j in range(int(Wlen)):
                    if i > k-1 or j > k-1 :
                        self.diffMatIn[i][j].deleteLater()

        elif k > Wlen:
            for i in range(k):
                for j in range(k):
                    if i > int(Wlen-1) or j > int(Wlen-1) :

                        self.diffMatIn[i][j] = QLabel()

                        #filling diffusion matrix based on condition
                        if self.diffR_2.isChecked():
                            if i ==j :
                                self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))
                            else:
                                self.diffMatIn[i][j].setText("-")
                        elif self.diffR.isChecked():
                            self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))


                        self.diffMatIn[i][j].setAlignment(QtCore.Qt.AlignCenter)
                        self.diffMatIn[i][j].setStyleSheet("color : #fff ; font: 75 11pt 'Ubuntu';")
                        if k<5:
                            self.diffMatIn[i][j].setFixedHeight(40)
                            self.diffMatIn[i][j].setStyleSheet("color : #fff ; font: 75 10pt 'Ubuntu';")

                        self.diffMat.layout().addWidget(self.diffMatIn[i][j], i,j)

        if self.elasticType[0] != '':

            if self.elasticType[0] == '0':
                self.es.setChecked(True)
                self.es_2.setChecked(False)
                self.es_3.setChecked(False)

            elif self.elasticType[0] == '1':
                self.es.setChecked(False)
                self.es_2.setChecked(True)
                self.es_3.setChecked(False)

            elif self.elasticType[0] == '2':
                self.es.setChecked(False)
                self.es_2.setChecked(False)
                self.es_3.setChecked(True)

        if self.DiffusivityType[0] !='':

            if self.DiffusivityType[0] == '0':
                self.diffR_2.setChecked(True)
                self.diffR_2.setChecked(False)
                self.diffR.setChecked(True)

            elif self.DiffusivityType[0] == '1':
                self.diffR.setChecked(True)
                self.diffR.setChecked(False)
                self.diffR_2.setChecked(True)


    def NextBtn4(self):
        
        

        

        self.First_widget.hide()
        self.Second_widget.hide()
        self.Four_widget.hide()
        self.Third_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.hide()
        self.Fifth_widget.show()

        self.sideBtn5.setGeometry(0,380,231,65)
        self.sideBtn5.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
        self.sideBtn5.setEnabled(True)
        self.Qbox.show()

    def NextBtn5(self):

        if self.phaseSave_BC():


            if self.BconV[0] =="" and len(self.BconV[0].split(",")) != 4:
                self.error7.setText("Please fill Boundary condtions Phi")
                return

            elif self.BconV[1] =="" and len(self.BconV[1].split(",")) != 4 and self.BconV[2] =="" and len(self.BconV[2].split(",")) != 4:
                self.error7.setText("Please fill Boundary condtions mu/c")
                return

            elif self.BconV[3] =="" and len(self.BconV[3].split(",")) != 4:
                self.error7.setText("Please fill Boundary condtions T")
                return
            else:
                self.error7.setText("")

        else:
            return


        self.addShape.setText("Add " + self.shape.currentText() +  " | "+self.pDropdown_3.currentText())

        self.First_widget.hide()
        self.Second_widget.hide()
        self.Four_widget.hide()
        self.Third_widget.hide()
        self.Fifth_widget.hide()
        self.Seven_widget.hide()
        self.Sixth_widget.show()

        self.sideBtn6.setGeometry(0,445,231,65)
        self.sideBtn6.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
        self.sideBtn6.setEnabled(True)
        self.Qbox.hide()

    def NextBtn6(self):

        if self.phaseSave():
            self.error6.setText("")
        else:
            return

        if self.phaseSave_BC():
            self.error6.setText("")
        else:
            return

        if self.ShapeList.count() == 0 and self.ShapeFlag == 0:
            self.error10.setText("required atleast 1 filling condition")
            return
        self.error10.setText("")
        self.First_widget.hide()
        self.Second_widget.hide()
        self.Four_widget.hide()
        self.Third_widget.hide()
        self.Fifth_widget.hide()
        self.Sixth_widget.hide()
        self.Seven_widget.show()
        
        #opening First frame here, As a default
        self.frame_8.show()
        self.frame_9.hide()
        self.frame_11.hide()
        #Btn Animation
        self.btn5.setGeometry(60, 20, 217, 70)
        self.btn6.setGeometry(277, 30, 216, 60)
        self.btn7.setGeometry(493, 30, 217, 60)


        self.btn5.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
        self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")
        self.btn7.setStyleSheet("background-color: rgb(238, 238, 236)")

        self.sideBtn7.setGeometry(0,510,231,65)
        self.sideBtn7.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
        self.sideBtn7.setEnabled(True)
        self.Qbox.hide()


    def FillDiffMat(self):
        diffData = str(self.diffInput.text())
        matData = diffData.split(",")
        k=self.noC.value()-1

        if len(matData) > k*k and self.diffR.isChecked():
            ReducedText = matData[0]
            for i in range(1,k*k ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.diffInput.setText(ReducedText)
            return

        if len(matData) > k and self.diffR_2.isChecked():
            ReducedText = matData[0]
            for i in range(1,k ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.diffInput.setText(ReducedText)
            return


        diffarray = [None]*k

        for i in range(k):
            diffarray[i] = self.diffMatIn[i][i]

        if self.diffR.isChecked():
            for i in range(k):
                for j in range(k):
                    if i!=j:
                        diffarray.append(self.diffMatIn[i][j])

        for i in range(len(matData)):
            diffarray[i].setText(matData[i])

        for i in range(k):
            for j in range(k):
                if self.diffMatIn[i][j].text() == "":
                    self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))


    def  dMatrixToggled(self):
        diffData = str(self.diffInput.text())
        matData = diffData.split(",")

        k=self.noC.value()-1

        if len(matData) > k and self.diffR_2.isChecked():
            ReducedText = matData[0]
            for i in range(1,k ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.diffInput.setText(ReducedText)

        for i in range(k):
            for j in range(k):
                if i!=j:
                    self.diffMatIn[i][j].setText("-")


    def  fMatrixToggled(self):
        diffData = str(self.diffInput.text())
        matData = diffData.split(",")

        k=self.noC.value()-1

        for i in range(k):
            for j in range(k):
                if i!=j:
                    if self.diffMatIn[i][j].text() == "-":
                        self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))



    def FillGammaMat(self):
        self.widgetGamma.show()
         
        self.error6.setText("")
        gammaData = self.gammaInput.text()
        matData = gammaData.split(",")
        k=self.noP.value()
        max_len = k*((k -1 )/2)
        
        GIndex = [""]*int(max_len)
        flag = 0
        for i in range(k):
            for j in range(k):
                if i<j :
                    GIndex[flag] = str(i+1) + str(j+1)
                    flag = flag +1 
                    
        if len(matData) > max_len:
            ReducedText = matData[0]
            for i in range(1,int(max_len) ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.gammaInput.setText(ReducedText)
            return
        else:
            self.gammaV.setText(GIndex[len(matData) -1 ])
            pass

    def FillGammaABC(self):
        self.widgetGammaABC.show()

        self.errorGP.setText("")
        gammaData = self.gammaABCGP.text()
        matData = gammaData.split(",")
        k=self.noP.value()
        max_len =  int(k * ((k - 1)*(k - 2) / 6))

        GIndex = [""]*max_len
        flag = 0
        for i in range(k):
            for j in range(k):
                for l in range(k):
                    if i<j and j<l:
                        GIndex[flag] = str(i+1) + str(j+1) + str(l+1)
                        flag = flag +1

        if len(matData) > max_len:
            ReducedText = matData[0]
            for i in range(1,int(max_len) ,1):
                ReducedText = ReducedText + "," + matData[i]

            self.gammaABCGP.setText(ReducedText)
            return
        else:
            self.GammaABCGPV.setText(GIndex[len(matData) -1 ])
            pass


    def phaseChange(self):
        currentPhase = self.pDropdown.currentIndex()

        if currentPhase == 0:
            self.allCheck.hide()

        else:
            self.allCheck.show()


        if currentPhase > int(self.marker.text()) and self.phaseSave():

            self.marker.setText(str(currentPhase ) )
            if self.Diffusivity[currentPhase] == "":
                self.phaseReset()
            else:
                self.phaseRetrive()

            self.error5.setText("")

        elif currentPhase < int(self.marker.text()) and self.phaseSave() :
            self.phaseRetrive()
            self.marker.setText(str(currentPhase ))
            return

        else:
            self.pDropdown.setCurrentIndex(int(self.marker.text()))
            return



    def phaseReset(self):
        self.allCheck.setChecked(False)
        self.diffR.setChecked(True)
        self.es.setChecked(True)

        self.diffInput.setText("")
        self.Estrain.setText("0.01,0.01,0.0,0.0,0.0,0.0")
        self.Econstant.setText("")

        k=self.noC.value()-1

        for i in range(k):
            for j in range(k):
                self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))

    def phaseRetrive(self):
        self.marker.setText(str(self.pDropdown.currentIndex()) )
        marker = int(self.marker.text())
        k=self.noC.value()-1
        diffInputData = self.Diffusivity[marker].split(",")

        if self.DiffusivityType[marker] == "0":
            self.diffR.setChecked(True)
            self.diffR_2.setChecked(False)

            p=0
            for i in range(k):
                for j in range(k):
                    if p < len(diffInputData):
                        self.diffMatIn[i][j].setText(diffInputData[p])
                        p = p+1
                    else:
                        self.diffMatIn[i][j].setText("D"+str(i+1)+str(j+1))


        elif self.DiffusivityType[marker] == "1":
            self.diffR_2.setChecked(True)
            self.diffR.setChecked(False)

            q=0
            for i in range(k):
                for j in range(k):
                    if i==j and q < len(diffInputData):
                        self.diffMatIn[i][j].setText(diffInputData[q])
                        q = q+1
                    else:
                        self.diffMatIn[i][j].setText("-")

        self.diffInput.setText(self.Diffusivity[marker])
        self.Estrain.setText(self.eigenStrain[marker])

        if self.elasticType[marker] == "0" :
            self.es.setChecked(True)
            self.es_2.setChecked(False)
            self.es_3.setChecked(False)

        elif self.elasticType[marker] == "1" :
            self.es_2.setChecked(True)
            self.es.setChecked(False)
            self.es_3.setChecked(False)

        elif self.elasticType[marker] == "2" :
            self.es_3.setChecked(True)
            self.es_2.setChecked(False)
            self.es.setChecked(False)

        self.Econstant.setText(self.elasticConstant[marker])
        self.allCheck.setChecked(False)



    def phaseSave(self):

        k=self.noC.value()-1
        marker = int(self.marker.text())
        diffInputData = self.diffInput.text().split(",")
        EstrainData = self.Estrain.text().split(",")
        EconstantData = self.Econstant.text().split(",")

        if self.diffInput.text() =="":
            self.error5.setText("Please fill Diffusivity")
            return False

        elif len(diffInputData) != k*k and self.diffR.isChecked():
            self.error5.setText("Invalid Diffusivity tuple length")
            return False

        elif len(diffInputData) != k and self.diffR_2.isChecked():
            self.error5.setText("Invalid Diffusivity tuple length")
            return False

        elif self.Estrain.text() =="":
            self.error5.setText("Please fill Eigen Strain")
            return False

        elif len(EstrainData) != 6:
            self.error5.setText("Invalid Eigen Strain tuple length")
            return False

        elif self.Econstant.text() =="":
            self.error5.setText("Please fill Elastic Constant")
            return False

        elif len(EconstantData) != 3 and self.es.isChecked():
            self.error5.setText("Invalid Elastic Constant tuple length")
            return False

        elif len(EconstantData) != 3 and self.es_2.isChecked():
            self.error5.setText("Invalid Elastic Constant tuple length")
            return False

        elif len(EconstantData) != 6 and self.es_3.isChecked():
            self.error5.setText("Invalid Elastic Constant tuple length")
            return False

        else:
            if self.diffR.isChecked():
                self.DiffusivityType[marker] = "0"

            elif self.diffR_2.isChecked():
                self.DiffusivityType[marker] = "1"

            self.Diffusivity[marker] = self.diffInput.text()

            self.eigenStrain[marker] = self.Estrain.text()

            if self.es.isChecked():
                self.elasticType[marker] = "0"

            elif self.es_2.isChecked():
                self.elasticType[marker] = "1"

            elif self.es_3.isChecked():
                self.elasticType[marker] = "2"

            self.elasticConstant[marker] = self.Econstant.text()

            return True

    def allCheckFunc(self):

        if self.allCheck.isChecked():

            marker = self.pDropdown.currentIndex()-1
            k=self.noC.value()-1
            diffInputData = self.Diffusivity[marker].split(",")

            if self.DiffusivityType[marker] == "0":
                self.diffR.setChecked(True)
                self.diffR_2.setChecked(False)

                p=0
                for i in range(k):
                    for j in range(k):
                        self.diffMatIn[i][j].setText(diffInputData[p])
                        p = p+1

            elif self.DiffusivityType[marker] == "1":
                self.diffR_2.setChecked(True)
                self.diffR.setChecked(False)

                q=0
                for i in range(k):
                    for j in range(k):
                        if i==j:
                            self.diffMatIn[i][j].setText(diffInputData[q])
                            q = q+1

            self.diffInput.setText(self.Diffusivity[marker])
            self.Estrain.setText(self.eigenStrain[marker])

            if self.elasticType[marker] == "0" :
                self.es.setChecked(True)
                self.es_2.setChecked(False)
                self.es_3.setChecked(False)

            elif self.elasticType[marker] == "1" :
                self.es_2.setChecked(True)
                self.es.setChecked(False)
                self.es_3.setChecked(False)

            elif self.elasticType[marker] == "2" :
                self.es_3.setChecked(True)
                self.es_2.setChecked(False)
                self.es.setChecked(False)

            self.Econstant.setText(self.elasticConstant[marker])
        else:
            return
            #self.phaseReset()

    def esToggled(self):
        self.es.setChecked(True)
        return

    def es2Toggled(self):
        self.es_2.setChecked(True)
        return

    def es3Toggled(self):
        self.es_3.setChecked(True)
        return


    #Boundary Frame Functions

    def phaseChange_BC(self):

        if self.phaseSave_BC():

            current_Index = self.pDropdown_2.currentIndex()

            if current_Index == 0:
                self.allCheck_2.hide()
            else:
                self.allCheck_2.show()


            if self.Bcnd[current_Index] == "" and self.BconV[current_Index] =="":
                self.phaseReset_BC()
            else:
                self.phaseRetrive_BC()

            if self.pDropdown_2.currentIndex() ==0:
                self.marker_bc.setText("0")

            elif self.pDropdown_2.currentIndex() == 1:
                self.marker_bc.setText("1")

            elif self.pDropdown_2.currentIndex() == 2:
                self.marker_bc.setText("2")

            elif self.pDropdown_2.currentIndex() == 3:
                self.marker_bc.setText("3")


        else:
            self.pDropdown_2.setCurrentIndex(int(self.marker_bc.text()))

    def phaseReset_BC(self):

        self.BC_1.setCurrentIndex(0)
        self.BC_2.setCurrentIndex(0)
        self.BC_3.setCurrentIndex(0)
        self.BC_4.setCurrentIndex(0)

        self.allCheck_BC.setChecked(False)
        self.allCheck_2.setChecked(False)


        self.BCV_1.setText("0")
        self.BCV_2.setText("0")
        self.BCV_3.setText("0")
        self.BCV_4.setText("0")

    def phaseSave_BC(self):

        if self.BCV_1.text()=="":
            self.error7.setText("Please fill Boundary Value for X+")
            return False

        elif self.BCV_2.text()=="":
            self.error7.setText("Please fill Boundary Value for X-")
            return False

        elif self.BCV_3.text()=="":
            self.error7.setText("Please fill Boundary Value for Y+")
            return False

        elif self.BCV_4.text()=="":
            self.error7.setText("Please fill Boundary Value for Y-")
            return False

        else:

            self.Bcnd[int(self.marker_bc.text())] =str(self.BC_1.currentIndex()) + "," + str(self.BC_2.currentIndex()) + "," + str(self.BC_3.currentIndex()) + "," + str(self.BC_4.currentIndex())
            self.BconV[int(self.marker_bc.text())] = self.BCV_1.text() + "," + self.BCV_2.text() + "," + self.BCV_3.text() + "," + self.BCV_4.text()
            self.error7.setText("")
            self.Qbox.setStyleSheet("background-color: rgb(218, 218, 218); border: 1px solid rgb(77, 77, 77);")
            return True


    def phaseRetrive_BC(self):
        current_Index = self.pDropdown_2.currentIndex()

        Bcondarray = self.Bcnd[current_Index].split(",")
        self.BC_1.setCurrentIndex(int(Bcondarray[0]))
        self.BC_2.setCurrentIndex(int(Bcondarray[1]))
        self.BC_3.setCurrentIndex(int(Bcondarray[2]))
        self.BC_4.setCurrentIndex(int(Bcondarray[3]))

        BcondVarray = self.BconV[current_Index].split(",")
        self.BCV_1.setText(BcondVarray[0])
        self.BCV_2.setText(BcondVarray[1])
        self.BCV_3.setText(BcondVarray[2])
        self.BCV_4.setText(BcondVarray[3])


    def allCheckBC(self):
        current_Index = self.pDropdown_2.currentIndex()

        if self.allCheck_2.isChecked() and self.Bcnd[current_Index-1] != "" and self.BconV[current_Index-1] != "":

            Bcondarray = self.Bcnd[current_Index-1].split(",")
            self.BC_1.setCurrentIndex(int(Bcondarray[0]))
            self.BC_2.setCurrentIndex(int(Bcondarray[1]))
            self.BC_3.setCurrentIndex(int(Bcondarray[2]))
            self.BC_4.setCurrentIndex(int(Bcondarray[3]))

            BcondVarray = self.BconV[current_Index-1].split(",")
            self.BCV_1.setText(BcondVarray[0])
            self.BCV_2.setText(BcondVarray[1])
            self.BCV_3.setText(BcondVarray[2])
            self.BCV_4.setText(BcondVarray[3])


    def allCheckBCV(self):

        if self.allCheck_BC.isChecked():

            self.BC_2.setCurrentIndex(self.BC_1.currentIndex())
            self.BC_3.setCurrentIndex(self.BC_1.currentIndex())
            self.BC_4.setCurrentIndex(self.BC_1.currentIndex())
            self.BCV_2.setText(self.BCV_1.text())
            self.BCV_3.setText(self.BCV_1.text())
            self.BCV_4.setText(self.BCV_1.text())

        else:
            self.BC_2.setCurrentIndex(0)
            self.BC_3.setCurrentIndex(0)
            self.BC_4.setCurrentIndex(0)
            self.BCV_2.setText("")
            self.BCV_3.setText("")
            self.BCV_4.setText("")


    def BCV1fill(self):
        BC_h = self.Qbox.frameGeometry().height()
        BC_w = self.Qbox.frameGeometry().width()
        BC_l = self.Qbox.frameGeometry().left()
        BC_t = self.Qbox.frameGeometry().top()

        self.Qbox.setStyleSheet("background-color: rgb(218, 218, 218); border-right: 4px solid red;")

    def BCV2fill(self):
        self.Qbox.setStyleSheet("background-color: rgb(218, 218, 218); border-left: 4px solid red;")

    def BCV3fill(self):
        self.Qbox.setStyleSheet("background-color: rgb(218, 218, 218); border-top: 4px solid red;")


    def BCV4fill(self):
        self.Qbox.setStyleSheet("background-color: rgb(218, 218, 218); border-bottom: 4px solid red;")


    def BCV1Change(self):

        if self.BC_1.currentIndex() == 1:
            self.BCV_1.setText("0")
            self.BCV_1.setEnabled(False)

        elif  self.BC_1.currentIndex() == 3:
            self.BC_2.setCurrentIndex(3)
            self.BCV_1.setText("0")
            self.BCV_2.setText("0")
            self.BCV_1.setEnabled(False)
            self.BCV_2.setEnabled(False)

        else:
            self.BCV_1.setEnabled(True)


        if self.BC_1.currentIndex() !=3 and self.BC_2.currentIndex() == 3:
            self.BC_2.setCurrentIndex(0)
            self.BCV_2.setEnabled(True)

    def BCV2Change(self):

        if self.BC_2.currentIndex() == 1:
            self.BCV_2.setText("0")
            self.BCV_2.setEnabled(False)

        elif  self.BC_2.currentIndex() == 3:
            self.BC_1.setCurrentIndex(3)
            self.BCV_1.setText("0")
            self.BCV_2.setText("0")
            self.BCV_1.setEnabled(False)
            self.BCV_2.setEnabled(False)

        else:
            self.BCV_2.setEnabled(True)


        if self.BC_2.currentIndex() !=3 and self.BC_1.currentIndex() == 3:
            self.BC_1.setCurrentIndex(0)
            self.BCV_1.setEnabled(True)

    def BCV3Change(self):

        if self.BC_3.currentIndex() == 1:
            self.BCV_3.setText("0")
            self.BCV_3.setEnabled(False)

        elif  self.BC_3.currentIndex() == 3:
            self.BC_4.setCurrentIndex(3)
            self.BCV_3.setText("0")
            self.BCV_4.setText("0")
            self.BCV_3.setEnabled(False)
            self.BCV_4.setEnabled(False)

        else:
            self.BCV_3.setEnabled(True)


        if self.BC_3.currentIndex() !=3 and self.BC_4.currentIndex() == 3:
            self.BC_4.setCurrentIndex(0)
            self.BCV_4.setEnabled(True)


    def BCV4Change(self):
        if self.BC_4.currentIndex() == 1:
            self.BCV_4.setText("0")
            self.BCV_4.setEnabled(False)

        elif  self.BC_4.currentIndex() == 3:
            self.BC_3.setCurrentIndex(3)
            self.BCV_3.setText("0")
            self.BCV_4.setText("0")
            self.BCV_3.setEnabled(False)
            self.BCV_4.setEnabled(False)

        else:
            self.BCV_4.setEnabled(True)


        if self.BC_4.currentIndex() !=3 and self.BC_3.currentIndex() == 3:
            self.BC_3.setCurrentIndex(0)
            self.BCV_3.setEnabled(True)


    def domainShapeChange(self):
        self.addShape.setText("Add " + self.shape.currentText() +  " | "+self.pDropdown_3.currentText())
        self.shapeFrameTitle.setText( self.shape.currentText() +  " | "+self.pDropdown_3.currentText())
        return

    def domainPhaseChange(self):
        self.addShape.setText("Add " + self.shape.currentText() +  " | "+self.pDropdown_3.currentText())
        self.shapeFrameTitle.setText( self.shape.currentText() +  " | "+self.pDropdown_3.currentText())
        return

    def shapeframeToggle(self):
        self.shapeframe.show()
        self.cube_end.setText("")
        self.cube_start.setText("")
        self.cylinder_center.setText("")
        self.cylinder_radius.setText("")
        self.cylinder_zend.setText("0")
        self.cylinder_zstart.setText("0")
        self.ellipse_center.setText("")
        self.ellipse_eccentric.setText("")
        self.ellipse_majorAxis.setText("")
        self.ellipse_rotation.setText("")
        self.sphere_center.setText("")
        self.sphere_radius.setText("")
        self.Rsphere_SD.setText("")
        self.Rsphere_pptradius.setText("")
        self.Rsphere_volf.setText("")
        self.Rsphere_Spread.setText("")
        self.Rcylinder_SD.setText("")
        self.Rcylinder_pptradius.setText("")
        self.Rcylinder_Spread.setText("")
        self.Rcylinder_volf.setText("")
        self.shapeSave.show()
        self.shapeUpdate.hide()
        self.shapeedit.setEnabled(False)
        self.shapedelete.setEnabled(False)

        if self.shape.currentIndex() ==0:
            self.fillCUBE.show()
            self.fillCYLINDER.hide()
            self.fillELLIPSE.hide()
            self.fillSPHERE.hide()
            self.fillRCYLINDER.hide()
            self.fillRSPHERE.hide()
            return

        elif self.shape.currentIndex() ==1:
            self.fillCUBE.hide()
            self.fillCYLINDER.show()
            self.fillELLIPSE.hide()
            self.fillSPHERE.hide()
            self.fillRCYLINDER.hide()
            self.fillRSPHERE.hide()
            return

        elif self.shape.currentIndex() ==2:
            self.fillCUBE.hide()
            self.fillCYLINDER.hide()
            self.fillELLIPSE.show()
            self.fillSPHERE.hide()
            self.fillRCYLINDER.hide()
            self.fillRSPHERE.hide()
            return

        elif self.shape.currentIndex() ==3:
            self.fillCUBE.hide()
            self.fillCYLINDER.hide()
            self.fillELLIPSE.hide()
            self.fillSPHERE.show()
            self.fillRCYLINDER.hide()
            self.fillRSPHERE.hide()
            return

        elif self.shape.currentIndex() ==4:
            self.fillCUBE.hide()
            self.fillCYLINDER.hide()
            self.fillELLIPSE.hide()
            self.fillSPHERE.hide()
            self.fillRCYLINDER.show()
            self.fillRSPHERE.hide()
            return

        elif self.shape.currentIndex() ==5:
            self.fillCUBE.hide()
            self.fillCYLINDER.hide()
            self.fillELLIPSE.hide()
            self.fillSPHERE.hide()
            self.fillRCYLINDER.hide()
            self.fillRSPHERE.show()
            return


    def shapeCancelClicked(self):
        self.shapeframe.hide()
        self.shapeedit.setEnabled(True)
        self.shapedelete.setEnabled(True)
        return

    def shapeSaveClicked(self):

        if self.shape.currentIndex() ==0:

            if self.cube_start.text() == "":
                self.shapeframe_error.setText("Please fill cube start point")
                return

            elif len(self.cube_start.text().split(",")) != 3:
                self.shapeframe_error.setText("Invalid cube start point")
                return

            elif self.cube_end.text() == "":
                self.shapeframe_error.setText("Please fill cube end point")
                return

            elif len(self.cube_end.text().split(",")) != 3:
                self.shapeframe_error.setText("Invalid cube end point")
                return

            else:
                self.ShapeList.addItem("CUBE {"+ str(self.pDropdown_3.currentIndex()) + "," + self.cube_start.text() + "," + self.cube_end.text()+"}" )
                self.shapeframe_error.setText("")


        elif self.shape.currentIndex() ==1:

            if self.cylinder_center.text() == "":
                self.shapeframe_error.setText("Please fill cylinder center point")
                return

            elif len(self.cylinder_center.text().split(",")) != 2:
                self.shapeframe_error.setText("Invalid cylinder center point")
                return

            elif self.cylinder_zstart.text() == "":
                self.shapeframe_error.setText("Please fill cylinder z-start point")
                return

            elif self.cylinder_zend.text() == "":
                self.shapeframe_error.setText("Please fill cylinder z-end point")
                return

            elif self.cylinder_radius.text() == "":
                self.shapeframe_error.setText("Please fill cylinder radius ")
                return

            else:
                self.ShapeList.addItem("CYLINDER {"+ str(self.pDropdown_3.currentIndex()) + "," + self.cylinder_center.text() + "," + self.cylinder_zstart.text() + "," +self.cylinder_zend.text() + "," + self.cylinder_radius.text() + "}")
                self.shapeframe_error.setText("")



        elif self.shape.currentIndex() ==2:
            if self.ellipse_center.text() == "":
                self.shapeframe_error.setText("Please fill ellipse center point")
                return

            elif len(self.ellipse_center.text().split(",")) != 2:
                self.shapeframe_error.setText("Invalid ellipse center point")
                return

            elif self.ellipse_majorAxis.text() == "":
                self.shapeframe_error.setText("Please fill ellipse major-axis point")
                return

            elif self.ellipse_eccentric.text() == "":
                self.shapeframe_error.setText("Please fill ellipse eccentricity point")
                return

            elif self.ellipse_rotation.text() == "":
                self.shapeframe_error.setText("Please fill ellipse rotation degree")
                return

            else:
                self.ShapeList.addItem("ELLIPSE {"+ str(self.pDropdown_3.currentIndex()) + "," + self.ellipse_center.text() + "," + self.ellipse_majorAxis.text() + "," +self.ellipse_eccentric.text() + "," + self.ellipse_rotation.text() + "}")
                self.shapeframe_error.setText("")


        elif self.shape.currentIndex() ==3:

            if self.sphere_center.text() == "":
                self.shapeframe_error.setText("Please fill sphere center point")
                return

            elif len(self.sphere_center.text().split(",")) != 3:
                self.shapeframe_error.setText("Invalid sphere center point")
                return

            elif self.sphere_radius.text() == "":
                self.shapeframe_error.setText("Please fill sphere radius")
                return

            else:
                self.ShapeList.addItem("SPHERE {"+ str(self.pDropdown_3.currentIndex()) + "," + self.sphere_center.text() + "," + self.sphere_radius.text()+"}" )
                self.shapeframe_error.setText("")
                
        elif self.shape.currentIndex() ==4:
            if self.Rcylinder_pptradius.text() == "":
                self.shapeframe_error.setText("Please fill Preipitate Radius")
                return
            
            elif self.Rcylinder_volf.text() == "":
                self.shapeframe_error.setText("Please fill Volume Fraction")
                return
            
            elif self.Rcylinder_SD.text() == "":
                self.shapeframe_error.setText("Please fill Shift Distance")
                return
            
            elif self.Rcylinder_Spread.text() == "":
                self.shapeframe_error.setText("Please fill Spread")
                return
            
            else:
                self.ShapeList.addItem("CYLINDERRANDOM {"+ str(self.pDropdown_3.currentIndex()) + "," + self.Rcylinder_pptradius.text() + "," + self.Rcylinder_volf.text()+","+ self.Rcylinder_SD.text() +  ","+ self.Rcylinder_Spread.text() +"}" )
                self.shapeframe_error.setText("")
        
        elif self.shape.currentIndex() ==5:
            if self.Rsphere_pptradius.text() == "":
                self.shapeframe_error.setText("Please fill Preipitate Radius")
                return
            
            elif self.Rsphere_volf.text() == "":
                self.shapeframe_error.setText("Please fill Volume Fraction")
                return
            
            elif self.Rsphere_SD.text() == "":
                self.shapeframe_error.setText("Please fill Shift Distance")
                return
            
            elif self.Rsphere_Spread.text() == "":
                self.shapeframe_error.setText("Please fill Spread")
                return
            else:
                self.ShapeList.addItem("SPHERERANDOM {"+ str(self.pDropdown_3.currentIndex()) + "," + self.Rsphere_pptradius.text() + "," + self.Rsphere_volf.text()+","+ self.Rsphere_SD.text() + ","+ self.Rsphere_Spread.text() +"}" )
                self.shapeframe_error.setText("")

        self.shapeframe.hide()
        self.shapeedit.setEnabled(True)
        self.shapedelete.setEnabled(True)

    def shapeUpdateClicked(self):

        shapeText  = self.ShapeList.item(self.ShapeList.currentRow()).text()
        shapeText = shapeText.replace("{", "")
        shapeText = shapeText.replace("}", "")
        shapeData = shapeText.split(" ")

        if shapeData[0] == "CUBE":

            if self.cube_start.text() == "":
                self.shapeframe_error.setText("Please fill cube start point")
                return

            elif len(self.cube_start.text().split(",")) != 3:
                self.shapeframe_error.setText("Invalid cube start point")
                return

            elif self.cube_end.text() == "":
                self.shapeframe_error.setText("Please fill cube end point")
                return

            elif len(self.cube_end.text().split(",")) != 3:
                self.shapeframe_error.setText("Invalid cube end point")
                return

            else:
                self.ShapeList.item(self.ShapeList.currentRow()).setText("CUBE {"+ str(self.pDropdown_3.currentIndex()) + "," + self.cube_start.text() + "," + self.cube_end.text()+"}" )
                self.shapeframe_error.setText("")


        elif shapeData[0] == "CYLINDER":

            if self.cylinder_center.text() == "":
                self.shapeframe_error.setText("Please fill cylinder center point")
                return

            elif len(self.cylinder_center.text().split(",")) != 2:
                self.shapeframe_error.setText("Invalid cylinder center point")
                return

            elif self.cylinder_zstart.text() == "":
                self.shapeframe_error.setText("Please fill cylinder z-start point")
                return

            elif self.cylinder_zend.text() == "":
                self.shapeframe_error.setText("Please fill cylinder z-end point")
                return

            elif self.cylinder_radius.text() == "":
                self.shapeframe_error.setText("Please fill cylinder radius ")
                return

            else:
                self.ShapeList.item(self.ShapeList.currentRow()).setText("CYLINDER {"+ str(self.pDropdown_3.currentIndex()) + "," + self.cylinder_center.text() + "," + self.cylinder_zstart.text() + "," +self.cylinder_zend.text() + "," + self.cylinder_radius.text() + "}")
                self.shapeframe_error.setText("")


        elif shapeData[0] == "ELLIPSE":
            if self.ellipse_center.text() == "":
                self.shapeframe_error.setText("Please fill ellipse center point")
                return

            elif len(self.ellipse_center.text().split(",")) != 2:
                self.shapeframe_error.setText("Invalid ellipse center point")
                return

            elif self.ellipse_majorAxis.text() == "":
                self.shapeframe_error.setText("Please fill ellipse major-axis point")
                return

            elif self.ellipse_eccentric.text() == "":
                self.shapeframe_error.setText("Please fill ellipse eccentricity point")
                return

            elif self.ellipse_rotation.text() == "":
                self.shapeframe_error.setText("Please fill ellipse rotation degree")
                return

            else:
                self.ShapeList.item(self.ShapeList.currentRow()).setText("ELLIPSE {"+ str(self.pDropdown_3.currentIndex()) + "," + self.ellipse_center.text() + "," + self.ellipse_majorAxis.text() + "," +self.ellipse_eccentric.text() + "," + self.ellipse_rotation.text() + "}")
                self.shapeframe_error.setText("")


        elif shapeData[0] == "SPHERE":

            if self.sphere_center.text() == "":
                self.shapeframe_error.setText("Please fill sphere center point")
                return

            elif len(self.sphere_center.text().split(",")) != 3:
                self.shapeframe_error.setText("Invalid sphere center point")
                return

            elif self.sphere_radius.text() == "":
                self.shapeframe_error.setText("Please fill sphere radius")
                return

            else:
                self.ShapeList.item(self.ShapeList.currentRow()).setText("SPHERE {"+ str(self.pDropdown_3.currentIndex()) + "," + self.sphere_center.text() + "," + self.sphere_radius.text()+"}" )
                self.shapeframe_error.setText("")

        elif shapeData[0] == "CYLINDERRANDOM":
            if self.Rcylinder_pptradius.text() == "":
                self.shapeframe_error.setText("Please fill Preipitate Radius")
                return

            elif self.Rcylinder_volf.text() == "":
                self.shapeframe_error.setText("Please fill Volume Fraction")
                return

            elif self.Rcylinder_SD.text() == "":
                self.shapeframe_error.setText("Please fill Shift Distance")
                return
            else:
                self.ShapeList.item(self.ShapeList.currentRow()).setText("CYLINDERRANDOM {"+ str(self.pDropdown_3.currentIndex()) + "," + self.Rcylinder_pptradius.text() + "," + self.Rcylinder_volf.text()+","+ self.Rcylinder_SD.text() + "}" )
                self.shapeframe_error.setText("")

        elif shapeData[0] == "SPHERERANDOM":
            if self.Rsphere_pptradius.text() == "":
                self.shapeframe_error.setText("Please fill Preipitate Radius")
                return

            elif self.Rsphere_volf.text() == "":
                self.shapeframe_error.setText("Please fill Volume Fraction")
                return

            elif self.Rsphere_SD.text() == "":
                self.shapeframe_error.setText("Please fill Shift Distance")
                return
            else:
                self.ShapeList.item(self.ShapeList.currentRow()).setText("SPHERERANDOM {"+ str(self.pDropdown_3.currentIndex()) + "," + self.Rsphere_pptradius.text() + "," + self.Rsphere_volf.text()+","+ self.Rsphere_SD.text() + "}" )
                self.shapeframe_error.setText("")




        self.shapeframe.hide()
        self.shapeedit.setEnabled(True)
        self.shapedelete.setEnabled(True)
        return

    def shapeeditClicked(self):

        if self.ShapeList.count() > 0:
            self.shapeSave.hide()
            self.shapeUpdate.show()
            self.shapeframe.show()
            self.shapeedit.setEnabled(False)
            self.shapedelete.setEnabled(False)

            shapeText  = self.ShapeList.item(self.ShapeList.currentRow()).text()
            shapeText = shapeText.replace("{", "")
            shapeText = shapeText.replace("}", "")
            shapeData = shapeText.split(" ")
            shapeValues = shapeData[1].split(",")


            self.shapeframe.show()
            self.cube_end.setText("")
            self.cube_start.setText("")
            self.cylinder_center.setText("")
            self.cylinder_radius.setText("")
            self.cylinder_zend.setText("0")
            self.cylinder_zstart.setText("0")
            self.ellipse_center.setText("")
            self.ellipse_eccentric.setText("")
            self.ellipse_majorAxis.setText("")
            self.ellipse_rotation.setText("")
            self.sphere_center.setText("")
            self.sphere_radius.setText("")
            self.Rsphere_SD.setText("")
            self.Rsphere_pptradius.setText("")
            self.Rsphere_volf.setText("")
            self.Rcylinder_SD.setText("")
            self.Rcylinder_pptradius.setText("")
            self.Rcylinder_volf.setText("")


            if shapeData[0] =="CUBE":
                self.fillCUBE.show()
                self.fillCYLINDER.hide()
                self.fillELLIPSE.hide()
                self.fillSPHERE.hide()
                self.fillRCYLINDER.hide()
                self.fillRSPHERE.hide()
                self.shapeFrameTitle.setText("CUBE | "+self.pDropdown_3.itemText(int(shapeValues[0])))

                self.cube_start.setText(','.join(map(str, shapeValues[1:4])))
                self.cube_end.setText(','.join(map(str, shapeValues[4:])))

                return

            elif shapeData[0] =="CYLINDER":
                self.fillCUBE.hide()
                self.fillCYLINDER.show()
                self.fillELLIPSE.hide()
                self.fillSPHERE.hide()
                self.fillRCYLINDER.hide()
                self.fillRSPHERE.hide()
                self.shapeFrameTitle.setText("CYLINDER | "+self.pDropdown_3.itemText(int(shapeValues[0])))
                self.cylinder_center.setText(','.join(map(str, shapeValues[1:3])))
                self.cylinder_zend.setText(str(shapeValues[3]))
                self.cylinder_zstart.setText(str(shapeValues[4]))
                self.cylinder_radius.setText(str(shapeValues[5]))
                return

            elif shapeData[0] =="ELLIPSE":
                self.fillCUBE.hide()
                self.fillCYLINDER.hide()
                self.fillELLIPSE.show()
                self.fillSPHERE.hide()
                self.fillRCYLINDER.hide()
                self.fillRSPHERE.hide()
                self.shapeFrameTitle.setText("ELLIPSE | "+self.pDropdown_3.itemText(int(shapeValues[0])))
                self.ellipse_center.setText(','.join(map(str, shapeValues[1:3])))
                self.ellipse_majorAxis.setText(str(shapeValues[3]))
                self.ellipse_eccentric.setText(str(shapeValues[4]))
                self.ellipse_rotation.setText(str(shapeValues[5]))
                return

            elif shapeData[0] =="SPHERE":
                self.fillCUBE.hide()
                self.fillCYLINDER.hide()
                self.fillELLIPSE.hide()
                self.fillSPHERE.show()
                self.fillRCYLINDER.hide()
                self.fillRSPHERE.hide()
                self.shapeFrameTitle.setText("SPHERE | "+self.pDropdown_3.itemText(int(shapeValues[0])))
                self.sphere_center.setText(','.join(map(str, shapeValues[1:4])))
                self.sphere_radius.setText(shapeValues[4])
                return
            
            elif shapeData[0] =="CYLINDERRANDOM":
                self.fillCUBE.hide()
                self.fillCYLINDER.hide()
                self.fillELLIPSE.hide()
                self.fillSPHERE.hide()
                self.fillRCYLINDER.show()
                self.fillRSPHERE.hide()
                self.shapeFrameTitle.setText("RANDOM CYLINDER | "+self.pDropdown_3.itemText(int(shapeValues[0])))
                self.Rcylinder_pptradius.setText(shapeValues[1])
                self.Rcylinder_volf.setText(shapeValues[2])
                self.Rcylinder_SD.setText(shapeValues[3])
                return
            
            elif shapeData[0] =="SPHERERANDOM":
                self.fillCUBE.hide()
                self.fillCYLINDER.hide()
                self.fillELLIPSE.hide()
                self.fillSPHERE.hide()
                self.fillRCYLINDER.hide()
                self.fillRSPHERE.show()
                self.shapeFrameTitle.setText("RANDOM SPHERE | "+self.pDropdown_3.itemText(int(shapeValues[0])))
                self.Rsphere_pptradius.setText(shapeValues[1])
                self.Rsphere_volf.setText(shapeValues[2])
                self.Rsphere_SD.setText(shapeValues[3])
                return


    def shapedeleteClicked(self):
        self.ShapeList.takeItem(self.ShapeList.currentRow())

    def radio_GPToggled(self):

        if self.radio_GP.isChecked():
            self.btn7.setEnabled(False)
            self.btn6.setText("Grand-Potential \n Model")
            self.frame_9GP.show()
            self.frame_9KKS.hide()
            self.frame_9CH.hide()
            self.frame_9KKS2.hide()


    def radio_CHToggled(self):

        if self.radio_CH.isChecked():
            self.btn7.setEnabled(False)
            self.btn6.setText("Cahn Hilliard\n Model")
            self.frame_9GP.hide()
            self.frame_9CH.show()
            self.frame_9KKS.hide()
            self.frame_9KKS2.hide()


    def radio_KKRToggled(self):

        if self.radio_KKR.isChecked():
            self.btn7.setEnabled(False)
            self.btn6.setText("KKS GPU CUDA\n   Model")
            self.frame_9GP.hide()
            self.frame_9CH.hide()
            self.frame_9KKS2.hide()
            self.frame_9KKS.show()

    def radio_KKS2Toggled(self):

        if self.radio_KKS2.isChecked():
            self.btn7.setEnabled(False)
            self.btn6.setText("KKS GPU OPENCL \n   Model")
            self.frame_9GP.hide()
            self.frame_9CH.hide()
            self.frame_9KKS.hide()
            self.frame_9KKS2.show()


    def GPnextClicked(self):

        if self.stackedWidgetGP.currentIndex() == 2:
            self.saveGP.show()

        if self.stackedWidgetGP.currentIndex() < 3:
            self.stackedWidgetGP.setCurrentIndex((self.stackedWidgetGP.currentIndex() +1) )
        else:
            return


    def GPpreClicked(self):
        self.saveGP.hide()
        if self.stackedWidgetGP.currentIndex() > 0:
            self.stackedWidgetGP.setCurrentIndex((self.stackedWidgetGP.currentIndex() -1)  )
        else:
            return

    def saveGPClicked(self):

        if self.saveGPChack():
            self.btn7.setEnabled(True)
            self.frame_8.hide()
            self.frame_9.hide()
            self.First_widget.hide()
            self.Second_widget.hide()
            self.Third_widget.hide()
            self.Four_widget.hide()
            self.Fifth_widget.hide()
            self.Sixth_widget.hide()
            self.Seven_widget.show()


            self.Qbox.hide()
            self.frame_11.show()


            #Btn Animation
            self.btn5.setGeometry(60, 30, 217, 60)
            self.btn6.setGeometry(277, 30, 216, 60)
            self.btn7.setGeometry(493, 20, 217, 70)


            self.btn7.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
            self.btn5.setStyleSheet("background-color: rgb(238, 238, 236)")
            self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")

        else:
            return
        
    def funcFflag(self):
        
        if self.funcF.value() == 1:
            self.Func1.show()
            self.Func2.hide()
            self.tableWidgetGP.setColumnHidden(4, False)
            self.tableWidgetGP.setColumnHidden(5, True)
            self.tableWidgetGP.setGeometry(60,50,681,181)

            
        elif self.funcF.value() == 2:
            self.Func1.hide()
            self.Func2.show()
            self.tableWidgetGP.setColumnHidden(4, True)
            self.tableWidgetGP.setColumnHidden(5, False)
            self.tableWidgetGP.setGeometry(55,50,681,181)
        
        elif self.funcF.value() == 3:
            self.Func1.hide()
            self.Func2.show()
            self.tableWidgetGP.setColumnHidden(4, True)
            self.tableWidgetGP.setColumnHidden(5, False)
            self.tableWidgetGP.setGeometry(50,50,681,181)
        
        elif self.funcF.value() == 4:
            self.Func1.hide()
            self.Func2.show()
            self.tableWidgetGP.setColumnHidden(4, True)
            self.tableWidgetGP.setColumnHidden(5, False)
            self.tableWidgetGP.setGeometry(55,50,681,181)


    def saveGPChack(self):

        noP_value = self.noP.value()
        
        
        if self.trackProgressGP.text() == "":
            self.errorGP.setText("Please fill Track Progress ")
            return False

        elif self.epsilonGP.text() == "":
            self.errorGP.setText("Please fill Epsilon value")
            return False

        elif self.tauGP.text() == "":
            self.errorGP.setText("Please fill tau Value")
            return False

        elif self.TauGP.text() == "":
            self.errorGP.setText("Please fill Tau values")
            return False

        elif len(self.TauGP.text().split(",")) != (noP_value * ((noP_value - 1) / 2)):
            self.errorGP.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for Tau" )
            return False

        elif self.FanisotropyGP.text() == "":
            self.errorGP.setText("Please fill Function Anisotropy")
            return False

        elif self.anisotropyTypeGP.text() == "":
            self.errorGP.setText("Please fill Anisotropy Type")
            return False

        elif self.debGP.text() == "":
            self.errorGP.setText("Please fill dab values")
            return False

        elif len(self.debGP.text().split(",")) != int(noP_value * ((noP_value - 1) / 2)):
            self.errorGP.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for dab" )
            return False

        elif self.funcWGP.text() == "":
            self.errorGP.setText("Please fill Functional W value")
            return False


        elif len(self.gammaABCGP.text().split(",")) != int(noP_value * ((noP_value - 1)*(noP_value - 2) / 6)) and self.gammaABCGP.text() != "":
            self.errorGP.setText("Required " + str(int((noP_value * ((noP_value - 1)*(noP_value - 2) / 6)))) + " values for Gamma abc" )
            return False

        elif self.shiftJGP.text() =="" and self.shiftGP.value() == 1:
            self.errorGP.setText("Please fill Shift J value")
            return False

        elif self.equTGP.text() == "":
            self.errorGP.setText("Please fill Equilibrium Temperature")
            return False

        elif self.fillingTGP.text() =="":
            self.errorGP.setText("Please fill Filling Temperature")
            return False

        elif self.TGP.text() =="":
            self.errorGP.setText("Please fill Temperature")
            return False

        elif self.tempgradyGP.text() == "":
            self.errorGP.setText("Please fill Tempgrady values")
            return False

        elif len(self.tempgradyGP.text().split(",")) != 5:
            self.errorGP.setText("Required 5 values for Tempgrady" )
            return False

        elif self.ampNoiseGP.text() =="" and self.noiseGP.value() == 1:
            self.errorGP.setText("Please fill AMP Noise value")
            return False

        elif self.writecompGP.text() == "":
            self.errorGP.setText("Please fill Writecomposition Value")
            return False

        else:
            self.errorGP.setText("")
            return True


    def KKSnextClicked(self):
        return
    
        '''

        if self.stackedWidgetKKS.currentIndex() == 0:
            self.saveKKS.show()

        if self.stackedWidgetKKS.currentIndex() < 1:
            self.stackedWidgetKKS.setCurrentIndex((self.stackedWidgetKKS.currentIndex() +1) )
        else:
            return
            
        '''


    def KKSpreClicked(self):
        return
    
        '''
        self.saveKKS.hide()
        if self.stackedWidgetKKS.currentIndex() > 0:
            self.stackedWidgetKKS.setCurrentIndex((self.stackedWidgetKKS.currentIndex() -1)  )
        else:
            return
            
        '''

    def saveKKSClicked(self):

        if self.saveKKSCheck():
            self.errorKKS.setText("")
            self.btn7.setEnabled(True)
            self.frame_8.hide()
            self.frame_9.hide()
            self.First_widget.hide()
            self.Second_widget.hide()
            self.Third_widget.hide()
            self.Four_widget.hide()
            self.Fifth_widget.hide()
            self.Sixth_widget.hide()
            self.Seven_widget.show()

            self.Qbox.hide()
            self.frame_11.show()


            #Btn Animation
            self.btn5.setGeometry(60, 30, 217, 60)
            self.btn6.setGeometry(277, 30, 216, 60)
            self.btn7.setGeometry(493, 20, 217, 70)


            self.btn7.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
            self.btn5.setStyleSheet("background-color: rgb(238, 238, 236)")
            self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")

        else:
            return

    def saveKKSCheck(self):

        noP_value = self.noP.value()
        
        '''
        for i in range(noP_value):
            if self.tableWidgetKKSF.item(i,1) is None or self.tableWidgetKKSF.item(i,1).text() == '':
                self.errorKKS.setText("Please fill All values of F")
                return False
        
        
        for i in range(noP_value*noP_value):
            if self.tableWidgetKKS.item(i,2) is None or self.tableWidgetKKS.item(i,2).text() == '':
                self.errorKKS.setText("Please fill All values of Ceq")
                return False
        '''

        if self.trackprogressKKS.text() == "":
            self.errorKKS.setText("Please fill Track Progress Size ")
            return False
        
        elif self.epsilonKKS.text() == "":
            self.errorKKS.setText("Please fill relaxCoeff value")
            return False

        elif self.TauKKS.text() == "":
            self.errorKKS.setText("Please fill Tau values")
            return False

        elif len(self.TauKKS.text().split(",")) != (noP_value * ((noP_value - 1) / 2)):
            self.errorKKS.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for Tau" )
            return False

        elif self.equTKKS.text() == "":
            self.errorKKS.setText("Please fill Equilibrium Temperature")
            return False
      

        elif self.temperatureKKS.text() == "":
            self.errorKKS.setText("Please fill Temperature 'T' value")
            return False

        else:
            self.errorKKS.setText("")
            return True

    def KKS2nextClicked(self):
        
        if self.stackedWidgetKKS2.currentIndex() == 1:
            self.saveKKS2.show()

        if self.stackedWidgetKKS2.currentIndex() < 2:
            self.stackedWidgetKKS2.setCurrentIndex((self.stackedWidgetKKS2.currentIndex() +1) )
        else:
            return
        


    def KKS2preClicked(self):
      
        self.saveKKS2.hide()
        if self.stackedWidgetKKS2.currentIndex() > 0:
            self.stackedWidgetKKS2.setCurrentIndex((self.stackedWidgetKKS2.currentIndex() -1)  )
        else:
            return
    

    def saveKKS2Clicked(self):

        if self.saveKKS2Check():
            self.errorKKS2.setText("")
            self.btn7.setEnabled(True)
            self.frame_8.hide()
            self.frame_9.hide()
            self.First_widget.hide()
            self.Second_widget.hide()
            self.Third_widget.hide()
            self.Four_widget.hide()
            self.Fifth_widget.hide()
            self.Sixth_widget.hide()
            self.Seven_widget.show()

            self.Qbox.hide()
            self.frame_11.show()


            #Btn Animation
            self.btn5.setGeometry(60, 30, 217, 60)
            self.btn6.setGeometry(277, 30, 216, 60)
            self.btn7.setGeometry(493, 20, 217, 70)


            self.btn7.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
            self.btn5.setStyleSheet("background-color: rgb(238, 238, 236)")
            self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")

        else:
            return

    def saveKKS2Check(self):
        noP_value = self.noP.value()
        
        
        '''
        for i in range(noP_value*noP_value):
            for j in range(2,5,1):
                if self.tableWidgetKKS2.item(i,j) is None or self.tableWidgetKKS2.item(i,j).text() == '':
                    self.errorKKS2.setText("Please fill All values of Ceq, cfill.")
                    return False
        '''
        
        if self.trackProgressKKS2.text() == "":
            self.errorKKS2.setText("Please fill Track Progress ")
            return False

        elif self.epsilonKKS2.text() == "":
            self.errorKKS2.setText("Please fill Epsilon value")
            return False


        elif self.FanisotropyKKS2.text() == "":
            self.errorKKS2.setText("Please fill Function Anisotropy")
            return False


        elif self.debKKS2.text() == "":
            self.errorKKS2.setText("Please fill dab values")
            return False

        elif len(self.debKKS2.text().split(",")) != int(noP_value * ((noP_value - 1) / 2)):
            self.errorKKS2.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for dab" )
            return False

        elif self.ampNoiseKKS2.text() == "" and self.noiseKKS2.value() == 1:
            self.errorKKS2.setText("Please fill AMP Noise value")
            return False

        elif self.tNoiseStartKKS2.text() == "":
            self.errorKKS2.setText("Please fill tNoiseStart value")
            return False
        

        elif self.TLKKS2.text() == "":
            self.errorKKS2.setText("Please fill Equ. T value")
            return False
        
        elif self.fillingTKKS.text() == "":
            self.errorKKS2.setText("Please fill Filling T value")
            return False 
        
        elif self.temperatureKKS2.text() == "" and self.thermalYKKS2.isChecked():
            self.errorKKS2.setText("Please fill Temperature 'T' value")
            return False
        
        elif self.fillingTKKS.text() == "":
            self.errorKKS2.setText("Please fill Filling T value")
            return False
        
        elif self.ShiftJKKS2.text() == "" and self.shiftKKS2.value() == 1:
            self.errorKKS2.setText("Please fill ShiftJ value")
            return False
        

        elif self.tempGradyKKS2.text() == "":
            self.errorKKS2.setText("Please fill Tempgrady values")
            return False

        elif len(self.tempGradyKKS2.text().split(",")) != 5:
            self.errorKKS2.setText("Required 5 values for Tempgrady" )
            return False

        elif self.atrKKS2.text() == "":
            self.errorKKS2.setText("Please fill atr value")
            return False

        elif self.CLPidKKS2.text() == "":
            self.errorKKS2.setText("Please fill CL Plateform ID value")
            return False

        elif self.CLDidKKS2.text() == "":
            self.errorKKS2.setText("Please fill CL devise ID value")
            return False
        
       

        else:
            self.errorKKS2.setText("")
            return True



    def CHnextClicked(self):

        if self.stackedWidgetCH.currentIndex() == 0:
            self.saveCH.show()

        if self.stackedWidgetCH.currentIndex() < 1:
            self.stackedWidgetCH.setCurrentIndex((self.stackedWidgetCH.currentIndex() +1) )
        else:
            return


    def CHpreClicked(self):
        self.saveCH.hide()
        if self.stackedWidgetCH.currentIndex() > 0:
            self.stackedWidgetCH.setCurrentIndex((self.stackedWidgetCH.currentIndex() -1)  )
        else:
            return

    def saveCHClicked(self):

        if self.saveCHCheck():
            self.btn7.setEnabled(True)
            self.frame_8.hide()
            self.frame_9.hide()
            self.First_widget.hide()
            self.Second_widget.hide()
            self.Third_widget.hide()
            self.Four_widget.hide()
            self.Fifth_widget.hide()
            self.Sixth_widget.hide()
            self.Seven_widget.show()

            self.Qbox.hide()
            self.frame_11.show()


            #Btn Animation
            self.btn5.setGeometry(60, 30, 217, 60)
            self.btn6.setGeometry(277, 30, 216, 60)
            self.btn7.setGeometry(493, 20, 217, 70)


            self.btn7.setStyleSheet("background-color: rgb(64, 140, 191); border:none ;color:#fff ")
            self.btn5.setStyleSheet("background-color: rgb(238, 238, 236)")
            self.btn6.setStyleSheet("background-color: rgb(238, 238, 236)")

        else:
            return


    def saveCHCheck(self):

        noP_value = self.noP.value()

        for i in range(noP_value):
            if self.tableWidgetCHA.item(i,2) is None or self.tableWidgetCHA.item(i,2).text() == '':
                self.errorCH.setText("Please fill All values of Atomic Mobility")
                return False
            
        '''
        for i in range(noP_value*noP_value):
            for j in range(2,4,1):
                if self.tableWidgetCH.item(i,j) is None or self.tableWidgetCH.item(i,j).text() == '':
                    self.errorCH.setText("Please fill All values of Ceq, cfill.")
                    return False
        '''

        if self.trackProgressCH.text() == "":
            self.errorCH.setText("Please fill Track Progress ")
            return False

        elif self.lPhiCH.text() == "":
            self.errorCH.setText("Please fill L Phi value")
            return False

        elif len(self.lPhiCH.text().split(",")) != int(noP_value * ((noP_value - 1) / 2)):
            self.errorCH.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for L Phi" )
            return False

        elif self.kappaPhiCH.text() == "":
            self.errorCH.setText("Please fill Kappa Phi value")
            return False

        elif len(self.kappaPhiCH.text().split(",")) != int(noP_value * ((noP_value - 1) / 2)):
            self.errorCH.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for Kappa Phi" )
            return False

        elif self.kappaCCH.text() == "":
            self.errorCH.setText("Please fill Kappa C value")
            return False

        elif len(self.kappaCCH.text().split(",")) != int(noP_value * ((noP_value - 1) / 2)):
            self.errorCH.setText("Required " + str((noP_value * ((noP_value - 1) / 2))) + " values for Kappa C" )
            return False

        elif self.afmCH.text() == "":
            self.errorCH.setText("Please fill A fm value")
            return False

        elif self.bfpCH.text() == "":
            self.errorCH.setText("Please fill B fm value")
            return False


        elif self.tdbfnameCH.text() == "" and self.tdbflagCH.value() == 1:
            self.errorCH.setText("Please fill tdbfname")
            return False

        else:
            self.errorCH.setText("")
            return True

    def updatetdbflag(self):
        if self.tdbflagCH.value() ==0:
            self.tdbfnameCH.setText("")
            self.tdbfnameCH.setEnabled(False)
        elif self.tdbflagCH.value() ==1:
            self.tdbfnameCH.setEnabled(True)

    def tableItemClickedCHA(self):
        if self.tableWidgetCHA.selectedItems()[0].text()  =="DM":
            self.tableWidgetCHA.selectedItems()[0].setText("FM")

        elif self.tableWidgetCHA.selectedItems()[0].text()  =="FM":
            self.tableWidgetCHA.selectedItems()[0].setText("DM")

        else:
            return


    def clickedfinish(self):  ##code for finish btn operation. it firstly varifies the data then generate file

        dimesion = self.dim.value()

        if self.mesh_x.text() != "":
            mesh_X = self.mesh_x.text()
        else:
            self.finish_error.setText("Please fill Mesh-X Value")
            return

        if self.mesh_y.text() != "":
            mesh_Y = self.mesh_y.text()
        else:
            self.finish_error.setText("Please fill Mesh-Y Value")
            return

        if self.mesh_z.text() != "":
            mesh_Z = self.mesh_z.text()
        else:
            self.finish_error.setText("Please fill Mesh-Z Value")
            return


        if self.dx.text() !="":
            Dx = self.dx.text()
        else:
            self.finish_error.setText("Please fill dx Value")
            return

        if self.dy.text() !="":
            Dy = self.dy.text()
        else:
            self.finish_error.setText("Please fill dy Value")
            return

        if self.dz.text() !="":
            Dz = self.dz.text()
        else:
            self.finish_error.setText("Please fill dz Value")
            return

        if self.dt.text() !="":
            Dt = self.dt.text()
        else:
            self.finish_error.setText("Please fill dt Value")
            return


        NoP = self.noP.value()
        NoC = self.noC.value()

        if self.timeSteps.text() !="":
            TimeSteps = self.timeSteps.text()
        else:
            self.finish_error.setText("Please fill TimeSteps Value")
            return

        if self.saveAt.text() !="":
            saveAt = self.saveAt.text()
        else:
            self.finish_error.setText("Please fill SaveAt Value")
            return

        if self.Nsmooth.text() !="":
            Nsmooth = self.Nsmooth.text()
        else:
            self.finish_error.setText("Please fill Nsmooth Value")
            return
        
        RESTART = self.reStart.value()

        if self.startTime.text() !="":
            STARTTIME = self.startTime.text()
        else:
            self.finish_error.setText("Please fill Start Time")
            return
        
        NumWORKERS = self.numWorkers.text()

        COMPONENTS_name = self.ctext.toPlainText().splitlines()
        if len( COMPONENTS_name) != NoC:
            self.finish_error.setText("Required " + str(NoC) + " Components Names ")
            return
        else:
            COMPONENTS =COMPONENTS_name[0]
            for j in range(1,len(COMPONENTS_name),1):
                COMPONENTS = COMPONENTS + "," + COMPONENTS_name[j]


        PHASES_name = self.ptext.toPlainText().splitlines()
        if len(PHASES_name) != NoP:
            self.finish_error.setText("Required " + str(NoP) + " Phases Names ")
            return
        else:
            PHASES =PHASES_name[0]
            for k in range(1,len(PHASES_name),1):
                PHASES = PHASES + "," +PHASES_name[k]


        GAMMA_val = self.gammaInput.text().split(",")
        if len(GAMMA_val) != int(NoP*((NoP - 1)/2)) or self.gammaInput.text() == "":
            self.finish_error.setText("Required " + str(int(NoP*((NoP - 1)/2))) + " Gamma Values ")
            return
        else:
            GAMMA = self.gammaInput.text()

        if self.R_Value.text() !="":
            R = self.R_Value.text()
        else:
            self.finish_error.setText("Please fill R Value")
            return
        
        if self.V_Value.text() !="":
            V = self.V_Value.text()
        else:
            self.finish_error.setText("Please fill V Value")
            return
        

        DIFFUSIVITY = [""]*NoP
        EIGEN_STRAIN =[""]*NoP
        VOIGT = [""]*NoP

        for i in range(NoP):
            if self.Diffusivity[i] != "" :
                diff = self.Diffusivity[i].split(",")
                if self.DiffusivityType[i] ==0 and len(diff) != NoP*NoP:
                    self.finish_error.setText("Required " + str(NoP*NoP) + "Diffusivity Values for phase " + PHASES_name[i])
                    return
                elif self.DiffusivityType[i] == 1 and len(diff) != NoP:
                    self.finish_error.setText("Required " + str(NoP) + "Diffusivity Values for phase " + PHASES_name[i])
                    return

                else:
                    DIFFUSIVITY[i] = "{" + str(self.DiffusivityType[i]) + "," + str(i) +"," + str(self.Diffusivity[i])+"};\n"



            if self.eigenStrain[i] == "" or len(self.eigenStrain[i].split(",")) !=6:
                self.finish_error.setText("Required 6 Eigenstrain Values for phase " + PHASES_name[i])
                return
            else:
                EIGEN_STRAIN[i] = "{"+str(i) + "," + str(self.eigenStrain[i]) +"};\n"

            if self.elasticConstant[i] != "":

                elasticCON = self.elasticConstant[i].split(",")
                elasticTP = ""

                if self.elasticType[i] == "0" and len(elasticCON) !=3:
                    self.finish_error.setText("Required 3 elastic Constant Values for phase " + PHASES_name[i])
                    return

                elif self.elasticType[i] == "0" and len(elasticCON) ==3:

                    elasticTP ="VOIGT_ISOTROPIC"

                elif self.elasticType[i] == "1" and len(elasticCON) !=3:
                    self.finish_error.setText("Required 3 elastic Constant Values for phase " + PHASES_name[i])
                    return

                elif self.elasticType[i] == "1" and len(elasticCON) ==3:
                    elasticTP = "VOIGT_CUBIC"

                elif self.elasticType[i] == "2" and len(elasticCON) !=6:
                    self.finish_error.setText("Required 6 elastic Constant Values for phase " + PHASES_name[i])
                    return

                elif self.elasticType[i] == "2" and len(elasticCON) ==6:
                    elasticTP ="VOIGT_TETRAGONAL"

                VOIGT[i] = elasticTP + " = {" + str(i) +","+  str(self.elasticConstant[i]) + "};\n"
                


        #checking infile filling file

        if self.infile.text() == "":
            self.finish_error.setText("Please fill Infile Name")
            return

        if self.filling.text() == "":
            self.finish_error.setText("Please fill filling Name")
            return


        ## WRITING ON FILE

        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        if dlg.exec_():
            self.runDir =  ''.join(dlg.selectedFiles())
            infilename =  self.runDir + "/" + self.infile.text()
            fillingname = self.runDir + "/" + self.filling.text()

        else:
            return

        try:
            f = open(infilename, "w")
        
        except PermissionError:
            self.finish_error.setText("PermissionError: Do not select root directory.")
        except IOError:
            print("could not write")

        f.write("##Geometrical dimensions of the simulation domain\n"
                "DIMENSION = " + str(dimesion) + ";\n"
                "MESH_X = " + str(mesh_X) + ";\n"
                "MESH_Y = " + str(mesh_Y) + ";\n"
                "MESH_Z = " + str(mesh_Z) + ";\n"
                "##Discretization, space and time\n"
                "DELTA_X = " + str(Dx) + ";\n"
                "DELTA_Y = " + str(Dy) + ";\n"
                "DELTA_Z = " + str(Dz) + ";\n"
                "DELTA_t = " + str(Dt) + ";\n"
                "##Number of phases and composition\n"
                "NUMPHASES = " + str(NoP) + ";\n"
                "NUMCOMPONENTS = " + str(NoC) + ";\n"
                "#Running and saving information\n"
                "NTIMESTEPS = " + str(TimeSteps) + ";\n"
                "NSMOOTH = " + str(Nsmooth) + ";\n"
                "SAVET = " + str(saveAt) + ";\n"
                "RESTART = " + str(RESTART) + ";\n"
                "STARTTIME = " + str(STARTTIME) + ";\n"
                "numworkers = " + str(NumWORKERS) + ";\n"
                "## Component and Phase names\n"
                "COMPONENTS = {" + COMPONENTS +"};\n"
                "PHASES = {" + PHASES +"};\n"
                "##Material properties\n"
                "GAMMA = {"+ str(GAMMA) +"};\n"
                "R = " + R +";\n"
                "V = " + V +";\n"
                )

        for i in range(len(DIFFUSIVITY)):
            f.write("DIFFUSIVITY = " + DIFFUSIVITY[i] )

        for i in range(len(EIGEN_STRAIN)):
            f.write("EIGEN_STRAIN = " + EIGEN_STRAIN[i] )

        for i in range(len(VOIGT)):
            f.write( VOIGT[i] )


        #Boundary Conditions
        f.write("##Boundary conditions\n")
        if self.Bcnd[0] =="":
            self.finish_error.setText("Required Boundary Conditions Values for phi ")

        else:
            f.write("BOUNDARY = {phi," + self.Bcnd[0] + ",0,0};\n")

        if self.Bcnd[1] =="" and self.Bcnd[2] =="":
            self.finish_error.setText("Required Boundary Conditions Values for mu ")

        else:
            f.write("BOUNDARY = {mu," + self.Bcnd[1] + ",0,0};\n")

        if self.Bcnd[2] !="":
            f.write("BOUNDARY = {c," + self.Bcnd[2] + ",0,0};\n")

        if self.Bcnd[3] =="":
            self.finish_error.setText("Required Boundary Conditions Values for T ")

        else:
            f.write("BOUNDARY = {T," + self.Bcnd[3] + ",0,0};\n")

        #BOUNDARY VALUE

        if self.BconV[0] =="":
            self.finish_error.setText("Required Boundary Values for phi ")

        else:
            f.write("BOUNDARY_VALUE = {phi," + self.BconV[0] + ",0,0};\n")

        if self.BconV[1] =="" and self.BconV[2] =="":
            self.finish_error.setText("Required Boundary Values for mu ")

        else:
            f.write("BOUNDARY_VALUE = {mu," + self.BconV[1] + ",0,0};\n")

        if self.BconV[2] !="":
            f.write("BOUNDARY_VALUE = {c," + self.BconV[2] + ",0,0};\n")

        if self.BconV[3] =="":
            self.finish_error.setText("Required Boundary Values for T ")

        else:
            f.write("BOUNDARY_VALUE = {T," + self.BconV[3] + ",0,0};\n")
            
        

        #MODEL SPECIFIC PARAMETER
        if self.radio_GP.isChecked():

            if self.saveGPChack():
                f.write("##Model-specific parameters: Grand-potential model\n")

                if self.thermalYGP.isChecked():
                    ISOTHERMALVvalue = 1
                elif self.thermalNGP.isChecked():
                    ISOTHERMALVvalue = 0

                f.write("ISOTHERMAL = " + str(ISOTHERMALVvalue) + ";\n")

                if self.simTypeGP.currentIndex() == 0:
                    f.write("BINARY = 1;\nTERNARY = 0;\nDILUTE = 0;\n")
                elif self.simTypeGP.currentIndex() == 1:
                    f.write("BINARY = 0;\nTERNARY = 1;\nDILUTE = 0;\n")
                elif self.simTypeGP.currentIndex() == 2:
                    f.write("BINARY = 0;\nTERNARY = 0;\nDILUTE = 1;\n")

                f.write("T = " + self.TGP.text() + ";\n"
                        "WRITEFORMAT = "+self.writeFormatGP.currentText()+";\n"
                        "WRITEHDF5 = " + str(self.writehdfGP.value()) +";\n"
                        "TRACK_PROGRESS = " + self.trackProgressGP.text()+";\n"
                        "epsilon = " + self.epsilonGP.text()+";\n"
                        "tau = " + self.tauGP.text()+";\n"
                        "Tau = {" + self.TauGP.text()+"};\n"
                        "Function_anisotropy = " + self.FanisotropyGP.text()+";\n"
                        "Anisotropy_type = " + self.anisotropyTypeGP.text()+";\n"
                        "dab = {" + self.debGP.text()+"};\n"
                        "Function_W = " + self.funcWGP.text()+";\n"
                        "Gamma_abc = {" + self.gammaABCGP.text()+"};\n"
                        "Shift = " + str(self.shiftGP.value())+";\n"
                        "Shiftj = " + self.shiftJGP.text()+";\n"
                        "Writecomposition = " + self.writecompGP.text()+";\n"
                        "Noise_phasefield = " + str(self.noiseGP.value()) +";\n"
                        "Amp_Noise_Phase = " + self.ampNoiseGP.text()+";\n"
                        "Equilibrium_temperature = " + self.equTGP.text()+";\n"
                        "Filling_temperature = " + self.fillingTGP.text()+";\n"
                        "Tempgrady = {" + self.tempgradyGP.text()+"};\n")
        
                
            else:
                self.finish_error.setText("Fill All required Model Specific Parameter")
                return


        elif self.radio_KKR.isChecked():

            if self.saveKKSCheck():

                f.write("##Model-specific parameters: KKS FFT GPU \n")
                f.write("WRITEFORMAT = "+self.writeFormatKKS.currentText()+";\n"
                        "TRACK_PROGRESS = " + self.trackprogressKKS.text()+";\n"
                        "Tau = {" + self.TauKKS.text()+"};\n"
                        "epsilon = " + self.epsilonKKS.text()+";\n"
                        "Equilibrium_temperature = " + self.equTKKS.text()+";\n"
                        "T = " + self.temperatureKKS.text()+";\n"
                    )
                
                '''
                for i in range(NoP):
                    f.write("f0 = {" +  self.tableWidgetKKSF.item(i,0).text() + ","+ self.tableWidgetKKSF.item(i,1).text() + "};\n")
                
                
                for i in range(NoP*NoP):
                    if self.tableWidgetKKS.item(i,2).text() !="-":
                        f.write("ceq = {" +  self.tableWidgetKKS.item(i,0).text() + ","+ self.tableWidgetKKS.item(i,1).text() + "," + self.tableWidgetKKS.item(i,2).text() + "};\n")
                '''


        elif self.radio_KKS2.isChecked():

            if self.saveKKS2Check():

                f.write("##Model-specific parameters: Kim model\n")

                if self.thermalYKKS2.isChecked():
                    ISOTHERMALvalue = 1
                elif self.thermalNKKS2.isChecked():
                    ISOTHERMALvalue = 0

                f.write("ISOTHERMAL = " + str(ISOTHERMALvalue) + ";\n")

                if self.simTypeKKS2.currentIndex() == 0:
                    f.write("BINARY = 1;\nTERNARY = 0;\nDILUTE = 0;\n")
                elif self.simTypeKKS2.currentIndex() == 1:
                    f.write("BINARY = 0;\nTERNARY = 1;\nDILUTE = 0;\n")
                elif self.simTypeKKS2.currentIndex() == 2:
                    f.write("BINARY = 0;\nTERNARY = 0;\nDILUTE = 1;\n")

                f.write("WRITEFORMAT = "+self.writeFormatKKS2.currentText()+";\n"
                        "TRACK_PROGRESS = " + self.trackProgressKKS2.text()+";\n"
                        "epsilon = " + self.epsilonKKS2.text()+";\n"
                        "Function_anisotropy = " + self.FanisotropyKKS2.text()+";\n"
                        "dab = {" + self.debKKS2.text()+"};\n"
                        "Noise_phasefield = " + str(self.noiseKKS2.value()) +";\n"
                        "Amp_Noise_Phase = " + self.ampNoiseKKS2.text()+";\n"
                        "Tempgrady = {" + self.tempGradyKKS2.text()+"};\n"
                        "tNoiseStart = " + self.tNoiseStartKKS2.text()+";\n"
                        
                        "Shift = " + str(self.shiftKKS2.value())+";\n"
                        "Shiftj = " + self.ShiftJKKS2.text()+";\n"
                        "Equilibrium_temperature = " + self.TLKKS2.text()+";\n"
                        "Filling_temperature = " + self.fillingTKKS.text()+";\n"
                        "T = " + self.temperatureKKS2.text()+";\n"                     
                
                        "atr = " + self.atrKKS2.text()+";\n"
                        "CLplatformID = " + self.CLPidKKS2.text()+";\n"
                        "CLdeviceID = " + self.CLDidKKS2.text()+";\n"
                        
                        )
     
                    
                '''
                for i in range(NoP*NoP):
                    if self.tableWidgetKKS2.item(i,2).text() !="-":
                        f.write("ceq = {" +  self.tableWidgetKKS2.item(i,0).text() + ","+ self.tableWidgetKKS2.item(i,1).text() + "," + self.tableWidgetKKS2.item(i,2).text() + "};\n")

                for i in range(NoP*NoP):
                    if self.tableWidgetKKS2.item(i,3).text() !="-":
                        f.write("cfill = {" +  self.tableWidgetKKS2.item(i,0).text() + ","+ self.tableWidgetKKS2.item(i,1).text() + "," + self.tableWidgetKKS2.item(i,3).text() + "};\n")

                dummycount =0

                for i in range(NoP):
                    for j in range(NoP):
                        if j!=i and j>i:
                            f.write("Rotation_matrix = {" +  self.tableWidgetKKS2.item(dummycount,0).text() + ","+ self.tableWidgetKKS2.item(dummycount,1).text() + "," + self.tableWidgetKKS2.item(dummycount,4).text() + "};\n")
                        dummycount = dummycount+1
                '''

        elif self.radio_CH.isChecked():

            if self.saveCHCheck():
                f.write("##Model-specific parameters: Preipitate growth (FFT) \n")
                f.write("WRITEFORMAT = "+self.writeFormatCH.currentText()+";\n"
                        "TRACK_PROGRESS = " + self.trackProgressCH.text()+";\n"
                        "L_phi = {" + self.lPhiCH.text()+"};\n"
                        "Kappa_phi = {" + self.kappaPhiCH.text()+"};\n"
                        "Kappa_c = {" + self.kappaCCH.text()+"};\n"
                        "A_fm  = {" + self.afmCH.text() +"};\n"
                        "B_fp  = {" + self.bfpCH.text()+"};\n"
                        "spinodal = " + str(self.spinodalCH.value())+";\n"
                        "tdbflag = " + str(self.tdbflagCH.value())+";\n")

                if self.tdbflagCH.value() == 1:
                    f.write("tdbfname = " + self.tdbfnameCH.text()+";\n")

                for i in range(NoP):

                    if self.tableWidgetCHA.item(i,1).text() == "FM":
                        matrix_CHA = "0"
                    else:
                        matrix_CHA = "1"
                    f.write("AtomicMobility = {" + matrix_CHA + ","+ self.tableWidgetCHA.item(i,0).text() + "," + self.tableWidgetCHA.item(i,2).text() + "};\n")
                    
                '''
                for i in range(NoP*NoP):
                    if self.tableWidgetCH.item(i,2).text() !="-":
                        f.write("ceq = {" +  self.tableWidgetCH.item(i,0).text() + ","+ self.tableWidgetCH.item(i,1).text() + "," + self.tableWidgetCH.item(i,2).text() + "};\n")


                for i in range(NoP*NoP):
                    if self.tableWidgetCH.item(i,3).text() !="-":
                        f.write("cfill = {" +  self.tableWidgetCH.item(i,0).text() + ","+ self.tableWidgetCH.item(i,1).text() + "," + self.tableWidgetCH.item(i,3).text() + "};\n")
                        
                '''
            else:
                self.finish_error.setText("Fill All required Model Specific Parameter")
                return
        
        
        ###Function Parameter
        
        if self.funcF.value() == 1:
            f.write("Function_F = " + str(self.funcF.value()) + ";\n")
            for i in range(NoP):
                if self.tableWidgetGPA.item(i,1) is None or self.tableWidgetGPA.item(i,1).text() == '':
                    self.finish_error.setText("Please fill All values of A")
                    return False
                else:
                    
                    f.write("A = {" + str(i) +"," +self.tableWidgetGPA.item(i,1).text()+"};\n")
                
        elif self.funcF.value() == 2 or self.funcF.value() == 3 or self.funcF.value() == 4 :
            f.write("Function_F = " + str(self.funcF.value()) + ";\n")
            
            if self.num_thermo_phases.value() == 0 :
                self.finish_error.setText("Incorrect num_thermo_phases")
                return False
            else:
                f.write("num_thermo_phases = " + str(self.num_thermo_phases.value()) + ";\n")
                
            if self.tdbfname.text() == "":
                self.finish_error.setText("Please fill tdbfname")
                return False
            
            else:
                f.write("tdbfname = " + self.tdbfname.text() + ";\n")
                
            
            if self.tdbphases.text() == "" or len(self.tdbphases.text().split(",")) != self.num_thermo_phases.value():
                self.finish_error.setText("Please fill Tdb Phases and required " + str(self.num_thermo_phases.value()) + " values")
                return False
            
            else:
                f.write("tdb_phases = {" + self.tdbphases.text() + "};\n")
            
        
            if self.phasemap.text() == "" or len(self.phasemap.text().split(",")) != NoP:
                self.finish_error.setText("Please fill Phase Map and required " + str(NoP) + " values")
                return False
            
            else :
                f.write("phase_map = {" + self.phasemap.text() + "};\n")
                
                
        if self.funcF.value() == 1:
           
            for i in range(NoP*NoP):
                if self.tableWidgetGP.item(i,2) is None or self.tableWidgetGP.item(i,2).text() == '':
                    self.finish_error.setText("Please fill All values of Ceq")
                    return False
                
                elif self.tableWidgetGP.item(i,2).text() !="-":
                    f.write("ceq = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,2).text() + "};\n")
                    
            for i in range(NoP*NoP):    
                if self.tableWidgetGP.item(i,3) is None or self.tableWidgetGP.item(i,3).text() == '':
                    self.finish_error.setText("Please fill All values of Cfill")
                    return False
                
                elif self.tableWidgetGP.item(i,3).text() !="-":
                    f.write("cfill = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,3).text() + "};\n")
            
            for i in range(NoP*NoP):
                
                if self.tableWidgetGP.item(i,4) is None or self.tableWidgetGP.item(i,4).text() == '':
                    self.finish_error.setText("Please fill All values of Slope")
                    return False
                
                elif self.tableWidgetGP.item(i,4).text() !="-":
                    f.write("slopes = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,4).text() + "};\n")
                    
            for i in range(NoP*NoP):
                
                if self.radio_GP.isChecked() and self.FanisotropyGP.text() == "0":
                    pass
                
                elif self.radio_KKS2.isChecked() and self.FanisotropyKKS2.text() == "0":
                    pass
                
                else:
                    if self.tableWidgetGP.item(i,6) is None or self.tableWidgetGP.item(i,6).text() == '':
                        self.finish_error.setText("Please fill All values of Rotation matrix")
                        return False
                    
                    elif self.tableWidgetGP.item(i,6).text() !="-":
                        f.write("Rotation_matrix = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,6).text() + "};\n")
   
            
        elif self.funcF.value() == 2:
            
            for i in range(NoP*NoP):
                if self.tableWidgetGP.item(i,2) is None or self.tableWidgetGP.item(i,2).text() == '':
                    self.finish_error.setText("Please fill All values of Ceq")
                    return False
                
                elif self.tableWidgetGP.item(i,2).text() !="-":
                    f.write("ceq = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,2).text() + "};\n")
                    
            for i in range(NoP*NoP):    
                if self.tableWidgetGP.item(i,3) is None or self.tableWidgetGP.item(i,3).text() == '':
                    self.finish_error.setText("Please fill All values of Cfill")
                    return False
                
                elif self.tableWidgetGP.item(i,3).text() !="-":
                    f.write("cfill = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,3).text() + "};\n")
            
            
            for i in range(NoP*NoP):    
                if self.tableWidgetGP.item(i,5) is None or self.tableWidgetGP.item(i,5).text() == '':
                    self.finish_error.setText("Please fill All values of Cguess")
                    return False
                
                elif self.tableWidgetGP.item(i,5).text() !="-":
                    f.write("c_guess = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,5).text() + "};\n")
        
            for i in range(NoP*NoP):
                
                if self.radio_GP.isChecked() and self.FanisotropyGP.text() == "0":
                    pass
                
                elif self.radio_KKS2.isChecked() and self.FanisotropyKKS2.text() == "0":
                    pass
                
                else:
                    if self.tableWidgetGP.item(i,6) is None or self.tableWidgetGP.item(i,6).text() == '':
                        self.finish_error.setText("Please fill All values of Rotation matrix")
                        return False
                    
                    elif self.tableWidgetGP.item(i,6).text() !="-":
                        f.write("Rotation_matrix = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,6).text() + "};\n")
        
        elif self.funcF.value() == 3:
            for i in range(NoP*NoP):
                if self.tableWidgetGP.item(i,2) is None or self.tableWidgetGP.item(i,2).text() == '':
                    self.finish_error.setText("Please fill All values of Ceq")
                    return False
                
                elif self.tableWidgetGP.item(i,2).text() !="-":
                    f.write("ceq = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,2).text() + "};\n")
            
            for i in range(NoP*NoP):
                if self.tableWidgetGP.item(i,3) is None or self.tableWidgetGP.item(i,3).text() == '':
                    self.finish_error.setText("Please fill All values of Cfill")
                    return False
                
                elif self.tableWidgetGP.item(i,3).text() !="-":
                    f.write("cfill = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,3).text() + "};\n")
            
            
            for i in range(NoP*NoP):                
                if self.tableWidgetGP.item(i,5) is None or self.tableWidgetGP.item(i,5).text() == '':
                    self.finish_error.setText("Please fill All values of Cguess")
                    return False
                elif self.tableWidgetGP.item(i,5).text() !="-":
                    f.write("c_guess = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,5).text() + "};\n")
                    
            for i in range(NoP*NoP):
                if self.radio_GP.isChecked() and self.FanisotropyGP.text() == "0":
                    pass
                
                elif self.radio_KKS2.isChecked() and self.FanisotropyKKS2.text() == "0":
                    pass
                
                else:
                    if self.tableWidgetGP.item(i,6) is None or self.tableWidgetGP.item(i,6).text() == '':
                        self.finish_error.setText("Please fill All values of Rotation matrix")
                        return False
                
                    elif self.tableWidgetGP.item(i,6).text() !="-":
                        f.write("Rotation_matrix = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,6).text() + "};\n")
        
        elif self.funcF.value() == 4:
            for i in range(NoP*NoP):
                if self.tableWidgetGP.item(i,2) is None or self.tableWidgetGP.item(i,2).text() == '':
                    self.finish_error.setText("Please fill All values of Ceq")
                    return False
                
                elif self.tableWidgetGP.item(i,2).text() !="-":
                    f.write("ceq = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,2).text() + "};\n")
            
            for i in range(NoP*NoP):
                if self.tableWidgetGP.item(i,3) is None or self.tableWidgetGP.item(i,3).text() == '':
                    self.finish_error.setText("Please fill All values of Cfill")
                    return False
                
                elif self.tableWidgetGP.item(i,3).text() !="-":
                    f.write("cfill = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,3).text() + "};\n")
            
            for i in range(NoP*NoP):
                if self.radio_GP.isChecked() and self.FanisotropyGP.text() == "0":
                    pass
                
                elif self.radio_KKS2.isChecked() and self.FanisotropyKKS2.text() == "0":
                    pass
                
                else:
                    if self.tableWidgetGP.item(i,6) is None or self.tableWidgetGP.item(i,6).text() == '':
                        self.finish_error.setText("Please fill All values of Rotation matrix")
                        return False
                    
                    elif self.tableWidgetGP.item(i,6).text() !="-":
                        f.write("Rotation_matrix = {" +  self.tableWidgetGP.item(i,0).text() + ","+ self.tableWidgetGP.item(i,1).text() + "," + self.tableWidgetGP.item(i,6).text() + "};\n")


        f.close()  ## closing infile writer


        ##writing filling file
        if self.ShapeList.count() > 0:
            f = open(fillingname, "w")

            for i in range(self.ShapeList.count()):

                shapeText  = self.ShapeList.item(i).text()
                shapeData = shapeText.split(" ")

                f.write( "FILL"+shapeData[0] + " = " + shapeData[1] + ";\n")

            f.close()
            writing_file_msg  = "\nSucessfully Created Input and Filling files as following :-\n\n               1) Input file saved as "+ self.infile.text()+"                    \n               2) Filing File saved as "+self.filling.text()+"              \n"
        else:
            writing_file_msg  = "\nSucessfully Created Input file :-\n\n  - Input file saved as "+ self.infile.text()+"                    \n\nUnable to create filling file. Error - Empty Filiing Data .\n"

        self.finish_error.setText("")

        Submitmsg = QMessageBox()
        Submitmsg.setWindowTitle("File Created")
        Submitmsg.setText(writing_file_msg)
        Submitmsg.exec_()

        self.runBtn.setEnabled(True)
        self.preview.setEnabled(True)
        self.PPbutton.setEnabled(True)

    def clickedpreview(self):
        if os.path.isdir(self.runDir + "/DATA/"):  ##checking data file status

            if os.path.isfile("/opt/paraviewopenfoam56/bin/paraview"):  ##checking paraview installation status
                list_of_files = glob.glob(self.runDir + "/DATA/"+ self.output.text() +"*.*")
                if len(list_of_files) == 0:
                    self.finish_error.setText("Sorry, output file not found.")
                    return
                latest_file = max(list_of_files, key=os.path.getctime)

                paraviewcmd = "gnome-terminal -e 'bash -c \"/opt/paraviewopenfoam56/bin/paraview " +latest_file +"; bash\" '"
                os.system(paraviewcmd)
            elif os.path.isfile(os.path.expanduser("~/MicroSim/.Paraview")): ## Checking for paraview saved path
                readPath = open(os.path.expanduser('~/MicroSim/.Paraview'), "r")
                readPathParaview = readPath.read().replace("\n", "")
                list_of_files = glob.glob(self.runDir + "/DATA/"+ self.output.text() +"*.*")
                if len(list_of_files) == 0:
                    self.finish_error.setText("Sorry, output file not found.")
                    return
                latest_file = max(list_of_files, key=os.path.getctime)

                paraviewcmd = "gnome-terminal -e 'bash -c \"" + readPathParaview +" " +latest_file +"; bash\" '"
                os.system(paraviewcmd)

            else:
                self.paraviewError.show()
        else:
            self.finish_error.setText("Sorry, DATA directory not found.")
            
            
    def paraviewErrorCloseClicked(self):
        self.paraviewError.hide()

    def paraviewBrowseClicked(self):

        ## WRITING ON FILE
        dlgParaview = QtWidgets.QFileDialog()
        dlgParaview.setFileMode(QtWidgets.QFileDialog.AnyFile)
        if dlgParaview.exec_():
            self.paraviewDir =  ''.join(dlgParaview.selectedFiles())
            self.paraviewPath.setText(self.paraviewDir)


        else:
            self.paraviewErrorLine.setText("Error occure while selecting directory.")

        return
    
    def paraviewOpenClicked(self):

        if self.paraviewPath.text() == "":
            self.paraviewErrorLine.setText("Error : Please select a path")
        else :
            HomePathparaview = os.path.expanduser("~/MicroSim/.Paraview")
            paraviewFileDir = open(HomePathparaview, "w")
            paraviewFileDir.write(self.paraviewPath.text())
            paraviewFileDir.close()
            list_of_files = glob.glob(self.runDir + "/DATA/"+ self.output.text() +"*.*")
            latest_file = max(list_of_files, key=os.path.getctime)
            paraviewcmd = "gnome-terminal -e 'bash -c \"" + self.paraviewPath.text() +" " +latest_file +"; bash\" '"
            os.system(paraviewcmd)
            
        return
    
            
    def clickedrunBtn(self):
        if self.output.text() == "":
            self.finish_error.setText("Please fill output file name")
            return
        else:
            self.finish_error.setText("")


        if os.path.isfile(self.runDir + "/" + self.infile.text()):  ##checking Infile Location
            pass
        else:
            self.finish_error.setText("Sorry, " + self.infile.text() + " not found." )
            return

        if os.path.isfile(self.runDir + "/" + self.filling.text()):  ##checking Infile Location
            pass
        else:
            self.finish_error.setText("Sorry, " + self.filling.text() + " file not found." )
            return

        if self.radio_GP.isChecked():
            

            commandLine ="cd ~/MicroSim/Grand_potential_Finite_difference_2D_MPI/; python3 GEdata_writer.py " +self.runDir +"/"+self.infile.text() + " ;make clean;make; cp microsim_gp ~/MicroSim/bin/;cd " + self.runDir + ";mpirun.mpich -np 4 ~/MicroSim/bin/microsim_gp "  +self.infile.text()+" "+self.filling.text()+" "+self.output.text() + " 2 2"
            
            os.system("gnome-terminal -e 'bash -c  \""+commandLine+";bash\"'")
        
        elif self.radio_KKR.isChecked():
            commandLine ="cd ~/MicroSim/KKS_CuFFT/; python3 GEdata_writer.py " +self.runDir +"/"+self.infile.text() + " ;make clean;make; cp microsim_kks_cufft ~/MicroSim/bin/;cd " + self.runDir + ";mpirun -n 4 ~/MicroSim/bin/microsim_kks_cufft "  +self.infile.text()+" "+self.filling.text()+" "+self.output.text()
            
            os.system("gnome-terminal -e 'bash -c \""+commandLine+";bash\"'")

        elif self.radio_KKS2.isChecked():
            commandLine ="cd ~/MicroSim/KKS_OpenCl/; python3 GEdata_writer.py " +self.runDir +"/"+self.infile.text() + " ;make clean;make; cp microsim_kks_opencl ~/MicroSim/bin/;cd " + self.runDir + ";~/MicroSim/bin/microsim_kks_opencl "  +self.infile.text()+" "+self.filling.text()+" "+self.output.text()
            
            os.system("gnome-terminal -e 'bash -c  \""+commandLine+";bash\"'")

        elif self.radio_CH.isChecked():
            commandLine ="cd ~/MicroSim/Cahn_Hilliard_FFT_2D/; python3 GEdata_writer.py " +self.runDir +"/"+self.infile.text() + " ;make clean;make; cp cp microsim_ch_fft ~/MicroSim/bin/;cd " + self.runDir + ";~/MicroSim/bin/microsim_ch_fft "  +self.infile.text()+" "+self.filling.text()+" "+self.output.text()
            
            os.system("gnome-terminal -e 'bash -c \""+commandLine+";bash\"'")


    def startNewClicked(self):
        self.resetAll()
        self.StartFrame.hide()

    def continueTabClicked(self):
        self.StartFrame.hide()

    def ReadfromFile(self):
        if os.path.exists(self.fileLabel.text()):
            try:
                fileDir = open(self.fileLabel.text(), 'r')
                fileLines = fileDir.readlines()
                self.StartFrame.hide()
                self.resetAll()
                self.ShapeFlag = 1
                self.gpFlag = [0]*27
                self.chFlag = [0]*26
                self.kksFlag = [0]*38
                self.kks2Flag = [0]*45
                for i in fileLines:

                    if "#" in i:
                        pass
                    elif "=" in i:
                        entries = i.split("=")
                        entries[1] = entries[1].replace(" ", "")
                        entries[1] = entries[1].replace(";", "")
                        entries[1] = entries[1].replace("\n", "")
                        if self.model_GP.isChecked():
                            self.fillEntryGP(entries[0].replace(" ", ""),entries[1] )
                        elif self.model_CH.isChecked():
                            self.fillEntryCH(entries[0].replace(" ", ""),entries[1] )
                        elif self.model_KKS.isChecked():
                            self.fillEntryKKS(entries[0].replace(" ", ""),entries[1] )
                        elif self.model_KKS2.isChecked():
                            self.fillEntryKKS2(entries[0].replace(" ", ""),entries[1] )

                #print(self.gpFlag)
                if self.model_GP.isChecked():
                    gpVariables =["DIMENSION", "MESH_X" ,"MESH_Y", "MESH_Z", "DELTA_X" ,"DELTA_Y", "DELTA_Z", "DELTA_t", "NUMPHASES", "NUMCOMPONENTS", "NTIMESTEPS", "NSMOOTH", "SAVET", "COMPONENTS", "PHASES", "GAMMA", "DIFFUSIVITY", "R", "V", "EIGEN_STRAIN", "Elastic Constant","BOUNDARY Phi","BOUNDARY mu/c","BOUNDARY T","BOUNDARY_VALUE Phi","BOUNDARY_VALUE mu/c","BOUNDARY_VALUE T"]
                    gpmsgFlag =0
                    gperror = "Oops ! we have noticed some missing parameters in your Infile\n"
                    for i in range(27):
                        if self.gpFlag[i] == 0:
                            gperror = gperror + "\n ("+str(gpmsgFlag+1) + ") " + gpVariables[i]
                            gpmsgFlag = gpmsgFlag +1
                    self.fillGPCheck()
                    if len(self.errorListGP) >0 or gpmsgFlag != 0:
                        GPmsg = QMessageBox()
                        GPmsg.setWindowTitle("Import error")
                        for n in range(len(self.errorListGP)):
                            gperror = gperror + "\n ("+str(n+1+gpmsgFlag) + ") " + self.errorListGP[n]
                        GPmsg.setText(gperror + "\n")
                        GPmsg.exec_()
                    
                if self.model_CH.isChecked():
                    chVariables =["DIMENSION", "MESH_X" ,"MESH_Y", "MESH_Z", "DELTA_X" ,"DELTA_Y", "DELTA_Z", "DELTA_t", "NUMPHASES", "NUMCOMPONENTS", "NTIMESTEPS", "NSMOOTH", "SAVET", "COMPONENTS", "PHASES", "R", "V", "WRITEFORMAT", "TRACK_PROGRESS", "AtomicMobility", "L_phi", "Kappa_phi" "Kappa_c", "A_fm", "B_fp", "ceq","cfill" ]
                    chmsgFlag =0
                    cherror = "Oops ! we have noticed some missing parameters in your Infile\n"
                    for i in range(26):
                        if self.chFlag[i] == 0:
                            cherror = cherror + "\n ("+str(chmsgFlag+1) + ") " + chVariables[i]
                            chmsgFlag = chmsgFlag +1
                    if chmsgFlag != 0:
                        CHmsg = QMessageBox()
                        CHmsg.setWindowTitle("Import error")
                        CHmsg.setText(cherror + "\n")
                        CHmsg.exec_()

                if self.model_KKS.isChecked():
                    kksVariables =["DIMENSION", "MESH_X" ,"MESH_Y", "MESH_Z", "DELTA_X" ,"DELTA_Y", "DELTA_Z", "DELTA_t", "NUMPHASES", "NUMCOMPONENTS", "NTIMESTEPS", "NSMOOTH", "SAVET", "COMPONENTS", "PHASES", "GAMMA", "DIFFUSIVITY", "R", "V", "EIGEN_STRAIN", "Elastic Constant","BOUNDARY Phi","BOUNDARY mu/c","BOUNDARY T","BOUNDARY_VALUE Phi","BOUNDARY_VALUE mu/c","BOUNDARY_VALUE T"," WRITEFORMAT", "TRACK_PROGRESS", "T","relax_coeff" ,"Equilibrium_temperature", "alpha", "lambda","Tau","epsilon"]
                    kksmsgFlag =0
                    kkserror = "Oops ! we have noticed some missing parameters in your Infile\n"
                    for i in range(36):
                        if self.kksFlag[i] == 0:
                            kkserror = kkserror + "\n ("+str(kksmsgFlag+1) + ") " + kksVariables[i]
                            kksmsgFlag = kksmsgFlag +1
                    if kksmsgFlag != 0:
                        KKSmsg = QMessageBox()
                        KKSmsg.setWindowTitle("Import error")
                        KKSmsg.setText(kkserror + "\n")
                        KKSmsg.exec_()

                if self.model_KKS2.isChecked():
                    kks2Variables =["DIMENSION", "MESH_X" ,"MESH_Y", "MESH_Z", "DELTA_X" ,"DELTA_Y", "DELTA_Z", "DELTA_t", "NUMPHASES", "NUMCOMPONENTS", "NTIMESTEPS", "NSMOOTH", "SAVET", "COMPONENTS", "PHASES", "GAMMA", "DIFFUSIVITY", "R", "V", "BOUNDARY Phi","BOUNDARY mu/c","BOUNDARY T","BOUNDARY_VALUE Phi","BOUNDARY_VALUE mu/c","BOUNDARY_VALUE T", "ISOTHERMAL", "BINARY/TERNARY/DILUTE", "WRITEFORMAT", "TRACK_PROGRESS", "epsilon", "Function_anisotropy",  "dab", "temperature", "Noise_phasefield", "Amp_Noise_Phase", "Tempgrady", "tNoiseStart", "Equilibrium_temperature", "atr", "CLplatformID", "CLdeviceID", "shift", "shift J", "Filling_temperature"]
                    kks2msgFlag =0
                    kks2error = "Oops ! we have noticed some missing parameters in your Infile\n"
                    for i in range(44):
                        if self.kks2Flag[i] == 0:
                            kks2error = kks2error + "\n ("+str(kks2msgFlag+1) + ") " + kks2Variables[i]
                            kks2msgFlag = kks2msgFlag +1
                    if kks2msgFlag != 0:
                        KKS2msg = QMessageBox()
                        KKS2msg.setWindowTitle("Import error")
                        KKS2msg.setText(kks2error + "\n")
                        KKS2msg.exec_()
                        
                        

                self.sideBtn2.setGeometry(0,185,231,65)
                self.sideBtn2.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
                self.sideBtn2.setEnabled(True)

                self.sideBtn3.setGeometry(0,250,231,65)
                self.sideBtn3.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
                self.sideBtn3.setEnabled(True)

                self.sideBtn4.setGeometry(0,315,231,65)
                self.sideBtn4.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
                self.sideBtn4.setEnabled(True)

                self.sideBtn5.setGeometry(0,380,231,65)
                self.sideBtn5.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
                self.sideBtn5.setEnabled(True)

                self.sideBtn6.setGeometry(0,445,231,65)
                self.sideBtn6.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
                self.sideBtn6.setEnabled(True)

                self.sideBtn7.setGeometry(0,510,231,65)
                self.sideBtn7.setStyleSheet('background-color: rgb(171, 196, 223);font: 10pt "Ubuntu";')
                self.sideBtn7.setEnabled(True)

            except IOError:
                print("could not read")

            except UnicodeDecodeError:
                print("could not read")

    def fillEntryGP(self,entryname, entryvalue):

        if entryname == "DIMENSION":
            self.dim.setValue(int(entryvalue))
            self.gpFlag[0] = 1
            return

        elif entryname == "MESH_X":
            self.mesh_x.setText(entryvalue)
            self.gpFlag[1] = 1
            return

        elif entryname == "MESH_Y":
            self.mesh_y.setText(entryvalue)
            self.gpFlag[2] = 1
            return

        elif entryname == "MESH_Z":
            self.mesh_z.setText(entryvalue)
            self.gpFlag[3] = 1
            return

        elif entryname == "DELTA_X":
            self.dx.setText(entryvalue)
            self.gpFlag[4] = 1
            return

        elif entryname == "DELTA_Y":
            self.dy.setText(entryvalue)
            self.gpFlag[5] = 1
            return

        elif entryname == "DELTA_Z":
            self.dz.setText(entryvalue)
            self.gpFlag[6] = 1
            return

        elif entryname == "DELTA_t":
            self.dt.setText(entryvalue)
            self.gpFlag[7] = 1
            return

        elif entryname == "NUMPHASES":
            self.noP.setValue(int(entryvalue))
            self.gpFlag[8] = 1
            return
            #self.updateNoP()

        elif entryname == "NUMCOMPONENTS":
            self.noC.setValue(int(entryvalue))
            self.gpFlag[9] = 1
            return
            #self.updateNoC()

        elif entryname == "NTIMESTEPS":
            self.timeSteps.setText(entryvalue)
            self.gpFlag[10] = 1
            return

        elif entryname == "NSMOOTH":
            self.Nsmooth.setText(entryvalue)
            self.gpFlag[11] = 1
            return

        elif entryname == "SAVET":
            self.saveAt.setText(entryvalue)
            self.gpFlag[12] = 1
            return
        
        elif entryname == "RESTART":
            self.reStart.setValue(int(entryvalue))
            return
        
        elif entryname == "STARTTIME":
            self.startTime.setText(entryvalue)
            return

        elif entryname == "numworkers":
            self.numWorkers.setText(entryvalue)
            return

        elif entryname == "COMPONENTS":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ctext.setPlainText(entryvalue)
            self.componentSaveBtnClicked()
            self.gpFlag[13] = 1
            return

        elif entryname == "PHASES":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ptext.setPlainText(entryvalue)
            self.phaseSaveBtnClicked()
            self.gpFlag[14] = 1
            return

        elif entryname == "GAMMA":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.gammaInput.setText(entryvalue)
            self.gpFlag[15] = 1
            return

        elif entryname == "DIFFUSIVITY":
            
            self.NextBtn3()
            self.gpFlag[16] = self.gpFlag[16] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")

            Diffdata = entryvalue.split(",")

            self.DiffusivityType[int(Diffdata[1])] = Diffdata[0]
            self.Diffusivity[int(Diffdata[1])] = ",".join(Diffdata[2:])


        elif entryname == "R":
            self.R_Value.setText(entryvalue)
            self.gpFlag[17] = 1

        elif entryname == "V":
            self.V_Value.setText(entryvalue)
            self.gpFlag[18] = 1

        elif entryname == "EIGEN_STRAIN":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ESdata = entryvalue.split(",")
            self.eigenStrain[int(ESdata[0])] = ",".join(ESdata[1:])
            self.gpFlag[19] = self.gpFlag[19] +1


        elif entryname == "VOIGT_ISOTROPIC":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ECdata = entryvalue.split(",")
            self.gpFlag[20] = self.gpFlag[20] +1

            self.elasticType[int(ECdata[0])] = "0"
            self.elasticConstant[int(ECdata[0])] = ",".join(ECdata[1:])


        elif entryname == "VOIGT_CUBIC":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ECdata = entryvalue.split(",")
            self.elasticType[int(ECdata[0])] = "1"
            self.elasticConstant[int(ECdata[0])] = ",".join(ECdata[1:])
            self.gpFlag[20] = self.gpFlag[20] +1

        elif entryname == "VOIGT_TETRAGONAL":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ECdata = entryvalue.split(",")
            self.elasticType[int(ECdata[0])] = "2"
            self.elasticConstant[int(ECdata[0])] = ",".join(ECdata[1:])
            self.gpFlag[20] = self.gpFlag[20] +1


        elif entryname == "BOUNDARY":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            BC_Cond = entryvalue.split(",")

            if BC_Cond[0] == "phi":
                self.pDropdown_2.setCurrentIndex(1)
                self.Bcnd[0] = ",".join(BC_Cond[1:5])
                self.gpFlag[21] = 1

            elif BC_Cond[0] == "mu":
                self.pDropdown_2.setCurrentIndex(2)
                self.Bcnd[1] = ",".join(BC_Cond[1:5])
                self.gpFlag[22] = 1

            elif BC_Cond[0] == "c":
                self.Bcnd[2] = ",".join(BC_Cond[1:5])
                self.gpFlag[22] = 1

            elif BC_Cond[0] == "T":
                self.Bcnd[3] = ",".join(BC_Cond[1:5])
                self.gpFlag[23] = 1

        elif entryname == "BOUNDARY_VALUE":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            BC_Cond = entryvalue.split(",")

            if BC_Cond[0] == "phi":
                self.BconV[0] = ",".join(BC_Cond[1:5])
                self.gpFlag[24] = 1

            elif BC_Cond[0] == "mu":
                self.BconV[1] = ",".join(BC_Cond[1:5])
                self.gpFlag[25] = 1

            elif BC_Cond[0] == "c":
                self.BconV[2] = ",".join(BC_Cond[1:5])
                self.gpFlag[25] = 1

            elif BC_Cond[0] == "T":
                self.BconV[3] = ",".join(BC_Cond[1:5])
                self.gpFlag[26] = 1


        self.pDropdown_2.setCurrentIndex(0)
        if self.DiffusivityType[0] == 1:
            self.diffR_2.setChecked(True)
        elif self.DiffusivityType[0] == 0:
            self.diffR.setChecked(True)

        self.diffInput.setText(self.Diffusivity[0])
        self.Estrain.setText( self.eigenStrain[0])
        self.Econstant.setText(self.elasticConstant[0])
        self.clickedBtn1()
        self.radio_GP.setChecked(True)

        ## Material Specific Parameter

        if entryname == "ISOTHERMAL":
            if int(entryvalue) == "1":
                self.thermalYGP.setChecked(True)
                self.thermalNGP.setChecked(False)

            elif entryvalue == "0":
                self.thermalYGP.setChecked(False)
                self.thermalNGP.setChecked(True)


        elif entryname == "BINARY" and entryvalue == "1":
            self.simTypeGP.setCurrentIndex(0)

        elif entryname == "TERNARY" and entryvalue == "1":
            self.simTypeGP.setCurrentIndex(1)

        elif entryname == "DILUTE" and entryvalue == "1":
            self.simTypeGP.setCurrentIndex(2)

        elif entryname == "T":
            self.TGP.setText(entryvalue)

        elif entryname == "WRITEFORMAT":
            if entryvalue =="ASCII":
                self.writeFormatGP.setCurrentIndex(0)
            elif entryvalue =="BINARY":
                self.writeFormatGP.setCurrentIndex(1)

        elif entryname == "WRITEHDF5":
            self.writehdfGP.setValue(int(entryvalue))

        elif entryname == "TRACK_PROGRESS":
            self.trackProgressGP.setText(entryvalue)

        elif entryname == "epsilon":
            self.epsilonGP.setText(entryvalue)

        elif entryname == "tau":
            self.tauGP.setText(entryvalue)

        elif entryname == "Tau":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.TauGP.setText(entryvalue)

        elif entryname == "Function_anisotropy":
            self.FanisotropyGP.setText(entryvalue)

        elif entryname == "Anisotropy_type":
            self.anisotropyTypeGP.setText(entryvalue)

        elif entryname == "dab":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.debGP.setText(entryvalue)

        elif entryname == "Function_W":
            self.funcWGP.setText(entryvalue)

        elif entryname == "Gamma_abc":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.gammaABCGP.setText(entryvalue)

        elif entryname == "Shift":
            self.shiftGP.setValue(int(entryvalue))

        elif entryname == "Shiftj":
            self.shiftJGP.setText(entryvalue)

        elif entryname == "Writecomposition":
            self.writecompGP.setText(entryvalue)


        elif entryname == "Noise_phasefield":
            self.noiseGP.setValue(int(entryvalue))

        elif entryname == "Amp_Noise_Phase":
            self.ampNoiseGP.setText(entryvalue)


        elif entryname == "Equilibrium_temperature":
            self.equTGP.setText(entryvalue)

        elif entryname == "Filling_temperature":
            self.fillingTGP.setText(entryvalue)

        elif entryname == "Tempgrady":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.tempgradyGP.setText(entryvalue)

        elif entryname == "Function_F":
            self.funcF.setValue(int(entryvalue))

        elif entryname == "A":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            Avalue = entryvalue.split(",")
            self.tableWidgetGPA.setItem(int(Avalue[0]),1, QTableWidgetItem(str(", ".join(Avalue[1:]))))
            
        elif entryname == "num_thermo_phases":
            self.num_thermo_phases.setValue(int(entryvalue))
            
        elif entryname == "tdbfname":
            self.tdbfname.setText(entryvalue)
            
        elif entryname == "tdb_phases":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.tdbphases.setText(entryvalue)
        
        elif entryname == "phase_map":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.phasemap.setText(entryvalue)

        elif entryname == "ceq":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,2, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "cfill":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,3, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "slopes":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,4, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
                    
        elif entryname == "c_guess":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,5, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "Rotation_matrix":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,6, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))


    def fillGPCheck(self):
        self.errorListGP = []
        noP_value = self.noP.value()

        if self.trackProgressGP.text() == "":
            self.errorListGP.append("Track Progress  ")

        if self.epsilonGP.text() == "":
            self.errorListGP.append("Epsilon ")

        if self.tauGP.text() == "":
            self.errorListGP.append("tau ")

        if self.TauGP.text() == "":
            self.errorListGP.append("Tau")

        if len(self.TauGP.text().split(",")) != (noP_value * ((noP_value - 1) / 2)):
            self.errorListGP.append("Invalid tuple length of Tau")

        if self.FanisotropyGP.text() == "":
            self.errorListGP.append("Function Anisotropy")

        if self.anisotropyTypeGP.text() == "":
            self.errorListGP.append("Anisotropy Type")

        if self.debGP.text() == "":
            self.errorListGP.append("dab")
            return False

        if len(self.debGP.text().split(",")) != int(noP_value * ((noP_value - 1) / 2)):
            self.errorListGP.append("Invalid tuple length of dab")

        if self.funcWGP.text() == "":
            self.errorListGP.append("Function W")


        if len(self.gammaABCGP.text().split(",")) != int(noP_value * ((noP_value - 1)*(noP_value - 2) / 6)) and self.gammaABCGP.text() != "":
            self.errorListGP.append("Invalid length of Gamma_abc")

        if self.shiftGP.value() > 1:
            self.errorListGP.append("Shift")

        if self.shiftJGP.text() =="":
            self.errorListGP.append("Shift J")

        if self.equTGP.text() == "":
            self.errorListGP.append("Equilibrium Temperature")

        if self.fillingTGP.text() =="":
            self.errorListGP.append("Filling Temperature")

        if self.TGP.text() =="":
            self.errorListGP.append("Temperature")

        if self.tempgradyGP.text() == "":
            self.errorListGP.append("Tempgrady")

        if len(self.tempgradyGP.text().split(",")) != 5:
            self.errorListGP.append("Invalid tuple length of Tempgrady")

        if self.ampNoiseGP.text() =="" and self.noiseGP.value() == 1:
            self.errorListGP.append("Amp_Noise_Phase")

        if self.writecompGP.text() == "":
            self.errorListGP.append("Writecomposition")


    def fillEntryCH(self,entryname, entryvalue):
        #print(entryvalue)

        if entryname == "DIMENSION":
            self.dim.setValue(int(entryvalue))
            self.chFlag[0] = 1
            return

        elif entryname == "MESH_X":
            self.mesh_x.setText(entryvalue)
            self.chFlag[1] = 1
            return

        elif entryname == "MESH_Y":
            self.mesh_y.setText(entryvalue)
            self.chFlag[2] = 1
            return

        elif entryname == "MESH_Z":
            self.mesh_z.setText(entryvalue)
            self.chFlag[3] = 1
            return

        elif entryname == "DELTA_X":
            self.dx.setText(entryvalue)
            self.chFlag[4] = 1
            return

        elif entryname == "DELTA_Y":
            self.dy.setText(entryvalue)
            self.chFlag[5] = 1
            return

        elif entryname == "DELTA_Z":
            self.dz.setText(entryvalue)
            self.chFlag[6] = 1
            return

        elif entryname == "DELTA_t":
            self.dt.setText(entryvalue)
            self.chFlag[7] = 1
            return

        elif entryname == "NUMPHASES":
            self.noP.setValue(int(entryvalue))
            self.chFlag[8] = 1
            #self.updateNoP()
            return

        elif entryname == "NUMCOMPONENTS":
            self.noC.setValue(int(entryvalue))
            self.chFlag[9] = 1
            #self.updateNoC()
            return

        elif entryname == "NTIMESTEPS":
            self.timeSteps.setText(entryvalue)
            self.chFlag[10] = 1
            return

        elif entryname == "NSMOOTH":
            self.Nsmooth.setText(entryvalue)
            self.chFlag[11] = 1
            return

        elif entryname == "SAVET":
            self.saveAt.setText(entryvalue)
            self.chFlag[12] = 1
            return

        elif entryname == "RESTART":
            self.reStart.setValue(int(entryvalue))
            return
        
        elif entryname == "STARTTIME":
            self.startTime.setText(entryvalue)
            return

        elif entryname == "numworkers":
            self.numWorkers.setText(entryvalue)
            return


        elif entryname == "COMPONENTS":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ctext.setPlainText(entryvalue)
            self.chFlag[13] = 1
            return

        elif entryname == "PHASES":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ptext.setPlainText(entryvalue)
            self.chFlag[14] = 1
            return

        elif entryname == "R":
            self.R_Value.setText(entryvalue)
            self.chFlag[15] = 1
            return

        elif entryname == "V":
            self.V_Value.setText(entryvalue)
            self.chFlag[16] = 1
            return

        self.NextBtn3()

        for i in range(self.noP.value()):
            self.DiffusivityType[i] = "1"
            self.Diffusivity[i] =  "1"+ ",1"*(self.noP.value()-2)
            self.eigenStrain[i] = "0.01, 0.01, 0.0, 0.0, 0.0, 0.0"
            self.elasticType[i] = "0"
            self.elasticConstant[i] = "270, 187.5, 125.0"
        

        self.diffInput.setText("1")
        self.Estrain.setText( "0.01, 0.01, 0.0, 0.0, 0.0, 0.0")
        self.Econstant.setText("270, 187.5, 125.0")

        self.gammaInput.setText("1.0")
        self.clickedBtn1()
        self.radio_CH.setChecked(True)

        ## Material Specific Parameter
        for i in range(4):
            self.Bcnd[i] = "1,1,1,1"
            self.BconV[i] = "1,1,1,1"


        if entryname == "WRITEFORMAT":
            self.chFlag[17] = 1
            if entryvalue =="ASCII":
                self.writeFormatCH.setCurrentIndex(0)
            elif entryvalue =="BINARY":
                self.writeFormatCH.setCurrentIndex(1)

        elif entryname == "TRACK_PROGRESS":
            self.trackProgressCH.setText(entryvalue)
            self.chFlag[18] = 1

        elif entryname == "L_phi":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.lPhiCH.setText(entryvalue)
            self.chFlag[19] = 1

        elif entryname == "Kappa_phi":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.kappaPhiCH.setText(entryvalue)
            self.chFlag[20] = 1

        elif entryname == "Kappa_c":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.kappaCCH.setText(entryvalue)
            self.chFlag[21] = 1

        elif entryname == "A_fm":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.afmCH.setText(entryvalue)
            self.chFlag[22] = 1

        elif entryname == "B_fp":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.bfpCH.setText(entryvalue)
            self.chFlag[23] = 1

        elif entryname == "spinodal":
            self.spinodalCH.setValue(int(entryvalue))

        elif entryname == "tdbflag":
            self.tdbflagCH.setValue(int(entryvalue))

        elif entryname == "tdbfname":
            self.tdbfnameCH.setText(entryvalue)

        elif entryname == "AtomicMobility":
            self.chFlag[24] =self.chFlag[24] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace("\n","")
            AMvalue = entryvalue.split(",")
            if int(AMvalue[0]) == 1:
                self.tableWidgetCHA.setItem(int(AMvalue[1]),1, QTableWidgetItem(str("DM")))
            else:
                self.tableWidgetCHA.setItem(int(AMvalue[1]),1, QTableWidgetItem(str("FM")))
            self.tableWidgetCHA.setItem(int(AMvalue[1]),2, QTableWidgetItem(str(", ".join(AMvalue[2:]))))
            
        '''
        elif entryname == "ceq":
            self.chFlag[25] =self.chFlag[25] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetCH.item(i,0).text() == ceqvalue[0] and self.tableWidgetCH.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetCH.setItem(i,2, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "cfill":
            self.chFlag[25] =self.chFlag[25] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetCH.item(i,0).text() == ceqvalue[0] and self.tableWidgetCH.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetCH.setItem(i,3, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
                    
        '''
    def fillEntryKKS(self,entryname, entryvalue): # KKS CUDA
        #print(entryvalue)

        if entryname == "DIMENSION":
            self.dim.setValue(int(entryvalue))
            self.kksFlag[0] = 1
            return

        elif entryname == "MESH_X":
            self.mesh_x.setText(entryvalue)
            self.kksFlag[1] = 1
            return

        elif entryname == "MESH_Y":
            self.mesh_y.setText(entryvalue)
            self.kksFlag[2] = 1
            return

        elif entryname == "MESH_Z":
            self.mesh_z.setText(entryvalue)
            self.kksFlag[3] = 1
            return

        elif entryname == "DELTA_X":
            self.dx.setText(entryvalue)
            self.kksFlag[4] = 1
            return

        elif entryname == "DELTA_Y":
            self.dy.setText(entryvalue)
            self.kksFlag[5] = 1
            return

        elif entryname == "DELTA_Z":
            self.dz.setText(entryvalue)
            self.kksFlag[6] = 1
            return

        elif entryname == "DELTA_t":
            self.dt.setText(entryvalue)
            self.kksFlag[7] = 1
            return

        elif entryname == "NUMPHASES":
            self.noP.setValue(int(entryvalue))
            self.kksFlag[8] = 1
            return
            #self.updateNoP()

        elif entryname == "NUMCOMPONENTS":
            self.noC.setValue(int(entryvalue))
            self.kksFlag[9] = 1
            return
            #self.updateNoC()

        elif entryname == "NTIMESTEPS":
            self.timeSteps.setText(entryvalue)
            self.kksFlag[10] = 1
            return

        
        self.Nsmooth.setText("0")
        self.kksFlag[11] = 1
            

        if entryname == "SAVET":
            self.saveAt.setText(entryvalue)
            self.kksFlag[12] = 1
            return

        elif entryname == "RESTART":
            self.reStart.setValue(int(entryvalue))
            return
        
        elif entryname == "STARTTIME":
            self.startTime.setText(entryvalue)
            return

        elif entryname == "numworkers":
            self.numWorkers.setText(entryvalue)
            return


        elif entryname == "COMPONENTS":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ctext.setPlainText(entryvalue)
            self.kksFlag[13] = 1
            return

        elif entryname == "PHASES":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ptext.setPlainText(entryvalue)
            self.kksFlag[14] = 1
            return

        elif entryname == "GAMMA":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.gammaInput.setText(entryvalue)
            self.kksFlag[15] = 1
            return

        elif entryname == "DIFFUSIVITY":
            self.NextBtn3()
            self.kksFlag[16] = self.kksFlag[16] +  1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")

            Diffdata = entryvalue.split(",")

            self.DiffusivityType[int(Diffdata[1])] = Diffdata[0]
            self.Diffusivity[int(Diffdata[1])] = ",".join(Diffdata[2:])

        elif entryname == "R":
            self.R_Value.setText(entryvalue)
            self.kksFlag[17] = 1

        elif entryname == "V":
            self.V_Value.setText(entryvalue)
            self.kksFlag[18] = 1

        elif entryname == "EIGEN_STRAIN":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ESdata = entryvalue.split(",")
            self.eigenStrain[int(ESdata[0])] = ",".join(ESdata[1:])
            self.kksFlag[19] = self.kksFlag[19] + 1


        elif entryname == "VOIGT_ISOTROPIC":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ECdata = entryvalue.split(",")

            self.elasticType[int(ECdata[0])] = "0"
            self.elasticConstant[int(ECdata[0])] = ",".join(ECdata[1:])
            self.kksFlag[20] = self.kksFlag[20] + 1


        elif entryname == "VOIGT_CUBIC":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ECdata = entryvalue.split(",")
            self.elasticType[int(ECdata[0])] = "1"
            self.elasticConstant[int(ECdata[0])] = ",".join(ECdata[1:])
            self.kksFlag[20] = self.kksFlag[20] + 1


        elif entryname == "VOIGT_TETRAGONAL":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ECdata = entryvalue.split(",")
            self.elasticType[int(ECdata[0])] = "2"
            self.elasticConstant[int(ECdata[0])] = ",".join(ECdata[1:])
            self.kksFlag[20] = self.kksFlag[20] + 1


        elif entryname == "BOUNDARY":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            BC_Cond = entryvalue.split(",")

            if BC_Cond[0] == "phi":
                self.pDropdown_2.setCurrentIndex(1)
                self.Bcnd[0] = ",".join(BC_Cond[1:5])
                self.kksFlag[21] =  + 1

            elif BC_Cond[0] == "mu":
                self.pDropdown_2.setCurrentIndex(2)
                self.Bcnd[1] = ",".join(BC_Cond[1:5])
                self.kksFlag[22] = 1

            elif BC_Cond[0] == "c":
                self.Bcnd[2] = ",".join(BC_Cond[1:5])
                self.kksFlag[22] =  self.kksFlag[22] + 1

            elif BC_Cond[0] == "T":
                self.Bcnd[3] = ",".join(BC_Cond[1:5])
                self.kksFlag[23] = 1

        elif entryname == "BOUNDARY_VALUE":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            BC_Cond = entryvalue.split(",")

            if BC_Cond[0] == "phi":
                self.BconV[0] = ",".join(BC_Cond[1:5])
                self.kksFlag[24] =  1

            elif BC_Cond[0] == "mu":
                self.BconV[1] = ",".join(BC_Cond[1:5])
                self.kksFlag[25] =  1

            elif BC_Cond[0] == "c":
                self.BconV[2] = ",".join(BC_Cond[1:5])
                self.kksFlag[25] = self.kksFlag[25] + 1

            elif BC_Cond[0] == "T":
                self.BconV[3] = ",".join(BC_Cond[1:5])
                self.kksFlag[26] =  1


        self.pDropdown_2.setCurrentIndex(0)
        if self.DiffusivityType[0] == 1:
            self.diffR_2.setChecked(True)
        elif self.DiffusivityType[0] == 0:
            self.diffR.setChecked(True)
        
        
        self.diffInput.setText(self.Diffusivity[0])

        for i in range(self.noP.value()):
            self.eigenStrain[i] = "0.01, 0.01, 0.0, 0.0, 0.0, 0.0"
            self.elasticType[i] = "0"
            self.elasticConstant[i] = "270, 187.5, 125.0"
        self.Estrain.setText( "0.01, 0.01, 0.0, 0.0, 0.0, 0.0")     
        self.Econstant.setText("270, 187.5, 125.0")
        
        self.kksFlag[19] =  1
        self.kksFlag[20] =  1
        self.kksFlag[21] =  1
        self.kksFlag[22] =  1
        self.kksFlag[23] =  1
        self.kksFlag[24] =  1
        self.kksFlag[25] =  1
        self.kksFlag[26] =  1
        self.kksFlag[30] =  1
        self.kksFlag[32] =  1
        self.kksFlag[33] =  1


        self.clickedBtn1()
        self.radio_KKR.setChecked(True)
        

        ## Material Specific Parameter

        if entryname == "WRITEFORMAT":
            self.kksFlag[27] = 1
            if entryvalue =="ASCII":
                self.writeFormatKKS.setCurrentIndex(0)
            elif entryvalue =="BINARY":
                self.writeFormatKKS.setCurrentIndex(1)

        elif entryname == "TRACK_PROGRESS":
            self.trackprogressKKS.setText(entryvalue)
            self.kksFlag[28] = 1

        elif entryname == "T":
            self.temperatureKKS.setText(entryvalue)
            self.kksFlag[29] = 1


        elif entryname == "Equilibrium_temperature":
            self.equTKKS.setText(entryvalue)
            self.kksFlag[31] = 1
       
        elif entryname == "Tau":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.TauKKS.setText(entryvalue)
            self.kksFlag[34] = 1
            
        elif entryname == "epsilon":
            self.epsilonKKS.setText(entryvalue)
            self.kksFlag[35] = 1

        
            
        elif entryname == "Function_F":
            self.funcF.setValue(int(entryvalue))

        elif entryname == "A":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            Avalue = entryvalue.split(",")
            self.tableWidgetGPA.setItem(int(Avalue[0]),1, QTableWidgetItem(str(", ".join(Avalue[1:]))))
            
        elif entryname == "num_thermo_phases":
            self.num_thermo_phases.setValue(int(entryvalue))
            
        elif entryname == "tdbfname":
            self.tdbfname.setText(entryvalue)
            
        elif entryname == "tdb_phases":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.tdbphases.setText(entryvalue)
        
        elif entryname == "phase_map":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.phasemap.setText(entryvalue)

        elif entryname == "ceq":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,2, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "cfill":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,3, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "slopes":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,4, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
                    
        elif entryname == "c_guess":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,5, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "Rotation_matrix":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,6, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

       
            
        '''
        elif entryname == "ceq":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            self.kksFlag[37] = self.kksFlag[37] + 1
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetKKS.item(i,0).text() == ceqvalue[0] and self.tableWidgetKKS.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetKKS.setItem(i,2, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
                    
        '''

    def fillEntryKKS2(self,entryname, entryvalue):
        #print(entryvalue)
        self.kks2Flag[32] =  1

        if entryname == "DIMENSION":
            self.dim.setValue(int(entryvalue))
            self.kks2Flag[0] = 1
            return

        elif entryname == "MESH_X":
            self.mesh_x.setText(entryvalue)
            self.kks2Flag[1] = 1
            return

        elif entryname == "MESH_Y":
            self.mesh_y.setText(entryvalue)
            self.kks2Flag[2] = 1
            return

        elif entryname == "MESH_Z":
            self.mesh_z.setText(entryvalue)
            self.kks2Flag[3] = 1
            return

        elif entryname == "DELTA_X":
            self.dx.setText(entryvalue)
            self.kks2Flag[4] = 1
            return

        elif entryname == "DELTA_Y":
            self.dy.setText(entryvalue)
            self.kks2Flag[5] = 1
            return

        elif entryname == "DELTA_Z":
            self.dz.setText(entryvalue)
            self.kks2Flag[6] = 1
            return

        elif entryname == "DELTA_t":
            self.dt.setText(entryvalue)
            self.kks2Flag[7] = 1
            return

        elif entryname == "NUMPHASES":
            self.noP.setValue(int(entryvalue))
            self.kks2Flag[8] = 1
            return
            #self.updateNoP()

        elif entryname == "NUMCOMPONENTS":
            self.noC.setValue(int(entryvalue))
            self.kks2Flag[9] = 1
            return
            #self.updateNoC()

        elif entryname == "NTIMESTEPS":
            self.timeSteps.setText(entryvalue)
            self.kks2Flag[10] = 1
            return

        elif entryname == "NSMOOTH":
            self.Nsmooth.setText(entryvalue)
            self.kks2Flag[11] = 1
            return

        elif entryname == "SAVET":
            self.saveAt.setText(entryvalue)
            self.kks2Flag[12] = 1
            return

        elif entryname == "RESTART":
            self.reStart.setValue(int(entryvalue))
            return
        
        elif entryname == "STARTTIME":
            self.startTime.setText(entryvalue)
            return

        elif entryname == "numworkers":
            self.numWorkers.setText(entryvalue)
            return


        elif entryname == "COMPONENTS":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ctext.setPlainText(entryvalue)
            self.kks2Flag[13] = 1
            return

        elif entryname == "PHASES":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            entryvalue = entryvalue.replace(",","\n")
            self.ptext.setPlainText(entryvalue)
            self.kks2Flag[14] = 1
            return

        elif entryname == "GAMMA":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.gammaInput.setText(entryvalue)
            self.kks2Flag[15] = 1
            return

        elif entryname == "DIFFUSIVITY":
            self.NextBtn3()

            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")

            Diffdata = entryvalue.split(",")

            self.DiffusivityType[int(Diffdata[1])] = Diffdata[0]
            self.Diffusivity[int(Diffdata[1])] = ",".join(Diffdata[2:])
            self.kks2Flag[16] = self.kks2Flag[16] + 1

        elif entryname == "R":
            self.R_Value.setText(entryvalue)
            self.kks2Flag[17] = 1

        elif entryname == "V":
            self.V_Value.setText(entryvalue)
            self.kks2Flag[18] = 1


        elif entryname == "BOUNDARY":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            BC_Cond = entryvalue.split(",")

            if BC_Cond[0] == "phi":
                self.pDropdown_2.setCurrentIndex(1)
                self.Bcnd[0] = ",".join(BC_Cond[1:5])
                self.kks2Flag[19] =  1

            elif BC_Cond[0] == "mu":
                self.pDropdown_2.setCurrentIndex(2)
                self.Bcnd[1] = ",".join(BC_Cond[1:5])
                self.kks2Flag[20] =  1

            elif BC_Cond[0] == "c":
                self.Bcnd[2] = ",".join(BC_Cond[1:5])
                self.kks2Flag[20] =  1

            elif BC_Cond[0] == "T":
                self.Bcnd[3] = ",".join(BC_Cond[1:5])
                self.kks2Flag[21] =  1

        elif entryname == "BOUNDARY_VALUE":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            BC_Cond = entryvalue.split(",")

            if BC_Cond[0] == "phi":
                self.BconV[0] = ",".join(BC_Cond[1:5])
                self.kks2Flag[22] =  1

            elif BC_Cond[0] == "mu":
                self.BconV[1] = ",".join(BC_Cond[1:5])
                self.kks2Flag[23] =  1

            elif BC_Cond[0] == "c":
                self.BconV[2] = ",".join(BC_Cond[1:5])
                self.kks2Flag[23] =  1

            elif BC_Cond[0] == "T":
                self.BconV[3] = ",".join(BC_Cond[1:5])
                self.kks2Flag[24] =  1


        self.pDropdown_2.setCurrentIndex(0)
        if self.DiffusivityType[0] == 1:
            self.diffR_2.setChecked(True)
        elif self.DiffusivityType[0] == 0:
            self.diffR.setChecked(True)

        self.diffInput.setText(self.Diffusivity[0])

        for i in range(self.noP.value()):
            self.eigenStrain[i] = "0.01, 0.01, 0.0, 0.0, 0.0, 0.0"
            self.elasticType[i] = "0"
            self.elasticConstant[i] = "270, 187.5, 125.0"
        self.Estrain.setText( "0.01, 0.01, 0.0, 0.0, 0.0, 0.0")
        self.Econstant.setText("270, 187.5, 125.0")

        self.clickedBtn1()
        self.radio_KKS2.setChecked(True)

        ## Material Specific Parameter

        if entryname == "ISOTHERMAL":
            self.kks2Flag[25] =  1
            if int(entryvalue) == 1:
                self.thermalYKKS2.setChecked(True)
                self.thermalNKKS2.setChecked(False)
            else:
                self.thermalNKKS2.setChecked(True)
                self.thermalYKKS2.setChecked(False)

        elif entryname == "BINARY" and entryvalue == "1":
            self.simTypeKKS2.setCurrentIndex(0)
            self.kks2Flag[26] =  1

        elif entryname == "TERNARY" and entryvalue == "1":
            self.simTypeKKS2.setCurrentIndex(1)
            self.kks2Flag[26] =  1

        elif entryname == "DILUTE" and entryvalue == "1":
            self.simTypeKKS2.setCurrentIndex(2)
            self.kks2Flag[26] =  1

        elif entryname == "WRITEFORMAT":
            self.kks2Flag[27] =  1
            if entryvalue =="ASCII":
                self.writeFormatKKS2.setCurrentIndex(0)

            elif entryvalue =="BINARY":
                self.writeFormatKKS2.setCurrentIndex(1)

        elif entryname == "TRACK_PROGRESS":
            self.trackProgressKKS2.setText(entryvalue)
            self.kks2Flag[28] =  1

        elif entryname == "epsilon":
            self.epsilonKKS2.setText(entryvalue)
            self.kks2Flag[29] =  1

        elif entryname == "Function_anisotropy":
            self.FanisotropyKKS2.setText(entryvalue)
            self.kks2Flag[30] =  1

        elif entryname == "dab":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.debKKS2.setText(entryvalue)
            self.kks2Flag[31] =  1

        elif entryname == "T":
            self.temperatureKKS2.setText(entryvalue)
            self.kks2Flag[32] =  1

        elif entryname == "Noise_phasefield":
            self.noiseKKS2.setValue(int(entryvalue))
            self.kks2Flag[33] =  1

        elif entryname == "Amp_Noise_Phase":
            self.ampNoiseKKS2.setText(entryvalue)
            self.kks2Flag[34] =  1

        elif entryname == "Tempgrady":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.tempGradyKKS2.setText(entryvalue)
            self.kks2Flag[35] =  1

        elif entryname == "tNoiseStart":
            self.tNoiseStartKKS2.setText(entryvalue)
            self.kks2Flag[36] =  1

        elif entryname == "Equilibrium_temperature":
            self.TLKKS2.setText(entryvalue)
            self.kks2Flag[37] =  1

        elif entryname == "atr":
            self.atrKKS2.setText(entryvalue)
            self.kks2Flag[38] =  1

        elif entryname == "CLplatformID":
            self.CLPidKKS2.setText(entryvalue)
            self.kks2Flag[39] =  1

        elif entryname == "CLdeviceID":
            self.CLDidKKS2.setText(entryvalue)
            self.kks2Flag[40] =  1         
            
        elif entryname == "Shift":
            self.shiftKKS2.setValue(int(entryvalue))
            self.kks2Flag[41] =  1

        elif entryname == "Shiftj":
            self.ShiftJKKS2.setText(entryvalue)
            self.kks2Flag[42] =  1
            
        elif entryname == "Filling_temperature":
            self.fillingTKKS.setText(entryvalue)
            self.kks2Flag[43] =  1
            
        elif entryname == "Function_F":
            self.funcF.setValue(int(entryvalue))

        elif entryname == "A":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            Avalue = entryvalue.split(",")
            self.tableWidgetGPA.setItem(int(Avalue[0]),1, QTableWidgetItem(str(", ".join(Avalue[1:]))))
            
        elif entryname == "num_thermo_phases":
            self.num_thermo_phases.setValue(int(entryvalue))
            
        elif entryname == "tdbfname":
            self.tdbfname.setText(entryvalue)
            
        elif entryname == "tdb_phases":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.tdbphases.setText(entryvalue)
        
        elif entryname == "phase_map":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            self.phasemap.setText(entryvalue)

        elif entryname == "ceq":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,2, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "cfill":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,3, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "slopes":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,4, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
                    
        elif entryname == "c_guess":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,5, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))

        elif entryname == "Rotation_matrix":
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetGP.item(i,0).text() == ceqvalue[0] and self.tableWidgetGP.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetGP.setItem(i,6, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))


        
'''
        elif entryname == "ceq":
            self.kks2Flag[42] =  self.kks2Flag[42] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetKKS2.item(i,0).text() == ceqvalue[0] and self.tableWidgetKKS2.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetKKS2.setItem(i,2, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
        elif entryname == "cfill":
            self.kks2Flag[43] =  self.kks2Flag[43] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetKKS2.item(i,0).text() == ceqvalue[0] and self.tableWidgetKKS2.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetKKS2.setItem(i,3, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))


        elif entryname == "Rotation_matrix":
            self.kks2Flag[44] =  self.kks2Flag[44] + 1
            entryvalue = entryvalue.replace("{","")
            entryvalue = entryvalue.replace("}","")
            ceqvalue = entryvalue.split(",")
            k=self.noP.value()

            for i in range(k*k):
                if self.tableWidgetKKS2.item(i,0).text() == ceqvalue[0] and self.tableWidgetKKS2.item(i,1).text() == ceqvalue[1]:
                    self.tableWidgetKKS2.setItem(i,4, QTableWidgetItem(str( ", ".join(ceqvalue[2:]))))
'''
#main

app = QApplication(sys.argv)

screen_resolution = app.desktop().screenGeometry()
width, height = screen_resolution.width(), screen_resolution.height()

dir_ = QtCore.QDir("Ubuntu")
QtGui.QFontDatabase.addApplicationFont("resources/font/Ubuntu-Bold.ttf")
QtGui.QFontDatabase.addApplicationFont("resources/font/Ubuntu-Regular.ttf")
mainScreen = StartScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainScreen)
widget.setFixedHeight(650)
widget.setFixedWidth(1100)
widget.setWindowTitle("MicroSim - Microstructure Simulator")
widget.setWindowIcon(QtGui.QIcon('resources/img/Mlogo.png'))
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
