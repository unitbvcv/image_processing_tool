from PyQt5 import QtCore, QtGui, QtWidgets

import Application.Settings
import Application.Utils.ZoomOperations
from Application.Views.MainWindowImageLabel import MainWindowImageLabel


class MainWindowView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._setupUi()
        self._setupImageLabels()
        self._setupMenuCornerWidget()
        self._setupZoomFunctionality()

        # synchronize the scrollbars of the scrollAreas
        self.scrollAreaOriginalImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.horizontalScrollBar().setValue)
        self.scrollAreaProcessedImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.horizontalScrollBar().setValue)

        self.scrollAreaOriginalImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.verticalScrollBar().setValue)
        self.scrollAreaProcessedImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.verticalScrollBar().setValue)

        # connect signals to slots
        self.labelOriginalImage.mouse_leaved.connect(self._mouseLeavedEvent)
        self.labelProcessedImage.mouse_leaved.connect(self._mouseLeavedEvent)
        self.labelOriginalImage.finished_painting.connect(self._labelFinishedPaintingEvent)
        self.labelProcessedImage.finished_painting.connect(self._labelFinishedPaintingEvent)

        # define necessary data for menu API
        self._menusDictionary = {
            "menuFile": self.menuFile,
            "menuTools": self.menuTools
        }

        self._menuActionsDictionary = {
            "actionLoadGrayscaleImage": self.actionLoadGrayscaleImage,
            "actionLoadColorImage": self.actionLoadColorImage,
            "actionSaveProcessedImage": self.actionSaveProcessedImage,
            "actionExit": self.actionExit,
            "actionMagnifier": self.actionMagnifier,
            "actionPlotter": self.actionPlotter,
            "actionInvert": self.actionInvert
        }

# region WINDOW SET UP

    def _setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1024, 768)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayoutImages = QtWidgets.QHBoxLayout()
        self.horizontalLayoutImages.setSpacing(6)
        self.horizontalLayoutImages.setObjectName("horizontalLayoutImages")
        self.groupBoxOriginalImage = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxOriginalImage.sizePolicy().hasHeightForWidth())
        self.groupBoxOriginalImage.setSizePolicy(sizePolicy)
        self.groupBoxOriginalImage.setObjectName("groupBoxOriginalImage")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBoxOriginalImage)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollAreaOriginalImage = QtWidgets.QScrollArea(self.groupBoxOriginalImage)
        self.scrollAreaOriginalImage.setStyleSheet("")
        self.scrollAreaOriginalImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaOriginalImage.setWidgetResizable(True)
        self.scrollAreaOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaOriginalImage.setObjectName("scrollAreaOriginalImage")
        self.scrollAreaWidgetOriginalImage = QtWidgets.QWidget()
        self.scrollAreaWidgetOriginalImage.setGeometry(QtCore.QRect(0, 0, 471, 568))
        self.scrollAreaWidgetOriginalImage.setObjectName("scrollAreaWidgetOriginalImage")
        self.scrollAreaOriginalImage.setWidget(self.scrollAreaWidgetOriginalImage)
        self.horizontalLayout.addWidget(self.scrollAreaOriginalImage)
        self.horizontalLayoutImages.addWidget(self.groupBoxOriginalImage)
        self.groupBoxProcessedImage = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxProcessedImage.sizePolicy().hasHeightForWidth())
        self.groupBoxProcessedImage.setSizePolicy(sizePolicy)
        self.groupBoxProcessedImage.setObjectName("groupBoxProcessedImage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxProcessedImage)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollAreaProcessedImage = QtWidgets.QScrollArea(self.groupBoxProcessedImage)
        self.scrollAreaProcessedImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaProcessedImage.setWidgetResizable(True)
        self.scrollAreaProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaProcessedImage.setObjectName("scrollAreaProcessedImage")
        self.scrollAreaWidgetProcessedImage = QtWidgets.QWidget()
        self.scrollAreaWidgetProcessedImage.setGeometry(QtCore.QRect(0, 0, 470, 568))
        self.scrollAreaWidgetProcessedImage.setObjectName("scrollAreaWidgetProcessedImage")
        self.scrollAreaProcessedImage.setWidget(self.scrollAreaWidgetProcessedImage)
        self.horizontalLayout_2.addWidget(self.scrollAreaProcessedImage)
        self.horizontalLayoutImages.addWidget(self.groupBoxProcessedImage)
        self.verticalLayout.addLayout(self.horizontalLayoutImages)
        self.horizontalLayoutZoom = QtWidgets.QHBoxLayout()
        self.horizontalLayoutZoom.setSpacing(6)
        self.horizontalLayoutZoom.setObjectName("horizontalLayoutZoom")
        self.buttonResetZoom = QtWidgets.QPushButton(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonResetZoom.sizePolicy().hasHeightForWidth())
        self.buttonResetZoom.setSizePolicy(sizePolicy)
        self.buttonResetZoom.setMinimumSize(QtCore.QSize(0, 33))
        self.buttonResetZoom.setObjectName("buttonResetZoom")
        self.horizontalLayoutZoom.addWidget(self.buttonResetZoom)
        self.horizontalSliderZoom = QtWidgets.QSlider(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSliderZoom.sizePolicy().hasHeightForWidth())
        self.horizontalSliderZoom.setSizePolicy(sizePolicy)
        self.horizontalSliderZoom.setMinimumSize(QtCore.QSize(0, 33))
        self.horizontalSliderZoom.setMaximum(1)
        self.horizontalSliderZoom.setSingleStep(1)
        self.horizontalSliderZoom.setPageStep(1)
        self.horizontalSliderZoom.setProperty("value", 1)
        self.horizontalSliderZoom.setSliderPosition(1)
        self.horizontalSliderZoom.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderZoom.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSliderZoom.setTickInterval(1)
        self.horizontalSliderZoom.setObjectName("horizontalSliderZoom")
        self.horizontalLayoutZoom.addWidget(self.horizontalSliderZoom)
        self.labelZoomFactor = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelZoomFactor.sizePolicy().hasHeightForWidth())
        self.labelZoomFactor.setSizePolicy(sizePolicy)
        self.labelZoomFactor.setMinimumSize(QtCore.QSize(0, 33))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelZoomFactor.setFont(font)
        self.labelZoomFactor.setObjectName("labelZoomFactor")
        self.horizontalLayoutZoom.addWidget(self.labelZoomFactor)
        self.verticalLayout.addLayout(self.horizontalLayoutZoom)
        self.gridLayoutMouseLabels = QtWidgets.QGridLayout()
        self.gridLayoutMouseLabels.setSpacing(6)
        self.gridLayoutMouseLabels.setObjectName("gridLayoutMouseLabels")
        self.labelOriginalImagePixelValue = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOriginalImagePixelValue.sizePolicy().hasHeightForWidth())
        self.labelOriginalImagePixelValue.setSizePolicy(sizePolicy)
        self.labelOriginalImagePixelValue.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelOriginalImagePixelValue.setFont(font)
        self.labelOriginalImagePixelValue.setText("")
        self.labelOriginalImagePixelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOriginalImagePixelValue.setObjectName("labelOriginalImagePixelValue")
        self.gridLayoutMouseLabels.addWidget(self.labelOriginalImagePixelValue, 0, 0, 1, 1)
        self.labelProcessedImagePixelValue = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProcessedImagePixelValue.sizePolicy().hasHeightForWidth())
        self.labelProcessedImagePixelValue.setSizePolicy(sizePolicy)
        self.labelProcessedImagePixelValue.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelProcessedImagePixelValue.setFont(font)
        self.labelProcessedImagePixelValue.setText("")
        self.labelProcessedImagePixelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelProcessedImagePixelValue.setObjectName("labelProcessedImagePixelValue")
        self.gridLayoutMouseLabels.addWidget(self.labelProcessedImagePixelValue, 0, 1, 1, 1)
        self.labelMousePosition = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMousePosition.sizePolicy().hasHeightForWidth())
        self.labelMousePosition.setSizePolicy(sizePolicy)
        self.labelMousePosition.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelMousePosition.setFont(font)
        self.labelMousePosition.setText("")
        self.labelMousePosition.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMousePosition.setObjectName("labelMousePosition")
        self.gridLayoutMouseLabels.addWidget(self.labelMousePosition, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayoutMouseLabels)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.setMenuBar(self.menuBar)
        self.actionLoadGrayscaleImage = QtWidgets.QAction(self)
        self.actionLoadGrayscaleImage.setObjectName("actionLoadGrayscaleImage")
        self.actionLoadColorImage = QtWidgets.QAction(self)
        self.actionLoadColorImage.setObjectName("actionLoadColorImage")
        self.actionSaveProcessedImage = QtWidgets.QAction(self)
        self.actionSaveProcessedImage.setObjectName("actionSaveProcessedImage")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionMagnifier = QtWidgets.QAction(self)
        self.actionMagnifier.setObjectName("actionMagnifier")
        self.actionPlotter = QtWidgets.QAction(self)
        self.actionPlotter.setObjectName("actionPlotter")
        self.actionInvert = QtWidgets.QAction(self)
        self.actionInvert.setObjectName("actionInvert")
        self.menuFile.addAction(self.actionLoadGrayscaleImage)
        self.menuFile.addAction(self.actionLoadColorImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveProcessedImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionMagnifier)
        self.menuTools.addAction(self.actionPlotter)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Image Processing Tool"))
        self.groupBoxOriginalImage.setTitle(_translate("MainWindow", "Original image"))
        self.groupBoxProcessedImage.setTitle(_translate("MainWindow", "Processed image"))
        self.buttonResetZoom.setText(_translate("MainWindow", "Reset"))
        self.labelZoomFactor.setText(_translate("MainWindow", "1.00x"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionLoadGrayscaleImage.setText(_translate("MainWindow", "Load grayscale image"))
        self.actionLoadColorImage.setText(_translate("MainWindow", "Load color image"))
        self.actionSaveProcessedImage.setText(_translate("MainWindow", "Save processed image"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionMagnifier.setText(_translate("MainWindow", "Magnifier"))
        self.actionPlotter.setText(_translate("MainWindow", "Plotter"))

    def _setupImageLabels(self):
        self.stackedLayoutOriginalImage = QtWidgets.QStackedLayout(self.scrollAreaWidgetOriginalImage)
        self.stackedLayoutProcessedImage = QtWidgets.QStackedLayout(self.scrollAreaWidgetProcessedImage)

        self.labelOriginalImage = MainWindowImageLabel(self.scrollAreaWidgetOriginalImage)
        self.labelOriginalImage.setMouseTracking(True)
        self.labelOriginalImage.setText("")
        self.labelOriginalImage.setScaledContents(False)
        self.labelOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelOriginalImage.setObjectName("labelOriginalImage")
        self.labelOriginalImage.setGeometry(0, 0, 0, 0)

        self.labelProcessedImage = MainWindowImageLabel(self.scrollAreaWidgetProcessedImage)
        self.labelProcessedImage.setMouseTracking(True)
        self.labelProcessedImage.setText("")
        self.labelProcessedImage.setScaledContents(False)
        self.labelProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelProcessedImage.setObjectName("labelProcessedImage")
        self.labelProcessedImage.setGeometry(0, 0, 0, 0)

        self.stackedLayoutOriginalImage.addWidget(self.labelOriginalImage)
        self.stackedLayoutProcessedImage.addWidget(self.labelProcessedImage)

    def _setupMenuCornerWidget(self):
        self.rightMenuBar = QtWidgets.QMenuBar()
        self.menuBar.setCornerWidget(self.rightMenuBar)
        self.actionSaveAsOriginalImage = QtWidgets.QAction(self)
        self.actionSaveAsOriginalImage.setObjectName("actionSaveAsOriginalImage")
        self.rightMenuBar.addAction(self.actionSaveAsOriginalImage)

        _translate = QtCore.QCoreApplication.translate
        self.actionSaveAsOriginalImage.setText(_translate("MainWindow", "Save as original image"))

    def _setupZoomFunctionality(self):
        # connect the zoom option
        self.horizontalSliderZoom.setMinimum(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomMinimumValue))
        self.horizontalSliderZoom.setMaximum(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomMaximumValue))
        self.horizontalSliderZoom.setSingleStep(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomSingleStep))
        self.horizontalSliderZoom.setPageStep(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomPageStep))
        self.horizontalSliderZoom.setTickInterval(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.ticksInterval)
        )

        self._zoom = Application.Settings.MainWindowSettings.zoomDefaultValue
        self.horizontalSliderZoom.setValue(Application.Utils.ZoomOperations.calculateSliderValueFromZoom(self._zoom))
        self.horizontalSliderZoom.valueChanged.connect(self._zoomValueChangedEvent)
        self.buttonResetZoom.pressed.connect(self._zoomValueResetEvent)

# endregion

# region MENU API
# TODO: make it possible to add submenus
    def addMenu(self, menuName, beforeMenuName=None):
        """
        Adds a QMenu to the top menu bar with the name and objectName menuName to the left of beforeMenuName.
        If it already exists, it does nothing.
        If beforeMenuName is None, it appends the menu.
        :param menuName: string
        :param beforeMenuName: string; default value: None
        :return: None
        """

        if menuName not in self._menusDictionary:
            beforeMenuAction = None
            if beforeMenuName is not None \
                    and beforeMenuName in self._menusDictionary:
                beforeMenuAction = self._menusDictionary[beforeMenuName].menuAction()
            menu = QtWidgets.QMenu(self.menuBar)
            menu.setObjectName(menuName)
            menu.setTitle(QtCore.QCoreApplication.translate("MainWindow", menuName))
            self.menuBar.insertAction(beforeMenuAction, menu.menuAction())
            self._menusDictionary[menuName] = menu

    def addMenuAction(self, menuName, actionName, beforeActionName=None):
        """
        Adds a QAction to the top menuName with the name and objectName actionName [before beforeActionName].
        If it already exists or the menuName doesn't exist, it does nothing.
        If beforeActionName is not found, it appends the new action.
        :param menuName: string
        :param actionName: string
        :param beforeActionName: string; default value: None
        :return: None
        """
        if menuName in self._menusDictionary \
                and actionName not in self._menuActionsDictionary:
            beforeAction = None
            if beforeActionName in self._menuActionsDictionary:
                beforeAction = self._menuActionsDictionary[beforeActionName]
            action = QtWidgets.QAction(self)
            action.setObjectName(actionName)
            action.setText(QtCore.QCoreApplication.translate("MainWindow", actionName))
            self._menusDictionary[menuName].insertAction(beforeAction, action)
            self._menuActionsDictionary[actionName] = action

    def addMenuSeparator(self, menuName, beforeActionName=None):
        """
        Adds a separator in the menuName [before beforeActionName].
        It does nothing if the menuName is not found.
        If beforeActionName is not found, it appends the new action.
        :param menuName: string
        :param beforeActionName: string; default value: None
        :return: None
        """
        if menuName in self._menusDictionary:
            beforeAction = None
            if beforeActionName is not None:
                beforeAction = self._menuActionsDictionary[beforeActionName]
            self._menusDictionary[menuName].insertSeparator(beforeAction)

# endregion

    def _mouseLeavedEvent(self, QEvent):
        self.labelMousePosition.setText('')
        self.labelOriginalImagePixelValue.setText('')
        self.labelProcessedImagePixelValue.setText('')

    def _labelFinishedPaintingEvent(self):
        # here we can synchronize scrollbars, after the paint event has finished
        # before paint event, the scrollbars don't exist
        self.scrollAreaProcessedImage.horizontalScrollBar().setValue(
            self.scrollAreaOriginalImage.horizontalScrollBar().value())

        self.scrollAreaProcessedImage.verticalScrollBar().setValue(
            self.scrollAreaOriginalImage.verticalScrollBar().value())

    def closeEvent(self, QCloseEvent):
        QtCore.QCoreApplication.quit()

# region ZOOM FUNCTIONALITY

    def _zoomValueResetEvent(self):
        sliderValue = Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
            Application.Settings.MainWindowSettings.zoomDefaultValue)
        self.horizontalSliderZoom.setValue(sliderValue)
        self._zoomValueChangedEvent(sliderValue)

    def _zoomValueChangedEvent(self, value):
        self._zoom = Application.Utils.ZoomOperations.calculateZoomFromSliderValue(value)
        self.labelZoomFactor.setText(f"{self._zoom:.2f}x")
        self._setZoom()

    def _setZoom(self):
        self.labelOriginalImage.setZoom(self._zoom)
        self.labelProcessedImage.setZoom(self._zoom)

# endregion
