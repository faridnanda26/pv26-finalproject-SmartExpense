import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QSequentialAnimationGroup, QEasingCurve, Signal, QPauseAnimation
from PySide6.QtGui import QPixmap

class SplashScreen(QWidget):
    animasi_selesai = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("splashPage")
        
        self.showFullScreen()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        self.lblLogo = QLabel()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "assets", "logo.png")
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            self.lblLogo.setPixmap(pixmap.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblLogo.setAlignment(Qt.AlignCenter)
        self.lblLogo.setObjectName("splashLogo")
        layout.addWidget(self.lblLogo)

        self.lblTitle = QLabel("SMART EXPENSE")
        self.lblTitle.setObjectName("splashTitle")
        self.lblTitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lblTitle)

        self.lblSubtitle = QLabel("AI-POWERED EXPENSE TRACKER\n© 2026 TIM INFORMATIKA UNRAM")
        self.lblSubtitle.setObjectName("splashSubtitle")
        self.lblSubtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lblSubtitle)

        # ============================================================================
        # ARSITEKTUR ANIMASI 
        # ============================================================================
        
        # Pasang lapisan Opacity Effect untuk menduplikasi efek transparansi 
        self.opacity_logo = QGraphicsOpacityEffect(self.lblLogo)
        self.opacity_title = QGraphicsOpacityEffect(self.lblTitle)
        self.opacity_subtitle = QGraphicsOpacityEffect(self.lblSubtitle)
        
        self.lblLogo.setGraphicsEffect(self.opacity_logo)
        self.lblTitle.setGraphicsEffect(self.opacity_title)
        self.lblSubtitle.setGraphicsEffect(self.opacity_subtitle)

        # STAGE 1: ANIMASI FADE-IN BERSAMAAN
        self.anim_logo_in = QPropertyAnimation(self.opacity_logo, b"opacity")
        self.anim_logo_in.setDuration(1500)
        self.anim_logo_in.setStartValue(0.0)
        self.anim_logo_in.setEndValue(1.0)
        self.anim_logo_in.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim_title_in = QPropertyAnimation(self.opacity_title, b"opacity")
        self.anim_title_in.setDuration(1500)
        self.anim_title_in.setStartValue(0.0)
        self.anim_title_in.setEndValue(1.0)
        self.anim_title_in.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim_subtitle_in = QPropertyAnimation(self.opacity_subtitle, b"opacity")
        self.anim_subtitle_in.setDuration(1800)
        self.anim_subtitle_in.setStartValue(0.0)
        self.anim_subtitle_in.setEndValue(1.0)
        self.anim_subtitle_in.setEasingCurve(QEasingCurve.InOutQuad)

        self.grup_fade_in = QParallelAnimationGroup()
        self.grup_fade_in.addAnimation(self.anim_logo_in)
        self.grup_fade_in.addAnimation(self.anim_title_in)
        self.grup_fade_in.addAnimation(self.anim_subtitle_in)

        # STAGE 2: ANIMASI FADE-OUT 
        self.anim_logo_out = QPropertyAnimation(self.opacity_logo, b"opacity")
        self.anim_logo_out.setDuration(800)
        self.anim_logo_out.setStartValue(1.0)
        self.anim_logo_out.setEndValue(0.0)

        self.anim_title_out = QPropertyAnimation(self.opacity_title, b"opacity")
        self.anim_title_out.setDuration(800)
        self.anim_title_out.setStartValue(1.0)
        self.anim_title_out.setEndValue(0.0)

        self.anim_subtitle_out = QPropertyAnimation(self.opacity_subtitle, b"opacity")
        self.anim_subtitle_out.setDuration(800)
        self.anim_subtitle_out.setStartValue(1.0)
        self.anim_subtitle_out.setEndValue(0.0)

        self.grup_fade_out = QParallelAnimationGroup()
        self.grup_fade_out.addAnimation(self.anim_logo_out)
        self.grup_fade_out.addAnimation(self.anim_title_out)
        self.grup_fade_out.addAnimation(self.anim_subtitle_out)

        # ============================================================================
        # MASTER ALUR ANIMASI
        # ============================================================================
        self.master_cinema = QSequentialAnimationGroup()
        self.master_cinema.addAnimation(self.grup_fade_in)
        
        self.jeda_layar = QPauseAnimation(1200) # Jeda diam 1.2 detik
        self.master_cinema.addAnimation(self.jeda_layar)
        
        self.master_cinema.addAnimation(self.grup_fade_out)
        
        # Hubungkan ketukan akhir animasi master langsung untuk memicu pemindahan halaman login
        self.master_cinema.finished.connect(self.Selesai)
        
        self.master_cinema.start()

    def Selesai(self):
        self.animasi_selesai.emit()
        self.close()