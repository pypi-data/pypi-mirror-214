try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    ISPYSIDE1 = True
except: raise ImportError('Cannot load PySide1.')
try: import nt
except: raise Exception('Windows, ReactOS or Wine is required.')
import sys
import ctypes
try: import winreg
except: import _winreg as winreg
from ctypes.wintypes import MSG, POINT, RECT


__all__ = ['CustomizedWindow', 'BlurWindow']


user32 = ctypes.windll.user32
libc = ctypes.cdll.msvcrt


class LOGFONT(ctypes.Structure):
    _fields_ = [
    ('lfHeight', ctypes.c_long),
    ('lfWidth', ctypes.c_long),
    ('lfEscapement', ctypes.c_long),
    ('lfOrientation', ctypes.c_long),
    ('lfWeight', ctypes.c_long),
    ('lfItalic', ctypes.c_byte),
    ('lfUnderline', ctypes.c_byte),
    ('lfStrikeOut', ctypes.c_byte),
    ('lfCharSet', ctypes.c_byte),
    ('lfOutPrecision', ctypes.c_byte),
    ('lfClipPrecision', ctypes.c_byte),
    ('lfQuality', ctypes.c_byte),
    ('lfPitchAndFamily', ctypes.c_byte),
    ('lfFaceName', ctypes.c_wchar * 32)]


class NONCLIENTMETRICS(ctypes.Structure):
    _fields_ = [
    ('cbSize', ctypes.c_ulong),
    ('iBorderWidth', ctypes.c_int),
    ('iScrollWidth', ctypes.c_int),
    ('iScrollHeight', ctypes.c_int),
    ('iCaptionWidth', ctypes.c_int),
    ('iCaptionHeight', ctypes.c_int),
    ('lfCaptionFont', LOGFONT),
    ('iSmCaptionWidth', ctypes.c_int),
    ('iSmCaptionHeight', ctypes.c_int),
    ('lfSmCaptionFont', LOGFONT),
    ('iMenuWidth', ctypes.c_int),
    ('iMenuHeight', ctypes.c_int),
    ('lfMenuFont', LOGFONT),
    ('lfStatusFont', LOGFONT),
    ('lfMessageFont', LOGFONT),
    ('iPaddedBorderWidth', ctypes.c_int),]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [('rgrc', RECT * 3), ('lppos', ctypes.POINTER(ctypes.c_void_p))]


class WindowCompositionAttribute(ctypes.Structure):
    _fields_ = [('Attribute', ctypes.c_int), ('Data', ctypes.POINTER(ctypes.c_int)), ('SizeOfData', ctypes.c_size_t)]


class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [('AccentState', ctypes.c_uint), ('AccentFlags', ctypes.c_uint), ('GradientColor', ctypes.c_uint),
        ('AnimationId', ctypes.c_uint)]


class DWM_BLURBEHIND(ctypes.Structure):
    _fields_ = [('dwFlags', ctypes.c_ulong), ('fEnable', ctypes.c_long), ('hRgnBlur', ctypes.c_void_p), ('fTransitionOnMaximized', ctypes.c_long)]


class MARGINS(ctypes.Structure):
    _fields_ = [('cxLeftWidth', ctypes.c_int), ('cxRightWidth', ctypes.c_int), ('cyTopHeight', ctypes.c_int), ('cyBottomHeight', ctypes.c_int)]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [('Attribute', ctypes.c_ulong), ('Data', ctypes.POINTER(ACCENT_POLICY)), ('SizeOfData', ctypes.c_ulong)]


class Win10BlurEffect:
    def __init__(self):
        self.WCA_ACCENT_POLICY, self.ACCENT_ENABLE_BLURBEHIND, self.ACCENT_ENABLE_ACRYLICBLURBEHIND = 19, 3, 4
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = self.WCA_ACCENT_POLICY
        self.winCompAttrData.SizeOfData = ctypes.sizeof(self.accentPolicy)
        self.winCompAttrData.Data = ctypes.pointer(self.accentPolicy)
    def setAeroEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        gradientColor = ctypes.c_ulong(int(gradientColor, base=16))
        animationId = ctypes.c_ulong(animationId)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100 | 0x200) if isEnableShadow else ctypes.c_ulong(0)
        self.accentPolicy.AccentState = self.ACCENT_ENABLE_BLURBEHIND
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        code = user32.SetWindowCompositionAttribute(hWnd, ctypes.byref(self.winCompAttrData))
        return code
    def setAcrylicEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        gradientColor = ctypes.c_ulong(int(gradientColor, base=16))
        animationId = ctypes.c_ulong(animationId)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100) if isEnableShadow else ctypes.c_ulong(0)
        self.accentPolicy.AccentState = self.ACCENT_ENABLE_ACRYLICBLURBEHIND
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        code = user32.SetWindowCompositionAttribute(hWnd, ctypes.byref(self.winCompAttrData))
        return code


class MenuButton(QAbstractButton):
    def __init__(self, parent):
        super(MenuButton, self).__init__(parent)
        self.isminsizebutton, self.ismaxsizebutton, self.isclosebutton = map(isinstance, [self] * 3, [MinSizeButton, MaxSizeButton, CloseButton])
        self.parent = parent
        self.setFixedSize(parent._CustomizedWindow__menubutton_w, parent._CustomizedWindow__title_h)
        self.setFocusPolicy(Qt.NoFocus)
        self.bgcolour = Qt.transparent
    def paintEvent(self, *args):
        w, h = self.width(), self.height()
        parent = self.parent
        self.setFixedSize(parent._CustomizedWindow__menubutton_w, parent._CustomizedWindow__title_h)
        dpi, realdpi = parent.dpi(), parent.realdpi()
        isdarktheme = parent.isDarkTheme()
        isactivewindow = parent.isActiveWindow()
        ismaximized = user32.IsZoomed(parent.hwnd())
        resizable_h, resizable_v = parent._CustomizedWindow__resizable_h, parent._CustomizedWindow__resizable_v
        resizable_hv = resizable_h and resizable_v
        painter, path = QPainter(self), QPainterPath()
        painter.setBrush(self.bgcolour)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        painter.setBrush(Qt.NoBrush)
        isdisabledmaxsizebutton = self.ismaxsizebutton and not(resizable_h or resizable_v)
        if isdarktheme: pen = QPen(Qt.white if isactivewindow and not isdisabledmaxsizebutton else QColor(*[155] * 3))
        else: pen = QPen(Qt.black if isactivewindow and not isdisabledmaxsizebutton else QColor(*[99] * 3))
        penwidth = int(1.35 * dpi / 96.0)
        pen.setWidth(penwidth)
        painter.setPen(pen)
        if realdpi >= 143: painter.setRenderHint(QPainter.Antialiasing)
        if self.isminsizebutton:
            path.moveTo(int(0.391 * w), int(0.500 * h))
            path.lineTo(int(0.609 * w), int(0.500 * h))
        elif self.ismaxsizebutton:
            if ismaximized:
                path.moveTo(int(0.402 * w), int(0.406 * h))
                path.lineTo(int(0.559 * w), int(0.406 * h))
                path.lineTo(int(0.559 * w), int(0.656 * h))
                path.lineTo(int(0.402 * w), int(0.656 * h))
                path.lineTo(int(0.402 * w), int(0.406 * h))
                path.moveTo(int(0.441 * w), int(0.344 * h))
                path.lineTo(int(0.598 * w), int(0.344 * h))
                path.lineTo(int(0.598 * w), int(0.594 * h))
            else:
                path.moveTo(int(0.402 * w), int(0.344 * h))
                path.lineTo(int(0.598 * w), int(0.344 * h))
                path.lineTo(int(0.598 * w), int(0.656 * h))
                path.lineTo(int(0.402 * w), int(0.656 * h))
                path.lineTo(int(0.402 * w), int(0.344 * h))
        elif self.isclosebutton:
            path.moveTo(int(0.402 * w), int(0.344 * h))
            path.lineTo(int(0.598 * w), int(0.656 * h))
            path.moveTo(int(0.598 * w), int(0.344 * h))
            path.lineTo(int(0.402 * w), int(0.656 * h))
        painter.drawPath(path)


class MinSizeButton(MenuButton):
    def __init__(self, *args):
        super(MinSizeButton, self).__init__(*args)


class MaxSizeButton(MenuButton):
    def __init__(self, *args):
        super(MaxSizeButton, self).__init__(*args)


class CloseButton(MenuButton):
    def __init__(self, *args):
        super(CloseButton, self).__init__(*args)


class SystemVBoxLayout(QVBoxLayout):
    def __init__(self, parent):
        super(SystemVBoxLayout, self).__init__()
        self.setContentsMargins(*[0] * 4)
        self.setSpacing(0)


class SystemHBoxLayout(QHBoxLayout):
    def __init__(self, parent):
        super(SystemHBoxLayout, self).__init__()
        self.istitlebarlayout, self.istitleiconlayout = map(isinstance, [self] * 2, [TitleBarLayout, TitleIconLayout])
        self.setContentsMargins(*[parent._CustomizedWindow__titleicon_margin if self.istitleiconlayout else 0] * 4)
        self.setSpacing(0)
    def paintEvent(self, *args):
        self.setContentsMargins(*[parent._CustomizedWindow__titleicon_margin if self.istitleiconlayout else 0] * 4)


class TitleBarLayout(SystemHBoxLayout):
    def __init__(self, *args):
        super(TitleBarLayout, self).__init__(*args)


class TitleIconLayout(SystemHBoxLayout):
    def __init__(self, *args):
        super(TitleIconLayout, self).__init__(*args)


class SystemLabel(QAbstractButton):
    def __init__(self, parent):
        super(SystemLabel, self).__init__(parent)
        self.istitlebar, self.isclientarealabel, self.istitletextlabel, self.istitleiconcontainerlabel, self.istitleiconlabel = map(isinstance, [self] * 5, [TitleBar, ClientAreaLabel, TitleTextLabel, TitleIconContainerLabel, TitleIconLabel])
        if self.istitlebar: self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed), self.setFixedHeight(parent._CustomizedWindow__title_h)
        elif self.isclientarealabel or self.istitletextlabel or self.istitleiconlabel: self.setSizePolicy(*[QSizePolicy.Expanding] * 2)
        elif self.istitleiconcontainerlabel: self.setFixedSize(*[parent._CustomizedWindow__title_h] * 2)
        self.parent = parent
        self.setFocusPolicy(Qt.NoFocus)
        self.bgcolour = Qt.transparent
        self.draw = True
    def paintEvent(self, *args):
        parent = self.parent
        isdarktheme = parent.isDarkTheme()
        isblurwindow = parent._CustomizedWindow__isblurwindow
        isaeroenabled = isAeroEnabled()
        isactivewindow = parent.isActiveWindow()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bgcolour = Qt.transparent
        if self.istitlebar:
            self.setFixedHeight(parent._CustomizedWindow__title_h)
            if isblurwindow:
                if self.draw:
                    bgcolour = QLinearGradient(*[0] * 3 + [self.height()])
                    if isaeroenabled: list(map(bgcolour.setColorAt, [0, 1], [QColor(*[0] * 3 + [107]), QColor(*[0] * 3 + [197])])) if isdarktheme else list(map(bgcolour.setColorAt, [0, 1], [QColor(*[255] * 3 + [107]), QColor(*[255] * 3 + [197])]))
                    else: list(map(bgcolour.setColorAt, [0, 1], [QColor(*[38] * 3), QColor(*[0] * 3)])) if isdarktheme else list(map(bgcolour.setColorAt, [0, 1], [QColor(*[217] * 3), QColor(*[255] * 3)]))
                else:
                    if isaeroenabled: bgcolour = QColor(*[0] * 3 + [127] if isdarktheme else [255] * 3 + [127])
                    else: bgcolour = QColor(*[20] * 3 if isdarktheme else [235] * 3)
            else: bgcolour = QColor(*[0] * 3 if isdarktheme else [255] * 3)
        elif self.isclientarealabel:
            parent.clientArea.setGeometry(self.rect())
            if isblurwindow:
                if isaeroenabled: bgcolour = QColor(*[0] * 3 + [127] if isdarktheme else [255] * 3 + [127])
                else: bgcolour = QColor(*[20] * 3 if isdarktheme else [235] * 3)
            else: bgcolour = QColor(*[0] * 3 if isdarktheme else [255] * 3)
        elif self.istitletextlabel:
            if isdarktheme: pen = QPen(parent._CustomizedWindow__titletextcolour_d_ac if isactivewindow else parent._CustomizedWindow__titletextcolour_d_in)
            else: pen = QPen(parent._CustomizedWindow__titletextcolour_l_ac if isactivewindow else parent._CustomizedWindow__titletextcolour_l_in)
            painter.setBrush(Qt.NoBrush)
            painter.setPen(pen)
            font = QFont(parent._CustomizedWindow__captionfont)
            font.setPixelSize(parent._CustomizedWindow__title_fontsize)
            painter.setFont(font)
            if self.draw: painter.drawText(self.rect(), Qt.AlignVCenter, parent.windowTitle())
        elif self.istitleiconlabel:
            pixmap = parent.windowIcon().pixmap(self.width(), self.height())
            if self.draw: painter.drawPixmap(0, 0, pixmap)
        painter.setBrush(bgcolour)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())


class TitleBar(SystemLabel):
    def __init__(self, *args):
        super(TitleBar, self).__init__(*args)


class ClientAreaLabel(SystemLabel):
    def __init__(self, *args):
        super(ClientAreaLabel, self).__init__(*args)


class TitleTextLabel(SystemLabel):
    def __init__(self, *args):
        super(TitleTextLabel, self).__init__(*args)


class TitleIconContainerLabel(SystemLabel):
    def __init__(self, *args):
        super(TitleIconContainerLabel, self).__init__(*args)


class TitleIconLabel(SystemLabel):
    def __init__(self, *args):
        super(TitleIconLabel, self).__init__(*args)


def isAeroEnabled():
    try:
        pfEnabled = ctypes.c_uint()
        ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(pfEnabled))
        return pfEnabled.value
    except: return 0


def isdarktheme():
    try: value = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize'), 'AppsUseLightTheme')[0]
    except: return False
    return False if value else True


def gethwnd(window):
    hwnd = window.winId()
    if type(hwnd) != int:
        try:
            Func = ctypes.pythonapi.PyCapsule_GetPointer
            Func.restype, Func.argtypes = ctypes.c_void_p, [ctypes.py_object, ctypes.c_char_p]
            hwnd = Func(hwnd, None)
        except ValueError:
            Func = ctypes.pythonapi.PyCObject_AsVoidPtr
            Func.restype, Func.argtypes = ctypes.c_void_p, [ctypes.py_object]
            hwnd = Func(hwnd)
    return hwnd


def getdpiforwindow_winapi(hwnd):
    dpi = 96
    try:
        dpi_x, dpi_y = [ctypes.c_uint()] * 2
        monitor_h = user32.MonitorFromWindow(hwnd, 2)
        ctypes.windll.shcore.GetDpiForMonitor(monitor_h, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
        dpi = dpi_x.value
    except:
        dpiaware = user32.IsProcessDPIAware() if hasattr(user32, 'IsProcessDPIAware') else True
        if dpiaware:
            hDC = user32.GetDC(None)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hDC, 88)
            user32.ReleaseDC(None, hDC)
    return dpi


def getautohidetbpos():
    SPI_GETWORKAREA = 0x30
    priscrc = RECT()
    priscwidth, prischeight = map(user32.GetSystemMetrics, [0, 1])
    priscrc.left = 0
    priscrc.top = 0
    priscrc.right = priscwidth
    priscrc.bottom = prischeight
    if priscwidth != priscrc.right - priscrc.left or prischeight != priscrc.bottom - priscrc.top: return 4
    tb_hwnd = user32.FindWindowA(b'Shell_TrayWnd', None)
    if not tb_hwnd: return 4
    tb_rc = RECT()
    user32.GetWindowRect(tb_hwnd, ctypes.byref(tb_rc))
    if tb_rc.left < priscrc.left and tb_rc.top == priscrc.top and tb_rc.right != priscrc.right and tb_rc.bottom == priscrc.bottom: return 0
    elif tb_rc.left == priscrc.left and tb_rc.top < priscrc.top and tb_rc.right == priscrc.right and tb_rc.bottom != priscrc.bottom: return 1
    elif tb_rc.left != priscrc.left and tb_rc.top == priscrc.top and tb_rc.right > priscrc.right and tb_rc.bottom == priscrc.bottom: return 2
    elif tb_rc.left == priscrc.left and tb_rc.top != priscrc.top and tb_rc.right == priscrc.right and tb_rc.bottom > priscrc.bottom: return 3
    else: return 4


def getcaptionfont():
    res = NONCLIENTMETRICS()
    res.cbSize = ctypes.sizeof(NONCLIENTMETRICS)
    user32.SystemParametersInfoW(0x29, ctypes.sizeof(NONCLIENTMETRICS), ctypes.byref(res), 0)
    captionfont = res.lfCaptionFont.lfFaceName
    return captionfont


class SplashScreen(QSplashScreen):
    def __init__(self, parent):
        super(SplashScreen, self).__init__()
        self.__hwnd = gethwnd(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        dpi = parent.dpi()
        sc = QApplication.desktop() if hasattr(QApplication, 'desktop') else QApplication.screens()[0].size()
        self.resize(*[500 * dpi / 96.0] * 2)
        self.move((sc.width() - self.width()) // 2, (sc.height() - self.height()) // 2)
        self.mainlabel = QLabel(self)
        bgcolour = 'rgba(0, 0, 0, 179)' if parent.isDarkTheme() else 'rgba(255, 255, 255, 179)'
        shadowcolour, bordercolour = '#7F7F7F', 'rgba(127, 127, 127, 79)'
        self.mainlabel.setStyleSheet('background: %s; border-radius: %dpx; border: %dpx solid %s' % (bgcolour, int(20 * dpi / 96.0), int(2 * dpi / 96.0), bordercolour))
        self.mainlabel.resize(self.width() - int(50 * dpi / 96.0), self.height() - int(50 * dpi / 96.0))
        self.mainlabel.move((self.width() - self.mainlabel.width()) // 2, (self.height() - self.mainlabel.height()) // 2)
        self.iconlabel = QLabel(self)
        icon = parent.windowIcon()
        iconsize = [150 * dpi / 96.0] * 2
        pixmap = QPixmap.fromImage(parent.windowIcon().pixmap(*iconsize).toImage()).scaled(*iconsize)
        self.iconlabel.resize(*iconsize)
        self.iconlabel.move(self.width() // 2 - self.iconlabel.width() // 2, self.height() // 2 - self.iconlabel.height() // 2)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(int(50 * dpi / 96.0))
        shadow.setColor(shadowcolour)
        shadow.setOffset(0, 0)
        self.mainlabel.setGraphicsEffect(shadow)


class CustomizedWindow(QWidget):
    '''A customized window based on PySideX.'''
    def __init__(self):
        super(CustomizedWindow, self).__init__()
        self.__hwnd = gethwnd(self)
        self.__isblurwindow = isinstance(self, BlurWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True) if ISPYSIDE1 else self.setStyleSheet('CustomizedWindow{background: rgba(0, 0, 0, 0)}')
        self.__SWL = user32.SetWindowLongPtrW if hasattr(user32, 'SetWindowLongPtrW') else user32.SetWindowLongW
        self.__WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
        self.__BasicMessageHandlerAddress = ctypes.cast(self.__WNDPROC(self.__BasicMessageHandler), ctypes.c_void_p)
        if hasattr(user32, 'GetWindowLongPtrW'): self.__originalBasicMessageHandler = user32.GetWindowLongPtrW(self.__hwnd, -4)
        else: self.__originalBasicMessageHandler = user32.GetWindowLongW(self.__hwnd, -4)
        self.__handle_setWindowFlags()
        if isAeroEnabled(): self.__setDWMEffect(self.__isblurwindow)
        self.__resizable_h, self.__resizable_v = [True] * 2
        self.__realdpi = getdpiforwindow_winapi(self.__hwnd)
        self.__hdpiscalingenabled = False
        self.__hdpisfroundingpolicy = 3
        if hasattr(Qt, 'AA_EnableHighDpiScaling') and QApplication.testAttribute(Qt.AA_EnableHighDpiScaling): self.__hdpiscalingenabled = True
        if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
            policy_dict = {Qt.HighDpiScaleFactorRoundingPolicy.Ceil: 1, Qt.HighDpiScaleFactorRoundingPolicy.Floor: 2, Qt.HighDpiScaleFactorRoundingPolicy.PassThrough: 3, Qt.HighDpiScaleFactorRoundingPolicy.Round: 4, Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor: 5}
            if hasattr(Qt.HighDpiScaleFactorRoundingPolicy, 'Unset'): self.__hdpisfroundingpolicy = 3 if QApplication.highDpiScaleFactorRoundingPolicy() == Qt.HighDpiScaleFactorRoundingPolicy.Unset else policy_dict[QApplication.highDpiScaleFactorRoundingPolicy()]
            else: self.__hdpisfroundingpolicy = policy_dict[QApplication.highDpiScaleFactorRoundingPolicy()]
        dpi = self.dpi()
        self.__maxwindowmargin_list = self.__getMaximizedMargin()
        self.__themecolour = 0
        self.__isdarktheme = isdarktheme()
        self.__titletextcolour_l_ac, self.__titletextcolour_d_ac, self.__titletextcolour_l_in, self.__titletextcolour_d_in = Qt.black, Qt.white, QColor(*[99] * 3), QColor(*[155] * 3)
        self.__updatedpiconstants()
        self.__updateautohidetbwidth()
        self.__inminbutton, self.__inmaxbutton, self.__inclosebutton, self.__intitlebar, self.__inborder_t, self.__inborder_l, self.__inborder_b, self.__inborder_r = [False] * 8
        self.__captionfont = getcaptionfont()
        self.__margin_l, self.__margin_r, self.__margin_t, self.__margin_b = [0] * 4
        self.__mainLayout = SystemVBoxLayout(self)
        self.setLayout(self.__mainLayout)
        self.__titleBar = TitleBar(self)
        self.__titleBarLayout = TitleBarLayout(self)
        self.__titleBar.setLayout(self.__titleBarLayout)
        self.__clientAreaLabel = ClientAreaLabel(self)
        self.clientArea = QWidget(self.__clientAreaLabel)
        self.__titleIconLayout = TitleIconLayout(self)
        self.__titleIconContainerLabel = TitleIconContainerLabel(self)
        self.__titleIconContainerLabel.setLayout(self.__titleIconLayout)
        self.__titleIconLabel = TitleIconLabel(self)
        self.__titleIconLayout.addWidget(self.__titleIconLabel)
        self.__titleTextLabel = TitleTextLabel(self)
        self.__minSizeButton = MinSizeButton(self)
        self.__maxSizeButton = MaxSizeButton(self)
        self.__closeButton = CloseButton(self)
        list(map(self.__mainLayout.addWidget, [self.__titleBar, self.__clientAreaLabel]))
        list(map(self.__titleBarLayout.addWidget, [self.__titleIconContainerLabel, self.__titleTextLabel, self.__minSizeButton, self.__maxSizeButton, self.__closeButton]))
        self.setDarkTheme(0)
        self.__originalSetWindowTitle, self.setWindowTitle = self.setWindowTitle, self.__setWindowTitle
        self.__originalSetWindowIcon, self.setWindowIcon = self.setWindowIcon, self.__setWindowIcon
        self.__originalSetFixedSize, self.setFixedSize = self.setFixedSize, self.__setFixedSize
        self.__originalSetFixedWidth, self.setFixedWidth = self.setFixedWidth, self.__setFixedWidth
        self.__originalSetFixedHeight, self.setFixedHeight = self.setFixedHeight, self.__setFixedHeight
        if not ISPYSIDE1: self.windowHandle().screenChanged.connect(self.__screenChangedHandler)
    def dpi(self):
        '''DPI divided by 96.0 is the scale factor of PySideX UI.
Example:
DPI = window.dpi()
window.resize(int(400.0 * DPI / 96.0), int(175.0 * DPI / 96.0))'''
        return self.__getdpibyrealdpi(self.realdpi())
    def realdpi(self):
        '''REALDPI divided by 96.0 is the scale factor of System UI.'''
        return self.__realdpi
    def hwnd(self):
        '''HWND is the window handle of this window.'''
        return self.__hwnd
    def isDarkTheme(self):
        '''Example:
ISDARKTHEME = window.isDarkTheme()
if ISDARKTHEME:
|->|print('Dark')'''
        return self.__isdarktheme
    def setDarkTheme(self, themecolour=0):
        '''themecolour=0: Auto; themecolour=1: Light; themecolour=2: Dark'''
        self.__themecolour = themecolour
        try: self.__isdarktheme = {0: isdarktheme(), 1: False, 2: True}[themecolour]
        except:
            ErrorType = ValueError if type(themecolour) == int else TypeError
            raise ErrorType('Parameter themecolour must be 0, 1 or 2.')
        self.__minSizeButton.update()
        self.__maxSizeButton.update()
        self.__closeButton.update()
        self.__titleBar.update()
        self.__clientAreaLabel.update()
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER = 0x1, 0x2, 0x4
        try: list(map(ctypes.windll.dwmapi.DwmSetWindowAttribute, [self.__hwnd] * 2, [19, 20], [ctypes.byref(ctypes.c_long(self.isDarkTheme()))] * 2, [ctypes.sizeof(ctypes.c_long(self.isDarkTheme))] * 2))
        except: pass
        hwnd = self.__hwnd
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER)
    def isAeroEnabled(self):
        '''Example:
ISAEROENABLED = window.isAeroEnabled()
if ISAEROENABLED:
|->|print('Aero enabled')'''
        return isAeroEnabled()
    def setTitleTextColour(self, colour, theme=0, state=0):
        '''colour=0: Default; colour=Qt....: Qt.GlobalColor; colour=QColor(...): QColor
theme=0: Auto; theme=1: Light; theme=2: Dark
state=0: All; state=1: Active; state=2: Inactive'''
        if theme not in [0, 1, 2]:
            ErrorType = ValueError if type(theme) == int else TypeError
            raise ErrorType('Parameter theme must be 0, 1 or 2.')
        if state not in [0, 1, 2]:
            ErrorType = ValueError if type(state) == int else TypeError
            raise ErrorType('Parameter state must be 0, 1 or 2.')
        setlightcolour, setdarkcolour = theme in [0, 1], theme in [0, 2]
        setactivecolour, setinavtivecolour = state in [0, 1], state in [0, 2]
        titletextcolour_l_ac, titletextcolour_d_ac, titletextcolour_l_in, titletextcolour_d_in = self.__titletextcolour_l_ac, self.__titletextcolour_d_ac, self.__titletextcolour_l_in, self.__titletextcolour_d_in
        if colour == 0:
            if setlightcolour:
                if setactivecolour: titletextcolour_l_ac = Qt.white
                if setinavtivecolour: titletextcolour_l_in = QColor(*[155] * 3)
            if setdarkcolour:
                if setactivecolour: titletextcolour_d_ac = Qt.white
                if setinavtivecolour: titletextcolour_d_in = QColor(*[155] * 3)
        elif type(colour) in [Qt.GlobalColor, QColor]:
            if setlightcolour:
                if setactivecolour: titletextcolour_l_ac = colour
                if setinavtivecolour: titletextcolour_l_in = colour
            if setdarkcolour:
                if setactivecolour: titletextcolour_d_ac = colour
                if setinavtivecolour: titletextcolour_d_in = colour
        else:
            ErrorType = ValueError if type(colour) == int else TypeError
            raise ErrorType('Parameter colour must be 0, %s or %s.' % (Qt.GlobalColor, QColor))
        self.__titletextcolour_l_ac, self.__titletextcolour_d_ac, self.__titletextcolour_l_in, self.__titletextcolour_d_in = titletextcolour_l_ac, titletextcolour_d_ac, titletextcolour_l_in, titletextcolour_d_in
        self.__titleTextLabel.update()
    def __setWindowTitle(self, arg__1):
        self.__originalSetWindowTitle(arg__1)
        self.__titleTextLabel.update()
    def __setWindowIcon(self, icon):
        self.__originalSetWindowIcon(icon)
        self.__titleIconLabel.update()
    def __setFixedSize(self, *args, **kwargs):
        self.__originalSetFixedSize(*args, **kwargs)
        self.__resizable_h, self.__resizable_v = [False] * 2
        self.__SWL(self.__hwnd, -16, 0)
    def __setFixedWidth(self, *args, **kwargs):
        self.__originalSetFixedWidth(*args, **kwargs)
        self.__resizable_h = False
        self.__SWL(self.__hwnd, -16, 0)
    def __setFixedHeight(self, *args, **kwargs):
        self.__originalSetFixedHeight(*args, **kwargs)
        self.__resizable_v = False
        self.__SWL(self.__hwnd, -16, 0)
    def setWindowFlag(self, arg__1, on=True):
        raise AttributeError('Function setWindowFlag has been deleted.')
    def setWindowFlags(self, type):
        raise AttributeError('Function setWindowFlags has been deleted.')
    def __handle_setWindowFlags(self):
        if ISPYSIDE1: self.__SWL(self.__hwnd, -4, self.__originalBasicMessageHandler)
        self.__hwnd = gethwnd(self)
        BasicMessageHandlerAddress = self.__BasicMessageHandlerAddress
        if hasattr(user32, 'GetWindowLongPtrW'): self.__originalBasicMessageHandler = user32.GetWindowLongPtrW(self.__hwnd, -4)
        else: self.__originalBasicMessageHandler = user32.GetWindowLongW(self.__hwnd, -4)
        self.__originalBasicMessageHandlerFunction = self.__WNDPROC(self.__originalBasicMessageHandler)
        self.__ncsizeinited = False
        if ISPYSIDE1:
            self.__SWL(self.__hwnd, -4, BasicMessageHandlerAddress.value)
            libc._aligned_free(BasicMessageHandlerAddress.value)
            self.__SWL(self.__hwnd, -16, 0x40000 | 0x20000 | 0x10000)
        else: self.__SWL(self.__hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | 0x10000)
        if isAeroEnabled(): self.__setDWMEffect(self.__isblurwindow)
    def __setMBS(self, button, state=1):
        bgcolour1, bgcolour2, bgcolour3 = [Qt.transparent] * 3
        if button == 1:
            if state == 1: bgcolour1 = QColor(*[255] * 3 + [25] if self.isDarkTheme() else [0] * 3 + [25])
            elif state == 2: bgcolour1 = QColor(*[255] * 3 + [50] if self.isDarkTheme() else [0] * 3 + [50])
        elif button == 2:
            if state == 1: bgcolour2 = QColor(*[255] * 3 + [25] if self.isDarkTheme() else [0] * 3 + [25])
            elif state == 2: bgcolour2 = QColor(*[255] * 3 + [50] if self.isDarkTheme() else [0] * 3 + [50])
        elif button == 3:
            if state == 1: bgcolour3 = QColor(255, 0, 0, 199)
            elif state == 2: bgcolour3 = QColor(255, 0, 0, 99)
        self.__minSizeButton.bgcolour, self.__maxSizeButton.bgcolour, self.__closeButton.bgcolour = bgcolour1, bgcolour2, bgcolour3
        self.__minSizeButton.update()
        self.__maxSizeButton.update()
        self.__closeButton.update()
    def MessageHandler(self, hwnd, message, wParam, lParam):
        '''Example:
class MyOwnWindow(BlurWindow):
|->|...
|->|def MessageHandler(self, hwnd, message, wParam, lParam):
|->||->|print(hwnd, message, wParam, lParam)
|->||->|...'''
        pass
    def __BasicMessageHandler(self, hwnd, message, wParam, lParam):
        WM_SIZE = 0x5
        WM_ACTIVATE = 0x6
        WM_PAINT = 0xf
        WM_SHOWWINDOW = 0x18
        WM_SETTINGCHANGE = 0x1a
        WM_STYLECHANGED = 0x7d
        WM_NCCALCSIZE = 0x83
        WM_NCHITTEST = 0x84
        WM_NCLBUTTONDOWN = 0xa1
        WM_NCLBUTTONUP = 0xa2
        WM_LBUTTONUP = 0x2a2
        WM_DPICHANGED = 0x2e0
        WM_SYSCOMMAND = 0x112
        WM_DWMCOMPOSITIONCHANGED = 0x31e
        SW_PARENTOPENING = 0x3
        SC_SIZE, SC_MOVE, SC_MINIMIZE, SC_MAXIMIZE, SC_CLOSE, SC_RESTORE = 0xf000, 0xf010, 0xf020, 0xf030, 0xf060, 0xf120
        HTCLIENT, HTCAPTION, HTMINBUTTON, HTMAXBUTTON, HTCLOSE = 0x1, 0x2, 0x8, 0x9, 0x14
        HTLEFT, HTRIGHT, HTTOP, HTTOPLEFT, HTTOPRIGHT, HTBOTTOM, HTBOTTOMLEFT, HTBOTTOMRIGHT, HTBORDER = 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER, SWP_FRAMECHANGED = 0x1, 0x2, 0x4, 0x20
        SPI_SETNONCLIENTMETRICS, SPI_SETWORKAREA = 0x2a, 0x2f
        try:
            dpi, realdpi = self.dpi(), self.realdpi()
            real_border_w = self.__real_border_w
            real_title_h = self.__real_title_h
            real_menubutton_w = self.__real_menubutton_w
            margin_l = self.__margin_l
            margin_r = self.__margin_r
            margin_t = self.__margin_t
            margin_b = self.__margin_b
            resizable_h, resizable_v = self.__resizable_h, self.__resizable_v
            resizable_hv = resizable_h and resizable_v
        except: dpi, realdpi, real_border_w, real_title_h, real_menubutton_w, margin_l, margin_r, margin_t, margin_b, resizable_h, resizable_v, resizable_hv = [96] * 2 + [0] * 7 + [True] * 3
        try: windowrc = self.GetWindowRect()
        except: windowrc = RECT(*[0] * 4)
        windowx, windowy = windowrc.left, windowrc.top
        globalpos = POINT()
        try:
            user32.GetPhysicalCursorPos(ctypes.byref(globalpos))
            user32.PhysicalToLogicalPoint(self.__hwnd, ctypes.byref(globalpos))
        except: user32.GetCursorPos(ctypes.byref(globalpos))
        x, y = globalpos.x - windowx, globalpos.y - windowy
        w, h = windowrc.right - windowx, windowrc.bottom - windowy
        intitlebar = margin_t <= y < real_title_h + margin_t
        inminbutton = w - margin_l - 3 * real_menubutton_w <= x < w - margin_l - 2 * real_menubutton_w and intitlebar
        inmaxbutton = w - margin_l - 2 * real_menubutton_w <= x < w - margin_l - real_menubutton_w and intitlebar
        inclosebutton = w - margin_l - real_menubutton_w <= x < w - margin_l and intitlebar
        inborder_t, inborder_l, inborder_b, inborder_r = y <= real_border_w, x <= real_border_w, h - y <= real_border_w, w - x <= real_border_w
        self.__inminbutton, self.__inmaxbutton, self.__inclosebutton, self.__intitlebar, self.__inborder_t, self.__inborder_l, self.__inborder_b, self.__inborder_r = inminbutton, inmaxbutton, inclosebutton, intitlebar, inborder_t, inborder_l, inborder_b, inborder_r
        if message == WM_NCCALCSIZE: return self.__Handle_WM_NCCALCSIZE_Message(hwnd, message, wParam, lParam)
        if message == WM_NCHITTEST:
            VK_LBUTTON = 0x1
            islbuttonpressed = user32.GetKeyState(VK_LBUTTON) not in [0, 1]
            if not self.isMaximized():
                if inborder_t and inborder_l: WM_NCHITTEST_res = HTTOPLEFT if resizable_hv else HTBORDER
                elif inborder_t and inborder_r: WM_NCHITTEST_res = HTTOPRIGHT if resizable_hv else HTBORDER
                elif inborder_b and inborder_l: WM_NCHITTEST_res = HTBOTTOMLEFT if resizable_hv else HTBORDER
                elif inborder_b and inborder_r: WM_NCHITTEST_res = HTBOTTOMRIGHT if resizable_hv else HTBORDER
                elif inborder_l: WM_NCHITTEST_res = HTLEFT if resizable_h else HTBORDER
                elif inborder_t: WM_NCHITTEST_res = HTTOP if resizable_v else HTBORDER
                elif inborder_r: WM_NCHITTEST_res = HTRIGHT if resizable_h else HTBORDER
                elif inborder_b: WM_NCHITTEST_res = HTBOTTOM if resizable_v else HTBORDER
            if not 'WM_NCHITTEST_res' in dir():
                if inminbutton:
                    if not islbuttonpressed: self.__setMBS(1, 1)
                    WM_NCHITTEST_res = HTMINBUTTON
                elif inmaxbutton:
                    if resizable_h or resizable_v:
                        if not islbuttonpressed: self.__setMBS(2, 1)
                        WM_NCHITTEST_res = HTMAXBUTTON
                    else: WM_NCHITTEST_res = HTBORDER
                elif inclosebutton:
                    if not islbuttonpressed: self.__setMBS(3, 1)
                    WM_NCHITTEST_res = HTCLOSE
                elif intitlebar: WM_NCHITTEST_res = HTCAPTION
                else: WM_NCHITTEST_res = HTCLIENT
            if WM_NCHITTEST_res not in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if not islbuttonpressed: self.__setMBS(0)
            return WM_NCHITTEST_res
        if message == WM_NCLBUTTONDOWN:
            if wParam in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if wParam == HTMINBUTTON: self.__setMBS(1, 2)
                if wParam == HTMAXBUTTON: self.__setMBS(2, 2)
                if wParam == HTCLOSE: self.__setMBS(3, 2)
                return 0
            return user32.DefWindowProcW(hwnd, message, wParam, lParam)
        if message == WM_NCLBUTTONUP:
            self.__setMBS(0)
            if wParam == HTMINBUTTON:
                user32.PostMessageW(self.__hwnd, WM_SYSCOMMAND, SC_MINIMIZE, 0)
            elif wParam == HTMAXBUTTON:
                if self.isMaximized(): user32.PostMessageW(self.__hwnd, WM_SYSCOMMAND, SC_RESTORE, 0)
                elif self.isFullScreen(): pass
                else: user32.PostMessageW(self.__hwnd, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
            elif wParam == HTCLOSE: user32.PostMessageW(self.__hwnd, WM_SYSCOMMAND, SC_CLOSE, 0)
            return user32.DefWindowProcW(hwnd, message, wParam, lParam)
        if message == WM_LBUTTONUP:
            self.__setMBS(0)
        if message == WM_DPICHANGED:
            windowrc = RECT.from_address(lParam)
            realdpi = wParam >> 16
            self.__realdpi = realdpi
            self.__maxwindowmargin_list = self.__getMaximizedMargin()
            if not self.__hdpiscalingenabled: self.setGeometry(QRect(*[int(i[0]) for i in windowrc._fields_]))
            self.__updatedpiconstants()
            self.__minSizeButton.update()
            self.__maxSizeButton.update()
            self.__closeButton.update()
            self.__titleTextLabel.update()
            self.__titleIconLabel.update()
        if message == WM_SETTINGCHANGE:
            try: lParam_string = str(ctypes.cast(lParam, ctypes.c_wchar_p).value)
            except: lParam_string = ''
            if wParam == SPI_SETWORKAREA:
                self.__updateautohidetbwidth()
                user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED)
            if wParam == SPI_SETNONCLIENTMETRICS:
                self.__maxwindowmargin_list = self.__getMaximizedMargin()
                self.__captionfont = getcaptionfont()
                self.__titleTextLabel.update()
            if self.__themecolour == 0 and lParam_string == 'ImmersiveColorSet': self.setDarkTheme(0)
        if message == WM_DWMCOMPOSITIONCHANGED:
            if isAeroEnabled(): self.__setDWMEffect(self.__isblurwindow)
            self.__titleBar.update()
            self.__clientAreaLabel.update()
        if message == WM_ACTIVATE:
            isactivewindow = 1 if wParam else 0
            if not isactivewindow: self.__setMBS(0)
        if message == WM_STYLECHANGED:
            if hasattr(self, '_CustomizedWindow__ncsizeinited') and self.__ncsizeinited: self.__SWL(self.__hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | (0x10000 if (resizable_h or resizable_v) else 0))
        messagehandlerres = self.MessageHandler(hwnd, message, wParam, lParam)
        if messagehandlerres != None: return messagehandlerres
        if ISPYSIDE1: return self.__originalBasicMessageHandlerFunction(hwnd, message, wParam, lParam)
    def __Handle_WM_NCCALCSIZE_Message(self, hwnd, message, wParam, lParam):
        try:
            autohidetbwidth_l = self.__autohidetbwidth_l
            autohidetbwidth_t = self.__autohidetbwidth_t
            autohidetbwidth_r = self.__autohidetbwidth_r
            autohidetbwidth_b = self.__autohidetbwidth_b
        except: autohidetbwidth_l, autohidetbwidth_t, autohidetbwidth_r, autohidetbwidth_b = [0] * 4
        rc = ctypes.cast(lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents.rgrc[0] if wParam else ctypes.cast(lParam, ctypes.POINTER(RECT)).contents
        ISMAXIMIZED = user32.IsZoomed(hwnd)
        try: maxwindowmargin_list = self.__maxwindowmargin_list
        except: maxwindowmargin_list = [0] * 2
        if ISMAXIMIZED:
            self.__margin_l = maxwindowmargin_list[0] + autohidetbwidth_l
            self.__margin_r = maxwindowmargin_list[0] + autohidetbwidth_r
            self.__margin_t = maxwindowmargin_list[1] + autohidetbwidth_t
            self.__margin_b = maxwindowmargin_list[1] + autohidetbwidth_b
        else: self.__margin_l, self.__margin_r, self.__margin_t, self.__margin_b = [0] * 4
        margin_l = self.__margin_l
        margin_r = self.__margin_r
        margin_t = self.__margin_t
        margin_b = self.__margin_b
        rc.left += margin_l
        rc.right -= margin_r
        rc.top += margin_t
        rc.bottom -= margin_b
        if hasattr(self, '_CustomizedWindow__ncsizeinited'):
            __ncsizeinited = self.__ncsizeinited
            if not __ncsizeinited:
                if ISPYSIDE1: self.__SWL(self.__hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | 0x10000)
                self.__ncsizeinited = True
        return 0
    def __getMaximizedMargin(self):
        SM_CXSIZEFRAME, SM_CYSIZEFRAME, SM_CXPADDEDBORDER = 32, 33, 92
        realdpi = self.realdpi()
        above14393 = hasattr(user32, 'GetSystemMetricsForDpi')
        Func = user32.GetSystemMetricsForDpi if above14393 else user32.GetSystemMetrics
        args = [Func, [SM_CXSIZEFRAME, SM_CXPADDEDBORDER, SM_CYSIZEFRAME, SM_CXPADDEDBORDER]]
        if above14393: args.append([realdpi] * 4)
        res = list(map(*args))
        return [sum(res[0:2]), sum(res[2:4])]
    def nativeEvent(self, eventType, msg):
        '''For PySide2/6, you should define MessageHandler instead of nativeEvent.'''
        WM_PAINT = 0xf
        WM_NCCALCSIZE = 0x83
        msg = MSG.from_address(msg.__int__())
        hwnd, message, wParam, lParam = msg.hWnd, msg.message, msg.wParam, msg.lParam
        basicmessagehandlerres = self.__BasicMessageHandler(hwnd, message, wParam, lParam)
        if basicmessagehandlerres != None: return True, basicmessagehandlerres
        return super(CustomizedWindow, self).nativeEvent(eventType, msg)
    def __setDWMEffect(self, blur=False, isEnableShadow=True):
        hwnd = self.__hwnd
        try:
            dwmapi = ctypes.windll.dwmapi
            if blur:
                dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
                bb = DWM_BLURBEHIND()
                bb.dwFlags = 1
                bb.fEnable = 1
                w11_21h2_blur_code, w11_22h2_blur_code = self.__setwin11blur(hwnd)
                if w11_22h2_blur_code:
                    dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 0, 0)))
                    dwmapi.DwmEnableBlurBehindWindow(ctypes.c_int(hwnd), ctypes.byref(bb))
                else:
                    dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(*[-1] * 4)))
                    return 3
                try:
                    AeroEffect = Win10BlurEffect()
                    w10_blur_code = AeroEffect.setAeroEffect(hwnd, isEnableShadow=isEnableShadow)
                    if w10_blur_code != 0: return 2
                except: pass
            else:
                dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
                dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 0, 0)))
            return 1
        except: return 0
    def __getdpibyrealdpi(self, realdpi):
        realsf = realdpi / 96.0
        if self.__hdpiscalingenabled:
            sf = realsf
            if self.__hdpisfroundingpolicy == 1: sf = int(realsf + 1 if realsf - int(realsf) > 0 else realsf)
            elif self.__hdpisfroundingpolicy == 2: sf = int(realsf)
            elif self.__hdpisfroundingpolicy == 4: sf = int(realsf + 1 if realsf - int(realsf) >= 0.5 else realsf)
            elif self.__hdpisfroundingpolicy == 5: sf = int(realsf + 1 if realsf - int(realsf) > 0.5 else realsf)
            dpi = int(float(realdpi) / sf)
        else: dpi = realdpi
        return dpi
    def __updatedpiconstants(self):
        dpi, realdpi = self.dpi(), self.realdpi()
        self.__border_w = int(5.0 * dpi / 96.0)
        self.__title_h = int(30.0 * dpi / 96.0)
        self.__menubutton_w = int(46.0 * dpi / 96.0)
        self.__title_fontsize = int(13.0 * dpi / 96.0)
        self.__real_border_w = int(5.0 * realdpi / 96.0)
        self.__real_title_h = int(30.0 * realdpi / 96.0)
        self.__real_menubutton_w = int(46.0 * realdpi / 96.0)
        self.__titleicon_margin = int(7.0 * dpi / 96.0)
    def __updateautohidetbwidth(self):
        autohidetbpos = getautohidetbpos()
        self.__autohidetbwidth_l = 2 if autohidetbpos == 0 else 0
        self.__autohidetbwidth_t = 2 if autohidetbpos == 1 else 0
        self.__autohidetbwidth_r = 2 if autohidetbpos == 2 else 0
        self.__autohidetbwidth_b = 2 if autohidetbpos == 3 else 0
    def __setwin11blur(self, hWnd):
        ENTRY_21H2, ENTRY_22H2, VALUE_21H2, VALUE_22H2 = 1029, 38, 1, 3
        return list(map(ctypes.windll.dwmapi.DwmSetWindowAttribute, [hWnd] * 2, [ENTRY_21H2, ENTRY_22H2], [ctypes.byref(ctypes.c_int(VALUE_21H2)), ctypes.byref(ctypes.c_int(VALUE_22H2))], [ctypes.sizeof(ctypes.c_int)] * 2))
    def GetWindowRect(self):
        lpRect = RECT()
        user32.GetWindowRect(self.__hwnd, ctypes.byref(lpRect))
        return lpRect
    def splashScreen(self):
        '''You should call splashscreen.show after window.setWindowIcon, window.setDarkTheme,
and before window.setGeometry, window.move, window.resize,
call splashscreen.finish before window.show.
Example:
window.setWindowIcon(QIcon('Icon.ico'))
splashscreen = window.splashScreen()
splashscreen.show()
window.resize(int(400.0 * window.dpi() / 96.0), int(175.0 * window.dpi() / 96.0))
...
window.show()
splashscreen.finish(window)'''
        return SplashScreen(self)
    def __screenChangedHandler(self):
        hwnd = gethwnd(self.windowHandle())
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER, SWP_FRAMECHANGED = 0x1, 0x2, 0x4, 0x20
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED)


class BlurWindow(CustomizedWindow):
    '''A blur window based on PySideX.
Blur effect is avaliable on Windows Vista and newer.'''
    def __init__(self):
        super(BlurWindow, self).__init__()


if __name__ == '__main__':
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except: pass
    app = QApplication(sys.argv)
    window = BlurWindow()
    help(window.MessageHandler)
    list(map(window.setTitleTextColour, [QColor(0, 0, 139), QColor(119, 235, 255)], [1, 2], [1] * 2))
    help(window.setTitleTextColour)
    window.setDarkTheme(2)
    help(window.setDarkTheme)
    window.setWindowIcon(QIcon('Icon.ico'))
    splashscreen = window.splashScreen()
    help(window.splashScreen)
    splashscreen.show()
    window.resize(int(400.0 * window.dpi() / 96.0), int(175.0 * window.dpi() / 96.0))
    window.setWindowTitle('Window')
    button = QPushButton('Button', window.clientArea)
    window.show()
    ISDARKTHEME = window.isDarkTheme()
    splashscreen.finish(window)
    app.exec_()
