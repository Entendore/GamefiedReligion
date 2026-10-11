import sys
import json
import os
import random
import math
from datetime import datetime, date, timedelta
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                               QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                               QProgressBar, QMessageBox, QCheckBox, QFrame, 
                               QScrollArea, QTextEdit, QSpinBox, QGridLayout,
                               QDialog, QSizePolicy, QComboBox, QLineEdit,
                               QInputDialog, QFileDialog, QTimeEdit, QSystemTrayIcon,
                               QMenu, QSlider, QDoubleSpinBox, QDateEdit, QTableWidget,
                               QTableWidgetItem, QHeaderView, QTimeEdit)
from PySide6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, 
                            QSize, QTime, QDate)
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QAction
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

try:
    import pyqtgraph as pg
    pg.setConfigOptions(antialias=True)
    HAS_PYQTGRAPH = True
except ImportError:
    HAS_PYQTGRAPH = False
    print("⚠️ pyqtgraph not installed. Charts disabled. Run: pip install pyqtgraph")

# ==========================================
# CONSTANTS & CONTENT
# ==========================================
SAVE_FILE = "soul_journey_save.json"

DAILY_QUOTES = [
    ("\"Be still, and know that I am God.\"", "— Psalm 46:10"),
    ("\"God is the light of the heavens and the earth.\"", "— Quran 24:35"),
    ("\"You have the right to work, but never to the fruit of work.\"", "— Bhagavad Gita 2.47"),
    ("\"The Tao that can be told is not the eternal Tao.\"", "— Tao Te Ching"),
    ("\"Peace comes from within. Do not seek it without.\"", "— Buddha"),
    ("\"Let yourself be silently drawn by the strange pull of what you really love.\"", "— Rumi"),
    ("\"Love all, trust a few, do wrong to none.\"", "— William Shakespeare"),
    ("\"The soul is healed by being with children.\"", "— Fyodor Dostoevsky"),
    ("\"Wherever you go, go with all your heart.\"", "— Confucius"),
    ("\"He who has a why to live can bear almost any how.\"", "— Friedrich Nietzsche"),
    ("\"The prayer of the righteous is powerful and effective.\"", "— James 5:16"),
    ("\"Verily, with hardship comes ease.\"", "— Quran 94:6"),
    ("\"The mind is everything. What you think you become.\"", "— Buddha"),
    ("\"Silence is the language of God, all else is poor translation.\"", "— Rumi"),
]

DIVINE_EVENTS = [
    {"name": "✨ Divine Inspiration", "desc": "A moment of clarity fills your soul.", "effect": "xp", "value": 75},
    {"name": "🕊️ Peace of Mind", "desc": "Inner tranquility grants you wisdom.", "effect": "virtue", "virtue": "Wisdom", "value": 25},
    {"name": "💝 Overflowing Grace", "desc": "Compassion flows through you.", "effect": "virtue", "virtue": "Compassion", "value": 25},
    {"name": "🔥 Sacred Fire", "desc": "Your discipline is strengthened.", "effect": "virtue", "virtue": "Discipline", "value": 25},
    {"name": "🌙 Night Vigil Blessing", "desc": "Your devotion is noticed.", "effect": "virtue", "virtue": "Devotion", "value": 25},
    {"name": "🎁 Unexpected Mercy", "desc": "A blessing doubles your next XP gain.", "effect": "double_xp", "value": 1},
]

ACHIEVEMENTS = [
    {"id": "first_step", "name": "First Step", "icon": "🌱", "desc": "Begin your journey", "cond": lambda s: s.data["level"] >= 1 and s.data["xp"] > 0},
    {"id": "seeker_5", "name": "Devoted Seeker", "icon": "🔍", "desc": "Reach Level 5", "cond": lambda s: s.data["level"] >= 5},
    {"id": "adept_15", "name": "Spiritual Adept", "icon": "⚡", "desc": "Reach Level 15", "cond": lambda s: s.data["level"] >= 15},
    {"id": "master_30", "name": "Illuminated Master", "icon": "👑", "desc": "Reach Level 30", "cond": lambda s: s.data["level"] >= 30},
    {"id": "streak_7", "name": "Week Warrior", "icon": "🔥", "desc": "7-day streak", "cond": lambda s: s.data["streak"] >= 7},
    {"id": "streak_30", "name": "Monthly Monk", "icon": "🌙", "desc": "30-day streak", "cond": lambda s: s.data["streak"] >= 30},
    {"id": "wise", "name": "Keeper of Wisdom", "icon": "📚", "desc": "100 Wisdom", "cond": lambda s: s.data["virtues"]["Wisdom"] >= 100},
    {"id": "compassionate", "name": "Heart of Gold", "icon": "💖", "desc": "100 Compassion", "cond": lambda s: s.data["virtues"]["Compassion"] >= 100},
    {"id": "disciplined", "name": "Iron Will", "icon": "⚔️", "desc": "100 Discipline", "cond": lambda s: s.data["virtues"]["Discipline"] >= 100},
    {"id": "devout", "name": "Divine Devotion", "icon": "🕯️", "desc": "100 Devotion", "cond": lambda s: s.data["virtues"]["Devotion"] >= 100},
    {"id": "journaler", "name": "Scribe of the Soul", "icon": "✍️", "desc": "10 journal entries", "cond": lambda s: len(s.data.get("journal", [])) >= 10},
    {"id": "meditator", "name": "Still Mind", "icon": "🧘", "desc": "10 meditations", "cond": lambda s: s.data.get("meditations", 0) >= 10},
    {"id": "resistor", "name": "Temptation Slayer", "icon": "🛡️", "desc": "Resist 20 times", "cond": lambda s: s.data.get("resists", 0) >= 20},
    {"id": "balanced", "name": "The Balanced Path", "icon": "☯️", "desc": "All virtues 50+", "cond": lambda s: all(v >= 50 for v in s.data["virtues"].values())},
    {"id": "beads_100", "name": "Bead Master", "icon": "📿", "desc": "100 beads counted", "cond": lambda s: s.data.get("beads_total", 0) >= 100},
    {"id": "fast_complete", "name": "Fulfilled Fast", "icon": "🌾", "desc": "Complete a fast", "cond": lambda s: s.data.get("fasts_completed", 0) >= 1},
    {"id": "giver", "name": "Generous Heart", "icon": "🎁", "desc": "10 charity acts", "cond": lambda s: len(s.data.get("charity", [])) >= 10},
    {"id": "released", "name": "Letting Go", "icon": "🕊️", "desc": "Release 5 burdens", "cond": lambda s: s.data.get("releases", 0) >= 5},
    {"id": "pilgrim", "name": "Sacred Pilgrim", "icon": "🗺️", "desc": "Visit 3 sacred sites", "cond": lambda s: len(s.data.get("pilgrimages", [])) >= 3},
    {"id": "devoted_year", "name": "Year of Faith", "icon": "📅", "desc": "Track 100 days", "cond": lambda s: len(s.data.get("calendar", {})) >= 100},
]

SCRIPTURE_BOOKS = {
    "Bible (OT)": ["Genesis", "Exodus", "Psalms", "Proverbs", "Isaiah", "Daniel"],
    "Bible (NT)": ["Matthew", "John", "Romans", "Ephesians", "Revelation"],
    "Quran": ["Al-Fatiha", "Al-Baqarah", "Al-Imran", "Ya-Sin", "Al-Mulk"],
    "Bhagavad Gita": ["Chapter 1", "Chapter 2", "Chapter 6", "Chapter 12", "Chapter 18"],
    "Tao Te Ching": ["Part 1 (1-37)", "Part 2 (38-81)"],
}

# Liturgical calendar - major holidays 2026-2027
LITURGICAL_HOLIDAYS = {
    "Christianity": [
        ("2026-04-05", "Easter Sunday", "🐣", "Resurrection of Christ"),
        ("2026-02-18", "Ash Wednesday", "✝️", "Beginning of Lent"),
        ("2026-12-25", "Christmas", "🎄", "Birth of Christ"),
        ("2026-11-29", "First Advent", "🕯️", "Beginning of Advent"),
        ("2027-03-28", "Easter 2027", "🐣", "Resurrection"),
        ("2027-04-04", "Pentecost 2027", "🕊️", "Holy Spirit"),
    ],
    "Islam": [
        ("2026-02-18", "Ramadan Begins", "🌙", "Month of fasting"),
        ("2026-03-20", "Eid al-Fitr", "🕌", "Festival of breaking fast"),
        ("2026-05-27", "Eid al-Adha", "🐑", "Festival of sacrifice"),
        ("2026-09-16", "Islamic New Year", "⭐", "1 Muharram 1448"),
        ("2027-02-08", "Ramadan 2027", "🌙", "Month of fasting"),
    ],
    "Judaism": [
        ("2026-04-01", "Passover (Pesach)", "🕎", "Exodus from Egypt"),
        ("2026-09-13", "Rosh Hashanah", "🍎", "Jewish New Year 5787"),
        ("2026-09-22", "Yom Kippur", "🕯️", "Day of Atonement"),
        ("2026-09-27", "Sukkot", "🌿", "Feast of Tabernacles"),
        ("2026-12-14", "Hanukkah Begins", "🕎", "Festival of Lights"),
    ],
    "Hinduism": [
        ("2026-03-03", "Holi", "🌸", "Festival of Colors"),
        ("2026-08-18", "Janmashtami", "🪈", "Birth of Krishna"),
        ("2026-11-08", "Diwali", "🪔", "Festival of Lights"),
        ("2027-03-22", "Holi 2027", "🌸", "Festival of Colors"),
    ],
    "Buddhism": [
        ("2026-05-02", "Vesak", "🪷", "Buddha's birth/enlightenment"),
        ("2026-07-29", "Asalha Puja", "☸️", "Dharma Day"),
        ("2026-12-26", "Bodhi Day", "🌳", "Enlightenment of Buddha"),
    ],
    "Taoism": [
        ("2026-02-17", "Chinese New Year", "🐉", "Year of the Horse"),
        ("2026-04-05", "Qingming", "🌱", "Tomb Sweeping Day"),
        ("2026-06-19", "Dragon Boat", "🐲", "Duanwu Festival"),
    ],
    "Sikhism": [
        ("2026-03-30", "Hola Mohalla", "⚔️", "Festival of colors"),
        ("2026-11-08", "Gurpurab", "🙏", "Guru Nanak's birthday"),
        ("2026-04-14", "Vaisakhi", "🌾", "Khalsa founding"),
    ],
    "Secular/Spiritual": [
        ("2026-06-21", "Summer Solstice", "☀️", "Longest day"),
        ("2026-09-22", "Autumn Equinox", "🍂", "Equal day & night"),
        ("2026-12-21", "Winter Solstice", "❄️", "Shortest day"),
        ("2027-03-20", "Spring Equinox", "🌸", "Equal day & night"),
    ],
}

# ==========================================
# GAME STATE
# ==========================================
class GameState:
    def __init__(self):
        self.data = self.load()
        self.check_daily_reset()
        self.double_xp_active = False

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    data = json.load(f)
                    defaults = self.default_data()
                    for k, v in defaults.items():
                        data.setdefault(k, v)
                    return data
            except json.JSONDecodeError:
                pass
        return self.default_data()

    def save(self):
        with open(SAVE_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def default_data(self):
        return {
            "xp": 0, "total_xp": 0, "level": 1, "streak": 0,
            "last_login": str(date.today()),
            "last_journal_date": None, "last_resist_date": None,
            "streak_shield_used": False,
            "virtues": {"Wisdom": 0, "Compassion": 0, "Discipline": 0, "Devotion": 0},
            "quests": [
                {"name": "Morning Devotion", "desc": "Pray or meditate for 15 mins", "xp": 20, "virtue": "Devotion", "done": False},
                {"name": "Sacred Study", "desc": "Read holy texts or scriptures", "xp": 30, "virtue": "Wisdom", "done": False},
                {"name": "Act of Charity", "desc": "Help someone in need or donate", "xp": 50, "virtue": "Compassion", "done": False},
                {"name": "Fasting / Discipline", "desc": "Fast or deny a worldly pleasure", "xp": 40, "virtue": "Discipline", "done": False}
            ],
            "journal": [], "meditations": 0, "resists": 0,
            "achievements": [], "calendar": {},
            "beads_total": 0, "beads_session": 0, "beads_target": 33,
            "beads_phrase": "SubhanAllah",
            "scripture": {},
            "fasts": [], "fasts_completed": 0,
            "charity": [],
            "custom_rituals": [],
            "releases": 0,
            "mantra": "Om", "mantra_count": 0,
            "settings": {"theme": "dark", "tradition": "Universal"},
            # NEW FIELDS
            "virtue_history": {},  # {date: {virtue: value}}
            "pilgrimages": [],  # [{name, date, location, notes, rating}]
            "prayer_times": {
                "enabled": False,
                "times": ["05:00", "12:30", "15:30", "18:30", "21:00"]
            },
            "ambient_audio_path": None,
            "partner_name": "",
        }

    def check_daily_reset(self):
        today = date.today()
        last = datetime.strptime(self.data["last_login"], "%Y-%m-%d").date()
        delta = (today - last).days
        
        if delta == 1:
            self.data["streak"] += 1
            self.data["streak_shield_used"] = False
        elif delta == 2 and not self.data.get("streak_shield_used", False):
            self.data["streak_shield_used"] = True
        elif delta > 1:
            self.data["streak"] = 1
            self.data["streak_shield_used"] = False
            
        if delta >= 1:
            self.data["last_login"] = str(today)
            for q in self.data["quests"]:
                q["done"] = False
            self.data["last_journal_date"] = None
            self.data["last_resist_date"] = None
            self.data["beads_session"] = 0
            self.snapshot_virtues()
            self.save()

    def snapshot_virtues(self):
        """Record today's virtue values for charting."""
        today_str = str(date.today())
        self.data.setdefault("virtue_history", {})[today_str] = dict(self.data["virtues"])
        # Keep only last 365 days
        keys = sorted(self.data["virtue_history"].keys())
        if len(keys) > 365:
            for k in keys[:-365]:
                del self.data["virtue_history"][k]

    def mark_activity_today(self):
        today_str = str(date.today())
        self.data["calendar"][today_str] = self.data["calendar"].get(today_str, 0) + 1
        self.save()

    def add_xp(self, amount, virtue=None, source=""):
        if self.double_xp_active:
            amount *= 2
            self.double_xp_active = False
        
        self.data["xp"] += amount
        self.data["total_xp"] = self.data.get("total_xp", 0) + amount
        if virtue and virtue in self.data["virtues"]:
            self.data["virtues"][virtue] += amount
        
        self.mark_activity_today()
        
        leveled_up = False
        new_level = self.data["level"]
        xp_needed = self.data["level"] * 100
        while self.data["xp"] >= xp_needed:
            self.data["xp"] -= xp_needed
            self.data["level"] += 1
            new_level = self.data["level"]
            leveled_up = True
            xp_needed = self.data["level"] * 100
            
        self.save()
        return {"leveled": leveled_up, "new_level": new_level, "amount": amount}

    def get_title(self):
        lvl = self.data["level"]
        if lvl < 5: return "Seeker"
        if lvl < 15: return "Acolyte"
        if lvl < 30: return "Adept"
        if lvl < 50: return "Illuminated"
        return "Ascended Master"

    def check_new_achievements(self):
        newly_unlocked = []
        for ach in ACHIEVEMENTS:
            if ach["id"] not in self.data["achievements"] and ach["cond"](self):
                self.data["achievements"].append(ach["id"])
                newly_unlocked.append(ach)
        if newly_unlocked:
            self.save()
        return newly_unlocked

    def get_daily_quote(self):
        day_of_year = date.today().timetuple().tm_yday
        return DAILY_QUOTES[day_of_year % len(DAILY_QUOTES)]

    def get_moon_phase(self):
        ref = datetime(2000, 1, 6, 18, 14)
        now = datetime.now()
        diff = (now - ref).total_seconds()
        lunar_cycle = 29.53058867 * 24 * 3600
        phase = (diff % lunar_cycle) / lunar_cycle
        if phase < 0.0625: return "New Moon", "🌑", 0
        if phase < 0.1875: return "Waxing Crescent", "🌒", int(phase / 0.25 * 100)
        if phase < 0.3125: return "First Quarter", "🌓", 50
        if phase < 0.4375: return "Waxing Gibbous", "🌔", int(phase / 0.5 * 100)
        if phase < 0.5625: return "Full Moon", "🌕", 100
        if phase < 0.6875: return "Waning Gibbous", "🌖", int((1 - phase) / 0.5 * 100)
        if phase < 0.8125: return "Last Quarter", "🌗", 50
        if phase < 0.9375: return "Waning Crescent", "🌘", int((1 - phase) / 0.25 * 100)
        return "New Moon", "🌑", 0


# ==========================================
# STYLESHEET
# ==========================================
STYLESHEET = """
    QMainWindow { background-color: #0f0f17; }
    QTabWidget::pane { border: 1px solid #d4af37; background: #16161f; border-radius: 5px; }
    QTabBar::tab { 
        background: #1e1e2a; color: #a0a0b0; padding: 10px 14px; 
        border: 1px solid #2a2a3a; border-bottom: none; 
        border-top-left-radius: 8px; border-top-right-radius: 8px;
        font-size: 11px; font-weight: bold; margin-right: 2px;
    }
    QTabBar::tab:selected { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0c850, stop:1 #d4af37); color: #12121a; }
    QTabBar::tab:hover:!selected { background: #262633; color: #d4af37; }
    
    QLabel { color: #e0e0e0; font-size: 13px; }
    .Title { font-size: 22px; font-weight: bold; color: #f0c850; }
    .Subtitle { font-size: 13px; color: #a0a0b0; }
    
    QProgressBar {
        border: 1px solid #333; border-radius: 8px; text-align: center; 
        background-color: #1e1e2a; color: #e0e0e0; height: 18px; font-weight: bold;
    }
    QProgressBar::chunk { 
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0c850, stop:1 #d4af37); 
        border-radius: 7px; 
    }
    
    QPushButton {
        background-color: #1e1e2a; color: #e0e0e0; border: 1px solid #d4af37;
        border-radius: 10px; padding: 10px; font-size: 12px; font-weight: bold;
    }
    QPushButton:hover { background-color: #d4af37; color: #12121a; }
    QPushButton:pressed { background-color: #b5952f; }
    QPushButton:disabled { background-color: #16161f; color: #555; border: 1px solid #2a2a3a; }
    
    QCheckBox { color: #e0e0e0; spacing: 8px; font-size: 13px; }
    QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #d4af37; border-radius: 4px; background: #1e1e2a; }
    QCheckBox::indicator:checked { background: #d4af37; }
    
    QFrame#Card {
        background-color: #1e1e2a; border: 1px solid #2a2a3a; border-radius: 12px; padding: 12px;
    }
    QFrame#GoldCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2a2418, stop:1 #1e1e2a);
        border: 1px solid #d4af37; border-radius: 12px; padding: 12px;
    }
    QFrame#BeadCard {
        background: radial-gradient(circle at center, #2a2418 0%, #16161f 100%);
        border: 2px solid #d4af37; border-radius: 20px; padding: 20px;
    }
    
    QTextEdit, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit {
        background-color: #1e1e2a; color: #e0e0e0; border: 1px solid #2a2a3a;
        border-radius: 6px; padding: 6px; font-size: 12px;
    }
    QTextEdit:focus, QLineEdit:focus, QComboBox:focus { border: 1px solid #d4af37; }
    
    QScrollArea { border: none; }
    
    QTableWidget {
        background-color: #1e1e2a; color: #e0e0e0; 
        border: 1px solid #2a2a3a; gridline-color: #2a2a3a;
    }
    QTableWidget::item { padding: 6px; }
    QHeaderView::section {
        background-color: #2a2418; color: #f0c850; padding: 6px;
        border: 1px solid #2a2a3a; font-weight: bold;
    }
"""


# ==========================================
# FLOATING XP ANIMATION
# ==========================================
class FloatingXPLabel(QLabel):
    def __init__(self, text, parent, start_pos):
        super().__init__(text, parent)
        self.setStyleSheet("color: #f0c850; font-size: 18px; font-weight: bold; background: transparent;")
        self.adjustSize()
        self.move(start_pos.x() - self.width() // 2, start_pos.y())
        self.raise_()
        self.show()
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(1200)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(QPoint(self.pos().x(), self.pos().y() - 80))
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(self.deleteLater)
        self.anim.start()


# ==========================================
# PAGES
# ==========================================
class DashboardPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        self.lbl_title = QLabel()
        self.lbl_title.setProperty("class", "Title")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_title)

        info_row = QHBoxLayout()
        self.lbl_moon = QLabel()
        self.lbl_moon.setStyleSheet("font-size: 14px;")
        self.lbl_streak = QLabel()
        self.lbl_streak.setStyleSheet("font-size: 14px;")
        info_row.addWidget(self.lbl_moon)
        info_row.addStretch()
        info_row.addWidget(self.lbl_streak)
        layout.addLayout(info_row)

        # Today's holidays
        self.holidays_frame = QFrame()
        self.holidays_frame.setObjectName("GoldCard")
        h_layout = QVBoxLayout(self.holidays_frame)
        self.holidays_title = QLabel()
        self.holidays_title.setStyleSheet("font-size: 14px; color: #f0c850; font-weight: bold;")
        self.holidays_list = QLabel()
        self.holidays_list.setWordWrap(True)
        self.holidays_list.setStyleSheet("font-size: 12px; color: #e0e0e0;")
        h_layout.addWidget(self.holidays_title)
        h_layout.addWidget(self.holidays_list)
        layout.addWidget(self.holidays_frame)

        # Daily Quote Card
        quote_frame = QFrame()
        quote_frame.setObjectName("GoldCard")
        q_layout = QVBoxLayout(quote_frame)
        self.lbl_quote = QLabel()
        self.lbl_quote.setWordWrap(True)
        self.lbl_quote.setStyleSheet("font-size: 14px; font-style: italic; color: #f0c850;")
        self.lbl_quote.setAlignment(Qt.AlignCenter)
        self.lbl_quote_src = QLabel()
        self.lbl_quote_src.setAlignment(Qt.AlignRight)
        self.lbl_quote_src.setStyleSheet("font-size: 11px; color: #a0a0b0;")
        q_layout.addWidget(self.lbl_quote)
        q_layout.addWidget(self.lbl_quote_src)
        layout.addWidget(quote_frame)

        xp_frame = QFrame()
        xp_frame.setObjectName("Card")
        xp_layout = QVBoxLayout(xp_frame)
        self.lbl_level = QLabel()
        self.lbl_level.setProperty("class", "Subtitle")
        xp_layout.addWidget(self.lbl_level)
        self.bar_xp = QProgressBar()
        self.bar_xp.setMaximum(100)
        xp_layout.addWidget(self.bar_xp)
        layout.addWidget(xp_frame)

        virtues_frame = QFrame()
        virtues_frame.setObjectName("Card")
        v_layout = QGridLayout(virtues_frame)
        v_layout.addWidget(QLabel("<b>Virtues</b>"), 0, 0, 1, 4)
        self.lbl_virtues = {}
        icons = {"Wisdom": "📖", "Compassion": "🤲", "Discipline": "⚔️", "Devotion": "🕯️"}
        for i, (v, icon) in enumerate(icons.items()):
            lbl = QLabel()
            self.lbl_virtues[v] = lbl
            v_layout.addWidget(QLabel(f"{icon} {v}:"), 1 + i // 2, (i % 2) * 2)
            v_layout.addWidget(lbl, 1 + i // 2, (i % 2) * 2 + 1)
        layout.addWidget(virtues_frame)
        
        layout.addStretch()
        self.refresh()

    def refresh(self):
        self.lbl_title.setText(f"✦ {self.state.get_title()} ✦")
        phase_name, phase_emoji, illum = self.state.get_moon_phase()
        self.lbl_moon.setText(f"{phase_emoji} {phase_name} ({illum}%)")
        self.lbl_streak.setText(f"🔥 {self.state.data['streak']} Day Streak   •   ⭐ {self.state.data.get('total_xp', 0)} XP")
        
        # Today's holidays
        today_str = str(date.today())
        todays_holidays = []
        tradition = self.state.data.get("settings", {}).get("tradition", "Universal")
        traditions_to_show = [tradition] if tradition != "Universal" else LITURGICAL_HOLIDAYS.keys()
        for trad in traditions_to_show:
            for d, name, icon, desc in LITURGICAL_HOLIDAYS.get(trad, []):
                if d == today_str:
                    todays_holidays.append(f"{icon} <b>{name}</b> ({trad}) — {desc}")
        
        if todays_holidays:
            self.holidays_frame.show()
            self.holidays_title.setText("📅 Today's Holy Day")
            self.holidays_list.setText("<br>".join(todays_holidays))
        else:
            # Show upcoming
            upcoming = []
            for trad in traditions_to_show:
                for d, name, icon, desc in LITURGICAL_HOLIDAYS.get(trad, []):
                    if d > today_str and len(upcoming) < 3:
                        upcoming.append(f"{icon} <b>{name}</b> — {d} ({trad})")
            if upcoming:
                self.holidays_frame.show()
                self.holidays_title.setText("📅 Upcoming Holy Days")
                self.holidays_list.setText("<br>".join(upcoming))
            else:
                self.holidays_frame.hide()
        
        quote, src = self.state.get_daily_quote()
        self.lbl_quote.setText(quote)
        self.lbl_quote_src.setText(src)
        
        lvl = self.state.data["level"]
        xp = self.state.data["xp"]
        needed = lvl * 100
        self.lbl_level.setText(f"Level {lvl}  •  {xp} / {needed} XP")
        self.bar_xp.setValue(int((xp / needed) * 100))
        
        for v, val in self.state.data["virtues"].items():
            self.lbl_virtues[v].setText(f"<b>{val}</b>")


class PracticesPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("Daily Spiritual Practices")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        # Ambient Sound Player (NEW)
        audio_frame = QFrame()
        audio_frame.setObjectName("GoldCard")
        a_layout = QVBoxLayout(audio_frame)
        a_layout.addWidget(QLabel("<b>🎵 Ambient Sound Player</b>"))
        a_layout.addWidget(QLabel("Load your own meditation audio (bells, chanting, nature, etc.)"))
        
        audio_btn_row = QHBoxLayout()
        load_btn = QPushButton("📂 Load Audio File")
        load_btn.clicked.connect(self.load_audio)
        audio_btn_row.addWidget(load_btn)
        self.audio_name_lbl = QLabel("No file loaded")
        self.audio_name_lbl.setStyleSheet("color: #a0a0b0; font-style: italic;")
        audio_btn_row.addWidget(self.audio_name_lbl, 1)
        a_layout.addLayout(audio_btn_row)
        
        controls_row = QHBoxLayout()
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self.toggle_audio)
        self.play_btn.setEnabled(False)
        controls_row.addWidget(self.play_btn)
        
        self.loop_cb = QCheckBox("🔁 Loop")
        self.loop_cb.setChecked(True)
        controls_row.addWidget(self.loop_cb)
        controls_row.addStretch()
        
        controls_row.addWidget(QLabel("🔊"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(120)
        self.volume_slider.valueChanged.connect(self.change_volume)
        controls_row.addWidget(self.volume_slider)
        a_layout.addLayout(controls_row)
        
        scroll_layout.addWidget(audio_frame)
        
        # Audio player setup
        self.audio_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_player.setAudioOutput(self.audio_output)
        self.audio_player.mediaStatusChanged.connect(self.on_media_status)
        self.change_volume(50)

        practices = [
            ("🧘 Meditate / Pray", "Center your mind and connect with the Divine.", 20, "Devotion"),
            ("📖 Read Scripture", "Study sacred texts and ancient wisdom.", 30, "Wisdom"),
            ("🤲 Act of Charity", "Give to the poor, help a neighbor, or donate.", 50, "Compassion"),
            ("🚫 Fasting / Discipline", "Deny a worldly pleasure to strengthen the spirit.", 40, "Discipline")
        ]

        for name, desc, xp, virtue in practices:
            frame = QFrame()
            frame.setObjectName("Card")
            f_layout = QHBoxLayout(frame)
            text_layout = QVBoxLayout()
            lbl_name = QLabel(f"<b>{name}</b>")
            lbl_name.setStyleSheet("font-size: 14px; color: #f0c850;")
            lbl_desc = QLabel(desc)
            lbl_desc.setStyleSheet("color: #a0a0b0; font-size: 11px;")
            text_layout.addWidget(lbl_name)
            text_layout.addWidget(lbl_desc)
            btn = QPushButton(f"+{xp} XP")
            btn.setFixedWidth(90)
            btn.clicked.connect(lambda checked, x=xp, v=virtue, b=btn: self.do_practice(x, v, b))
            f_layout.addLayout(text_layout, 1)
            f_layout.addWidget(btn, 0, Qt.AlignRight | Qt.AlignVCenter)
            scroll_layout.addWidget(frame)

        # Meditation Timer
        timer_frame = QFrame()
        timer_frame.setObjectName("GoldCard")
        t_layout = QVBoxLayout(timer_frame)
        t_layout.addWidget(QLabel("<b>🧘 Meditation Timer</b>"))
        timer_row = QHBoxLayout()
        timer_row.addWidget(QLabel("Minutes:"))
        self.timer_spin = QSpinBox()
        self.timer_spin.setRange(1, 120)
        self.timer_spin.setValue(10)
        timer_row.addWidget(self.timer_spin)
        timer_row.addStretch()
        t_layout.addLayout(timer_row)
        self.timer_display = QLabel("00:00")
        self.timer_display.setAlignment(Qt.AlignCenter)
        self.timer_display.setStyleSheet("font-size: 40px; font-weight: bold; color: #f0c850; font-family: monospace;")
        t_layout.addWidget(self.timer_display)
        self.timer_btn = QPushButton("▶ Start Meditation")
        self.timer_btn.clicked.connect(self.toggle_timer)
        t_layout.addWidget(self.timer_btn)
        self.meditation_timer = QTimer()
        self.meditation_timer.timeout.connect(self.timer_tick)
        self.timer_remaining = 0
        self.timer_total = 0
        scroll_layout.addWidget(timer_frame)

        # Resist Temptation
        resist_frame = QFrame()
        resist_frame.setObjectName("Card")
        r_layout = QHBoxLayout(resist_frame)
        r_text = QVBoxLayout()
        r_text.addWidget(QLabel("<b>⚔️ Resisted Temptation?</b>"))
        r_text.addWidget(QLabel("Log when you overcome a worldly urge. +25 XP"))
        r_layout.addLayout(r_text, 1)
        self.resist_btn = QPushButton("+25 XP")
        self.resist_btn.setFixedWidth(90)
        self.resist_btn.clicked.connect(self.resist_temptation)
        r_layout.addWidget(self.resist_btn, 0, Qt.AlignRight | Qt.AlignVCenter)
        scroll_layout.addWidget(resist_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Load saved audio
        if self.state.data.get("ambient_audio_path"):
            path = self.state.data["ambient_audio_path"]
            if os.path.exists(path):
                self._load_audio_file(path)

    def load_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Audio", "", 
                                              "Audio Files (*.mp3 *.wav *.ogg *.m4a);;All Files (*)")
        if path:
            self._load_audio_file(path)
            self.state.data["ambient_audio_path"] = path
            self.state.save()

    def _load_audio_file(self, path):
        self.audio_player.setSource(QUrl.fromLocalFile(path))
        self.audio_name_lbl.setText(os.path.basename(path))
        self.audio_name_lbl.setStyleSheet("color: #f0c850;")
        self.play_btn.setEnabled(True)

    def toggle_audio(self):
        if self.audio_player.playbackState() == QMediaPlayer.PlayingState:
            self.audio_player.pause()
            self.play_btn.setText("▶ Play")
        else:
            if self.loop_cb.isChecked():
                self.audio_player.setLoops(QMediaPlayer.Infinite)
            else:
                self.audio_player.setLoops(1)
            self.audio_player.play()
            self.play_btn.setText("⏸ Pause")

    def change_volume(self, val):
        self.audio_output.setVolume(val / 100.0)

    def on_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_btn.setText("▶ Play")

    def toggle_timer(self):
        if self.meditation_timer.isActive():
            self.meditation_timer.stop()
            self.timer_btn.setText("▶ Start Meditation")
            self.timer_display.setText("00:00")
            self.timer_remaining = 0
        else:
            mins = self.timer_spin.value()
            self.timer_total = mins * 60
            self.timer_remaining = self.timer_total
            self.update_timer_display()
            self.meditation_timer.start(1000)
            self.timer_btn.setText("■ Stop")

    def timer_tick(self):
        self.timer_remaining -= 1
        self.update_timer_display()
        if self.timer_remaining <= 0:
            self.meditation_timer.stop()
            self.timer_btn.setText("▶ Start Meditation")
            self.state.data["meditations"] = self.state.data.get("meditations", 0) + 1
            bonus_xp = 20 + (self.timer_total // 60) * 5
            result = self.state.add_xp(bonus_xp, "Devotion")
            self.on_action(bonus_xp, self.timer_btn, result)

    def update_timer_display(self):
        m, s = divmod(self.timer_remaining, 60)
        self.timer_display.setText(f"{m:02d}:{s:02d}")

    def resist_temptation(self):
        result = self.state.add_xp(25, "Discipline")
        self.state.data["resists"] = self.state.data.get("resists", 0) + 1
        self.state.save()
        self.on_action(25, self.resist_btn, result)

    def do_practice(self, xp, virtue, btn):
        result = self.state.add_xp(xp, virtue)
        self.on_action(xp, btn, result)


class PrayerBeadsPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("📿 Prayer Beads")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        phrase_row = QHBoxLayout()
        phrase_row.addWidget(QLabel("Phrase:"))
        self.phrase_combo = QComboBox()
        self.phrase_combo.addItems([
            "SubhanAllah", "Alhamdulillah", "Allahu Akbar",
            "Hail Mary", "Our Father", "Om Mani Padme Hum",
            "Om", "Namo Amitabha", "Hare Krishna", "Custom"
        ])
        current = self.state.data.get("beads_phrase", "SubhanAllah")
        if current in [self.phrase_combo.itemText(i) for i in range(self.phrase_combo.count())]:
            self.phrase_combo.setCurrentText(current)
        self.phrase_combo.currentTextChanged.connect(self.change_phrase)
        phrase_row.addWidget(self.phrase_combo)
        layout.addLayout(phrase_row)

        target_row = QHBoxLayout()
        target_row.addWidget(QLabel("Target:"))
        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 10000)
        self.target_spin.setValue(self.state.data.get("beads_target", 33))
        self.target_spin.valueChanged.connect(self.change_target)
        target_row.addWidget(self.target_spin)
        target_row.addStretch()
        layout.addLayout(target_row)

        bead_frame = QFrame()
        bead_frame.setObjectName("BeadCard")
        bead_layout = QVBoxLayout(bead_frame)
        bead_layout.setAlignment(Qt.AlignCenter)
        
        self.phrase_lbl = QLabel(self.state.data.get("beads_phrase", "SubhanAllah"))
        self.phrase_lbl.setAlignment(Qt.AlignCenter)
        self.phrase_lbl.setStyleSheet("font-size: 18px; color: #f0c850; font-weight: bold;")
        bead_layout.addWidget(self.phrase_lbl)
        
        self.count_lbl = QLabel("0")
        self.count_lbl.setAlignment(Qt.AlignCenter)
        self.count_lbl.setStyleSheet("font-size: 64px; font-weight: bold; color: #ffffff;")
        bead_layout.addWidget(self.count_lbl)
        
        self.target_lbl = QLabel(f"/ {self.state.data.get('beads_target', 33)}")
        self.target_lbl.setAlignment(Qt.AlignCenter)
        self.target_lbl.setStyleSheet("font-size: 16px; color: #a0a0b0;")
        bead_layout.addWidget(self.target_lbl)
        
        self.bar_beads = QProgressBar()
        self.bar_beads.setMaximum(self.state.data.get("beads_target", 33))
        self.bar_beads.setValue(self.state.data.get("beads_session", 0))
        self.bar_beads.setFormat("%v / %m")
        bead_layout.addWidget(self.bar_beads)
        
        self.bead_btn = QPushButton("📿 TAP")
        self.bead_btn.setMinimumHeight(110)
        self.bead_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0c850, stop:1 #d4af37);
                color: #12121a; font-size: 26px; font-weight: bold;
                border: 3px solid #f0c850; border-radius: 55px;
            }
            QPushButton:pressed { background: #b5952f; }
        """)
        self.bead_btn.clicked.connect(self.tap_bead)
        bead_layout.addWidget(self.bead_btn)
        layout.addWidget(bead_frame)

        stats_row = QHBoxLayout()
        self.session_lbl = QLabel()
        self.total_lbl = QLabel()
        stats_row.addWidget(self.session_lbl)
        stats_row.addStretch()
        stats_row.addWidget(self.total_lbl)
        layout.addLayout(stats_row)

        reset_btn = QPushButton("↺ Reset Session")
        reset_btn.clicked.connect(self.reset_session)
        layout.addWidget(reset_btn)
        layout.addStretch()
        self.refresh()

    def change_phrase(self, text):
        if text == "Custom":
            custom, ok = QInputDialog.getText(self, "Custom Phrase", "Enter your sacred phrase:")
            if ok and custom.strip():
                self.state.data["beads_phrase"] = custom.strip()
                self.phrase_lbl.setText(custom.strip())
                self.state.save()
        else:
            self.state.data["beads_phrase"] = text
            self.phrase_lbl.setText(text)
            self.state.save()

    def change_target(self, value):
        self.state.data["beads_target"] = value
        self.bar_beads.setMaximum(value)
        self.target_lbl.setText(f"/ {value}")
        self.refresh()
        self.state.save()

    def tap_bead(self):
        self.state.data["beads_session"] = self.state.data.get("beads_session", 0) + 1
        self.state.data["beads_total"] = self.state.data.get("beads_total", 0) + 1
        target = self.state.data.get("beads_target", 33)
        if self.state.data["beads_session"] % 10 == 0:
            result = self.state.add_xp(5, "Devotion")
            self.on_action(5, self.bead_btn, result)
        if self.state.data["beads_session"] == target:
            result = self.state.add_xp(30, "Devotion")
            self.state.save()
            QMessageBox.information(self, "📿 Round Complete!", f"You completed {target} repetitions!\n+30 XP")
            self.state.data["beads_session"] = 0
            self.on_action(30, self.bead_btn, result)
        self.state.mark_activity_today()
        self.state.save()
        self.refresh()

    def reset_session(self):
        self.state.data["beads_session"] = 0
        self.state.save()
        self.refresh()

    def refresh(self):
        self.count_lbl.setText(str(self.state.data.get("beads_session", 0)))
        target = self.state.data.get("beads_target", 33)
        self.bar_beads.setMaximum(target)
        self.bar_beads.setValue(self.state.data.get("beads_session", 0))
        self.target_lbl.setText(f"/ {target}")
        self.session_lbl.setText(f"Session: {self.state.data.get('beads_session', 0)}")
        self.total_lbl.setText(f"Lifetime: {self.state.data.get('beads_total', 0)}")


class ScripturePage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("📖 Sacred Texts")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(12)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def refresh(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        scripture_data = self.state.data.get("scripture", {})
        for book, chapters in SCRIPTURE_BOOKS.items():
            frame = QFrame()
            frame.setObjectName("Card")
            b_layout = QVBoxLayout(frame)
            header = QLabel(f"<b>{book}</b>")
            header.setStyleSheet("font-size: 15px; color: #f0c850;")
            b_layout.addWidget(header)
            book_data = scripture_data.get(book, {})
            total_progress = 0
            for chapter in chapters:
                ch_row = QHBoxLayout()
                ch_lbl = QLabel(chapter)
                ch_row.addWidget(ch_lbl)
                progress = book_data.get(chapter, 0)
                total_progress += progress
                bar = QProgressBar()
                bar.setMaximum(100)
                bar.setValue(progress)
                bar.setFixedHeight(14)
                bar.setFormat(f"{progress}%")
                ch_row.addWidget(bar, 1)
                btn = QPushButton("+25%")
                btn.setFixedWidth(60)
                btn.clicked.connect(lambda checked, b=book, c=chapter, p=progress: self.increment(b, c, p))
                ch_row.addWidget(btn)
                b_layout.addLayout(ch_row)
            avg = total_progress // len(chapters) if chapters else 0
            total_lbl = QLabel(f"Book Progress: {avg}%")
            total_lbl.setStyleSheet("color: #a0a0b0; font-style: italic;")
            b_layout.addWidget(total_lbl)
            self.scroll_layout.addWidget(frame)
        self.scroll_layout.addStretch()

    def increment(self, book, chapter, current):
        new_val = min(100, current + 25)
        self.state.data.setdefault("scripture", {}).setdefault(book, {})[chapter] = new_val
        if new_val == 100 and current < 100:
            result = self.state.add_xp(20, "Wisdom")
            self.on_action(20, None, result)
            QMessageBox.information(self, "📖 Chapter Complete!", f"You finished {chapter}!\n+20 XP")
        self.state.save()
        self.refresh()


class FastingPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("🌙 Fasting Tracker")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        new_frame = QFrame()
        new_frame.setObjectName("Card")
        n_layout = QVBoxLayout(new_frame)
        n_layout.addWidget(QLabel("<b>Start a New Fast</b>"))
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Ramadan 2026")
        row1.addWidget(self.name_input)
        n_layout.addLayout(row1)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Days:"))
        self.days_spin = QSpinBox()
        self.days_spin.setRange(1, 60)
        self.days_spin.setValue(30)
        row2.addWidget(self.days_spin)
        row2.addStretch()
        start_btn = QPushButton("🌙 Begin Fast")
        start_btn.clicked.connect(self.start_fast)
        row2.addWidget(start_btn)
        n_layout.addLayout(row2)
        layout.addWidget(new_frame)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(10)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def start_fast(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter a name.")
            return
        days = self.days_spin.value()
        fast = {"name": name, "days": days, "current_day": 0, "completed": False, "started": str(date.today())}
        self.state.data.setdefault("fasts", []).append(fast)
        self.state.save()
        self.name_input.clear()
        self.refresh()

    def check_in(self, idx):
        fast = self.state.data["fasts"][idx]
        if fast.get("completed"):
            return
        fast["current_day"] = fast.get("current_day", 0) + 1
        result = self.state.add_xp(15, "Discipline")
        self.on_action(15, None, result)
        if fast["current_day"] >= fast["days"]:
            fast["completed"] = True
            self.state.data["fasts_completed"] = self.state.data.get("fasts_completed", 0) + 1
            bonus = self.state.add_xp(100, "Discipline")
            QMessageBox.information(self, "🌾 Fast Complete!", f"You completed {fast['name']}!\n+100 XP")
            self.on_action(100, None, bonus)
        self.state.save()
        self.refresh()

    def delete_fast(self, idx):
        reply = QMessageBox.question(self, "Delete Fast", "Remove this fast?")
        if reply == QMessageBox.Yes:
            self.state.data["fasts"].pop(idx)
            self.state.save()
            self.refresh()

    def refresh(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        fasts = self.state.data.get("fasts", [])
        if not fasts:
            empty = QLabel("No fasts tracked yet.")
            empty.setStyleSheet("color: #666; font-style: italic;")
            empty.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(empty)
        else:
            for i, fast in enumerate(reversed(fasts)):
                real_idx = len(fasts) - 1 - i
                frame = QFrame()
                frame.setObjectName("GoldCard" if fast.get("completed") else "Card")
                f_layout = QVBoxLayout(frame)
                header = QHBoxLayout()
                name_lbl = QLabel(f"<b>{fast['name']}</b>")
                name_lbl.setStyleSheet("font-size: 14px; color: #f0c850;")
                header.addWidget(name_lbl)
                header.addStretch()
                if fast.get("completed"):
                    status = QLabel("✓ Complete")
                    status.setStyleSheet("color: #27ae60; font-weight: bold;")
                    header.addWidget(status)
                f_layout.addLayout(header)
                bar = QProgressBar()
                bar.setMaximum(fast["days"])
                bar.setValue(fast.get("current_day", 0))
                bar.setFormat(f"Day %v / {fast['days']}")
                f_layout.addWidget(bar)
                btn_row = QHBoxLayout()
                if not fast.get("completed"):
                    check_btn = QPushButton("✓ Daily Check-in (+15 XP)")
                    check_btn.clicked.connect(lambda checked, idx=real_idx: self.check_in(idx))
                    btn_row.addWidget(check_btn)
                del_btn = QPushButton("🗑️")
                del_btn.setFixedWidth(45)
                del_btn.clicked.connect(lambda checked, idx=real_idx: self.delete_fast(idx))
                btn_row.addWidget(del_btn)
                f_layout.addLayout(btn_row)
                self.scroll_layout.addWidget(frame)
        self.scroll_layout.addStretch()


class CharityPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("💝 Charity & Service")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setObjectName("Card")
        f_layout = QVBoxLayout(form_frame)
        f_layout.addWidget(QLabel("<b>Log a New Act</b>"))
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["💰 Money Donated", "⏰ Hours Volunteered", "🤝 Act of Kindness", "🍞 Food Given", "📚 Knowledge Shared"])
        row1.addWidget(self.type_combo)
        f_layout.addLayout(row1)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Amount/Hours:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("e.g. 50 or 2 hours")
        row2.addWidget(self.amount_input)
        f_layout.addLayout(row2)
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Note:"))
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Optional note...")
        row3.addWidget(self.note_input)
        f_layout.addLayout(row3)
        log_btn = QPushButton("💝 Log Act (+25 XP)")
        log_btn.clicked.connect(self.log_charity)
        f_layout.addWidget(log_btn)
        layout.addWidget(form_frame)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.hist_layout = QVBoxLayout(scroll_widget)
        self.hist_layout.setSpacing(8)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def log_charity(self):
        ctype = self.type_combo.currentText()
        amount = self.amount_input.text().strip()
        note = self.note_input.text().strip()
        if not amount:
            QMessageBox.warning(self, "Missing Amount", "Please enter an amount.")
            return
        entry = {"date": str(date.today()), "type": ctype, "amount": amount, "note": note}
        self.state.data.setdefault("charity", []).append(entry)
        result = self.state.add_xp(25, "Compassion")
        self.on_action(25, None, result)
        self.amount_input.clear()
        self.note_input.clear()
        self.state.save()
        self.refresh()

    def refresh(self):
        while self.hist_layout.count():
            child = self.hist_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        charity = self.state.data.get("charity", [])
        recent = list(reversed(charity))[:15]
        if not recent:
            empty = QLabel("No acts logged yet.")
            empty.setStyleSheet("color: #666; font-style: italic;")
            empty.setAlignment(Qt.AlignCenter)
            self.hist_layout.addWidget(empty)
        else:
            for entry in recent:
                frame = QFrame()
                frame.setObjectName("Card")
                e_layout = QHBoxLayout(frame)
                icon = entry["type"].split(" ")[0]
                icon_lbl = QLabel(icon)
                icon_lbl.setStyleSheet("font-size: 22px;")
                e_layout.addWidget(icon_lbl)
                text_layout = QVBoxLayout()
                text_layout.addWidget(QLabel(f"<b>{entry['type']}</b>"))
                detail = f"{entry['amount']}"
                if entry.get("note"):
                    detail += f" — {entry['note']}"
                detail_lbl = QLabel(f"{entry['date']} • {detail}")
                detail_lbl.setStyleSheet("color: #a0a0b0; font-size: 11px;")
                text_layout.addWidget(detail_lbl)
                e_layout.addLayout(text_layout, 1)
                self.hist_layout.addWidget(frame)
        self.hist_layout.addStretch()


class RitualsPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("🕉️ Sacred Rituals")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(12)

        mantra_frame = QFrame()
        mantra_frame.setObjectName("GoldCard")
        m_layout = QVBoxLayout(mantra_frame)
        m_layout.addWidget(QLabel("<b>🕉️ Mantra Repeater</b>"))
        m_row = QHBoxLayout()
        m_row.addWidget(QLabel("Mantra:"))
        self.mantra_input = QLineEdit()
        self.mantra_input.setText(self.state.data.get("mantra", "Om"))
        self.mantra_input.textChanged.connect(self.update_mantra)
        m_row.addWidget(self.mantra_input)
        m_layout.addLayout(m_row)
        self.mantra_display = QLabel(self.state.data.get("mantra", "Om"))
        self.mantra_display.setAlignment(Qt.AlignCenter)
        self.mantra_display.setStyleSheet("font-size: 42px; font-weight: bold; color: #f0c850;")
        m_layout.addWidget(self.mantra_display)
        self.mantra_count_lbl = QLabel(f"Repeated: {self.state.data.get('mantra_count', 0)} times")
        self.mantra_count_lbl.setAlignment(Qt.AlignCenter)
        m_layout.addWidget(self.mantra_count_lbl)
        mantra_btn = QPushButton("🕉️ Repeat (+2 XP)")
        mantra_btn.clicked.connect(self.repeat_mantra)
        m_layout.addWidget(mantra_btn)
        scroll_layout.addWidget(mantra_frame)

        release_frame = QFrame()
        release_frame.setObjectName("Card")
        r_layout = QVBoxLayout(release_frame)
        r_layout.addWidget(QLabel("<b>🕯️ Release Your Burdens</b>"))
        r_layout.addWidget(QLabel("Write what weighs on your heart."))
        self.release_edit = QTextEdit()
        self.release_edit.setPlaceholderText("I release...")
        self.release_edit.setMaximumHeight(90)
        r_layout.addWidget(self.release_edit)
        release_btn = QPushButton("🔥 Release & Let Go (+20 XP)")
        release_btn.clicked.connect(self.release_burden)
        r_layout.addWidget(release_btn)
        scroll_layout.addWidget(release_frame)

        custom_frame = QFrame()
        custom_frame.setObjectName("Card")
        c_layout = QVBoxLayout(custom_frame)
        c_layout.addWidget(QLabel("<b>✨ Custom Rituals</b>"))
        add_btn = QPushButton("+ Add Custom Ritual")
        add_btn.clicked.connect(self.add_custom)
        c_layout.addWidget(add_btn)
        self.custom_layout = QVBoxLayout()
        c_layout.addLayout(self.custom_layout)
        scroll_layout.addWidget(custom_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh_custom()

    def update_mantra(self, text):
        self.state.data["mantra"] = text
        self.mantra_display.setText(text or "Om")
        self.state.save()

    def repeat_mantra(self):
        self.state.data["mantra_count"] = self.state.data.get("mantra_count", 0) + 1
        result = self.state.add_xp(2, "Devotion")
        self.on_action(2, None, result)
        self.mantra_count_lbl.setText(f"Repeated: {self.state.data['mantra_count']} times")
        self.mantra_display.setStyleSheet("font-size: 50px; font-weight: bold; color: #ffffff;")
        QTimer.singleShot(200, lambda: self.mantra_display.setStyleSheet("font-size: 42px; font-weight: bold; color: #f0c850;"))

    def release_burden(self):
        text = self.release_edit.toPlainText().strip()
        if len(text) < 5:
            QMessageBox.warning(self, "Too Short", "Write at least a few words.")
            return
        self.state.data["releases"] = self.state.data.get("releases", 0) + 1
        result = self.state.add_xp(20, "Devotion")
        self.on_action(20, None, result)
        self.release_edit.clear()
        QMessageBox.information(self, "🕊️ Released", "Your burden has been released.")

    def add_custom(self):
        name, ok = QInputDialog.getText(self, "New Ritual", "Ritual name:")
        if not ok or not name.strip():
            return
        desc, ok = QInputDialog.getText(self, "Description", "Brief description:")
        if not ok:
            desc = ""
        xp, ok = QInputDialog.getInt(self, "XP Reward", "XP on completion:", 25, 5, 500)
        if not ok:
            return
        ritual = {"name": name.strip(), "desc": desc.strip(), "xp": xp, "virtue": "Devotion"}
        self.state.data.setdefault("custom_rituals", []).append(ritual)
        self.state.save()
        self.refresh_custom()

    def do_custom(self, idx, btn):
        ritual = self.state.data["custom_rituals"][idx]
        result = self.state.add_xp(ritual["xp"], ritual["virtue"])
        self.on_action(ritual["xp"], btn, result)

    def delete_custom(self, idx):
        self.state.data["custom_rituals"].pop(idx)
        self.state.save()
        self.refresh_custom()

    def refresh_custom(self):
        while self.custom_layout.count():
            child = self.custom_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for i, ritual in enumerate(self.state.data.get("custom_rituals", [])):
            frame = QFrame()
            frame.setObjectName("Card")
            f_layout = QHBoxLayout(frame)
            text = QVBoxLayout()
            text.addWidget(QLabel(f"<b>{ritual['name']}</b>"))
            if ritual.get("desc"):
                desc_lbl = QLabel(ritual["desc"])
                desc_lbl.setStyleSheet("color: #a0a0b0; font-size: 11px;")
                text.addWidget(desc_lbl)
            f_layout.addLayout(text, 1)
            do_btn = QPushButton(f"+{ritual['xp']} XP")
            do_btn.setFixedWidth(80)
            do_btn.clicked.connect(lambda checked, idx=i, b=do_btn: self.do_custom(idx, b))
            f_layout.addWidget(do_btn)
            del_btn = QPushButton("🗑️")
            del_btn.setFixedWidth(35)
            del_btn.clicked.connect(lambda checked, idx=i: self.delete_custom(idx))
            f_layout.addWidget(del_btn)
            self.custom_layout.addWidget(frame)


class PilgrimagePage(QWidget):
    """Track visits to sacred sites."""
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("🗺️ Pilgrimage Tracker")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("Log your visits to sacred sites, temples, churches, mosques, and holy places.")
        desc.setProperty("class", "Subtitle")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Add form
        form_frame = QFrame()
        form_frame.setObjectName("Card")
        f_layout = QVBoxLayout(form_frame)
        f_layout.addWidget(QLabel("<b>Log a Sacred Visit</b>"))
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Site Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Mecca, Vatican, Bodh Gaya")
        row1.addWidget(self.name_input)
        f_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        row2.addWidget(self.date_input)
        row2.addWidget(QLabel("Location:"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("City, Country")
        row2.addWidget(self.location_input)
        f_layout.addLayout(row2)
        
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Rating:"))
        self.rating_spin = QDoubleSpinBox()
        self.rating_spin.setRange(1, 5)
        self.rating_spin.setValue(5)
        self.rating_spin.setSingleStep(0.5)
        row3.addWidget(self.rating_spin)
        row3.addWidget(QLabel("⭐"))
        row3.addStretch()
        f_layout.addLayout(row3)
        
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Notes:"))
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("What moved you?")
        row4.addWidget(self.notes_input)
        f_layout.addLayout(row4)
        
        add_btn = QPushButton("🗺️ Log Pilgrimage (+40 XP)")
        add_btn.clicked.connect(self.add_pilgrimage)
        f_layout.addWidget(add_btn)
        layout.addWidget(form_frame)

        # Stats
        self.stats_lbl = QLabel()
        self.stats_lbl.setStyleSheet("font-size: 13px; color: #f0c850;")
        layout.addWidget(self.stats_lbl)

        # History
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.hist_layout = QVBoxLayout(scroll_widget)
        self.hist_layout.setSpacing(8)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def add_pilgrimage(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter the site name.")
            return
        entry = {
            "name": name,
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "location": self.location_input.text().strip(),
            "rating": self.rating_spin.value(),
            "notes": self.notes_input.text().strip()
        }
        self.state.data.setdefault("pilgrimages", []).append(entry)
        result = self.state.add_xp(40, "Devotion")
        self.on_action(40, None, result)
        self.name_input.clear()
        self.location_input.clear()
        self.notes_input.clear()
        self.state.save()
        self.refresh()

    def delete_pilgrimage(self, idx):
        reply = QMessageBox.question(self, "Delete", "Remove this pilgrimage?")
        if reply == QMessageBox.Yes:
            self.state.data["pilgrimages"].pop(idx)
            self.state.save()
            self.refresh()

    def refresh(self):
        pils = self.state.data.get("pilgrimages", [])
        self.stats_lbl.setText(f"🗺️ {len(pils)} sacred sites visited   •   🌍 A pilgrim's path")
        
        while self.hist_layout.count():
            child = self.hist_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not pils:
            empty = QLabel("No pilgrimages logged yet. Begin your sacred journey.")
            empty.setStyleSheet("color: #666; font-style: italic;")
            empty.setAlignment(Qt.AlignCenter)
            self.hist_layout.addWidget(empty)
        else:
            for i, p in enumerate(reversed(pils)):
                real_idx = len(pils) - 1 - i
                frame = QFrame()
                frame.setObjectName("Card")
                p_layout = QHBoxLayout(frame)
                
                icon_lbl = QLabel("🕌")
                icon_lbl.setStyleSheet("font-size: 26px;")
                p_layout.addWidget(icon_lbl)
                
                text_layout = QVBoxLayout()
                name_lbl = QLabel(f"<b>{p['name']}</b>   {'⭐' * int(p.get('rating', 5))}")
                name_lbl.setStyleSheet("font-size: 14px; color: #f0c850;")
                text_layout.addWidget(name_lbl)
                
                details = f"📅 {p['date']}"
                if p.get('location'):
                    details += f"   •   📍 {p['location']}"
                if p.get('notes'):
                    details += f"   •   {p['notes']}"
                det_lbl = QLabel(details)
                det_lbl.setStyleSheet("color: #a0a0b0; font-size: 11px;")
                det_lbl.setWordWrap(True)
                text_layout.addWidget(det_lbl)
                p_layout.addLayout(text_layout, 1)
                
                del_btn = QPushButton("🗑️")
                del_btn.setFixedWidth(40)
                del_btn.clicked.connect(lambda checked, idx=real_idx: self.delete_pilgrimage(idx))
                p_layout.addWidget(del_btn)
                
                self.hist_layout.addWidget(frame)
        
        self.hist_layout.addStretch()


class CalendarPage(QWidget):
    """Liturgical calendar with major holidays."""
    def __init__(self, state: GameState, parent=None):
        super().__init__(parent)
        self.state = state
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("📅 Liturgical Calendar")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("Major holy days across world traditions (2026–2027).")
        desc.setProperty("class", "Subtitle")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # Filter by tradition
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Traditions"] + list(LITURGICAL_HOLIDAYS.keys()))
        current_trad = self.state.data.get("settings", {}).get("tradition", "Universal")
        if current_trad in LITURGICAL_HOLIDAYS:
            self.filter_combo.setCurrentText(current_trad)
        self.filter_combo.currentTextChanged.connect(lambda _: self.refresh())
        filter_row.addWidget(self.filter_combo)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Icon", "Holiday", "Tradition", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        filter_text = self.filter_combo.currentText()
        
        # Collect all holidays
        all_holidays = []
        traditions = [filter_text] if filter_text != "All Traditions" else LITURGICAL_HOLIDAYS.keys()
        for trad in traditions:
            for d, name, icon, desc in LITURGICAL_HOLIDAYS.get(trad, []):
                all_holidays.append((d, icon, name, trad, desc))
        
        all_holidays.sort(key=lambda x: x[0])
        today_str = str(date.today())
        
        self.table.setRowCount(len(all_holidays))
        for row, (d, icon, name, trad, desc) in enumerate(all_holidays):
            is_past = d < today_str
            is_today = d == today_str
            
            # Date
            date_item = QTableWidgetItem(d)
            if is_today:
                date_item.setForeground(QColor("#f0c850"))
                date_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            elif is_past:
                date_item.setForeground(QColor("#666"))
            self.table.setItem(row, 0, date_item)
            
            # Icon
            icon_item = QTableWidgetItem(icon)
            icon_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, icon_item)
            
            # Name
            name_item = QTableWidgetItem(name)
            if is_today:
                name_item.setForeground(QColor("#f0c850"))
                name_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            elif is_past:
                name_item.setForeground(QColor("#666"))
            self.table.setItem(row, 2, name_item)
            
            # Tradition
            trad_item = QTableWidgetItem(trad)
            if is_past:
                trad_item.setForeground(QColor("#666"))
            self.table.setItem(row, 3, trad_item)
            
            # Description
            desc_item = QTableWidgetItem(desc)
            if is_past:
                desc_item.setForeground(QColor("#666"))
            self.table.setItem(row, 4, desc_item)
        
        self.table.resizeRowsToContents()


class QuestsPage(QWidget):
    def __init__(self, state: GameState, parent=None):
        super().__init__(parent)
        self.state = state
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("📜 Daily Quests")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(10)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def refresh(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for q in self.state.data["quests"]:
            frame = QFrame()
            frame.setObjectName("Card")
            f_layout = QHBoxLayout(frame)
            cb = QCheckBox()
            cb.setChecked(q["done"])
            cb.setEnabled(False)
            text_layout = QVBoxLayout()
            lbl_name = QLabel(f"<b>{q['name']}</b>")
            style = "font-size: 13px; color: #e0e0e0;"
            if q["done"]:
                style = "font-size: 13px; color: #666; text-decoration: line-through;"
            lbl_name.setStyleSheet(style)
            lbl_desc = QLabel(f"{q['desc']}  •  <span style='color:#f0c850;'>+{q['xp']} XP</span>")
            lbl_desc.setStyleSheet("color: #a0a0b0; font-size: 11px;")
            text_layout.addWidget(lbl_name)
            text_layout.addWidget(lbl_desc)
            f_layout.addWidget(cb)
            f_layout.addLayout(text_layout, 1)
            self.scroll_layout.addWidget(frame)
        self.scroll_layout.addStretch()


class VirtuesPage(QWidget):
    def __init__(self, state: GameState, parent=None):
        super().__init__(parent)
        self.state = state
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("🌟 The Path of Virtues")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.bars = {}
        virtues_info = {
            "Wisdom": ("📖", "Gained through studying sacred texts and reflection."),
            "Compassion": ("🤲", "Gained through charity, kindness, and helping others."),
            "Discipline": ("⚔️", "Gained through fasting, resisting temptation, and routine."),
            "Devotion": ("🕯️", "Gained through prayer, meditation, and worship.")
        }
        for v, (icon, desc_text) in virtues_info.items():
            frame = QFrame()
            frame.setObjectName("Card")
            v_layout = QVBoxLayout(frame)
            header = QHBoxLayout()
            lbl_name = QLabel(f"{icon} <b>{v}</b>")
            lbl_name.setStyleSheet("font-size: 15px; color: #f0c850;")
            self.lbl_val = QLabel()
            self.lbl_val.setStyleSheet("font-size: 15px; font-weight: bold;")
            header.addWidget(lbl_name)
            header.addStretch()
            header.addWidget(self.lbl_val)
            v_layout.addLayout(header)
            lbl_desc = QLabel(desc_text)
            lbl_desc.setStyleSheet("color: #a0a0b0; margin-bottom: 6px; font-size: 11px;")
            v_layout.addWidget(lbl_desc)
            bar = QProgressBar()
            bar.setMaximum(1000)
            v_layout.addWidget(bar)
            self.bars[v] = (bar, self.lbl_val)
            layout.addWidget(frame)
        layout.addStretch()
        self.refresh()

    def refresh(self):
        for v, (bar, lbl) in self.bars.items():
            val = self.state.data["virtues"][v]
            bar.setValue(val)
            lbl.setText(str(val))


class JournalPage(QWidget):
    def __init__(self, state: GameState, on_action, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_action = on_action
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        title = QLabel("📔 Gratitude Journal")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Today I am grateful for...")
        self.text_edit.setMinimumHeight(110)
        layout.addWidget(self.text_edit)

        self.save_btn = QPushButton("💾 Save Entry (+30 XP)")
        self.save_btn.clicked.connect(self.save_entry)
        layout.addWidget(self.save_btn)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.entries_layout = QVBoxLayout(scroll_widget)
        self.entries_layout.setSpacing(6)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def save_entry(self):
        today = str(date.today())
        if self.state.data.get("last_journal_date") == today:
            QMessageBox.information(self, "Already Written", "You've already written today.")
            return
        text = self.text_edit.toPlainText().strip()
        if len(text) < 20:
            QMessageBox.warning(self, "Too Short", "Please write at least 20 characters.")
            return
        entry = {"date": today, "text": text, "timestamp": datetime.now().isoformat()}
        self.state.data["journal"].append(entry)
        self.state.data["last_journal_date"] = today
        result = self.state.add_xp(30, "Wisdom")
        self.state.save()
        self.text_edit.clear()
        self.on_action(30, self.save_btn, result)
        self.refresh()

    def refresh(self):
        while self.entries_layout.count():
            child = self.entries_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        entries = list(reversed(self.state.data.get("journal", [])))[:8]
        for entry in entries:
            frame = QFrame()
            frame.setObjectName("Card")
            f_layout = QVBoxLayout(frame)
            date_lbl = QLabel(f"📅 {entry['date']}")
            date_lbl.setStyleSheet("color: #f0c850; font-weight: bold; font-size: 11px;")
            text_lbl = QLabel(entry["text"])
            text_lbl.setWordWrap(True)
            text_lbl.setStyleSheet("color: #c0c0c0; font-size: 11px;")
            f_layout.addWidget(date_lbl)
            f_layout.addWidget(text_lbl)
            self.entries_layout.addWidget(frame)
        if not entries:
            empty = QLabel("No entries yet.")
            empty.setStyleSheet("color: #666; font-style: italic;")
            empty.setAlignment(Qt.AlignCenter)
            self.entries_layout.addWidget(empty)
        self.entries_layout.addStretch()
        today = str(date.today())
        if self.state.data.get("last_journal_date") == today:
            self.save_btn.setText("✓ Written Today")
            self.save_btn.setEnabled(False)
        else:
            self.save_btn.setText("💾 Save Entry (+30 XP)")
            self.save_btn.setEnabled(True)


class AchievementsPage(QWidget):
    def __init__(self, state: GameState, parent=None):
        super().__init__(parent)
        self.state = state
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        title = QLabel("🏆 Achievements")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.count_lbl = QLabel()
        self.count_lbl.setProperty("class", "Subtitle")
        self.count_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.count_lbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.grid = QGridLayout(scroll_widget)
        self.grid.setSpacing(8)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def refresh(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        unlocked = self.state.data.get("achievements", [])
        self.count_lbl.setText(f"{len(unlocked)} / {len(ACHIEVEMENTS)} Unlocked")
        for i, ach in enumerate(ACHIEVEMENTS):
            is_unlocked = ach["id"] in unlocked
            frame = QFrame()
            frame.setObjectName("GoldCard" if is_unlocked else "Card")
            f_layout = QVBoxLayout(frame)
            f_layout.setAlignment(Qt.AlignCenter)
            icon_lbl = QLabel(ach["icon"] if is_unlocked else "🔒")
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setStyleSheet("font-size: 24px;")
            name_lbl = QLabel(f"<b>{ach['name']}</b>")
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"font-size: 11px; color: {'#f0c850' if is_unlocked else '#666'};")
            name_lbl.setWordWrap(True)
            desc_lbl = QLabel(ach["desc"])
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setStyleSheet("font-size: 10px; color: #a0a0b0;")
            desc_lbl.setWordWrap(True)
            f_layout.addWidget(icon_lbl)
            f_layout.addWidget(name_lbl)
            f_layout.addWidget(desc_lbl)
            self.grid.addWidget(frame, i // 3, i % 3)


class StatsPage(QWidget):
    def __init__(self, state: GameState, parent=None):
        super().__init__(parent)
        self.state = state
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        title = QLabel("📊 Journey Statistics")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(12)

        # Stats grid
        stats_frame = QFrame()
        stats_frame.setObjectName("Card")
        s_layout = QGridLayout(stats_frame)
        self.stat_labels = {}
        stats = [
            ("Total XP", "total_xp"), ("Level", "level"),
            ("Streak", "streak"), ("Meditations", "meditations"),
            ("Journal", "journal_count"), ("Resists", "resists"),
            ("Beads", "beads"), ("Fasts", "fasts"),
            ("Charity", "charity"), ("Releases", "releases"),
            ("Pilgrimages", "pilgrimages"), ("Achievements", "achievements"),
        ]
        for i, (name, key) in enumerate(stats):
            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("color: #a0a0b0; font-size: 11px;")
            lbl_val = QLabel()
            lbl_val.setStyleSheet("font-size: 16px; font-weight: bold; color: #f0c850;")
            lbl_val.setAlignment(Qt.AlignRight)
            s_layout.addWidget(lbl_name, i // 3, (i % 3) * 2)
            s_layout.addWidget(lbl_val, i // 3, (i % 3) * 2 + 1)
            self.stat_labels[key] = lbl_val
        scroll_layout.addWidget(stats_frame)

        # Virtue Growth Chart (NEW)
        if HAS_PYQTGRAPH:
            chart_frame = QFrame()
            chart_frame.setObjectName("Card")
            c_layout = QVBoxLayout(chart_frame)
            c_layout.addWidget(QLabel("<b>📈 Virtue Growth Over Time</b>"))
            
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setBackground('#1e1e2a')
            self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
            self.plot_widget.setLabel('left', 'Virtue Points')
            self.plot_widget.setLabel('bottom', 'Days')
            self.plot_widget.setMinimumHeight(280)
            self.plot_widget.addLegend()
            c_layout.addWidget(self.plot_widget)
            
            range_row = QHBoxLayout()
            range_row.addWidget(QLabel("Show last:"))
            self.range_spin = QSpinBox()
            self.range_spin.setRange(7, 365)
            self.range_spin.setValue(30)
            self.range_spin.setSuffix(" days")
            self.range_spin.valueChanged.connect(self.refresh_chart)
            range_row.addWidget(self.range_spin)
            range_row.addStretch()
            c_layout.addLayout(range_row)
            
            scroll_layout.addWidget(chart_frame)
        else:
            no_chart = QLabel("⚠️ Install pyqtgraph to see virtue charts: pip install pyqtgraph")
            no_chart.setStyleSheet("color: #e74c3c; font-style: italic;")
            no_chart.setAlignment(Qt.AlignCenter)
            scroll_layout.addWidget(no_chart)

        # Calendar heatmap
        cal_title = QLabel("<b>Activity Calendar (Last 90 Days)</b>")
        cal_title.setStyleSheet("font-size: 14px; color: #f0c850; margin-top: 8px;")
        scroll_layout.addWidget(cal_title)

        self.heatmap_frame = QFrame()
        self.heatmap_frame.setObjectName("Card")
        self.heatmap_layout = QGridLayout(self.heatmap_frame)
        self.heatmap_layout.setSpacing(3)
        scroll_layout.addWidget(self.heatmap_frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        self.refresh()

    def refresh(self):
        d = self.state.data
        self.stat_labels["total_xp"].setText(str(d.get("total_xp", 0)))
        self.stat_labels["level"].setText(str(d["level"]))
        self.stat_labels["streak"].setText(str(d["streak"]))
        self.stat_labels["meditations"].setText(str(d.get("meditations", 0)))
        self.stat_labels["journal_count"].setText(str(len(d.get("journal", []))))
        self.stat_labels["resists"].setText(str(d.get("resists", 0)))
        self.stat_labels["beads"].setText(str(d.get("beads_total", 0)))
        self.stat_labels["fasts"].setText(str(d.get("fasts_completed", 0)))
        self.stat_labels["charity"].setText(str(len(d.get("charity", []))))
        self.stat_labels["releases"].setText(str(d.get("releases", 0)))
        self.stat_labels["pilgrimages"].setText(str(len(d.get("pilgrimages", []))))
        self.stat_labels["achievements"].setText(f"{len(d.get('achievements', []))}/{len(ACHIEVEMENTS)}")

        if HAS_PYQTGRAPH:
            self.refresh_chart()

        while self.heatmap_layout.count():
            child = self.heatmap_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        today = date.today()
        calendar = d.get("calendar", {})
        for week in range(13):
            for day in range(7):
                d_date = today - timedelta(days=(12 - week) * 7 + (6 - day))
                count = calendar.get(str(d_date), 0)
                cell = QLabel()
                cell.setFixedSize(15, 15)
                if count == 0: color = "#1e1e2a"
                elif count == 1: color = "#3d3520"
                elif count == 2: color = "#6b5a28"
                elif count <= 4: color = "#a88930"
                else: color = "#f0c850"
                cell.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
                cell.setToolTip(f"{d_date.strftime('%Y-%m-%d')}: {count} actions")
                self.heatmap_layout.addWidget(cell, day, week)

    def refresh_chart(self):
        if not HAS_PYQTGRAPH:
            return
        self.plot_widget.clear()
        
        history = self.state.data.get("virtue_history", {})
        if not history:
            # Add current as first data point
            today_str = str(date.today())
            history[today_str] = dict(self.state.data["virtues"])
        
        days = self.range_spin.value()
        sorted_dates = sorted(history.keys())
        
        # Filter to last N days
        cutoff = str(date.today() - timedelta(days=days))
        sorted_dates = [d for d in sorted_dates if d >= cutoff]
        
        if len(sorted_dates) < 2:
            # Need at least 2 points to draw a line
            self.plot_widget.setTitle("Not enough data yet. Keep practicing!")
            return
        
        self.plot_widget.setTitle("")
        
        colors = {
            "Wisdom": (100, 180, 255),
            "Compassion": (255, 120, 150),
            "Discipline": (255, 200, 80),
            "Devotion": (180, 130, 255),
        }
        
        x = list(range(len(sorted_dates)))
        for virtue, color in colors.items():
            y = [history[d].get(virtue, 0) for d in sorted_dates]
            self.plot_widget.plot(x, y, pen=pg.mkPen(color, width=2), name=virtue,
                                  symbol='o', symbolSize=4, symbolBrush=color)
        
        # Set x-axis ticks to show dates
        tick_spacing = max(1, len(sorted_dates) // 6)
        ticks = [(i, sorted_dates[i][5:]) for i in range(0, len(sorted_dates), tick_spacing)]
        self.plot_widget.getAxis('bottom').setTicks([ticks])


class SettingsPage(QWidget):
    def __init__(self, state: GameState, on_refresh, parent=None):
        super().__init__(parent)
        self.state = state
        self.on_refresh = on_refresh
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        title = QLabel("⚙️ Settings")
        title.setProperty("class", "Title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        s_layout = QVBoxLayout(scroll_widget)
        s_layout.setSpacing(12)

        # Tradition
        trad_frame = QFrame()
        trad_frame.setObjectName("Card")
        t_layout = QVBoxLayout(trad_frame)
        t_layout.addWidget(QLabel("<b>Your Spiritual Tradition</b>"))
        self.trad_combo = QComboBox()
        self.trad_combo.addItems(["Universal", "Christianity", "Islam", "Judaism", "Hinduism", 
                                   "Buddhism", "Taoism", "Sikhism", "Secular/Spiritual"])
        self.trad_combo.setCurrentText(self.state.data.get("settings", {}).get("tradition", "Universal"))
        self.trad_combo.currentTextChanged.connect(self.change_tradition)
        t_layout.addWidget(self.trad_combo)
        s_layout.addWidget(trad_frame)

        # Prayer Times (NEW)
        prayer_frame = QFrame()
        prayer_frame.setObjectName("GoldCard")
        p_layout = QVBoxLayout(prayer_frame)
        p_layout.addWidget(QLabel("<b>🔔 Prayer Time Reminders</b>"))
        p_layout.addWidget(QLabel("Get system notifications at your chosen prayer times."))
        
        self.prayer_enabled_cb = QCheckBox("Enable prayer reminders")
        self.prayer_enabled_cb.setChecked(self.state.data.get("prayer_times", {}).get("enabled", False))
        self.prayer_enabled_cb.toggled.connect(self.toggle_prayer_times)
        p_layout.addWidget(self.prayer_enabled_cb)
        
        self.prayer_times_container = QWidget()
        pt_layout = QVBoxLayout(self.prayer_times_container)
        pt_layout.setContentsMargins(0, 0, 0, 0)
        
        self.time_edits = []
        times = self.state.data.get("prayer_times", {}).get("times", ["05:00", "12:30", "15:30", "18:30", "21:00"])
        labels = ["Fajr / Morning", "Dhuhr / Midday", "Asr / Afternoon", "Maghrib / Evening", "Isha / Night"]
        for i, (label, time_str) in enumerate(zip(labels, times)):
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}:"))
            time_edit = QTimeEdit()
            time_edit.setDisplayFormat("HH:mm")
            h, m = map(int, time_str.split(":"))
            time_edit.setTime(QTime(h, m))
            time_edit.timeChanged.connect(self.save_prayer_times)
            row.addWidget(time_edit)
            row.addStretch()
            pt_layout.addLayout(row)
            self.time_edits.append(time_edit)
        
        p_layout.addWidget(self.prayer_times_container)
        self.prayer_times_container.setVisible(self.prayer_enabled_cb.isChecked())
        
        test_btn = QPushButton("🔔 Test Notification")
        test_btn.clicked.connect(self.test_notification)
        p_layout.addWidget(test_btn)
        s_layout.addWidget(prayer_frame)

        # Accountability Partner (NEW)
        partner_frame = QFrame()
        partner_frame.setObjectName("Card")
        pa_layout = QVBoxLayout(partner_frame)
        pa_layout.addWidget(QLabel("<b>👥 Accountability Partner</b>"))
        pa_layout.addWidget(QLabel("Share your spiritual journey with a friend."))
        
        p_row = QHBoxLayout()
        p_row.addWidget(QLabel("Partner Name:"))
        self.partner_input = QLineEdit()
        self.partner_input.setPlaceholderText("e.g. Sarah, Brother John")
        self.partner_input.setText(self.state.data.get("partner_name", ""))
        self.partner_input.textChanged.connect(self.save_partner)
        p_row.addWidget(self.partner_input)
        pa_layout.addLayout(p_row)
        
        share_row = QHBoxLayout()
        export_btn = QPushButton("📤 Export Pilgrim Card")
        export_btn.clicked.connect(self.export_partner_card)
        share_row.addWidget(export_btn)
        import_btn = QPushButton("📥 Import Partner's Card")
        import_btn.clicked.connect(self.import_partner_card)
        share_row.addWidget(import_btn)
        pa_layout.addLayout(share_row)
        s_layout.addWidget(partner_frame)

        # Data management
        export_frame = QFrame()
        export_frame.setObjectName("Card")
        e_layout = QVBoxLayout(export_frame)
        e_layout.addWidget(QLabel("<b>💾 Data Management</b>"))
        btn_row = QHBoxLayout()
        export_btn = QPushButton("📤 Export Save")
        export_btn.clicked.connect(self.export_save)
        btn_row.addWidget(export_btn)
        import_btn = QPushButton("📥 Import Save")
        import_btn.clicked.connect(self.import_save)
        btn_row.addWidget(import_btn)
        e_layout.addLayout(btn_row)
        s_layout.addWidget(export_frame)

        # Reset
        reset_frame = QFrame()
        reset_frame.setObjectName("Card")
        r_layout = QVBoxLayout(reset_frame)
        r_layout.addWidget(QLabel("<b>⚠️ Reset Journey</b>"))
        reset_btn = QPushButton("🗑️ Reset All Data")
        reset_btn.setStyleSheet("border-color: #c0392b; color: #e74c3c;")
        reset_btn.clicked.connect(self.reset_data)
        r_layout.addWidget(reset_btn)
        s_layout.addWidget(reset_frame)

        # About
        about_frame = QFrame()
        about_frame.setObjectName("GoldCard")
        a_layout = QVBoxLayout(about_frame)
        a_layout.addWidget(QLabel("<b>🌟 Soul Journey — Divine Edition</b>"))
        a_layout.addWidget(QLabel("A gamified companion for your spiritual path."))
        a_layout.addWidget(QLabel("Version 4.0 — Divine Edition"))
        a_layout.addWidget(QLabel("May your journey be blessed. 🙏"))
        s_layout.addWidget(about_frame)

        s_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

    def change_tradition(self, text):
        self.state.data.setdefault("settings", {})["tradition"] = text
        self.state.save()
        self.on_refresh()

    def toggle_prayer_times(self, enabled):
        self.state.data.setdefault("prayer_times", {})["enabled"] = enabled
        self.prayer_times_container.setVisible(enabled)
        self.state.save()
        # Notify main window to start/stop reminder timer
        if hasattr(self.window(), 'update_prayer_timer'):
            self.window().update_prayer_timer()

    def save_prayer_times(self):
        times = [te.time().toString("HH:mm") for te in self.time_edits]
        self.state.data.setdefault("prayer_times", {})["times"] = times
        self.state.save()

    def test_notification(self):
        if hasattr(self.window(), 'show_notification'):
            self.window().show_notification("🔔 Test Reminder", "Prayer notifications are working!")

    def save_partner(self, text):
        self.state.data["partner_name"] = text
        self.state.save()

    def export_partner_card(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Pilgrim Card", 
                                               f"pilgrim_card_{date.today()}.json", "JSON (*.json)")
        if path:
            card = {
                "type": "soul_journey_pilgrim_card",
                "version": "4.0",
                "exported": datetime.now().isoformat(),
                "pilgrim": {
                    "name": self.state.data.get("partner_name", "Anonymous Pilgrim"),
                    "title": self.state.get_title(),
                    "level": self.state.data["level"],
                    "total_xp": self.state.data.get("total_xp", 0),
                    "streak": self.state.data["streak"],
                    "virtues": dict(self.state.data["virtues"]),
                    "achievements": len(self.state.data.get("achievements", [])),
                    "pilgrimages": len(self.state.data.get("pilgrimages", [])),
                    "meditations": self.state.data.get("meditations", 0),
                    "journal_entries": len(self.state.data.get("journal", [])),
                    "charity_acts": len(self.state.data.get("charity", [])),
                }
            }
            with open(path, 'w') as f:
                json.dump(card, f, indent=2)
            QMessageBox.information(self, "Exported", f"Pilgrim card saved to:\n{path}\n\nShare this file with your accountability partner!")

    def import_partner_card(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Partner's Card", "", "JSON (*.json)")
        if path:
            try:
                with open(path, 'r') as f:
                    card = json.load(f)
                if card.get("type") != "soul_journey_pilgrim_card":
                    QMessageBox.warning(self, "Invalid Card", "This is not a valid pilgrim card.")
                    return
                p = card["pilgrim"]
                msg = (f"👤 {p['name']}\n"
                       f"✦ {p['title']} (Level {p['level']})\n"
                       f"⭐ {p['total_xp']} XP  •  🔥 {p['streak']} day streak\n\n"
                       f"📖 Wisdom: {p['virtues']['Wisdom']}\n"
                       f"🤲 Compassion: {p['virtues']['Compassion']}\n"
                       f"⚔️ Discipline: {p['virtues']['Discipline']}\n"
                       f"🕯️ Devotion: {p['virtues']['Devotion']}\n\n"
                       f"🏆 {p['achievements']} achievements\n"
                       f"🗺️ {p['pilgrimages']} pilgrimages\n"
                       f"🧘 {p['meditations']} meditations\n"
                       f"📔 {p['journal_entries']} journal entries\n"
                       f"💝 {p['charity_acts']} charity acts")
                QMessageBox.information(self, "Partner's Journey", msg)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not read file: {e}")

    def export_save(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Save", "soul_journey_backup.json", "JSON (*.json)")
        if path:
            import shutil
            shutil.copy(SAVE_FILE, path)
            QMessageBox.information(self, "Exported", f"Save exported to:\n{path}")

    def import_save(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Save", "", "JSON (*.json)")
        if path:
            reply = QMessageBox.question(self, "Import Save", "This will replace your current progress. Continue?")
            if reply == QMessageBox.Yes:
                import shutil
                shutil.copy(path, SAVE_FILE)
                QMessageBox.information(self, "Imported", "Save imported. Restart the app.")

    def reset_data(self):
        reply = QMessageBox.warning(self, "Reset Data", "Are you sure? This will erase ALL progress.",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            QMessageBox.information(self, "Reset", "All data erased. Restart the app.")


# ==========================================
# MAIN WINDOW
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.state = GameState()
        self.setWindowTitle("Soul Journey — Divine Edition")
        self.resize(1000, 780)
        
        # System tray (NEW)
        self.tray_icon = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            # Create a simple icon programmatically
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setPen(QColor("#f0c850"))
            painter.setFont(QFont("Segoe UI Emoji", 20))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, "🕯️")
            painter.end()
            self.tray_icon.setIcon(QIcon(pixmap))
            self.tray_icon.setToolTip("Soul Journey — Divine Edition")
            
            tray_menu = QMenu()
            show_action = QAction("Show", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)
            quit_action = QAction("Quit", self)
            quit_action.triggered.connect(QApplication.instance().quit)
            tray_menu.addAction(quit_action)
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.dashboard = DashboardPage(self.state, self.refresh_all)
        self.practices = PracticesPage(self.state, self.handle_action)
        self.beads = PrayerBeadsPage(self.state, self.handle_action)
        self.scripture = ScripturePage(self.state, self.handle_action)
        self.fasting = FastingPage(self.state, self.handle_action)
        self.charity = CharityPage(self.state, self.handle_action)
        self.rituals = RitualsPage(self.state, self.handle_action)
        self.pilgrimage = PilgrimagePage(self.state, self.handle_action)
        self.calendar = CalendarPage(self.state)
        self.quests = QuestsPage(self.state)
        self.journal = JournalPage(self.state, self.handle_action)
        self.virtues = VirtuesPage(self.state)
        self.achievements = AchievementsPage(self.state)
        self.stats = StatsPage(self.state)
        self.settings = SettingsPage(self.state, self.refresh_all)
        
        self.tabs.addTab(self.dashboard, "🏛️ Home")
        self.tabs.addTab(self.practices, "⚔️ Practices")
        self.tabs.addTab(self.beads, "📿 Beads")
        self.tabs.addTab(self.scripture, "📖 Texts")
        self.tabs.addTab(self.fasting, "🌙 Fasting")
        self.tabs.addTab(self.charity, "💝 Giving")
        self.tabs.addTab(self.rituals, "🕉️ Rituals")
        self.tabs.addTab(self.pilgrimage, "🗺️ Pilgrim")
        self.tabs.addTab(self.calendar, "📅 Calendar")
        self.tabs.addTab(self.quests, "📜 Quests")
        self.tabs.addTab(self.journal, "📔 Journal")
        self.tabs.addTab(self.virtues, "🌟 Virtues")
        self.tabs.addTab(self.achievements, "🏆 Trophies")
        self.tabs.addTab(self.stats, "📊 Stats")
        self.tabs.addTab(self.settings, "⚙️ Settings")

        QTimer.singleShot(500, self.maybe_trigger_event)
        
        # Prayer reminder timer (NEW) - checks every 30 seconds
        self.prayer_timer = QTimer()
        self.prayer_timer.timeout.connect(self.check_prayer_times)
        self.update_prayer_timer()
        
        # Track already-notified times today
        self.notified_times_today = set()
        today_str = str(date.today())
        if self.state.data.get("last_prayer_date") != today_str:
            self.state.data["last_prayer_date"] = today_str
            self.state.save()
        else:
            self.notified_times_today = set(self.state.data.get("notified_times_today", []))

    def update_prayer_timer(self):
        enabled = self.state.data.get("prayer_times", {}).get("enabled", False)
        if enabled:
            self.prayer_timer.start(30000)  # Check every 30 seconds
        else:
            self.prayer_timer.stop()

    def check_prayer_times(self):
        """Check if current time matches any prayer time."""
        now = QTime.currentTime()
        times = self.state.data.get("prayer_times", {}).get("times", [])
        today_str = str(date.today())
        
        # Reset daily notification tracking
        if self.state.data.get("last_prayer_date") != today_str:
            self.state.data["last_prayer_date"] = today_str
            self.state.data["notified_times_today"] = []
            self.notified_times_today = set()
            self.state.save()
        
        for i, time_str in enumerate(times):
            h, m = map(int, time_str.split(":"))
            prayer_time = QTime(h, m)
            
            # If within 1 minute window and not yet notified
            diff_seconds = abs(now.secsTo(prayer_time))
            if diff_seconds <= 30 and time_str not in self.notified_times_today:
                self.notified_times_today.add(time_str)
                self.state.data["notified_times_today"] = list(self.notified_times_today)
                self.state.save()
                
                labels = ["Fajr / Morning", "Dhuhr / Midday", "Asr / Afternoon", 
                          "Maghrib / Evening", "Isha / Night"]
                label = labels[i] if i < len(labels) else f"Prayer {i+1}"
                self.show_notification(f"🔔 {label} Prayer", 
                                       f"It's time for {label} prayer. May your devotion be accepted.")
                break

    def show_notification(self, title, message):
        """Show system tray notification."""
        if self.tray_icon and self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)
        else:
            # Fallback to message box
            QMessageBox.information(self, title, message)

    def handle_action(self, xp_amount, source_widget, result):
        if source_widget:
            try:
                pos = source_widget.mapTo(self.tabs, QPoint(source_widget.width() // 2, 0))
                text = f"+{result['amount']} XP"
                FloatingXPLabel(text, self.tabs, pos)
            except Exception:
                pass
        if result.get("leveled"):
            QTimer.singleShot(300, lambda: self.celebrate_level(result["new_level"]))
        new_achs = self.state.check_new_achievements()
        if new_achs:
            QTimer.singleShot(800, lambda: self.show_achievements(new_achs))
        self.refresh_all()

    def refresh_all(self):
        self.dashboard.refresh()
        self.beads.refresh()
        self.scripture.refresh()
        self.fasting.refresh()
        self.charity.refresh()
        self.rituals.refresh_custom()
        self.pilgrimage.refresh()
        self.calendar.refresh()
        self.quests.refresh()
        self.virtues.refresh()
        self.journal.refresh()
        self.achievements.refresh()
        self.stats.refresh()

    def celebrate_level(self, new_level):
        dlg = QDialog(self)
        dlg.setWindowTitle("✦ Ascension ✦")
        dlg.resize(400, 250)
        layout = QVBoxLayout(dlg)
        title = QLabel(f"🌟 Level {new_level}! 🌟")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #f0c850;")
        new_title = self.state.get_title()
        subtitle = QLabel(f"You are now a {new_title}")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #e0e0e0;")
        msg = QLabel("Your soul grows stronger.")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("font-size: 13px; color: #a0a0b0;")
        btn = QPushButton("Continue")
        btn.clicked.connect(dlg.accept)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(msg)
        layout.addWidget(btn)
        dlg.exec()

    def show_achievements(self, achievements):
        for ach in achievements:
            QMessageBox.information(self, "🏆 Achievement Unlocked!", 
                                    f"{ach['icon']} {ach['name']}\n\n{ach['desc']}")

    def maybe_trigger_event(self):
        if random.random() < 0.20:
            event = random.choice(DIVINE_EVENTS)
            self.trigger_event(event)

    def trigger_event(self, event):
        if event["effect"] == "xp":
            self.state.add_xp(event["value"])
        elif event["effect"] == "virtue":
            self.state.data["virtues"][event["virtue"]] += event["value"]
            self.state.mark_activity_today()
            self.state.save()
        elif event["effect"] == "double_xp":
            self.state.double_xp_active = True
        self.refresh_all()
        msg = f"{event['name']}\n\n{event['desc']}\n\n"
        if event["effect"] == "xp":
            msg += f"+{event['value']} XP"
        elif event["effect"] == "virtue":
            msg += f"+{event['value']} {event['virtue']}"
        elif event["effect"] == "double_xp":
            msg += "Your next action gives DOUBLE XP!"
        QMessageBox.information(self, "✨ Divine Event ✨", msg)

    def closeEvent(self, event):
        # Minimize to tray instead of closing (if tray available)
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            self.tray_icon.showMessage("Soul Journey", 
                                       "App minimized to tray. Keep walking the path. 🙏",
                                       QSystemTrayIcon.Information, 2000)
            event.ignore()
        else:
            event.accept()


# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray
    window = MainWindow()
    window.show()
    sys.exit(app.exec())