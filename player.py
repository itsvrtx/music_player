# Developed by itsvrtx
# Github: https://github.com/itsvrtx

import sys
import os
import platform
import ctypes
from PySide6.QtCore import (
    Qt, QUrl, QPoint, QRectF, QThread, Signal, Slot, QPropertyAnimation, 
    QEasingCurve, QTimer, QSettings, QSize
)
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSlider, QPushButton, QFileDialog, QMenu,
    QListWidget, QListWidgetItem, QSizeGrip, QFrame,
    QLineEdit
)
from PySide6.QtGui import QColor, QFont, QPixmap, QImage, QPainter, QPainterPath, QAction, QPen, QFontMetrics, QCursor, QRegion
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import mutagen


def apply_windows_acrylic(hwnd, enable=True, blur_opacity=0xBB, round_corners=True):
    if platform.system() != "Windows":
        return
    try:
        class ACCENT_POLICY(ctypes.Structure):
            _fields_ = [
                ("AccentState", ctypes.c_uint),
                ("AccentFlags", ctypes.c_uint),
                ("GradientColor", ctypes.c_uint),
                ("AnimationId", ctypes.c_uint)
            ]

        class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
            _fields_ = [
                ("Attribute", ctypes.c_int),
                ("Data", ctypes.c_void_p),
                ("SizeOfData", ctypes.c_size_t)
            ]

        policy = ACCENT_POLICY()
        if enable:
            policy.AccentState = 3 
            policy.GradientColor = (blur_opacity << 24) | 0x151518
        else:
            policy.AccentState = 0

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = 19
        data.Data = ctypes.cast(ctypes.pointer(policy), ctypes.c_void_p)
        data.SizeOfData = ctypes.sizeof(policy)

        ctypes.windll.user32.SetWindowCompositionAttribute(int(hwnd), ctypes.byref(data))

        if round_corners:
            try:
                DWMWA_WINDOW_CORNER_PREFERENCE = 33
                preference = ctypes.c_int(2)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    int(hwnd),
                    DWMWA_WINDOW_CORNER_PREFERENCE,
                    ctypes.byref(preference),
                    ctypes.sizeof(preference),
                )
            except Exception:
                pass
    except Exception:
        pass

SVG_ICONS = {
    "play": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M8 5v14l11-7z"/></svg>',
    "pause": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>',
    "next": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>',
    "prev": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg>',
    "folder": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>',
    "lock_open": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 17c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm6-9h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6h1.9c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm0 12H6V10h12v10z"/></svg>',
    "lock_closed": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>',
    "repeat": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>',
    "circle_mode": '<svg viewBox="0 0 24 24" fill="{color}"><circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="2" fill="none"/></svg>',
    "music": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>',
    "back": '<svg viewBox="0 0 24 24" fill="{color}"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'
}

def render_svg_pixmap(name, color="#FFFFFF", size=16):
    svg_str = SVG_ICONS.get(name, "").format(color=color)
    renderer = QSvgRenderer(bytes(svg_str, "utf-8"))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap

class MarqueeLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._offset = 0
        self._scroll_enabled = False
        self.setMinimumWidth(0)

        self.timer = QTimer(self)
        self.timer.setInterval(30)
        self.timer.timeout.connect(self._update_scroll)

    def setText(self, text):
        super().setText(text)
        self._offset = 0
        self._check_scroll_needed()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._check_scroll_needed()

    def _check_scroll_needed(self):
        fm = QFontMetrics(self.font())
        text_width = fm.horizontalAdvance(self.text())
        if text_width > self.width() and self.width() > 30:
            if not self._scroll_enabled:
                self._scroll_enabled = True
                self.timer.start()
        else:
            self._scroll_enabled = False
            self.timer.stop()
            self._offset = 0
            self.update()

    def _update_scroll(self):
        fm = QFontMetrics(self.font())
        text_width = fm.horizontalAdvance(self.text() + "   •   ")
        self._offset += 1
        if self._offset >= text_width:
            self._offset = 0
        self.update()

    def paintEvent(self, event):
        if self.width() < 20:
            return

        painter = QPainter(self)
        painter.setClipRect(self.rect())

        if not self._scroll_enabled or self.width() <= 30:
            fm = QFontMetrics(self.font())
            elided = fm.elidedText(self.text(), Qt.TextElideMode.ElideRight, self.width())
            painter.setPen(self.palette().color(self.foregroundRole()))
            painter.setFont(self.font())
            y = (self.height() + fm.ascent() - fm.descent()) // 2
            painter.drawText(0, y, elided)
            painter.end()
            return

        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.setFont(self.font())
        fm = QFontMetrics(self.font())

        y = (self.height() + fm.ascent() - fm.descent()) // 2
        scroll_text = self.text() + "   •   "
        text_width = fm.horizontalAdvance(scroll_text)

        painter.drawText(-self._offset, y, scroll_text)
        painter.drawText(text_width - self._offset, y, scroll_text)
        painter.end()


class MetadataWorker(QThread):
    loaded = Signal(str, QPixmap, str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        if not self.file_path or not os.path.exists(self.file_path):
            self.loaded.emit("", self.get_default_cover(), "No Track Loaded")
            return

        filename = os.path.basename(self.file_path)
        name, _ = os.path.splitext(filename)
        pix = None

        try:
            audio = mutagen.File(self.file_path)
            if audio and hasattr(audio, 'tags') and audio.tags:
                image_data = None
                for key in audio.tags.keys():
                    if key.startswith('APIC'):
                        image_data = audio.tags[key].data
                        break
                if not image_data and hasattr(audio, 'pictures') and audio.pictures:
                    image_data = audio.pictures[0].data
                elif not image_data and 'covr' in audio.tags:
                    image_data = audio.tags['covr'][0]

                if image_data:
                    image = QImage.fromData(image_data)
                    pix = QPixmap.fromImage(image).scaled(
                        120, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation
                    )
        except Exception:
            pass

        if not pix:
            pix = self.get_default_cover()

        self.loaded.emit(self.file_path, pix, name)

    def get_default_cover(self):
        pix = render_svg_pixmap("music", color="#FFFFFF", size=30)
        base = QPixmap(120, 120)
        base.fill(QColor("#222328"))
        painter = QPainter(base)
        painter.drawPixmap(45, 45, pix)
        painter.end()
        return base

class CircularProgressButton(QPushButton):
    hovered = Signal(bool)

    def __init__(self, size=80, parent=None):
        super().__init__(parent)
        self.size_val = size
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        
        self.progress = 0.0
        self.cover_pixmap = None

    def set_progress(self, val):
        self.progress = max(0.0, min(1.0, val))
        self.update()

    def set_cover(self, pixmap):
        self.cover_pixmap = pixmap
        self.update()

    def enterEvent(self, event):
        self.hovered.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.rect().contains(self.mapFromGlobal(self.cursor().pos())):
            self.hovered.emit(False)
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        edge_pad = 4
        art_gap = 4
        ring_width = 2
        rect = QRectF(self.rect()).adjusted(edge_pad, edge_pad, -edge_pad, -edge_pad)
        inset = art_gap + ring_width / 2.0
        inner_rect = rect.adjusted(inset, inset, -inset, -inset)

        path = QPainterPath()
        path.addEllipse(inner_rect)
        painter.save()
        painter.setClipPath(path)

        if self.cover_pixmap and not self.cover_pixmap.isNull():
            scaled_pix = self.cover_pixmap.scaled(
                inner_rect.toRect().size(), 
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            x = inner_rect.x() + (inner_rect.width() - scaled_pix.width()) / 2
            y = inner_rect.y() + (inner_rect.height() - scaled_pix.height()) / 2
            painter.drawPixmap(int(x), int(y), scaled_pix)
        else:
            painter.fillRect(inner_rect, QColor(40, 40, 40))
            
        painter.restore()

        pen = QPen(QColor(255, 255, 255, 130), ring_width)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        if self.progress > 0.0:
            pen.setColor(QColor(255, 255, 255, 235))
            painter.setPen(pen)
            span_angle = int(-self.progress * 360 * 16)
            painter.drawArc(rect, 90 * 16, span_angle)

        painter.end()

class AnimatedMiniPlayer(QWidget):
    restore_requested = Signal()
    toggle_play_requested = Signal()
    next_requested = Signal()
    prev_requested = Signal()
    repeat_requested = Signal()

    def __init__(self, main_player, parent=None):
        super().__init__(parent if parent is not None else main_player)

        self.main_player = main_player
        self.circle_size = 67
        self.mini_height = 67
        self.tray_expanded_width = 225

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFixedSize(self.circle_size + self.tray_expanded_width, self.mini_height)

        self.collapse_timer = QTimer(self)
        self.collapse_timer.setInterval(1000)
        self.collapse_timer.setSingleShot(True)
        self.collapse_timer.timeout.connect(self._do_collapse)

        self.tray_widget = QWidget(self)
        self.tray_widget.setObjectName("MiniTray")
        self.tray_widget.setFixedHeight(self.mini_height)
        self.tray_widget.setMinimumWidth(0)
        self.tray_widget.setMaximumWidth(0)
        self.tray_widget.setMouseTracking(True)
        self.tray_widget.move(0, 0)

        self.circle_btn = CircularProgressButton(self.circle_size, self)
        self.circle_btn.clicked.connect(self.restore_requested.emit)
        self.circle_btn.hovered.connect(self.on_disc_hovered)
        self.disc = self.circle_btn
        self.circle_btn.move(0, max(0, (self.mini_height - self.circle_size) // 2))
        self.circle_btn.raise_()

        self.tray_widget.setStyleSheet(f"""
            QWidget#MiniTray {{
                background: rgba(20, 20, 28, 0.45);
                border: 0.5px solid rgba(255, 255, 255, 0.20);
                border-radius: 0px;
            }}
            QWidget#MiniTrayContent {{
                background: transparent;
                border: none;
            }}
            QLabel {{
                background: transparent;
                color: #FFFFFF;
                border: none;
            }}
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.15);
                border-radius: 4px;
            }}
            QSlider::groove:horizontal {{
                height: 3px;
                background: rgba(255, 255, 255, 0.25);
                border-radius: 1px;
            }}
            QSlider::sub-page:horizontal {{
                background: #FFFFFF;
                border-radius: 1px;
            }}
            QSlider::handle:horizontal {{
                background: #FFFFFF;
                border: none;
                width: 8px;
                height: 8px;
                margin: -2.5px 0;
                border-radius: 4px;
            }}
        """)

        outer_layout = QVBoxLayout(self.tray_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.tray_content = QWidget(self.tray_widget)
        self.tray_content.setObjectName("MiniTrayContent")
        self._pill_width = self.circle_size + self.tray_expanded_width
        self.tray_content.setFixedWidth(self._pill_width)
        self.tray_content.setMouseTracking(True)
        outer_layout.addWidget(self.tray_content)

        tray_layout = QVBoxLayout(self.tray_content)
        tray_layout.setContentsMargins(self.circle_size + 8, 0, 12, 8)
        tray_layout.setSpacing(2)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = MarqueeLabel("Zulfein")
        title_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setFixedHeight(18)

        self.btn_back_to_full = self.main_player.create_icon_button("back")
        self.btn_back_to_full.setFixedSize(20, 20)
        self.btn_back_to_full.setProperty("icon_size", 12)
        self.btn_back_to_full.setToolTip("Back to full player")
        self.btn_back_to_full.clicked.connect(self.restore_requested.emit)

        header_row.addWidget(self.title_label, stretch=1)
        header_row.addWidget(self.btn_back_to_full)

        self.folder_label = QLabel("Folder: fine shyte")
        self.folder_label.setFont(QFont("Segoe UI", 8))
        self.folder_label.setStyleSheet("color: rgba(255, 255, 255, 0.70);")
        self.folder_label.setFixedHeight(14)

        seek_row = QHBoxLayout()
        seek_row.setSpacing(6)

        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("font-size: 8px; color: rgba(255, 255, 255, 0.65);")
        self.duration_label = QLabel("00:00")
        self.duration_label.setStyleSheet("font-size: 8px; color: rgba(255, 255, 255, 0.65);")

        self.mini_seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.mini_seek_slider.setRange(0, 0)
        self.mini_seek_slider.setFixedHeight(10)
        self.mini_seek_slider.sliderMoved.connect(self.main_player.set_position)
        self.mini_seek_slider.sliderReleased.connect(
            lambda: self.main_player.player.setPosition(self.mini_seek_slider.value())
        )

        seek_row.addWidget(self.time_label)
        seek_row.addWidget(self.mini_seek_slider, stretch=1)
        seek_row.addWidget(self.duration_label)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 2, 0, 0)
        btn_layout.setSpacing(0)

        self.btn_repeat = self.main_player.create_icon_button("repeat")
        self.btn_prev = self.main_player.create_icon_button("prev")
        self.btn_play = self.main_player.create_icon_button("play")
        self.btn_next = self.main_player.create_icon_button("next")

        self.btn_repeat.setFixedSize(22, 22)
        self.btn_repeat.setProperty("icon_size", 14)
        self.btn_prev.setFixedSize(22, 22)
        self.btn_prev.setProperty("icon_size", 14)
        self.btn_next.setFixedSize(22, 22)
        self.btn_next.setProperty("icon_size", 14)
        self.btn_play.setFixedSize(22, 22)
        self.btn_play.setProperty("icon_size", 14)

        self.btn_repeat.clicked.connect(self.repeat_requested.emit)
        self.btn_prev.clicked.connect(self.prev_requested.emit)
        self.btn_play.clicked.connect(self.toggle_play_requested.emit)
        self.btn_next.clicked.connect(self.next_requested.emit)

        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_repeat)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_prev)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_play)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addStretch(1)

        tray_layout.addLayout(header_row)
        tray_layout.addWidget(self.folder_label)
        tray_layout.addLayout(seek_row)
        tray_layout.addLayout(btn_layout)

        self.width_anim = QPropertyAnimation(self.tray_widget, b"maximumWidth")
        self.width_anim.setEasingCurve(QEasingCurve.Type.OutExpo)
        self.width_anim.valueChanged.connect(self._on_tray_width_changed)

    def _on_tray_width_changed(self, value):
        if self.main_player and self.main_player.is_mini_mode:
            self.main_player.sync_mini_window_size(int(value))

    def _animate_to(self, expanded):
        self.width_anim.stop()
        self.width_anim.setStartValue(self.tray_widget.maximumWidth())
        self.width_anim.setEndValue(self._pill_width if expanded else 0)
        self.width_anim.setDuration(300)
        self.width_anim.start()

    def on_disc_hovered(self, hovered):
        if hovered:
            self.collapse_timer.stop()
            self._animate_to(True)
        else:
            self.collapse_timer.start()

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            self.collapse_timer.start()
        super().leaveEvent(event)

    def _do_collapse(self):
        global_pos = QCursor.pos()
        if not self.circle_btn.rect().contains(self.circle_btn.mapFromGlobal(global_pos)) and \
           not self.tray_widget.rect().contains(self.tray_widget.mapFromGlobal(global_pos)):
            self._animate_to(False)

class FinalGlassMusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("GlassPlayer", "StateMemory")
        self.drag_position = QPoint()
        self.folders = {}
        self.current_folder = None
        self.playlist = []
        self.current_index = -1
        self.cover_cache = {}

        self.pending_resume_position = 0

        self.is_locked = False
        self.repeat_mode = False
        self.is_mini_mode = False
        self._playlist_visible = False

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.init_ui()
        self.setup_signals()
        self.apply_dark_theme()
        self.update_window_flags()

        self.load_saved_state()

    def init_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(240, 160)
        self.resize(360, 200)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.container = QWidget(self)
        self.container.setObjectName("GlassContainer")

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(8)

        self.resume_banner = QFrame()
        self.resume_banner.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.12);
                border-radius: 8px;
            }
            QLabel { font-size: 10px; color: #FFFFFF; }
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 2px 6px;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.35); }
        """)
        banner_layout = QHBoxLayout(self.resume_banner)
        banner_layout.setContentsMargins(8, 4, 8, 4)
        banner_layout.setSpacing(6)

        self.resume_label = QLabel("Resume playback?")
        self.btn_accept_resume = QPushButton("Resume")
        self.btn_dismiss_resume = QPushButton("✕")

        banner_layout.addWidget(self.resume_label)
        banner_layout.addStretch()
        banner_layout.addWidget(self.btn_accept_resume)
        banner_layout.addWidget(self.btn_dismiss_resume)

        self.resume_banner.hide()
        container_layout.addWidget(self.resume_banner)

        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(4)
        self.header_layout.setContentsMargins(8, 4, 8, 4)

        self.cover_label = QLabel()
        self.cover_label.setFixedSize(42, 42)

        self.info_widget = QWidget()
        self.info_widget.setMinimumWidth(30)
        info_layout = QVBoxLayout(self.info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)

        self.title_label = MarqueeLabel("No Track Loaded")
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

        self.artist_label = MarqueeLabel("Add audio folders")
        self.artist_label.setFont(QFont("Segoe UI", 8))

        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.artist_label)

        self.folder_btn = self.create_icon_button("folder")
        self.lock_btn = self.create_icon_button("lock_open")
        self.circle_mode_btn = self.create_icon_button("circle_mode")
        self.close_btn = self.create_icon_button("close")

        self.header_layout.addWidget(self.cover_label)
        self.header_layout.addWidget(self.info_widget, stretch=1)
        self.header_layout.addWidget(self.folder_btn)
        self.header_layout.addWidget(self.lock_btn)
        self.header_layout.addWidget(self.circle_mode_btn)
        self.header_layout.addWidget(self.close_btn)

        container_layout.addLayout(self.header_layout)

        seek_layout = QVBoxLayout()
        seek_layout.setSpacing(2)

        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 0)
        self.seek_slider.setFixedHeight(14)

        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("0:00")
        self.remaining_time_label = QLabel("- 0:00")

        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.remaining_time_label)

        seek_layout.addWidget(self.seek_slider)
        seek_layout.addLayout(time_layout)

        container_layout.addLayout(seek_layout)

        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(8)

        self.repeat_btn = self.create_icon_button("repeat")
        self.prev_btn = self.create_icon_button("prev")
        self.play_btn = self.create_icon_button("play")
        self.next_btn = self.create_icon_button("next")

        self.size_grip = QSizeGrip(self)
        self.size_grip.setFixedSize(14, 14)

        controls_layout.addWidget(self.repeat_btn)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.prev_btn)
        controls_layout.addSpacing(12)
        controls_layout.addWidget(self.play_btn)
        controls_layout.addSpacing(12)
        controls_layout.addWidget(self.next_btn)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.size_grip)

        container_layout.addLayout(controls_layout)

        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("PlaylistWidget")
        self.playlist_widget.setMaximumHeight(0)
        self.playlist_widget.hide()
        container_layout.addWidget(self.playlist_widget)

        main_layout.addWidget(self.container)

        self.mini_player = AnimatedMiniPlayer(self, parent=self)
        self.mini_player.hide()
        main_layout.addWidget(self.mini_player, alignment=Qt.AlignmentFlag.AlignLeft)

        self.playlist_anim = QPropertyAnimation(self.playlist_widget, b"maximumHeight")
        self.playlist_anim.setDuration(300)
        self.playlist_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def setup_signals(self):
        self.folder_btn.clicked.connect(self.show_folder_menu)
        self.lock_btn.clicked.connect(self.toggle_lock)
        self.circle_mode_btn.clicked.connect(self.toggle_mini_mode)
        self.close_btn.clicked.connect(QApplication.quit)

        self.play_btn.clicked.connect(self.toggle_play)
        self.prev_btn.clicked.connect(self.play_previous)
        self.next_btn.clicked.connect(self.play_next)
        self.repeat_btn.clicked.connect(self.toggle_repeat)

        self.mini_player.restore_requested.connect(self.toggle_mini_mode)
        self.mini_player.toggle_play_requested.connect(self.toggle_play)
        self.mini_player.next_requested.connect(self.play_next)
        self.mini_player.prev_requested.connect(self.play_previous)
        self.mini_player.repeat_requested.connect(self.toggle_repeat)

        self.playlist_widget.itemClicked.connect(self.on_playlist_item_clicked)

        self.btn_accept_resume.clicked.connect(self.accept_resume)
        self.btn_dismiss_resume.clicked.connect(self.resume_banner.hide)

        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.playbackStateChanged.connect(self.handle_state_change)

        self.seek_slider.sliderMoved.connect(self.set_position)
        self.seek_slider.sliderReleased.connect(
            lambda: self.set_position(self.seek_slider.value())
        )

    def create_icon_button(self, icon_name):
        btn = QPushButton()
        btn.setFixedSize(22, 22)
        btn.setProperty("icon_name", icon_name)
        return btn

    def apply_dark_theme(self):
        text_color = "#FFFFFF"
        subtext_color = "rgba(255, 255, 255, 0.65)"
        bg_css = "rgba(20, 20, 28, 0.45)"
        border_css = "rgba(255, 255, 255, 0.20)"
        hover_bg = "rgba(255, 255, 255, 0.15)"

        self.container.setStyleSheet(f"""
            #GlassContainer {{
                background: {bg_css};
                border: 0.5px solid {border_css};
                border-radius: 4px;
            }}
            QLabel {{
                color: {text_color};
            }}
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
            }}
            QSlider::groove:horizontal {{
                height: 3px;
                background: rgba(255, 255, 255, 0.25);
                border-radius: 1px;
            }}
            QSlider::sub-page:horizontal {{
                background: #FFFFFF;
                border-radius: 1px;
            }}
            QSlider::handle:horizontal {{
                background: #FFFFFF;
                width: 8px;
                height: 8px;
                margin: -2px 0;
                border-radius: 4px;
            }}
            QListWidget {{
                background: transparent;
                border: none;
                color: {text_color};
                font-size: 11px;
            }}
            QListWidget::item {{
                padding: 4px;
                border-radius: 4px;
            }}
            QListWidget::item:hover {{
                background: {hover_bg};
            }}
            QListWidget::item:selected {{
                background: rgba(255, 255, 255, 0.2);
            }}
        """)

        self.artist_label.setStyleSheet(f"color: {subtext_color};")
        self.current_time_label.setStyleSheet(f"color: {subtext_color}; font-size: 9px;")
        self.remaining_time_label.setStyleSheet(f"color: {subtext_color}; font-size: 9px;")

        for btn in self.findChildren(QPushButton):
            icon_name = btn.property("icon_name")
            if icon_name:
                icon_color = text_color
                if icon_name == "repeat" and not self.repeat_mode:
                    icon_color = "#8A8A90"
                icon_size = btn.property("icon_size") or 14
                btn.setIconSize(QSize(icon_size, icon_size))
                btn.setIcon(render_svg_pixmap(icon_name, color=icon_color, size=icon_size))

        if self.current_index < 0 or (self.playlist and self.playlist[self.current_index] not in self.cover_cache):
            worker = MetadataWorker("")
            default_pix = worker.get_default_cover()
            self.cover_label.setPixmap(self.get_rounded_pixmap(default_pix, 8))
            self.mini_player.disc.set_cover(default_pix)

    def update_window_flags(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.show()
        apply_windows_acrylic(self.winId(), enable=True, blur_opacity=0xBB, round_corners=True)

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        self.update_window_flags()

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            if self.playlist and self.current_index >= 0:
                if not self.player.source().isValid():
                    self.load_track_fast(self.playlist[self.current_index], auto_play=False)
                self.player.play()

    def play_previous(self):
        if self.playlist and self.current_index > 0:
            self.current_index -= 1
            self.load_track_fast(self.playlist[self.current_index])
        else:
            self.player.setPosition(0)

    def play_next(self):
        if self.playlist:
            if self.repeat_mode:
                self.player.setPosition(0)
                self.player.play()
            elif self.current_index < len(self.playlist) - 1:
                self.current_index += 1
                self.load_track_fast(self.playlist[self.current_index])

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        self.apply_dark_theme()

    def update_position(self, position):
        self.seek_slider.setValue(position)
        self.current_time_label.setText(self.format_time(position))
        
        duration = self.player.duration()
        if duration > 0:
            remaining = duration - position
            self.remaining_time_label.setText(f"- {self.format_time(remaining)}")
            pct = position / duration
            self.mini_player.disc.set_progress(pct)
            
            if hasattr(self.mini_player, 'mini_seek_slider'):
                self.mini_player.mini_seek_slider.setValue(position)
            if hasattr(self.mini_player, 'time_label'):
                self.mini_player.time_label.setText(self.format_time(position))
                self.mini_player.duration_label.setText(self.format_time(duration))
                
            if position >= duration and duration > 0:
                self.play_next()

    def update_duration(self, duration):
        self.seek_slider.setRange(0, duration)
        if hasattr(self, 'mini_player') and hasattr(self.mini_player, 'mini_seek_slider'):
            self.mini_player.mini_seek_slider.setRange(0, duration)
            self.mini_player.duration_label.setText(self.format_time(duration))

    def handle_state_change(self, state):
        is_playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        icon_name = "pause" if is_playing else "play"
        
        main_size = self.play_btn.property("icon_size") or 14
        self.play_btn.setIcon(render_svg_pixmap(icon_name, color="#FFFFFF", size=main_size))
        self.play_btn.setProperty("icon_name", icon_name)

        if hasattr(self, 'mini_player') and hasattr(self.mini_player, 'btn_play'):
            mini_size = self.mini_player.btn_play.property("icon_size") or 14
            self.mini_player.btn_play.setIcon(render_svg_pixmap(icon_name, color="#FFFFFF", size=mini_size))
            self.mini_player.btn_play.setProperty("icon_name", icon_name)

    def set_position(self, position):
        self.player.setPosition(position)

    def format_time(self, ms):
        seconds = int(ms / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"

    def save_state(self):
        saved_folders = list(self.folders.keys())
        folder_paths = [os.path.dirname(self.folders[k][0]) for k in saved_folders if self.folders[k]]

        self.settings.setValue("folders", folder_paths)
        if self.current_folder:
            self.settings.setValue("last_folder", self.current_folder)
        self.settings.setValue("last_index", self.current_index)
        self.settings.setValue("last_position", self.player.position())

    def load_saved_state(self):
        folder_paths = self.settings.value("folders", [])
        if isinstance(folder_paths, str):
            folder_paths = [folder_paths]

        valid_exts = ('.mp3', '.wav', '.flac', '.m4a', '.aac')
        for fpath in folder_paths:
            if os.path.exists(fpath):
                files = [os.path.join(fpath, f) for f in os.listdir(fpath) if f.lower().endswith(valid_exts)]
                if files:
                    fname = os.path.basename(fpath)
                    self.folders[fname] = files

        last_folder = self.settings.value("last_folder", None)
        last_index = int(self.settings.value("last_index", 0))
        last_pos = int(self.settings.value("last_position", 0))

        if last_folder and last_folder in self.folders:
            self.select_folder(last_folder, auto_play=False)
            if 0 <= last_index < len(self.playlist):
                self.current_index = last_index
                file_path = self.playlist[self.current_index]

                name, _ = os.path.splitext(os.path.basename(file_path))
                self.title_label.setText(name)
                self.mini_player.title_label.setText(name)
                self.artist_label.setText(f"Folder: {self.current_folder}")
                self.mini_player.folder_label.setText(f"Folder: {self.current_folder}")
                self.playlist_widget.setCurrentRow(self.current_index)

                self.player.setSource(QUrl.fromLocalFile(file_path))

                self.worker = MetadataWorker(file_path)
                self.worker.loaded.connect(self.on_metadata_loaded)
                self.worker.start()

                if last_pos > 3000:
                    self.pending_resume_position = last_pos
                    time_str = self.format_time(last_pos)
                    self.resume_label.setText(f"Resume from {time_str}?")
                    self.resume_banner.show()

    def accept_resume(self):
        if self.playlist and self.current_index >= 0:
            self.load_track_fast(self.playlist[self.current_index], auto_play=True)
            if self.pending_resume_position > 0:
                self.player.setPosition(self.pending_resume_position)
        self.resume_banner.hide()

    def closeEvent(self, event):
        self.save_state()
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.width() < 260:
            self.info_widget.hide()
            self.header_layout.setSpacing(8)
        else:
            self.info_widget.show()
            self.header_layout.setSpacing(8)

        if self.height() > 220 and not self.is_mini_mode:
            if not self._playlist_visible:
                self._playlist_visible = True
                self.playlist_widget.show()
                self.playlist_anim.stop()
                self.playlist_anim.setStartValue(self.playlist_widget.maximumHeight())
                self.playlist_anim.setEndValue(300)
                self.playlist_anim.start()
        else:
            if self._playlist_visible:
                self._playlist_visible = False
                self.playlist_anim.stop()
                self.playlist_anim.setStartValue(self.playlist_widget.maximumHeight())
                self.playlist_anim.setEndValue(0)
                self.playlist_anim.start()

    def showEvent(self, event):
        super().showEvent(event)
        apply_windows_acrylic(self.winId(), enable=True, blur_opacity=0xBB, round_corners=True)

    def show_folder_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(20, 20, 25, 0.90);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 4px;
            }
        """)

        add_action = QAction("➕ Add New Folder", self)
        add_action.triggered.connect(self.add_folder_dialog)
        menu.addAction(add_action)

        if self.folders:
            menu.addSeparator()
            for folder_name in self.folders.keys():
                action = QAction(f"📁 {folder_name}", self)
                action.setCheckable(True)
                if folder_name == self.current_folder:
                    action.setChecked(True)
                action.triggered.connect(lambda checked, f=folder_name: self.select_folder(f))
                menu.addAction(action)

        menu.exec(self.folder_btn.mapToGlobal(QPoint(0, self.folder_btn.height())))

    def add_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Audio Folder")
        if folder:
            valid_exts = ('.mp3', '.wav', '.flac', '.m4a', '.aac')
            files = [
                os.path.join(folder, f) for f in os.listdir(folder)
                if f.lower().endswith(valid_exts)
            ]
            if files:
                folder_name = os.path.basename(folder)
                self.folders[folder_name] = files
                self.select_folder(folder_name)

    def select_folder(self, folder_name, auto_play=True):
        self.current_folder = folder_name
        self.playlist = self.folders[folder_name]
        self.current_index = 0

        self.playlist_widget.clear()
        for idx, f in enumerate(self.playlist, 1):
            name = os.path.splitext(os.path.basename(f))[0]
            self.playlist_widget.addItem(QListWidgetItem(f"{idx}.  {name}"))

        if auto_play:
            self.load_track_fast(self.playlist[self.current_index], auto_play=True)

    def on_playlist_item_clicked(self, item):
        row = self.playlist_widget.row(item)
        if 0 <= row < len(self.playlist):
            self.current_index = row
            self.load_track_fast(self.playlist[self.current_index], auto_play=True)

    def load_track_fast(self, file_path, auto_play=True):
        self.player.setSource(QUrl.fromLocalFile(file_path))
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)

        self.title_label.setText(name)
        self.mini_player.title_label.setText(name)
        self.artist_label.setText(f"Folder: {self.current_folder}")
        self.mini_player.folder_label.setText(f"Folder: {self.current_folder}")
        self.playlist_widget.setCurrentRow(self.current_index)

        if file_path in self.cover_cache:
            pix = self.cover_cache[file_path]
            self.cover_label.setPixmap(self.get_rounded_pixmap(pix, 8))
            self.mini_player.disc.set_cover(pix)
        else:
            self.worker = MetadataWorker(file_path)
            self.worker.loaded.connect(self.on_metadata_loaded)
            self.worker.start()

        if auto_play:
            self.player.play()

    @Slot(str, QPixmap, str)
    def on_metadata_loaded(self, file_path, pixmap, title):
        self.cover_cache[file_path] = pixmap
        if self.playlist and self.playlist[self.current_index] == file_path:
            self.cover_label.setPixmap(self.get_rounded_pixmap(pixmap, 8))
            self.mini_player.disc.set_cover(pixmap)

    def get_rounded_pixmap(self, pixmap, radius):
        rounded = QPixmap(42, 42)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, 42, 42), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, 42, 42, pixmap)
        painter.end()
        return rounded

    def sync_mini_window_size(self, tray_width=None):
        if not self.is_mini_mode:
            return

        h = self.mini_player.mini_height
        disc = self.mini_player.circle_size
        if tray_width is None:
            tray_width = max(0, self.mini_player.tray_widget.maximumWidth())
        w = max(disc, int(tray_width))

        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)
        self.resize(w, h)
        self.mini_player.setFixedSize(w, h)
        self.mini_player.tray_widget.setGeometry(0, 0, w, h)
        self.mini_player.circle_btn.move(0, max(0, (h - disc) // 2))
        self.mini_player.circle_btn.raise_()

    def toggle_mini_mode(self):
        self.is_mini_mode = not self.is_mini_mode
        if self.is_mini_mode:
            self.container.hide()
            self.setStyleSheet("background: transparent; border: none;")
            self.mini_player.show()
            self.mini_player.circle_btn.raise_()
            self.mini_player._animate_to(True)
            self.sync_mini_window_size(self.mini_player._pill_width)
        else:
            self.mini_player.hide()
            self.container.show()
            self.setStyleSheet("")
            self.setMinimumSize(240, 160)
            self.setMaximumSize(16777215, 16777215)
            self.resize(360, 200)

            if not self.is_locked:
                self.size_grip.show()

        self.update_window_flags()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_locked:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self.is_locked:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = FinalGlassMusicPlayer()
    player.show()
    sys.exit(app.exec())
