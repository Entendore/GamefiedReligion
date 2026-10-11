#!/usr/bin/env python3
"""
Sacred Path v4 — Ultimate Gamified Spiritual Practice Tracker (25+ Systems)
Single-file PySide6 application
"""

import sys, json, math, random, uuid, time
from datetime import datetime, date, timedelta
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

SAVE_DIR = Path.home() / ".sacred_path"
SAVE_FILE = SAVE_DIR / "save.json"

# ── Theme Colors ─────────────────────────────────────────────────
C_BG=QColor(13,13,26);C_BG2=QColor(22,22,42);C_BG3=QColor(34,34,64)
C_GOLD=QColor(212,168,67);C_GOLD_L=QColor(240,208,120);C_AMBER=QColor(232,168,56)
C_TEXT=QColor(240,230,211);C_TEXT2=QColor(139,139,158)
C_GREEN=QColor(78,204,163);C_RED=QColor(231,76,60);C_BLUE=QColor(52,152,219)
C_PURPLE=QColor(155,89,182);C_PINK=QColor(232,100,150)

VC={"faith":QColor(240,208,120),"hope":QColor(243,156,18),"love":QColor(231,76,60),
    "wisdom":QColor(52,152,219),"patience":QColor(78,204,163),"humility":QColor(155,89,182)}
VI={"faith":"✦","hope":"☀","love":"♥","wisdom":"◈","patience":"⚒","humility":"❋"}
VT={0:"Novice",10:"Acolyte",25:"Devotee",50:"Sage",75:"Master",100:"Transcendent"}

PRACTICES={
    "prayer":{"name":"Prayer","xp":15,"ico":"✦","virtues":{"faith":3,"hope":1}},
    "meditation":{"name":"Meditation","xp":20,"ico":"◎","virtues":{"patience":3,"wisdom":1}},
    "scripture":{"name":"Sacred Reading","xp":25,"ico":"✎","virtues":{"wisdom":3,"faith":1}},
    "charity":{"name":"Charity","xp":30,"ico":"♡","virtues":{"love":3,"humility":1}},
    "fasting":{"name":"Self-Discipline","xp":35,"ico":"◈","virtues":{"patience":2,"humility":2}},
    "gratitude":{"name":"Gratitude","xp":10,"ico":"✿","virtues":{"hope":2,"love":2}},
}
MOODS={"joy":"😊","peace":"😌","gratitude":"🙏","hope":"🌟","love":"💖","sadness":"😢","anxiety":"😰","anger":"😤","neutral":"😐","tired":"😴"}
TASBIH_PRESETS=[{"name":"SubhanAllah","count":33,"desc":"Glory be to God"},{"name":"Alhamdulillah","count":33,"desc":"Praise be to God"},{"name":"Allahu Akbar","count":34,"desc":"God is Greatest"},{"name":"Jesus Prayer","count":100,"desc":"Lord Jesus Christ, have mercy"},{"name":"Om Mani Padme Hum","count":108,"desc":"The jewel is in the lotus"},{"name":"Custom","count":33,"desc":"Set your own count"}]
DAILY_OFFICE={
    "lauds":{"name":"Lauds (Morning)","time":"Dawn","verses":["This is the day the Lord has made; let us rejoice.","O Lord, open my lips, and my mouth shall declare your praise.","Let the morning bring me word of your unfailing love.","Be still, and know that I am God."]},
    "terce":{"name":"Terce (Mid-Morning)","time":"9 AM","verses":["Create in me a pure heart, O God.","The Lord is my shepherd; I shall not want.","Show me your ways, Lord, teach me your paths.","I can do all things through Christ who strengthens me."]},
    "sext":{"name":"Sext (Midday)","time":"Noon","verses":["The Lord is my light and my salvation—whom shall I fear?","Trust in the Lord with all your heart.","Be strong and courageous. Do not be afraid.","In quietness and trust is your strength."]},
    "none":{"name":"None (Afternoon)","time":"3 PM","verses":["The Lord is close to the brokenhearted.","Come to me, all who are weary and burdened.","He heals the brokenhearted and binds up their wounds.","Cast all your anxiety on Him because He cares for you."]},
    "vespers":{"name":"Vespers (Evening)","time":"Dusk","verses":["The Lord bless you and keep you.","Evening and morning and at noon I will pray.","May the peace of God guard your heart and mind.","Into your hands I commit my spirit."]},
    "compline":{"name":"Compline (Night)","time":"Bedtime","verses":["In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.","Be still before the Lord and wait patiently for him.","He grants sleep to those he loves.","Now I lay me down to sleep, I pray the Lord my soul to keep."]},
}
EXAMEN_STEPS=[{"name":"Gratitude","prompt":"What am I most grateful for today?","icon":"🙏"},{"name":"Review","prompt":"Review your day. What stands out?","icon":"🔍"},{"name":"Awareness","prompt":"Where did I feel the divine presence? Where did I feel distant?","icon":"💡"},{"name":"Repentance","prompt":"What do I need to ask forgiveness for?","icon":"💔"},{"name":"Resolution","prompt":"What is one concrete step I will take tomorrow?","icon":"✦"}]
LECTIO_TEXTS=[
    {"ref":"Psalm 23:1-4","text":"The Lord is my shepherd, I shall not want. He makes me lie down in green pastures. He leads me beside still waters. He restores my soul. He guides me in paths of righteousness for his name's sake. Even though I walk through the valley of the shadow of death, I will fear no evil, for you are with me; your rod and your staff, they comfort me.","source":"Hebrew Bible"},
    {"ref":"Matthew 5:3-8","text":"Blessed are the poor in spirit, for theirs is the kingdom of heaven. Blessed are those who mourn, for they will be comforted. Blessed are the meek, for they will inherit the earth. Blessed are those who hunger and thirst for righteousness, for they will be filled. Blessed are the merciful, for they will be shown mercy. Blessed are the pure in heart, for they will see God.","source":"New Testament"},
    {"ref":"Quran 24:35","text":"Allah is the Light of the heavens and the earth. The example of His light is like a niche within which is a lamp, the lamp within glass, the glass as if it were a pearly white star lit from the oil of a blessed olive tree... Light upon light. Allah guides to His light whom He wills.","source":"Quran"},
    {"ref":"Bhagavad Gita 2:47","text":"You have the right to work, but never to the fruit of work. You should never engage in action for the sake of reward, nor should you long for inaction. Perform your duty, abandoning all attachment to success or failure. Such evenness of mind is called Yoga.","source":"Bhagavad Gita"},
    {"ref":"Dhammapada 1-2","text":"Mind is the forerunner of all states. Mind is chief; mind-made are they. If one speaks or acts with a wicked mind, suffering follows one... If one speaks or acts with a pure mind, happiness follows one, like a shadow that never departs.","source":"Buddhism"},
    {"ref":"Tao Te Ching 1","text":"The Tao that can be told is not the eternal Tao. The name that can be named is not the eternal name. The nameless is the beginning of heaven and earth... Darkness within darkness, the gate to all mystery.","source":"Taoism"},
    {"ref":"1 Corinthians 13:4-7","text":"Love is patient, love is kind. It does not envy, it does not boast, it is not proud. It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs. Love does not delight in evil but rejoices with the truth. It always protects, always trusts, always hopes, always perseveres.","source":"New Testament"},
    {"ref":"Rumi: Guest House","text":"This being human is a guest house. Every morning a new arrival. A joy, a depression, a meanness... Welcome and entertain them all! Even if they are a crowd of sorrows, who violently sweep your house empty of its furniture, still, treat each guest honorably. He may be clearing you out for some new delight.","source":"Sufi Poetry"},
]
HOLY_FIGURES=[
    {"name":"Saint Francis","trad":"Christianity","date":"Oct 4","quote":"Start by doing what is necessary; then do what is possible; suddenly you are doing the impossible.","virtue":"humility"},
    {"name":"Rumi","trad":"Sufi Islam","date":"Sep 30","quote":"The wound is the place where the Light enters you.","virtue":"love"},
    {"name":"Thich Nhat Hanh","trad":"Buddhism","date":"Oct 11","quote":"The present moment is filled with joy and happiness. If you are attentive, you will see it.","virtue":"patience"},
    {"name":"Thomas Merton","trad":"Christianity","date":"Dec 10","quote":"In the last analysis, the individual person is responsible for living his own life and for finding himself.","virtue":"wisdom"},
    {"name":"Rabbi Hillel","trad":"Judaism","date":"Unknown","quote":"If I am not for myself, who will be? If I am only for myself, what am I?","virtue":"faith"},
    {"name":"Gandhi","trad":"Hinduism","date":"Oct 2","quote":"Be the change you wish to see in the world.","virtue":"patience"},
    {"name":"Julian of Norwich","trad":"Christianity","date":"May 13","quote":"All shall be well, and all shall be well, and all manner of thing shall be well.","virtue":"hope"},
    {"name":"Lao Tzu","trad":"Taoism","date":"Unknown","quote":"The journey of a thousand miles begins with a single step.","virtue":"wisdom"},
    {"name":"Prophet Muhammad ﷺ","trad":"Islam","date":"Unknown","quote":"The best among you are those who have the best manners and character.","virtue":"humility"},
    {"name":"Buddha","trad":"Buddhism","date":"Unknown","quote":"Peace comes from within. Do not seek it without.","virtue":"patience"},
    {"name":"Mother Teresa","trad":"Christianity","date":"Sep 5","quote":"Not all of us can do great things. But we can do small things with great love.","virtue":"love"},
    {"name":"MLK Jr.","trad":"Christianity","date":"Jan 15","quote":"Darkness cannot drive out darkness; only light can do that.","virtue":"hope"},
]
ACHIEVEMENTS=[
    {"id":"first_prayer","name":"First Light","desc":"First practice","cond":lambda d:d["total"]>=1},
    {"id":"daily_full","name":"Devoted Day","desc":"All 6 in one day","cond":lambda d:d.get("all_today",False)},
    {"id":"streak_3","name":"Kindling Faith","desc":"3-day streak","cond":lambda d:d["streak"]>=3},
    {"id":"streak_7","name":"Week of Light","desc":"7-day streak","cond":lambda d:d["streak"]>=7},
    {"id":"streak_30","name":"Monthly Devotion","desc":"30-day streak","cond":lambda d:d["streak"]>=30},
    {"id":"streak_100","name":"Century","desc":"100-day streak","cond":lambda d:d["streak"]>=100},
    {"id":"level_5","name":"Pathfinder","desc":"Level 5","cond":lambda d:d["level"]>=5},
    {"id":"level_10","name":"Pillar","desc":"Level 10","cond":lambda d:d["level"]>=10},
    {"id":"level_25","name":"Beacon","desc":"Level 25","cond":lambda d:d["level"]>=25},
    {"id":"prac_50","name":"Dedicated","desc":"50 practices","cond":lambda d:d["total"]>=50},
    {"id":"prac_100","name":"Unwavering","desc":"100 practices","cond":lambda d:d["total"]>=100},
    {"id":"prac_500","name":"Legend","desc":"500 practices","cond":lambda d:d["total"]>=500},
    {"id":"virtue_25","name":"Virtue Awakened","desc":"Any virtue 25","cond":lambda d:any(v>=25 for v in d["virtues"].values())},
    {"id":"virtue_50","name":"Virtue Mastered","desc":"Any virtue 50","cond":lambda d:any(v>=50 for v in d["virtues"].values())},
    {"id":"all_v10","name":"Balanced Soul","desc":"All virtues ≥10","cond":lambda d:all(v>=10 for v in d["virtues"].values())},
    {"id":"all_v50","name":"Harmonious Spirit","desc":"All virtues ≥50","cond":lambda d:all(v>=50 for v in d["virtues"].values())},
    {"id":"med_30","name":"Contemplative","desc":"30m meditation","cond":lambda d:d["med_total"]>=30},
    {"id":"med_120","name":"Deep Dweller","desc":"2h meditation","cond":lambda d:d["med_total"]>=120},
    {"id":"journal_10","name":"Scribe","desc":"10 journal entries","cond":lambda d:len(d["journal"])>=10},
    {"id":"tasbih_100","name":"Dhikr Adept","desc":"100 recitations","cond":lambda d:d.get("tasbih_total",0)>=100},
    {"id":"quests_10","name":"Quest Seeker","desc":"10 quests","cond":lambda d:d.get("quests_done",0)>=10},
    {"id":"skills_5","name":"Skill Adept","desc":"5 skill nodes","cond":lambda d:sum(d.get("skills",{}).values())>=5},
    {"id":"altar_full","name":"Sacred Space","desc":"All altar items","cond":lambda d:len(d.get("altar_unlocked",[]))>=12},
    {"id":"office_all","name":"Prayerful Day","desc":"All offices","cond":lambda d:len(d.get("offices_today",[]))>=6},
    {"id":"fast_8","name":"Ascetic","desc":"8h fast","cond":lambda d:d.get("longest_fast",0)>=8},
    {"id":"mood_30","name":"Self-Aware","desc":"30 moods","cond":lambda d:len(d.get("moods",[]))>=30},
    {"id":"examen_5","name":"Examen Adept","desc":"5 examens","cond":lambda d:d.get("examen_total",0)>=5},
    {"id":"lectio_5","name":"Lectio Adept","desc":"5 lectios","cond":lambda d:d.get("lectio_total",0)>=5},
]
BLESSINGS=[
    {"id":"divine_favor","name":"Divine Favor","desc":"+15% XP","from":"first_prayer","ico":"✧"},
    {"id":"kindled_flame","name":"Kindled Flame","desc":"Streak +50%","from":"streak_3","ico":"🔥"},
    {"id":"steady_shield","name":"Steadfast Shield","desc":"1-day grace","from":"streak_7","ico":"🛡"},
    {"id":"wisdom_flow","name":"Wisdom Flow","desc":"+1 Wisdom","from":"virtue_25","ico":"◈"},
    {"id":"sacred_radiance","name":"Sacred Radiance","desc":"+25% XP","from":"level_10","ico":"☀"},
    {"id":"love_aura","name":"Love's Aura","desc":"+1 Love","from":"virtue_50","ico":"♥"},
    {"id":"devotion_mastery","name":"Devotion Mastery","desc":"+40% XP","from":"level_25","ico":"✦"},
    {"id":"harmony","name":"Harmony","desc":"+1 all virtues","from":"all_v10","ico":"❋"},
    {"id":"eternal_flame","name":"Eternal Flame","desc":"Streak never resets","from":"streak_100","ico":"★"},
    {"id":"transcendence","name":"Transcendence","desc":"Virtue ×2","from":"all_v50","ico":"✧"},
]
SKILL_TREE={
    "inner_light":{"name":"Inner Light","desc":"Prayer XP +10%/lv","cost":5,"virtue":"faith","icon":"✦","max":3},
    "steadfast_hope":{"name":"Steadfast Hope","desc":"Streak bonus +20%/lv","cost":5,"virtue":"hope","icon":"☀","max":3},
    "radiant_love":{"name":"Radiant Love","desc":"+1 Love/Charity/lv","cost":5,"virtue":"love","icon":"♥","max":3},
    "deep_wisdom":{"name":"Deep Wisdom","desc":"+1 Wisdom/Reading/lv","cost":5,"virtue":"wisdom","icon":"◈","max":3},
    "enduring_patience":{"name":"Enduring Patience","desc":"Meditation XP +15%/lv","cost":5,"virtue":"patience","icon":"⚒","max":3},
    "true_humility":{"name":"True Humility","desc":"+1 Humility/Fast/lv","cost":5,"virtue":"humility","icon":"❋","max":3},
    "devotion_mastery":{"name":"Devotion Mastery","desc":"All XP +5%/lv","cost":8,"virtue":"faith","icon":"★","max":5},
    "harmonic_balance":{"name":"Harmonic Balance","desc":"+0.5 all virtues/lv","cost":10,"virtue":"wisdom","icon":"☯","max":3},
    "sacred_resilience":{"name":"Sacred Resilience","desc":"1-day shield/lv","cost":8,"virtue":"patience","icon":"🛡","max":2},
    "overflowing_grace":{"name":"Overflowing Grace","desc":"Double XP on levelup","cost":12,"virtue":"love","icon":"✧","max":1},
}
ALTAR_ITEMS=[
    {"id":"candle","name":"Candle","ico":"🕯","unlock":"first_prayer","pos":[.5,.7]},
    {"id":"cross","name":"Cross","ico":"✝","unlock":"streak_7","pos":[.3,.65]},
    {"id":"star_david","name":"Star of David","ico":"✡","unlock":"streak_7","pos":[.7,.65]},
    {"id":"crescent","name":"Crescent","ico":"☪","unlock":"streak_7","pos":[.5,.3]},
    {"id":"om","name":"Om","ico":"ॐ","unlock":"virtue_25","pos":[.25,.4]},
    {"id":"lotus","name":"Lotus","ico":"🪷","unlock":"virtue_25","pos":[.75,.4]},
    {"id":"book","name":"Sacred Book","ico":"📕","unlock":"prac_50","pos":[.5,.5]},
    {"id":"incense","name":"Incense","ico":"🪔","unlock":"med_30","pos":[.4,.55]},
    {"id":"water","name":"Holy Water","ico":"💧","unlock":"level_10","pos":[.6,.55]},
    {"id":"dove","name":"Dove","ico":"🕊","unlock":"all_v10","pos":[.35,.3]},
    {"id":"light","name":"Divine Light","ico":"✨","unlock":"level_25","pos":[.65,.3]},
    {"id":"crown","name":"Crown","ico":"👑","unlock":"all_v50","pos":[.5,.15]},
]
QUEST_TEMPLATES=[
    {"text":"Complete {p} twice today","type":"double","xp":20,"icon":"⚡"},
    {"text":"Spend 10+ minutes in meditation","type":"med","val":10,"xp":25,"icon":"⏱"},
    {"text":"Write a journal entry","type":"journal","xp":15,"icon":"✎"},
    {"text":"Log your mood","type":"mood","xp":15,"icon":"😊"},
    {"text":"Complete a Tasbih round","type":"tasbih","xp":20,"icon":"📿"},
    {"text":"Add a prayer intention","type":"intention","xp":10,"icon":"♡"},
    {"text":"Practice 3 different virtues","type":"multi_v","val":3,"xp":30,"icon":"✦"},
    {"text":"Complete all practices","type":"all","xp":50,"icon":"★"},
    {"text":"Recite a daily office","type":"office","xp":15,"icon":"🕰"},
    {"text":"Complete the Examen","type":"examen","xp":25,"icon":"🔍"},
    {"text":"Do Lectio Divina","type":"lectio","xp":25,"icon":"📖"},
    {"text":"Fast for 4+ hours","type":"fast","val":4,"xp":30,"icon":"◈"},
]
TITLES=[
    {"id":"seeker","name":"Seeker","cond":lambda d:d["total"]>=1},
    {"id":"devotee","name":"Devotee","cond":lambda d:d["total"]>=25},
    {"id":"disciple","name":"Disciple","cond":lambda d:d["level"]>=5},
    {"id":"keeper","name":"Keeper of the Flame","cond":lambda d:d["streak"]>=7},
    {"id":"contemplative","name":"Contemplative","cond":lambda d:d["med_total"]>=60},
    {"id":"sage","name":"Sage","cond":lambda d:all(v>=25 for v in d["virtues"].values())},
    {"id":"shepherd","name":"Shepherd of Souls","cond":lambda d:d["total"]>=100},
    {"id":"pillar","name":"Pillar of Faith","cond":lambda d:d["streak"]>=30},
    {"id":"illuminated","name":"The Illuminated","cond":lambda d:d["level"]>=25},
    {"id":"master","name":"Master of Virtues","cond":lambda d:all(v>=50 for v in d["virtues"].values())},
    {"id":"beacon","name":"Sacred Beacon","cond":lambda d:d["total"]>=500},
    {"id":"transcendent","name":"The Transcendent","cond":lambda d:d["streak"]>=100 and d["level"]>=50},
]
WISDOM=[("The journey of a thousand miles begins with a single step.","Lao Tzu"),("Peace comes from within. Do not seek it without.","Buddha"),("Love your neighbor as yourself.","Jesus"),("The best of people are those most beneficial to others.","Muhammad ﷺ"),("You have the right to work, but never to the fruit of work.","Bhagavad Gita"),("Be the change you wish to see in the world.","Gandhi"),("The only true wisdom is in knowing you know nothing.","Socrates"),("Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.","Buddha"),("What we think, we become.","Buddha"),("The wound is the place where the Light enters you.","Rumi"),("In the middle of difficulty lies opportunity.","Einstein"),("Faith is taking the first step even when you don't see the whole staircase.","MLK Jr."),("He who knows others is wise; he who knows himself is enlightened.","Lao Tzu"),("The soul always knows what to do to heal itself. The challenge is to silence the mind.","Caroline Myss"),("Happiness depends upon ourselves.","Aristotle"),("The present moment is filled with joy and happiness. If you are attentive, you will see it.","Thich Nhat Hanh"),("God does not burden a soul beyond that it can bear.","Quran 2:286"),("Darkness cannot drive out darkness; only light can do that.","MLK Jr."),("We are what we repeatedly do. Excellence is not an act, but a habit.","Aristotle"),("Knowing yourself is the beginning of all wisdom.","Aristotle"),("The greatest glory in living lies not in never falling, but in rising every time we fall.","Mandela"),("When you realize nothing is lacking, the whole world belongs to you.","Lao Tzu"),("Your task is not to seek for love, but merely to seek and find all the barriers within yourself.","Rumi"),("He who has a why to live can bear almost any how.","Nietzsche"),("Surrender to what is. Let go of what was. Have faith in what will be.","Sonia Ricotti"),("The mind is everything. What you think you become.","Buddha"),("Act without expectation.","Lao Tzu"),("Patience is not the ability to wait, but how you act while you're waiting.","Joyce Meyer"),("Every moment is a fresh beginning.","T.S. Eliot"),("Where there is love, there is life.","Gandhi")]
PROMPTS=["What am I most grateful for today?","Where did I experience beauty today?","How did I show kindness?","What challenged me today?","How did I grow closer to my values?","What brought me peace?","Who needs my prayers?","What am I holding onto?","How can I serve others?","What am I proud of?","What am I avoiding?","How did I practice patience?","What gave me hope?","In what ways was I humble?","How did I express love?","What would my highest self say?","What habit served me well?","What connection did I make with the divine?","What fear did I face?","How can I be more present tomorrow?"]

# ── Utility Functions ────────────────────────────────────────────
def L(txt, sz=11, b=False, c=C_TEXT):
    l=QLabel(txt); l.setStyleSheet(f"font-size:{sz}px;{'font-weight:bold;' if b else ''}color:{c.name()};"); return l
def Btn(txt, bg="#d4a843", fg="#0d0d1a", h="#f0d078", b=True):
    b=QPushButton(txt); b.setCursor(Qt.PointingHandCursor)
    s=f"QPushButton{{background:{bg};color:{fg};font-size:11px;{'font-weight:bold;' if b else ''}border:none;border-radius:6px;padding:7px 14px;}}QPushButton:hover{{background:{h};}}"
    b.setStyleSheet(s); return b
def Card(bg="#1a1a2e", bd="#32325a"):
    c=QFrame(); c.setStyleSheet(f"QFrame{{background:{bg};border:1px solid {bd};border-radius:10px;}}"); return c

# ── Data Manager ─────────────────────────────────────────────────
class DM:
    def __init__(self):
        self.data=self._def(); self._load(); self._check_day()
    def _def(self):
        return {"name":"Pilgrim","level":1,"xp":0,"xp_next":100,"virtues":{k:0 for k in VC},
                "streak":0,"best_streak":0,"achievements":[],"total":0,"counts":{k:0 for k in PRACTICES},
                "history":{},"med_sessions":[],"med_total":0,"intentions":[],"journal":[],
                "cur_date":str(date.today()),"all_today":False,"today_done":[],
                "tasbih_total":0,"tasbih_sessions":[],"moods":[],"quests_done":0,
                "skills":{k:0 for k in SKILL_TREE},"skill_points":0,"altar_unlocked":[],"altar_placed":[],
                "offices_today":[],"fast_sessions":[],"longest_fast":0,
                "active_title":"seeker","fav_quotes":[],"examen_today":[],"examen_total":0,
                "lectio_today":False,"lectio_total":0,"figures_visited":[]}
    def save(self):
        SAVE_DIR.mkdir(parents=True,exist_ok=True); SAVE_FILE.write_text(json.dumps(self.data,indent=2))
    def _load(self):
        if not SAVE_FILE.exists(): return
        try:
            ld=json.loads(SAVE_FILE.read_text())
            for k in self._def(): ld.setdefault(k,self._def()[k])
            if not ld.get("history"): ld["history"]={}
            ld["skills"]={k:ld["skills"].get(k,0) for k in SKILL_TREE}
            self.data=ld
        except: pass
    def _check_day(self):
        today=str(date.today())
        if self.data["cur_date"]!=today:
            if self.data["history"].get(self.data["cur_date"]): self.data["today_done"]=list(self.data["history"][self.data["cur_date"]])
            else: self.data["today_done"]=[]
            self.data["all_today"]=False; self.data["cur_date"]=today
            self.data["offices_today"]=[]; self.data["examen_today"]=[]; self.data["lectio_today"]=False
            self._calc_streak(); self._gen_quests(); self._calc_title(); self.save()
    def _calc_streak(self):
        if self._has_blessing("eternal_flame"):
            s=0;d=date.today()
            while str(d) in self.data["history"] and self.data["history"][str(d)]: s+=1;d-=timedelta(days=1)
            if s==0: d=date.today()-timedelta(days=1)
            while str(d) in self.data["history"] and self.data["history"][str(d)]: s+=1;d-=timedelta(days=1)
        else:
            shields=self.data["skills"].get("sacred_resilience",0);s=0;d=date.today();gap=0
            while True:
                ds=str(d)
                if ds in self.data["history"] and self.data["history"][ds]: s+=1;d-=timedelta(days=1)
                elif gap<shields: gap+=1;d-=timedelta(days=1)
                else: break
        self.data["streak"]=s; self.data["best_streak"]=max(self.data["best_streak"],s)
    def _has_blessing(self,bid): return next((b["from"] for b in BLESSINGS if b["id"]==bid),None) in self.data["achievements"]
    def _xp_mult(self):
        m=1.0
        if self._has_blessing("divine_favor"): m=max(m,1.15)
        if self._has_blessing("sacred_radiance"): m=max(m,1.25)
        if self._has_blessing("devotion_mastery"): m=max(m,1.40)
        m+=self.data["skills"].get("devotion_mastery",0)*0.05; return m
    def _virtue_bonus(self):
        bonus={};sk=self.data["skills"];today=self.data["history"].get(str(date.today()),[])
        if self._has_blessing("wisdom_flow"): bonus["wisdom"]=bonus.get("wisdom",0)+1
        if self._has_blessing("love_aura"): bonus["love"]=bonus.get("love",0)+1
        if self._has_blessing("harmony"):
            for k in VC: bonus[k]=bonus.get(k,0)+1
        if sk.get("radiant_love",0)>0 and "charity" in today: bonus["love"]=bonus.get("love",0)+sk["radiant_love"]
        if sk.get("deep_wisdom",0)>0 and "scripture" in today: bonus["wisdom"]=bonus.get("wisdom",0)+sk["deep_wisdom"]
        if sk.get("true_humility",0)>0 and "fasting" in today: bonus["humility"]=bonus.get("humility",0)+sk["true_humility"]
        if sk.get("harmonic_balance",0)>0:
            for k in VC: bonus[k]=bonus.get(k,0)+sk["harmonic_balance"]*0.5
        return bonus, self._has_blessing("transcendence")
    def _add_xp(self,n):
        if self.data["skills"].get("overflowing_grace",0)>0: n*=2
        self.data["xp"]+=n
        while self.data["xp"]>=self.data["xp_next"]:
            self.data["xp"]-=self.data["xp_next"]; self.data["level"]+=1
            self.data["xp_next"]=self.data["level"]*100; self.data["skill_points"]+=self.data["level"]//3
    def _gen_quests(self):
        today=str(date.today())
        if self.data.get("quests_date")==today: return
        pks=list(PRACTICES.keys()); quests=[]
        for _ in range(3):
            qt=random.choice(QUEST_TEMPLATES).copy()
            if "{p}" in qt.get("text",""): qt["text"]=qt["text"].replace("{p}",PRACTICES[random.choice(pks)]["name"])
            qt["id"]=str(uuid.uuid4())[:8]; qt["done"]=False; quests.append(qt)
        self.data["quests"]=quests; self.data["quests_date"]=today
    def _calc_title(self):
        for t in TITLES:
            try:
                if t["cond"](self.data): self.data["active_title"]=t["id"]; break
            except: pass
    def _check_ach(self):
        found=[]
        for a in ACHIEVEMENTS:
            if a["id"] not in self.data["achievements"]:
                try:
                    if a["cond"](self.data): self.data["achievements"].append(a["id"]); found.append(a)
                except: pass
        return found
    def do_practice(self,key):
        today=str(date.today())
        if key in self.data["history"].get(today,[]): return []
        p=PRACTICES[key]; xp=int(p["xp"]*self._xp_mult()); sk=self.data["skills"]
        if key=="meditation": xp=int(xp*(1+sk.get("enduring_patience",0)*0.15))
        if key=="prayer": xp=int(xp*(1+sk.get("inner_light",0)*0.10))
        if today not in self.data["history"]: self.data["history"][today]=[]
        self.data["history"][today].append(key); self.data["today_done"]=list(self.data["history"][today])
        self.data["total"]+=1; self.data["counts"][key]=self.data["counts"].get(key,0)+1
        old_lv=self.data["level"]; self._add_xp(xp); leveled=self.data["level"]>old_lv
        vb,vd=self._virtue_bonus()
        for v,a in p["virtues"].items():
            tot=a+vb.get(v,0)
            if vd: tot*=2
            self.data["virtues"][v]=min(100,self.data["virtues"][v]+tot)
        self._calc_streak(); s=self.data["streak"]
        if s>0 and s%7==0:
            sm=1.5 if self._has_blessing("kindled_flame") else 1.0
            sm*=1+self.data["skills"].get("steadfast_hope",0)*0.2
            self._add_xp(int(s*2*sm))
        if len(self.data["history"].get(today,[]))==len(PRACTICES): self.data["all_today"]=True; self._add_xp(50)
        na=self._check_ach(); self._calc_title(); self.save(); res=[]
        if leveled: res.append(("level_up",self.data["level"]))
        for a in na: res.append(("achievement",a))
        return res
    def complete_med(self,m): self.data["med_sessions"].append({"date":str(date.today()),"minutes":m}); self.data["med_total"]+=m; na=self._check_ach(); self._calc_title(); self.save(); return na
    def add_tasbih(self,c): self.data["tasbih_total"]+=c; self.data["tasbih_sessions"].append({"date":str(date.today()),"count":c}); na=self._check_ach(); self._calc_title(); self.save(); return na
    def log_mood(self,m,ctx=""): self.data["moods"].append({"date":str(date.today()),"time":datetime.now().strftime("%H:%M"),"mood":m,"context":ctx}); na=self._check_ach(); self.save(); return na
    def complete_quest(self,qid):
        for q in self.data.get("quests",[]):
            if q["id"]==qid and not q["done"]: q["done"]=True; self.data["quests_done"]+=1; self._add_xp(q.get("xp",20)); na=self._check_ach(); self._calc_title(); self.save(); return q.get("xp",20),na
        return 0,[]
    def unlock_skill(self,sid):
        sk=self.data["skills"];n=SKILL_TREE[sid]
        if sk.get(sid,0)>=n["max"]: return False
        cost=n["cost"]*(sk.get(sid,0)+1); req=(sk.get(sid,0)+1)*n["cost"]
        if self.data["skill_points"]<cost or self.data["virtues"][n["virtue"]]<req: return False
        self.data["skill_points"]-=cost; sk[sid]=sk.get(sid,0)+1; na=self._check_ach(); self._calc_title(); self.save(); return True
    def add_intention(self,t,c): self.data["intentions"].append({"id":str(uuid.uuid4())[:8],"text":t,"cat":c,"date":str(date.today()),"done":False}); self.save()
    def complete_intention(self,iid):
        for i in self.data["intentions"]:
            if i["id"]==iid and not i["done"]: i["done"]=True; i["done_date"]=str(date.today()); break
        self.save()
    def remove_intention(self,iid): self.data["intentions"]=[i for i in self.data["intentions"] if i["id"]!=iid]; self.save()
    def add_journal(self,t): self.data["journal"].append({"date":str(date.today()),"time":datetime.now().strftime("%H:%M"),"text":t}); na=self._check_ach(); self.save(); return na
    def toggle_fav(self,q,s): e=f"{q}|{s}"; (self.data["fav_quotes"].remove(e) if e in self.data["fav_quotes"] else self.data["fav_quotes"].append(e)); self.save()
    def is_fav(self,q,s): return f"{q}|{s}" in self.data.get("fav_quotes",[])
    def complete_office(self,h): self.data["offices_today"].append(h); na=self._check_ach(); self.save(); return na
    def log_fast(self,h): self.data["fast_sessions"].append({"date":str(date.today()),"hours":h}); self.data["longest_fast"]=max(self.data["longest_fast"],h); na=self._check_ach(); self._calc_title(); self.save(); return na
    def complete_examen(self,answers): self.data["examen_today"]=answers; self.data["examen_total"]+=1; na=self._check_ach(); self.save(); return na
    def complete_lectio(self,answers): self.data["lectio_today"]=True; self.data["lectio_total"]+=1; self._add_xp(25); na=self._check_ach(); self.save(); return na
    def visit_figure(self,name): self.data["figures_visited"].append(name); self.save()
    def vtitle(self,k): v=self.data["virtues"][k]; return "Novice" if v<10 else "Acolyte" if v<25 else "Devotee" if v<50 else "Sage" if v<75 else "Master" if v<100 else "Transcendent"
    def reset(self): self.data=self._def(); self.save()

# ── Base UI Components ──────────────────────────────────────────
class ParticleBg(QWidget):
    def __init__(self,p=None): super().__init__(p); self.ps=[]; self.setAttribute(Qt.WA_TransparentForMouseEvents); t=QTimer(self); t.timeout.connect(self._tick); t.start(40)
    def resizeEvent(self,e): self.ps=[{"x":random.uniform(0,self.width()),"y":random.uniform(0,self.height()),"vy":random.uniform(-.3,-.05),"s":random.uniform(1,2),"a":random.uniform(.1,.4),"l":random.uniform(.3,1)} for _ in range(45)]; super().resizeEvent(e)
    def _tick(self):
        w,h=self.width(),self.height()
        for p in self.ps: p["y"]+=p["vy"]; p["l"]-=.003
        if p["l"]<=0 or p["y"]<-10: p["x"]=random.uniform(0,w); p["y"]=h+10; p["l"]=random.uniform(.3,1)
        self.update()
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing)
        for p in self.ps: a=int(p["a"]*p["l"]*255); pt.setPen(Qt.NoPen); pt.setBrush(QColor(212,168,67,max(0,min(255,a)))); pt.drawEllipse(QPointF(p["x"],p["y"]),p["s"],p["s"])

class XPBar(QWidget):
    def __init__(self,h=28): super().__init__(); self.setFixedHeight(h); self._p=0.0; self._a=QPropertyAnimation(self,b"p"); self._a.setDuration(600)
    def get_p(self): return self._p
    def set_p(self,v): self._p=v; self.update()
    p=Property(float,get_p,set_p)
    def set_val(self,xp,xn): self._a.stop(); self._a.setStartValue(self._p); self._a.setEndValue(xp/max(1,xn)); self._a.start()
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); r=self.rect(); hr=self.height()//2
        pt.setPen(Qt.NoPen); pt.setBrush(C_BG3); pt.drawRoundedRect(r,hr,hr)
        if self._p>0: fw=max(self.height(),r.width()*self._p); g=QLinearGradient(0,0,fw,0); g.setColorAt(0,QColor(180,140,40)); g.setColorAt(1,C_GOLD_L); pt.setBrush(g); pt.drawRoundedRect(QRectF(r.x(),r.y(),fw,r.height()),hr,hr)

class CircleMeter(QWidget):
    def __init__(self,label,color): super().__init__(); self.label=label; self.color=color; self._v=0.0; self.setFixedSize(90,110); self._a=QPropertyAnimation(self,b"v"); self._a.setDuration(800)
    def get_v(self): return self._v
    def set_v(self,val): self._v=val; self.update()
    v=Property(float,get_v,set_v)
    def set_val(self,val): self._a.stop(); self._a.setStartValue(self._v); self._a.setEndValue(float(val)); self._a.start()
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); cx,cy,r=45,40,30
        pt.setPen(QPen(C_BG3,4,Qt.SolidLine,Qt.RoundCap)); pt.drawArc(QRectF(cx-r,cy-r,r*2,r*2),0,5760)
        if self._v>0: sp=int(5760*self._v/100); pt.setPen(QPen(self.color,4,Qt.SolidLine,Qt.RoundCap)); pt.drawArc(QRectF(cx-r,cy-r,r*2,r*2),90*16,-sp)
        f=pt.font(); f.setPixelSize(16); f.setBold(True); pt.setFont(f); pt.setPen(C_TEXT); pt.drawText(QRectF(cx-22,cy-10,44,20),Qt.AlignCenter,f"{int(self._v)}")
        f.setPixelSize(9); f.setBold(False); pt.setFont(f); pt.setPen(C_TEXT2); pt.drawText(QRectF(0,cy+22,90,14),Qt.AlignCenter,self.label)
        ico=VI.get(self.label.lower(),""); f.setPixelSize(11); pt.setFont(f); pt.setPen(self.color); pt.drawText(QRectF(0,cy+34,90,14),Qt.AlignCenter,ico)

class Toast(QWidget):
    def __init__(self,p=None): super().__init__(p); self.setWindowFlags(Qt.FramelessWindowHint|Qt.Tool|Qt.WindowStaysOnTopHint); self.setAttribute(Qt.WA_TranslucentBackground); self.setFixedWidth(320); self._q=[]; self._t=QTimer(self); self._t.setSingleShot(True); self._t.timeout.connect(self._hide); self._al=0.0; self._a=QPropertyAnimation(self,b"al"); self._a.setDuration(300)
    def get_al(self): return self._al
    def set_al(self,v): self._al=v; self.update()
    al=Property(float,get_al,set_al)
    def show_t(self,t,m,c=C_GOLD): self._q.append((t,m,c)); (self._show_next() if not self._t.isActive() else None)
    def _show_next(self):
        if not self._q: return
        self._cur=self._q.pop(0); self.setFixedHeight(60); self._a.stop(); self._a.setStartValue(0.0); self._a.setEndValue(1.0); self._a.start()
        p=self.parent(); (self.move(p.width()-self.width()-20,20) if p else None); self.show(); self.raise_(); self._t.start(2000)
    def _hide(self): self._a.stop(); self._a.setStartValue(self._al); self._a.setEndValue(0.0); self._a.start(); QTimer.singleShot(300,lambda:(self.hide(), self._show_next() if self._q else None))
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); pt.setOpacity(self._al); r=self.rect()
        pt.setPen(Qt.NoPen); pt.setBrush(QColor(20,20,40,230)); pt.drawRoundedRect(r,12,12)
        t,m,c=self._cur; pt.setPen(QPen(c,2)); pt.setBrush(Qt.NoBrush); pt.drawRoundedRect(r.adjusted(1,1,-1,-1),12,12)
        f=pt.font(); f.setPixelSize(11); f.setBold(True); pt.setFont(f); pt.setPen(c); pt.drawText(QRectF(12,6,self.width()-24,18),Qt.AlignLeft|Qt.AlignVCenter,t)
        f.setPixelSize(10); f.setBold(False); pt.setFont(f); pt.setPen(C_TEXT); pt.drawText(QRectF(12,26,self.width()-24,18),Qt.AlignLeft|Qt.AlignVCenter,m)

class PracticeCard(QFrame):
    clicked=Signal(str)
    def __init__(self,key,data,done): super().__init__(); self.key=key; self.data=data; self.done=done; self.setFixedSize(190,105); self.setCursor(Qt.PointingHandCursor); self._h=False
    def set_done(self,d): self.done=d; self.update()
    def enterEvent(self,e): self._h=True; self.update()
    def leaveEvent(self,e): self._h=False; self.update()
    def mousePressEvent(self,e):
        if not self.done: self.clicked.emit(self.key)
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); r=self.rect().adjusted(2,2,-2,-2)
        bg,bd=(QColor(20,50,40),C_GREEN) if self.done else (C_BG3,C_GOLD) if self._h else (C_BG2,QColor(50,50,80))
        pt.setPen(QPen(bd,1.5)); pt.setBrush(bg); pt.drawRoundedRect(r,11,11)
        f=pt.font(); f.setPixelSize(22); pt.setFont(f); pt.setPen(C_GOLD_L if not self.done else C_GREEN); pt.drawText(QRectF(r.x()+10,r.y()+8,34,34),Qt.AlignCenter,self.data["ico"])
        f.setPixelSize(12); f.setBold(True); pt.setFont(f); pt.setPen(C_TEXT if not self.done else C_GREEN); pt.drawText(QRectF(r.x()+46,r.y()+8,130,20),Qt.AlignLeft|Qt.AlignVCenter,self.data["name"])
        f.setPixelSize(9); f.setBold(False); pt.setFont(f); pt.setPen(C_GOLD if not self.done else C_GREEN); pt.drawText(QRectF(r.x()+46,r.y()+28,130,16),Qt.AlignLeft|Qt.AlignVCenter,f"+{self.data['xp']} XP")
        vy=r.y()+50; vx=r.x()+10; f.setPixelSize(8); pt.setFont(f)
        for vk,va in self.data["virtues"].items(): pt.setPen(VC[vk]); pt.drawText(QRectF(vx,vy,84,12),Qt.AlignLeft|Qt.AlignVCenter,f"{VI[vk]}{vk[:3].upper()}+{va}"); vx+=88
        if self.done: pt.setPen(Qt.NoPen); pt.setBrush(C_GREEN); pt.drawEllipse(QPointF(r.right()-16,r.y()+16),7,7); pt.setPen(C_BG); f.setPixelSize(9); f.setBold(True); pt.setFont(f); pt.drawText(QRectF(r.right()-22,r.y()+8,12,16),Qt.AlignCenter,"✓")

class MeditationTimer(QWidget):
    session_done=Signal(int); IDLE,RUNNING,PAUSED,COMPLETE=range(4)
    def __init__(self,dm,toast): super().__init__(); self.dm=dm; self.toast=toast; self.state=self.IDLE; self.total=300; self.remain=300; self.breath=0.0; self.sel_min=5
        self._ct=QTimer(self); self._ct.setInterval(1000); self._ct.timeout.connect(self._tick)
        self._at=QTimer(self); self._at.setInterval(33); self._at.timeout.connect(self._anim)
    def _tick(self):
        self.remain-=1
        if self.remain<=0: self.remain=0; self.state=self.COMPLETE; self._ct.stop(); self._at.stop(); QApplication.beep(); m=self.total//60; na=self.dm.complete_med(m); self.session_done.emit(m); self.toast.show_t("◎ Complete",f"{m}m recorded",C_GREEN)
        self.update()
    def _anim(self): self.breath=(self.breath+0.033/4.0)%1.0; self.update()
    def start(self):
        if self.state==self.IDLE: self.remain=self.sel_min*60; self.total=self.remain
        self.state=self.RUNNING; self._ct.start(); self._at.start(); self.update()
    def pause(self): self.state=self.PAUSED; self._ct.stop(); self._at.stop(); self.update()
    def reset(self): self.state=self.IDLE; self._ct.stop(); self._at.stop(); self.remain=self.sel_min*60; self.total=self.remain; self.update()
    def set_dur(self,m):
        if self.state==self.IDLE: self.sel_min=m; self.remain=m*60; self.total=self.remain; self.update()
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); w,h=self.width(),self.height(); cx,cy=w/2,h/2-25; mr=min(w,h)*.25
        if self.state==self.RUNNING:
            g=QRadialGradient(cx,cy,mr*1.4); g.setColorAt(0,QColor(78,204,163,20)); g.setColorAt(1,QColor(78,204,163,0)); pt.setPen(Qt.NoPen); pt.setBrush(g); pt.drawEllipse(QPointF(cx,cy),mr*1.4,mr*1.4)
        if self.state in (self.RUNNING,PAUSED) and self.total>0:
            prog=self.remain/self.total
            pt.setPen(QPen(C_BG3,3)); pt.setBrush(Qt.NoBrush); pt.drawArc(QRectF(cx-mr-10,cy-mr-10,(mr+10)*2,(mr+10)*2),90*16,-5760)
            pt.setPen(QPen(C_GREEN,3,Qt.SolidLine,Qt.RoundCap)); pt.drawArc(QRectF(cx-mr-10,cy-mr-10,(mr+10)*2,(mr+10)*2),90*16,-int(5760*prog))
        if self.state==self.RUNNING:
            sc=.6+.4*(self.breath/.5) if self.breath<.5 else 1-.4*((self.breath-.5)/.5); bt="Breathe In" if self.breath<.5 else "Breathe Out"
            r=mr*sc; g=QRadialGradient(cx,cy,r); g.setColorAt(0,QColor(78,204,163,40)); g.setColorAt(1,QColor(78,204,163,5)); pt.setPen(QPen(C_GREEN,1.5)); pt.setBrush(g); pt.drawEllipse(QPointF(cx,cy),r,r)
            f=pt.font(); f.setPixelSize(12); pt.setFont(f); pt.setPen(QColor(78,204,163,150)); pt.drawText(QRectF(cx-60,cy+mr+14,120,16),Qt.AlignCenter,bt)
        elif self.state==self.IDLE: pt.setPen(QPen(C_BG3,1.5)); pt.setBrush(QColor(78,204,163,15)); pt.drawEllipse(QPointF(cx,cy),mr*.6,mr*.6)
        elif self.state==self.PAUSED: pt.setPen(QPen(C_AMBER,1.5)); pt.setBrush(QColor(232,168,56,10)); pt.drawEllipse(QPointF(cx,cy),mr*.6,mr*.6)
        elif self.state==self.COMPLETE: pt.setPen(QPen(C_GOLD,1.5)); pt.setBrush(QColor(212,168,67,30)); pt.drawEllipse(QPointF(cx,cy),mr*.7,mr*.7)
        f=pt.font()
        if self.state in (self.RUNNING,PAUSED): m,s=self.remain//60,self.remain%60; f.setPixelSize(40); f.setBold(True); pt.setFont(f); pt.setPen(C_TEXT); pt.drawText(QRectF(cx-70,cy-24,140,48),Qt.AlignCenter,f"{m}:{s:02d}")
        elif self.state==self.IDLE: f.setPixelSize(13); pt.setFont(f); pt.setPen(C_TEXT2); pt.drawText(QRectF(cx-80,cy-8,160,16),Qt.AlignCenter,"Select duration & begin")
        elif self.state==self.COMPLETE: f.setPixelSize(16); f.setBold(True); pt.setFont(f); pt.setPen(C_GOLD); pt.drawText(QRectF(cx-100,cy-12,200,24),Qt.AlignCenter,"Session Complete ✦")

class AltarCanvas(QWidget):
    def __init__(self,dm): super().__init__(); self.dm=dm; self.placed=[]; self.setMinimumHeight(260); self._load()
    def _load(self):
        self.placed=[]
        for pid in self.dm.data.get("altar_placed",[]):
            item=next((i for i in ALTAR_ITEMS if i["id"]==pid),None)
            if item: self.placed.append(dict(item))
    def place_item(self,iid):
        if not any(p["id"]==iid for p in self.placed):
            item=next((i for i in ALTAR_ITEMS if i["id"]==iid),None)
            if item: self.placed.append(dict(item)); self.dm.data["altar_placed"]=[p["id"] for p in self.placed]; self.dm.save(); self.update()
    def clear_items(self): self.placed=[]; self.dm.data["altar_placed"]=[]; self.dm.save(); self.update()
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); w,h=self.width(),self.height()
        g=QLinearGradient(0,0,0,h); g.setColorAt(0,QColor(16,16,32)); g.setColorAt(1,QColor(24,20,36)); pt.fillRect(self.rect(),g)
        pt.setPen(Qt.NoPen); pt.setBrush(QColor(40,30,22)); pt.drawRoundedRect(QRectF(w*.05,h*.65,w*.9,h*.3),8,8)
        pt.setBrush(QColor(60,20,20,80)); pt.drawRoundedRect(QRectF(w*.1,h*.62,w*.8,h*.35),6,6)
        for i in range(5):
            cx=w*(.2+i*.15); g2=QLinearGradient(cx,0,cx,h*.7); g2.setColorAt(0,QColor(212,168,67,12)); g2.setColorAt(1,QColor(212,168,67,0))
            pt.setBrush(g2); path=QPainterPath(); path.moveTo(cx-8,0); path.lineTo(cx+8,0); path.lineTo(cx+25,h*.7); path.lineTo(cx-25,h*.7); path.closeSubpath(); pt.drawPath(path)
        for item in self.placed:
            px,py=item["pos"][0]*w, item["pos"][1]*h; g3=QRadialGradient(px,py,22); g3.setColorAt(0,QColor(212,168,67,35)); g3.setColorAt(1,QColor(212,168,67,0)); pt.setPen(Qt.NoPen); pt.setBrush(g3); pt.drawEllipse(QPointF(px,py),22,22)
            f=pt.font(); f.setPixelSize(26); pt.setFont(f); pt.setPen(C_TEXT); pt.drawText(QRectF(px-16,py-16,32,32),Qt.AlignCenter,item["ico"])
        if not self.placed: f=pt.font(); f.setPixelSize(12); pt.setFont(f); pt.setPen(C_TEXT2); pt.drawText(QRectF(0,h/2-10,w,20),Qt.AlignCenter,"Click items below to place on altar")

# ── Pages ────────────────────────────────────────────────────────
class DashboardPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        hdr=QHBoxLayout(); self.lbl_name=QLabel(); self.lbl_name.setStyleSheet("font-size:20px;font-weight:bold;color:#f0e6d3;"); hdr.addWidget(self.lbl_name)
        self.lbl_title=QLabel(); self.lbl_title.setStyleSheet("font-size:10px;color:#d4a843;background:#1a1a2e;border:1px solid #32325a;border-radius:8px;padding:2px 8px;"); hdr.addWidget(self.lbl_title)
        hdr.addStretch(); self.lbl_level=QLabel(); self.lbl_level.setStyleSheet("font-size:14px;color:#d4a843;font-weight:bold;"); hdr.addWidget(self.lbl_level); lay.addLayout(hdr)
        xr=QHBoxLayout(); self.lbl_xp=QLabel(); self.lbl_xp.setStyleSheet("font-size:9px;color:#8b8b9e;"); self.lbl_xp.setFixedWidth(90); xr.addWidget(self.lbl_xp); self.xp_bar=XPBar(); xr.addWidget(self.xp_bar)
        self.lbl_sp=QLabel(); self.lbl_sp.setStyleSheet("font-size:9px;color:#4ecca3;"); self.lbl_sp.setFixedWidth(70); xr.addWidget(self.lbl_sp); lay.addLayout(xr)
        qc=Card("#161630","#2a2a50"); ql=QVBoxLayout(qc); ql.setContentsMargins(12,6,12,6); self.lbl_quote=QLabel(); self.lbl_quote.setWordWrap(True); self.lbl_quote.setStyleSheet("font-size:11px;color:#b0a888;font-style:italic;"); ql.addWidget(self.lbl_quote)
        self.lbl_src=QLabel(); self.lbl_src.setStyleSheet("font-size:9px;color:#666680;"); self.lbl_src.setAlignment(Qt.AlignRight); ql.addWidget(self.lbl_src); lay.addWidget(qc)
        sr=QHBoxLayout(); sc=Card(); sl=QVBoxLayout(sc); sl.setContentsMargins(12,6,12,6); self.lbl_streak=QLabel(); self.lbl_streak.setStyleSheet("font-size:28px;font-weight:bold;color:#e8a838;"); self.lbl_streak.setAlignment(Qt.AlignCenter); sl.addWidget(self.lbl_streak)
        sl.addWidget(L("Day Streak",9,c=C_TEXT2)); self.lbl_best=QLabel(); self.lbl_best.setStyleSheet("font-size:8px;color:#555570;"); self.lbl_best.setAlignment(Qt.AlignCenter); sl.addWidget(self.lbl_best); sc.setFixedWidth(130); sr.addWidget(sc)
        tc=Card(); tl=QVBoxLayout(tc); tl.setContentsMargins(12,6,12,6); tl.addWidget(L("Today",11,b=True)); tg=QGridLayout(); tg.setSpacing(3); tl.addLayout(tg); self.today_lbls={}
        for i,(k,p) in enumerate(PRACTICES.items()): lb=QLabel(f"{p['ico']} {p['name']}"); lb.setStyleSheet("font-size:9px;color:#8b8b9e;padding:2px 4px;background:#222240;border-radius:4px;"); self.today_lbls[k]=lb; tg.addWidget(lb,i//3,i%3)
        sr.addWidget(tc,1); lay.addLayout(sr,1)
        vr=QHBoxLayout(); vr.setSpacing(4); self.meters={}
        for k,c in VC.items(): m=CircleMeter(k.capitalize(),c); vr.addWidget(m); self.meters[k]=m
        vr.addStretch(); lay.addLayout(vr); self.lbl_bless=QLabel(); self.lbl_bless.setStyleSheet("font-size:9px;color:#d4a843;"); self.lbl_bless.setWordWrap(True); lay.addWidget(self.lbl_bless)
    def refresh(self):
        d=self.dm.data; self.lbl_name.setText(f"✦ {d['name']}"); self.lbl_level.setText(f"Lv.{d['level']}"); self.xp_bar.set_val(d['xp'],d['xp_next']); self.lbl_xp.setText(f"{d['xp']}/{d['xp_next']} XP")
        sp=d.get('skill_points',0); self.lbl_sp.setText(f"✧ {sp} SP" if sp else "")
        tname=next((t["name"] for t in TITLES if t["id"]==d.get("active_title","seeker")),"Seeker"); self.lbl_title.setText(f"«{tname}»")
        self.lbl_streak.setText(str(d['streak'])); self.lbl_best.setText(f"Best: {d['best_streak']}")
        today=d['history'].get(str(date.today()),[])
        for k,lb in self.today_lbls.items(): lb.setStyleSheet(f"font-size:9px;color:{'#4ecca3' if k in today else '#8b8b9e'};padding:2px 4px;background:{'#1a3028' if k in today else '#222240'};border-radius:4px;{'font-weight:bold;' if k in today else ''}")
        for k,m in self.meters.items(): m.set_val(d['virtues'][k])
        q,s=WISDOM[(date.today().toordinal())%len(WISDOM)]; self.lbl_quote.setText(f'"{q}"'); self.lbl_src.setText(f"— {s}")
        active=[b["ico"]+b["name"] for b in BLESSINGS if b["from"] in d['achievements']]; self.lbl_bless.setText("Blessings: "+" • ".join(active) if active else "")

class PracticesPage(QWidget):
    practice_done=Signal(str,list)
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Sacred Practices",17,b=True)); bc=Card(); bl=QHBoxLayout(bc); bl.setContentsMargins(12,4,12,4)
        self.lbl_bonus=QLabel(); self.lbl_bonus.setStyleSheet("font-size:10px;color:#d4a843;"); bl.addWidget(self.lbl_bonus); bl.addStretch()
        self.lbl_sk=QLabel(); self.lbl_sk.setStyleSheet("font-size:9px;color:#e8a838;"); bl.addWidget(self.lbl_sk); lay.addWidget(bc)
        g=QGridLayout(); g.setSpacing(8); self.cards={}
        for i,(k,p) in enumerate(PRACTICES.items()): c=PracticeCard(k,p,k in self.dm.data['history'].get(str(date.today()),[])); c.clicked.connect(self._do); g.addWidget(c,i//3,i%3); self.cards[k]=c
        lay.addLayout(g,1)
    def _do(self,key):
        res=self.dm.do_practice(key); self.cards[key].set_done(True); p=PRACTICES[key]; xp=int(p["xp"]*self.dm._xp_mult()); self.toast.show_t(f"{p['ico']} {p['name']}",f"+{xp} XP",C_GREEN)
        for typ,val in res:
            if typ=="level_up": self.toast.show_t("✦ LEVEL UP!",f"Level {val}! +{val//3} SP",C_GOLD_L)
            elif typ=="achievement": self.toast.show_t("★ Achievement!",val["name"],C_GREEN)
        self.practice_done.emit(key,res); self._upd()
    def _upd(self):
        today=self.dm.data['history'].get(str(date.today()),[]); done=len(today); t=len(PRACTICES)
        self.lbl_bonus.setText(f"Today: {done}/{t}"+(" ✦ ALL COMPLETE!" if done==t else ""))
        self.lbl_sk.setText(f"🔥 {self.dm.data['streak']}d" + (f" • ×{self.dm._xp_mult():.0%}" if self.dm._xp_mult()>1 else ""))
    def refresh(self):
        today=self.dm.data['history'].get(str(date.today()),[])
        for k,c in self.cards.items(): c.set_done(k in today); self._upd()

class MeditationPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Meditation",17,b=True)); self.timer=MeditationTimer(dm,toast); lay.addWidget(self.timer,1)
        dr=QHBoxLayout(); self._dbs=[]
        for m in [1,3,5,10,15,20,30]:
            b=QPushButton(f"{m}m"); b.setFixedHeight(30); b.setCursor(Qt.PointingHandCursor); b.setCheckable(True)
            b.setStyleSheet("QPushButton{background:#1a1a2e;color:#8b8b9e;border:1px solid #32325a;border-radius:6px;font-size:10px;}QPushButton:hover{border-color:#4ecca3;color:#4ecca3;}QPushButton:checked{background:#1a3028;border-color:#4ecca3;color:#4ecca3;font-weight:bold;}")
            b.clicked.connect(lambda _,mm=m,btn=b: (self.timer.set_dur(mm), [x.setChecked(False) for x in self._dbs], btn.setChecked(True))); dr.addWidget(b); self._dbs.append(b)
        lay.addLayout(dr); cr=QHBoxLayout()
        self.btn_s=Btn("▶ Start","#4ecca3","#0d0d1a","#5eddad"); self.btn_s.setFixedHeight(36); self.btn_s.clicked.connect(self._start); cr.addWidget(self.btn_s)
        self.btn_p=Btn("⏸ Pause","#e8a838","#0d0d1a","#f0b848"); self.btn_p.setFixedHeight(36); self.btn_p.clicked.connect(self._pause); self.btn_p.setEnabled(False); cr.addWidget(self.btn_p)
        self.btn_r=Btn("↺","#1a1a2e","#8b8b9e","#1a1a2e"); self.btn_r.setFixedHeight(36); self.btn_r.setFixedWidth(36); self.btn_r.clicked.connect(self._reset); cr.addWidget(self.btn_r)
        cr.addStretch(); lay.addLayout(cr); self.lbl_st=QLabel(); self.lbl_st.setStyleSheet("font-size:9px;color:#555570;"); lay.addWidget(self.lbl_st)
        if self._dbs: self._dbs[2].click()
    def _start(self): self.timer.start(); self.btn_s.setEnabled(False); self.btn_p.setEnabled(True)
    def _pause(self):
        if self.timer.state==MeditationTimer.RUNNING: self.timer.pause(); self.btn_p.setText("▶ Resume")
        elif self.timer.state==MeditationTimer.PAUSED: self.timer.start(); self.btn_p.setText("⏸ Pause")
    def _reset(self): self.timer.reset(); self.btn_s.setEnabled(True); self.btn_p.setEnabled(False); self.btn_p.setText("⏸ Pause")
    def refresh(self): t=self.dm.data.get("med_total",0); self.lbl_st.setText(f"Total: {t}m ({t//60}h {t%60}m)")

class TasbihPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; self.count=0; self.target=33; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Tasbih / Prayer Beads",17,b=True)); pr=QHBoxLayout()
        self.combo=QComboBox(); self.combo.addItems([p["name"] for p in TASBIH_PRESETS]); self.combo.setStyleSheet("QComboBox{background:#222240;border:1px solid #32325a;border-radius:6px;color:#f0e6d3;font-size:11px;padding:6px;}QComboBox::drop-down{border:none;}QComboBox QAbstractItemView{background:#1a1a2e;color:#f0e6d3;}")
        self.combo.currentIndexChanged.connect(self._sel); pr.addWidget(self.combo); self.lbl_desc=QLabel(); self.lbl_desc.setStyleSheet("font-size:10px;color:#8b8b9e;"); pr.addWidget(self.lbl_desc,1); lay.addLayout(pr)
        self.lbl_count=QLabel("0"); self.lbl_count.setStyleSheet("font-size:48px;font-weight:bold;color:#d4a843;"); self.lbl_count.setAlignment(Qt.AlignCenter); lay.addWidget(self.lbl_count)
        self.lbl_target=QLabel(); self.lbl_target.setStyleSheet("font-size:12px;color:#8b8b9e;"); self.lbl_target.setAlignment(Qt.AlignCenter); lay.addWidget(self.lbl_target)
        self.prog=XPBar(12); lay.addWidget(self.prog); br=QHBoxLayout()
        btn_c=Btn("◉ Count","#d4a843","#0d0d1a","#f0d078"); btn_c.setFixedHeight(44); btn_c.clicked.connect(self._tap); br.addWidget(btn_c)
        btn_r=Btn("↺ Reset","#1a1a2e","#8b8b9e","#1a1a2e"); btn_r.setFixedHeight(44); btn_r.clicked.connect(self._reset); br.addWidget(btn_r)
        lay.addLayout(br); self.lbl_tot=QLabel(); self.lbl_tot.setStyleSheet("font-size:9px;color:#555570;"); lay.addWidget(self.lbl_tot); self._sel(0)
    def _sel(self,i): p=TASBIH_PRESETS[i]; self.target=p["count"]; self.lbl_desc.setText(p["desc"]); self.count=0; self._upd()
    def _tap(self):
        self.count+=1
        if self.count>=self.target: na=self.dm.add_tasbih(self.count); self.toast.show_t("📿 Complete",f"{self.count} recorded",C_GREEN); self.count=0
        self._upd()
    def _reset(self): self.count=0; self._upd()
    def _upd(self): self.lbl_count.setText(str(self.count)); self.lbl_target.setText(f"of {self.target}"); self.prog.set_val(self.count,self.target); self.lbl_tot.setText(f"Lifetime: {self.dm.data.get('tasbih_total',0)}")
    def refresh(self): self._upd()

class MoodPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Mood Tracker",17,b=True)); lay.addWidget(L("How are you feeling?",11,c=C_TEXT2))
        mg=QGridLayout(); mg.setSpacing(6)
        for i,(k,ico) in enumerate(MOODS.items()):
            b=QPushButton(ico); b.setFixedSize(48,48); b.setCursor(Qt.PointingHandCursor); b.setStyleSheet("QPushButton{background:#1a1a2e;color:#f0e6d3;font-size:20px;border:1px solid #32325a;border-radius:10px;}QPushButton:hover{border-color:#d4a843;background:#222240;}")
            b.clicked.connect(lambda _,m=k: self._log(m)); mg.addWidget(b,i//5,i%5)
        lay.addLayout(mg); self.inp=QLineEdit(); self.inp.setPlaceholderText("Context (optional)"); self.inp.setStyleSheet("QLineEdit{background:#222240;border:1px solid #32325a;border-radius:6px;color:#f0e6d3;font-size:11px;padding:6px;}QLineEdit:focus{border-color:#d4a843;}"); lay.addWidget(self.inp)
        lay.addWidget(L("Recent",12,b=True)); scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        self.inner=QWidget(); self.il=QVBoxLayout(self.inner); self.il.setSpacing(3); self.il.setContentsMargins(0,0,0,0); scroll.setWidget(self.inner); lay.addWidget(scroll,1)
    def _log(self,m): self.dm.log_mood(m,self.inp.text().strip()); self.toast.show_t(f"Mood: {MOODS[m]}","Recorded",C_GREEN); self.inp.clear(); self.refresh()
    def refresh(self):
        while self.il.count(): w=self.il.takeAt(0).widget(); (w.deleteLater() if w else None)
        for m in reversed(self.dm.data.get("moods",[])[-30:]):
            l=QLabel(f"{MOODS.get(m['mood'],'?')}  {m['mood']}  —  {m['date']} {m.get('time','')}  {m.get('context','')}"); l.setStyleSheet("font-size:10px;color:#8b8b9e;padding:3px 6px;background:#1a1a2e;border-radius:4px;"); self.il.addWidget(l)
        self.il.addStretch()

class QuestsPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        hdr=QHBoxLayout(); hdr.addWidget(L("Daily Quests",17,b=True)); hdr.addStretch(); self.lbl_d=QLabel(); self.lbl_d.setStyleSheet("font-size:11px;color:#8b8b9e;"); hdr.addWidget(self.lbl_d); lay.addLayout(hdr)
        self.ql=QVBoxLayout(); self.ql.setSpacing(8); lay.addLayout(self.ql,1)
    def refresh(self):
        while self.ql.count(): w=self.ql.takeAt(0).widget(); (w.deleteLater() if w else None)
        for q in self.dm.data.get("quests",[]):
            c=Card("#1a3028" if q["done"] else "#1a1a2e","#4ecca3" if q["done"] else "#32325a"); cl=QHBoxLayout(c); cl.setContentsMargins(12,8,12,8)
            ico=QLabel(q.get("icon","⚡")); ico.setStyleSheet("font-size:18px;"); ico.setFixedWidth(30); cl.addWidget(ico)
            tl=QLabel(q["text"]); tl.setStyleSheet(f"font-size:11px;color:{'#4ecca3' if q['done'] else '#f0e6d3'};"); tl.setWordWrap(True); cl.addWidget(tl,1)
            xpl=L(f"+{q.get('xp',20)} XP",10,b=True,C_GREEN if q["done"] else C_GOLD); xpl.setFixedWidth(55); xpl.setAlignment(Qt.AlignRight|Qt.AlignVCenter); cl.addWidget(xpl)
            if not q["done"]:
                btn=Btn("Claim","#d4a843","#0d0d1a","#f0d078",False); btn.setFixedHeight(26); btn.clicked.connect(lambda _,qid=q["id"]: self._claim(qid)); cl.addWidget(btn)
            else: cl.addWidget(L("✓",10,b=True,C_GREEN))
            self.ql.addWidget(c)
        self.lbl_d.setText(f"Total: {self.dm.data.get('quests_done',0)}"); self.ql.addStretch()
    def _claim(self,qid):
        xp,na=self.dm.complete_quest(qid)
        if xp: self.toast.show_t("⚡ Quest!",f"+{xp} XP",C_GOLD_L)
        for a in na: self.toast.show_t("★ Achievement!",a["name"],C_GREEN)
        self.refresh()

class SkillTreePage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        hdr=QHBoxLayout(); hdr.addWidget(L("Skill Tree",17,b=True)); hdr.addStretch(); self.lbl_sp=L("",12,b=True,C_GREEN); hdr.addWidget(self.lbl_sp); lay.addLayout(hdr)
        self.grid=QGridLayout(); self.grid.setSpacing(6); lay.addLayout(self.grid,1)
    def refresh(self):
        while self.grid.count(): w=self.grid.takeAt(0).widget(); (w.deleteLater() if w else None)
        self.lbl_sp.setText(f"✧ {self.dm.data.get('skill_points',0)} SP")
        for i,(sid,n) in enumerate(SKILL_TREE.items()):
            c=Card(); cl=QVBoxLayout(c); cl.setContentsMargins(10,6,10,6)
            hr=QHBoxLayout(); hr.addWidget(L(n["icon"],16)); hr.addWidget(L(n["name"],11,b=True)); hr.addStretch(); cl.addLayout(hr)
            cl.addWidget(L(n["desc"],9,c=C_TEXT2)); pr=QHBoxLayout()
            for lv in range(n["max"]): pr.addWidget(L("●",10,c=VC[n["virtue"]] if lv<self.dm.data["skills"].get(sid,0) else QColor(50,50,80)))
            pr.addStretch(); cl.addLayout(pr)
            br=QHBoxLayout(); cur=self.dm.data["skills"].get(sid,0)
            if cur<n["max"]:
                cost=n["cost"]*(cur+1); req=(cur+1)*n["cost"]; ok=self.dm.data["skill_points"]>=cost and self.dm.data["virtues"][n["virtue"]]>=req
                br.addWidget(L(f"Cost: {cost}SP + {req}{n['virtue'][:3]}",8,c=C_GREEN if ok else C_RED))
                btn=Btn("Unlock","#d4a843","#0d0d1a","#f0d078",False); btn.setFixedHeight(22); btn.clicked.connect(lambda _,s=sid: self._unlock(s))
                if not ok: btn.setEnabled(False); br.addWidget(btn)
            else: br.addWidget(L("MAX",9,b=True,C_GOLD))
            br.addStretch(); cl.addLayout(br); self.grid.addWidget(c,i//3,i%3)
    def _unlock(self,sid):
        if self.dm.unlock_skill(sid): n=SKILL_TREE[sid]; self.toast.show_t(f"{n['icon']} Unlocked",f"{n['name']} Lv{self.dm.data['skills'][sid]}",C_GREEN); self.refresh()
        else: self.toast.show_t("Cannot Unlock","Not enough SP or virtue",C_RED)

class AltarPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Sacred Altar",17,b=True)); lay.addWidget(L("Arrange your sacred space",10,c=C_TEXT2))
        self.canvas=AltarCanvas(dm); lay.addWidget(self.canvas,1)
        ir=QHBoxLayout()
        for item in ALTAR_ITEMS:
            is_u=item["unlock"] in self.dm.data["achievements"]
            if is_u and item["id"] not in self.dm.data.get("altar_unlocked",[]): self.dm.data["altar_unlocked"].append(item["id"]); self.dm.save()
            b=QPushButton(item["ico"]); b.setFixedSize(38,38); b.setToolTip(item["name"]); b.setCursor(Qt.PointingHandCursor)
            if is_u: b.setStyleSheet("QPushButton{background:#1a1a2e;color:#f0e6d3;font-size:16px;border:1px solid #32325a;border-radius:8px;}QPushButton:hover{border-color:#d4a843;}"); b.clicked.connect(lambda _,iid=item["id"]: self.canvas.place_item(iid))
            else: req=next((a["name"] for a in ACHIEVEMENTS if a["id"]==item["unlock"]),"?"); b.setEnabled(False); b.setToolTip(f"🔒 {req}"); b.setStyleSheet("QPushButton{background:#12121e;color:#333350;font-size:16px;border:1px solid #1e1e36;border-radius:8px;}")
            ir.addWidget(b)
        lay.addLayout(ir); clr=Btn("Clear","#1a1a2e","#8b8b9e","#1a1a2e",False); clr.clicked.connect(self.canvas.clear_items); lay.addWidget(clr,alignment=Qt.AlignRight)
    def refresh(self): self.canvas.update()

class DailyOfficePage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Daily Office",17,b=True)); self.grid=QGridLayout(); self.grid.setSpacing(8); lay.addLayout(self.grid,1)
    def refresh(self):
        while self.grid.count(): w=self.grid.takeAt(0).widget(); (w.deleteLater() if w else None)
        for i,(h,d) in enumerate(DAILY_OFFICE.items()):
            done=h in self.dm.data.get("offices_today",[]); c=Card("#1a3028" if done else "#1a1a2e","#4ecca3" if done else "#32325a")
            cl=QVBoxLayout(c); cl.setContentsMargins(10,6,10,6); hr=QHBoxLayout(); hr.addWidget(L(d["name"],11,b=True)); hr.addStretch(); hr.addWidget(L(d["time"],9,c=C_TEXT2)); cl.addLayout(hr)
            cl.addWidget(L(d["verses"][0],10,c=QColor(176,168,136))); br=QHBoxLayout(); br.addStretch()
            btn=Btn("Prayed ✓","#1a3028","#4ecca3","#1a3028",True) if done else Btn("✓ Pray","#d4a843","#0d0d1a","#f0d078")
            btn.setFixedHeight(24); btn.clicked.connect(lambda _,ho=h: self._pray(ho))
            if done: btn.setEnabled(False)
            br.addWidget(btn); cl.addLayout(br); self.grid.addWidget(c,i//2,i%2)
    def _pray(self,h):
        na=self.dm.complete_office(h); self.toast.show_t(f"🕰 {DAILY_OFFICE[h]['name']}","Prayed",C_GREEN)
        for a in na: self.toast.show_t("★ Achievement!",a["name"],C_GREEN)
        self.refresh()

class ExamenPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; self.steps=[]; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Examen Prayer",17,b=True)); lay.addWidget(L("A 5-step guided prayer of self-reflection",10,c=C_TEXT2))
        self.stack=QStackedWidget(); lay.addWidget(self.stack,1)
        nav=QHBoxLayout(); self.btn_prev=Btn("◀ Prev","#1a1a2e","#8b8b9e","#1a1a2e",False); self.btn_prev.clicked.connect(lambda: (self.stack.setCurrentIndex(self.stack.currentIndex()-1) if self.stack.currentIndex()>0 else None)); nav.addWidget(self.btn_prev)
        self.btn_next=Btn("Next ▶","#d4a843","#0d0d1a","#f0d078"); self.btn_next.clicked.connect(self._next); nav.addWidget(self.btn_next)
        nav.addStretch(); lay.addLayout(nav); self._build()
    def _build(self):
        done=self.dm.data.get("examen_today",[]); is_done=len(done)==len(EXAMEN_STEPS)
        for i,s in enumerate(EXAMEN_STEPS):
            w=QWidget(); wl=QVBoxLayout(w); wl.setContentsMargins(10,10,10,10)
            wl.addWidget(L(f"{s['icon']} Step {i+1}: {s['name']}",14,b=True)); wl.addWidget(L(s["prompt"],11,c=QColor(176,168,136)))
            if is_done and i<len(done): wl.addWidget(L("Your reflection:",10,b=True,C_TEXT2)); te=QTextEdit(); te.setPlainText(done[i] if is_done and i<len(done) else ""); te.setStyleSheet("QTextEdit{background:#222240;border:1px solid #32325a;border-radius:6px;color:#f0e6d3;font-size:12px;padding:8px;}"); wl.addWidget(te,1); self.steps.append(te)
            self.stack.addWidget(w)
        if is_done: self.btn_next.setText("✓ Completed"); self.btn_next.setEnabled(False)
    def _next(self):
        i=self.stack.currentIndex()+1
        if i<len(EXAMEN_STEPS): self.stack.setCurrentIndex(i)
        else: self._complete()
        self.btn_prev.setEnabled(self.stack.currentIndex()>0)
        if i>=len(EXAMEN_STEPS)-1: self.btn_next.setText("✓ Complete")
    def _complete(self):
        answers=[te.toPlainText() for te in self.steps]; na=self.dm.complete_examen(answers); self.toast.show_t("🔍 Examen Complete","Your reflection is recorded",C_GREEN)
        for a in na: self.toast.show_t("★ Achievement!",a["name"],C_GREEN)
        self.btn_next.setText("✓ Completed"); self.btn_next.setEnabled(False); self.refresh()
    def refresh(self):
        self.steps=[]; while self.stack.count(): w=self.stack.takeAt(0).widget(); w.deleteLater()
        self._build(); self.stack.setCurrentIndex(0)

class LectioPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; self.steps=[]; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Lectio Divina",17,b=True)); lay.addWidget(L("Sacred reading: Listen, Reflect, Pray, Rest",10,c=C_TEXT2))
        # Text selector
        tr=QHBoxLayout(); tr.addWidget(L("Select Text:",10)); self.combo=QComboBox(); self.combo.addItems([f"{t['ref']} ({t['source']})" for t in LECTIO_TEXTS]); self.combo.setStyleSheet("QComboBox{background:#222240;border:1px solid #32325a;border-radius:6px;color:#f0e6d3;font-size:11px;padding:6px;}QComboBox::drop-down{border:none;}QComboBox QAbstractItemView{background:#1a1a2e;color:#f0e6d3;}"); tr.addWidget(self.combo,1); lay.addLayout(tr)
        self.stack=QStackedWidget(); lay.addWidget(self.stack,1)
        nav=QHBoxLayout(); self.btn_p=Btn("◀","#1a1a2e","#8b8b9e","#1a1a2e",False); self.btn_p.clicked.connect(lambda: (self.stack.setCurrentIndex(self.stack.currentIndex()-1) if self.stack.currentIndex()>0 else None)); nav.addWidget(self.btn_p)
        self.btn_n=Btn("Next ▶","#d4a843","#0d0d1a","#f0d078"); self.btn_n.clicked.connect(self._next); nav.addWidget(self.btn_n); nav.addStretch(); lay.addLayout(nav)
        self.combo.currentIndexChanged.connect(self._build); self._build(0)
    def _build(self,i=0):
        self.steps=[]; while self.stack.count(): w=self.stack.takeAt(0).widget(); w.deleteLater()
        if i<0: i=0
        text=LECTIO_TEXTS[i]["text"]; phases=[("Lectio (Read)","Read the text slowly. What word or phrase stands out to you?"),("Meditatio (Reflect)","How does this text speak to your life right now?"),("Oratio (Pray)","Respond to God. What do you want to say?"),("Contemplatio (Rest)","Rest in silence. Simply be present to the divine.")]
        for j,(name,prompt) in enumerate(phases):
            w=QWidget(); wl=QVBoxLayout(w); wl.setContentsMargins(10,10,10,10)
            wl.addWidget(L(name,14,b=True)); wl.addWidget(L(prompt,10,c=QColor(176,168,136)))
            if j==0:
                te=QTextEdit(); te.setPlainText(text); te.setReadOnly(True); te.setStyleSheet("QTextEdit{background:#161630;border:1px solid #2a2a50;border-radius:6px;color:#f0e6d3;font-size:12px;padding:10px;font-style:italic;}"); wl.addWidget(te,1)
            resp=QTextEdit(); resp.setPlaceholderText("Write your response..."); resp.setStyleSheet("QTextEdit{background:#222240;border:1px solid #32325a;border-radius:6px;color:#f0e6d3;font-size:12px;padding:8px;}"); wl.addWidget(resp,1)
            self.steps.append(resp); self.stack.addWidget(w)
        is_done=self.dm.data.get("lectio_today",False)
        if is_done: self.btn_n.setText("✓ Done Today"); self.btn_n.setEnabled(False)
    def _next(self):
        i=self.stack.currentIndex()+1
        if i<len(self.steps): self.stack.setCurrentIndex(i)
        else: self._complete()
        self.btn_p.setEnabled(self.stack.currentIndex()>0)
        if i>=len(self.steps)-1: self.btn_n.setText("✓ Complete")
    def _complete(self):
        na=self.dm.complete_lectio([te.toPlainText() for te in self.steps]); self.toast.show_t("📖 Lectio Complete","+25 XP",C_GREEN)
        for a in na: self.toast.show_t("★ Achievement!",a["name"],C_GREEN)
        self.btn_n.setText("✓ Done Today"); self.btn_n.setEnabled(False)
    def refresh(self): self._build(self.combo.currentIndex())

class FiguresPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Holy Figures",17,b=True)); scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        inner=QWidget(); self.fl=QVBoxLayout(inner); self.fl.setSpacing(8); self.fl.setContentsMargins(0,0,0,0)
        for fig in HOLY_FIGURES:
            c=Card(); cl=QVBoxLayout(c); cl.setContentsMargins(12,8,12,8); hr=QHBoxLayout()
            hr.addWidget(L(fig["name"],13,b=True)); hr.addStretch(); hr.addWidget(L(fig["trad"],10,c=C_TEXT2)); hr.addWidget(L(fig["date"],9,c=C_AMBER)); cl.addLayout(hr)
            cl.addWidget(L(f'"{fig["quote"]}"',11,c=QColor(176,168,136))); vr=QHBoxLayout(); vr.addStretch()
            vc=VC.get(fig["virtue"],C_TEXT2); vr.addWidget(L(f"Virtue: {fig['virtue'].capitalize()}",10,b=True,c=vc)); vr.addStretch(); cl.addLayout(vr)
            self.fl.addWidget(c)
        self.fl.addStretch(); scroll.setWidget(inner); lay.addWidget(scroll,1)
    def refresh(self): pass

class FastingPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; self.running=False; self.start_time=None; self.elapsed=0
        self._t=QTimer(self); self._t.setInterval(1000); self._t.timeout.connect(self._tick); lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Fasting Timer",17,b=True)); self.disp=QLabel("0:00:00"); self.disp.setStyleSheet("font-size:48px;font-weight:bold;color:#e8a838;"); self.disp.setAlignment(Qt.AlignCenter); lay.addWidget(self.disp)
        self.lbl_st=QLabel("Ready"); self.lbl_st.setStyleSheet("font-size:12px;color:#8b8b9e;"); self.lbl_st.setAlignment(Qt.AlignCenter); lay.addWidget(self.lbl_st)
        br=QHBoxLayout(); self.btn_s=Btn("◈ Begin","#e8a838","#0d0d1a","#f0b848"); self.btn_s.setFixedHeight(40); self.btn_s.clicked.connect(self._toggle); br.addWidget(self.btn_s)
        self.btn_l=Btn("Log & Reset","#1a1a2e","#8b8b9e","#1a1a2e",False); self.btn_l.setFixedHeight(40); self.btn_l.clicked.connect(self._log); self.btn_l.setEnabled(False); br.addWidget(self.btn_l); br.addStretch(); lay.addLayout(br)
        self.lbl_st2=QLabel(); self.lbl_st2.setStyleSheet("font-size:9px;color:#555570;"); lay.addWidget(self.lbl_st2); lay.addStretch()
    def _toggle(self):
        if not self.running: self.running=True; self.start_time=time.time()-self.elapsed; self._t.start(); self.btn_s.setText("⏸ Pause"); self.btn_l.setEnabled(True); self.lbl_st.setText("Fasting..."); self.lbl_st.setStyleSheet("font-size:12px;color:#e8a838;")
        else: self.running=False; self._t.stop(); self.elapsed=time.time()-self.start_time; self.btn_s.setText("◈ Resume"); self.lbl_st.setText("Paused")
    def _tick(self): self.elapsed=time.time()-self.start_time; h=int(self.elapsed//3600); m=int((self.elapsed%3600)//60); s=int(self.elapsed%60); self.disp.setText(f"{h}:{m:02d}:{s:02d}")
    def _log(self):
        hours=round(self.elapsed/3600,1)
        if hours<0.1: self.toast.show_t("Too Short","Log at least a few minutes",C_RED); return
        na=self.dm.log_fast(hours); self.running=False; self._t.stop(); self.elapsed=0; self.disp.setText("0:00:00"); self.btn_s.setText("◈ Begin"); self.btn_l.setEnabled(False); self.lbl_st.setText("Logged!"); self.lbl_st.setStyleSheet("font-size:12px;color:#4ecca3;"); self.toast.show_t("◈ Logged",f"{hours}h",C_GREEN)
    def refresh(self): fs=self.dm.data.get("fast_sessions",[]); lf=self.dm.data.get("longest_fast",0); self.lbl_st2.setText(f"Sessions: {len(fs)} • Longest: {lf}h")

class VirtuesPage(QWidget):
    def __init__(self,dm):
        super().__init__(); self.dm=dm; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8); lay.addWidget(L("Virtues",17,b=True)); self.cards={}
        for k,c in VC.items():
            card=Card(); cl=QVBoxLayout(card); cl.setContentsMargins(14,8,14,8); hr=QHBoxLayout()
            hr.addWidget(L(VI[k],16,c=c)); hr.addWidget(L(k.capitalize(),13,b=True)); hr.addStretch()
            tl=QLabel(); tl.setStyleSheet(f"font-size:10px;color:{c.name()};font-weight:bold;"); hr.addWidget(tl)
            vl=QLabel(); vl.setStyleSheet("font-size:13px;font-weight:bold;color:#f0e6d3;"); vl.setFixedWidth(50); vl.setAlignment(Qt.AlignRight|Qt.AlignVCenter); hr.addWidget(vl); cl.addLayout(hr)
            bar=XPBar(12); cl.addWidget(bar); src=QLabel(); src.setStyleSheet("font-size:8px;color:#555570;"); cl.addWidget(src)
            lay.addWidget(card); self.cards[k]={"bar":bar,"val":vl,"title":tl,"src":src}
        lay.addStretch()
    def refresh(self):
        for k,w in self.cards.items():
            v=self.dm.data['virtues'][k]; w['bar'].set_val(v,100); w['val'].setText(f"{v}/100"); w['title'].setText(self.dm.vtitle(k))
            srcs=[f"{PRACTICES[p]['ico']}{PRACTICES[p]['name']}(+{a})" for p,d in PRACTICES.items() for vk,a in d['virtues'].items() if vk==k]
            w['src'].setText("Grows from: "+" • ".join(srcs))

class BlessingsPage(QWidget):
    def __init__(self,dm):
        super().__init__(); self.dm=dm; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8); lay.addWidget(L("Blessings",17,b=True)); self.grid=QGridLayout(); self.grid.setSpacing(6); lay.addLayout(self.grid,1)
    def refresh(self):
        while self.grid.count(): w=self.grid.takeAt(0).widget(); (w.deleteLater() if w else None)
        for i,b in enumerate(BLESSINGS):
            a=b["from"] in self.dm.data['achievements']; c=Card("#2a2818" if a else "#1a1a2e","#d4a843" if a else "#32325a"); cl=QVBoxLayout(c); cl.setContentsMargins(10,6,10,6)
            hr=QHBoxLayout(); hr.addWidget(L(b["ico"],16,c=C_GOLD_L if a else C_TEXT2)); hr.addWidget(L(b["name"],11,b=True,c=C_GOLD_L if a else C_TEXT2)); hr.addStretch(); cl.addLayout(hr)
            cl.addWidget(L(b["desc"],9,c=C_TEXT2)); src=next((a["name"] for a in ACHIEVEMENTS if a["id"]==b["from"]),"?"); cl.addWidget(L(f"Unlocks: {src}",8,c=QColor(80,80,110))); self.grid.addWidget(c,i//2,i%2)

class AchievementsPage(QWidget):
    def __init__(self,dm):
        super().__init__(); self.dm=dm; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        hdr=QHBoxLayout(); hdr.addWidget(L("Achievements",17,b=True)); hdr.addStretch(); self.lbl_c=QLabel(); self.lbl_c.setStyleSheet("font-size:10px;color:#8b8b9e;"); hdr.addWidget(self.lbl_c); lay.addLayout(hdr)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        inner=QWidget(); self.al=QVBoxLayout(inner); self.al.setSpacing(4); self.al.setContentsMargins(0,0,0,0)
        for a in ACHIEVEMENTS:
            u=a['id'] in self.dm.data['achievements']; c=Card("#1e2318" if u else "#1a1a2e",C_GOLD if u else "#32325a")
            cl=QHBoxLayout(c); cl.setContentsMargins(10,4,10,4)
            ico=QLabel("★" if u else "🔒"); ico.setStyleSheet(f"font-size:11px;color:{C_GOLD.name() if u else C_TEXT2.name()};"); ico.setFixedWidth(20); cl.addWidget(ico)
            cl.addWidget(L(a["name"],11,b=True,C_TEXT if u else C_TEXT2)); cl.addStretch(); cl.addWidget(L(a["desc"],9,c=C_TEXT2)); self.al.addWidget(c)
        self.al.addStretch(); scroll.setWidget(inner); lay.addWidget(scroll,1)
    def refresh(self): self.lbl_c.setText(f"{len(self.dm.data['achievements'])}/{len(ACHIEVEMENTS)}")

class CalendarPage(QWidget):
    def __init__(self,dm):
        super().__init__(); self.dm=dm; self._y=date.today().year; self._m=date.today().month; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Sacred Calendar",17,b=True)); nav=QHBoxLayout()
        bp=Btn("◀","#1a1a2e","#8b8b9e","#1a1a2e",False); bp.setFixedSize(30,26); bp.clicked.connect(lambda:self._chg(-1)); nav.addWidget(bp)
        self.lbl_m=QLabel(); self.lbl_m.setStyleSheet("font-size:13px;font-weight:bold;color:#f0e6d3;"); self.lbl_m.setAlignment(Qt.AlignCenter); nav.addWidget(self.lbl_m)
        bn=Btn("▶","#1a1a2e","#8b8b9e","#1a1a2e",False); bn.setFixedSize(30,26); bn.clicked.connect(lambda:self._chg(1)); nav.addWidget(bn); nav.addStretch(); lay.addLayout(nav)
        dh=QGridLayout(); dh.setSpacing(2)
        for i,dn in enumerate(["M","T","W","T","F","S","S"]): dh.addWidget(L(dn,8,b=True,C_TEXT2),0,i)
        lay.addLayout(dh); self.cg=QGridLayout(); self.cg.setSpacing(2); lay.addLayout(self.cg); lay.addStretch()
    def _chg(self,d):
        self._m+=d
        if self._m>12: self._m=1; self._y+=1
        elif self._m<1: self._m=12; self._y-=1
        self.refresh()
    def refresh(self):
        mn=["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]; self.lbl_m.setText(f"{mn[self._m]} {self._y}")
        while self.cg.count(): w=self.cg.takeAt(0).widget(); (w.deleteLater() if w else None)
        first=date(self._y,self._m,1); sw=(first.weekday())%7; dim=(date(self._y,self._m+1,1)-timedelta(days=1)).day if self._m<12 else 31; ts=str(date.today())
        for i in range(42):
            r,c=i//7,i%7; dn=i-sw+1; cell=QFrame(); cell.setFixedHeight(44)
            if 1<=dn<=dim:
                ds=f"{self._y}-{self._m:02d}-{dn:02d}"; it=ds==ts; pr=self.dm.data['history'].get(ds,[])
                if it: cell.setStyleSheet("QFrame{background:#1a2520;border:1px solid #4ecca3;border-radius:5px;}")
                elif pr: cell.setStyleSheet("QFrame{background:#1a1a30;border:1px solid #32325a;border-radius:5px;}")
                else: cell.setStyleSheet("QFrame{background:#12121e;border:1px solid #1e1e36;border-radius:5px;}")
                cl=QVBoxLayout(cell); cl.setContentsMargins(2,1,2,1); cl.setSpacing(0)
                dl=QLabel(str(dn)); dl.setAlignment(Qt.AlignCenter); dl.setStyleSheet(f"font-size:9px;font-weight:bold;color:{'#4ecca3' if it else '#f0e6d3' if pr else '#444460'};"); cl.addWidget(dl)
                dots=QHBoxLayout(); dots.setSpacing(1); dots.setAlignment(Qt.AlignCenter)
                for pk in pr: dot=QLabel(PRACTICES[pk]['ico']); dot.setStyleSheet(f"font-size:7px;color:{VC[list(PRACTICES[pk]['virtues'].keys())[0]].name()};"); dots.addWidget(dot)
                cl.addLayout(dots)
            else: cell.setStyleSheet("QFrame{background:transparent;}")
            self.cg.addWidget(cell,r,c)

class StatsPage(QWidget):
    def __init__(self,dm):
        super().__init__(); self.dm=dm; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10); lay.addWidget(L("Statistics",17,b=True))
        sr=QGridLayout(); sr.setSpacing(6); self.sc={}
        for i,(k,ico,lbl) in enumerate([("total","◈","Practices"),("level","✦","Level"),("streak","🔥","Streak"),("med","◎","Meditation"),("tasbih","📿","Tasbih"),("quests","⚡","Quests")]):
            c=Card(); cl=QVBoxLayout(c); cl.setContentsMargins(10,6,10,6); v=QLabel(); v.setStyleSheet("font-size:18px;font-weight:bold;color:#d4a843;"); v.setAlignment(Qt.AlignCenter); cl.addWidget(v)
            cl.addWidget(L(lbl,8,c=C_TEXT2)); sr.addWidget(c,0,i); self.sc[k]=v
        lay.addLayout(sr); self.heatmap=QWidget(); self.heatmap.setMinimumHeight(160); lay.addWidget(self.heatmap,1)
    def refresh(self):
        d=self.dm.data; self.sc["total"].setText(str(d['total'])); self.sc["level"].setText(str(d['level'])); self.sc["streak"].setText(str(d['streak']))
        self.sc["med"].setText(f"{d.get('med_total',0)}m"); self.sc["tasbih"].setText(str(d.get('tasbih_total',0))); self.sc["quests"].setText(str(d.get('quests_done',0))); self.heatmap.update()
    def paintEvent(self,e): super().paintEvent(e); self.heatmap.update()

class HeatmapWidget(QWidget):
    def __init__(self,dm): super().__init__(dm); self.dm=dm; self.setMinimumHeight(160)
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); w,h=self.width(),self.height(); pt.fillRect(self.rect(),C_BG2)
        today=date.today(); start=today-timedelta(days=365); history=self.dm.data["history"]
        mx=max((len(history.get(str(start+timedelta(days=i)),[])) for i in range(366)),default=1) or 1
        cell=5; gap=1; step=cell+gap; ox=30; oy=16
        f=pt.font(); f.setPixelSize(7); pt.setFont(f); pt.setPen(C_TEXT2); last_m=-1
        for i in range(366): d=start+timedelta(days=i); col=i//7; x=ox+col*step
        if d.month!=last_m: pt.drawText(QPointF(x,oy-2),d.strftime("%b")[:3]); last_m=d.month
        for r,dn in enumerate(["","","M","","","F",""]):
            if dn: pt.drawText(QPointF(0,oy+r*step+7),dn)
        for i in range(366):
            d=start+timedelta(days=i); col=i//7; row=i%7; x=ox+col*step; y=oy+row*step; v=len(history.get(str(d),[]))
            if v==0: c=QColor(30,30,55)
            elif v<=mx*.25: c=QColor(30,60,45)
            elif v<=mx*.5: c=QColor(40,100,70)
            elif v<=mx*.75: c=QColor(60,150,100)
            else: c=C_GREEN
            pt.setPen(Qt.NoPen); pt.setBrush(c); pt.drawRoundedRect(QRectF(x,y,cell,cell),1,1)

class IntentionsPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Prayer Intentions",17,b=True)); form=Card(); fl=QVBoxLayout(form); fl.setContentsMargins(10,6,10,6); row=QHBoxLayout()
        self.inp=QLineEdit(); self.inp.setPlaceholderText("Add intention..."); self.inp.setStyleSheet("QLineEdit{background:#222240;border:1px solid #32325a;border-radius:5px;color:#f0e6d3;font-size:11px;padding:6px;}QLineEdit:focus{border-color:#d4a843;}"); row.addWidget(self.inp)
        self.cat=QComboBox(); self.cat.addItems(["Self","Others","World","Gratitude"]); self.cat.setStyleSheet("QComboBox{background:#222240;border:1px solid #32325a;border-radius:5px;color:#f0e6d3;font-size:10px;padding:5px 8px;}QComboBox::drop-down{border:none;}QComboBox QAbstractItemView{background:#1a1a2e;color:#f0e6d3;}"); self.cat.setFixedWidth(90); row.addWidget(self.cat)
        btn=Btn("Add","#d4a843","#0d0d1a","#f0d078",False); btn.setFixedHeight(28); btn.clicked.connect(self._add); row.addWidget(btn); fl.addLayout(row); lay.addWidget(form)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        self.inner=QWidget(); self.il=QVBoxLayout(self.inner); self.il.setSpacing(3); self.il.setContentsMargins(0,0,0,0); scroll.setWidget(self.inner); lay.addWidget(scroll,1)
    def _add(self):
        t=self.inp.text().strip()
        if not t: self.toast.show_t("Empty","Write an intention",C_RED); return
        self.dm.add_intention(t,self.cat.currentText()); self.inp.clear(); self.toast.show_t("Added",t,C_GREEN); self.refresh()
    def refresh(self):
        while self.il.count(): w=self.il.takeAt(0).widget(); (w.deleteLater() if w else None)
        active=[i for i in self.dm.data['intentions'] if not i['done']]; done=[i for i in self.dm.data['intentions'] if i['done']]
        if active: self.il.addWidget(L("Active",10,b=True,C_GOLD))
        for it in active: self.il.addWidget(self._ic(it))
        if done: self.il.addWidget(L(f"Completed ({len(done)})",10,b=True,C_GREEN))
        for it in reversed(done[-10:]): self.il.addWidget(self._ic(it))
        if not active and not done: self.il.addWidget(L("No intentions yet",10,c=C_TEXT2))
        self.il.addStretch()
    def _ic(self,it):
        c=Card(); cl=QHBoxLayout(c); cl.setContentsMargins(8,4,8,4); cc={"Self":C_GOLD,"Others":C_GREEN,"World":C_BLUE,"Gratitude":C_AMBER}
        cl.addWidget(L(f"● {it['cat']}",8,b=True,c=cc.get(it['cat'],C_TEXT2))); tl=QLabel(it['text']); tl.setStyleSheet("font-size:10px;color:#f0e6d3;"); tl.setWordWrap(True); cl.addWidget(tl,1)
        if not it['done']: btn=QPushButton("✓"); btn.setFixedSize(22,22); btn.setCursor(Qt.PointingHandCursor); btn.setStyleSheet("QPushButton{background:#1a3028;color:#4ecca3;border:1px solid #4ecca3;border-radius:4px;font-size:10px;}"); btn.clicked.connect(lambda _,iid=it['id']: (self.dm.complete_intention(iid),self.refresh())); cl.addWidget(btn)
        rb=QPushButton("✕"); rb.setFixedSize(22,22); rb.setCursor(Qt.PointingHandCursor); rb.setStyleSheet("QPushButton{background:transparent;color:#555570;border:1px solid #333350;border-radius:4px;font-size:10px;}QPushButton:hover{color:#e74c3c;border-color:#e74c3c;}"); rb.clicked.connect(lambda _,iid=it['id']: (self.dm.remove_intention(iid),self.refresh())); cl.addWidget(rb); return c

class JournalPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(8)
        lay.addWidget(L("Reflection Journal",17,b=True)); pr=QHBoxLayout()
        self.lbl_p=QLabel("Click for prompt"); self.lbl_p.setWordWrap(True); self.lbl_p.setStyleSheet("font-size:10px;color:#b0a888;font-style:italic;"); pr.addWidget(self.lbl_p,1)
        pb=QPushButton("✎"); pb.setFixedSize(26,26); pb.setCursor(Qt.PointingHandCursor); pb.setStyleSheet("QPushButton{background:#222240;color:#d4a843;border:1px solid #32325a;border-radius:5px;font-size:12px;}QPushButton:hover{border-color:#d4a843;}"); pb.clicked.connect(lambda: self.lbl_p.setText(PROMPTS[random.randint(0,len(PROMPTS)-1)])); pr.addWidget(pb)
        lay.addLayout(pr); self.ed=QTextEdit(); self.ed.setPlaceholderText("Write your reflections..."); self.ed.setStyleSheet("QTextEdit{background:#1a1a2e;border:1px solid #32325a;border-radius:8px;color:#f0e6d3;font-size:11px;padding:8px;}"); self.ed.setFixedHeight(90); lay.addWidget(self.ed)
        btn=Btn("Save","#d4a843","#0d0d1a","#f0d078"); btn.clicked.connect(self._save); lay.addWidget(btn,alignment=Qt.AlignRight)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        self.ew=QWidget(); self.el=QVBoxLayout(self.ew); self.el.setSpacing(3); self.el.setContentsMargins(0,0,0,0); scroll.setWidget(self.ew); lay.addWidget(scroll,1)
    def _save(self):
        t=self.ed.toPlainText().strip()
        if not t: self.toast.show_t("Empty","Write something",C_RED); return
        na=self.dm.add_journal(t); self.ed.clear(); self.toast.show_t("Saved","",C_GREEN)
        for a in na: self.toast.show_t("★ Achievement!",a["name"],C_GREEN)
        self.refresh()
    def refresh(self):
        while self.el.count(): w=self.el.takeAt(0).widget(); (w.deleteLater() if w else None)
        for e in reversed(self.dm.data['journal'][-40:]):
            c=Card(); cl=QVBoxLayout(c); cl.setContentsMargins(8,4,8,4); cl.addWidget(L(f"{e['date']} {e.get('time','')}",8,c=C_TEXT2)); tx=QLabel(e['text']); tx.setStyleSheet("font-size:10px;color:#f0e6d3;"); tx.setWordWrap(True); cl.addWidget(tx); self.el.addWidget(c)
        self.el.addStretch()

class WisdomPage(QWidget):
    def __init__(self,dm):
        super().__init__(); self.dm=dm; self._idx=(date.today().toordinal())%len(WISDOM); lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(14)
        lay.addWidget(L("Wisdom Oracle",17,b=True)); lay.addStretch()
        self.lbl_i=L("✦",36,b=True,C_GOLD); self.lbl_i.setAlignment(Qt.AlignCenter); lay.addWidget(self.lbl_i)
        self.lbl_q=QLabel(); self.lbl_q.setWordWrap(True); self.lbl_q.setAlignment(Qt.AlignCenter); self.lbl_q.setStyleSheet("font-size:16px;color:#f0e6d3;font-style:italic;"); lay.addWidget(self.lbl_q)
        self.lbl_s=QLabel(); self.lbl_s.setAlignment(Qt.AlignCenter); self.lbl_s.setStyleSheet("font-size:12px;color:#d4a843;"); lay.addWidget(self.lbl_s)
        self.lbl_fav=QLabel("♡"); self.lbl_fav.setCursor(Qt.PointingHandCursor); self.lbl_fav.setAlignment(Qt.AlignCenter); self.lbl_fav.clicked.connect(self._toggle); lay.addWidget(self.lbl_fav)
        lay.addStretch(); nav=QHBoxLayout()
        for txt,fn in [("◀ Prev",lambda:self._go(-1)),("Daily ▶",self._daily),("Next ▶",lambda:self._go(1))]:
            b=Btn(txt,"#1a1a2e","#8b8b9e","#1a1a2e","Daily" in txt); b.clicked.connect(fn); nav.addWidget(b)
        lay.addLayout(nav); self._show()
    def _go(self,d): self._idx=(self._idx+d)%len(WISDOM); self._show()
    def _daily(self): self._idx=(date.today().toordinal())%len(WISDOM); self._show()
    def _show(self):
        q,s=WISDOM[self._idx]; self.lbl_q.setText(f'"{q}"'); self.lbl_s.setText(f"— {s}"); fav=self.dm.is_fav(q,s); self.lbl_fav.setText("♥" if fav else "♡"); self.lbl_fav.setStyleSheet(f"font-size:18px;color:{C_RED.name() if fav else '#555570'};")
    def _toggle(self): q,s=WISDOM[self._idx]; self.dm.toggle_fav(q,s); self._show()
    def refresh(self): self._show()

class SettingsPage(QWidget):
    def __init__(self,dm,toast):
        super().__init__(); self.dm=dm; self.toast=toast; lay=QVBoxLayout(self); lay.setContentsMargins(20,12,20,12); lay.setSpacing(10)
        lay.addWidget(L("Settings",17,b=True)); nc=Card(); ncl=QVBoxLayout(nc); ncl.setContentsMargins(12,8,12,8); ncl.addWidget(L("Pilgrim Name",10,b=True))
        nr=QHBoxLayout(); self.ni=QLineEdit(); self.ni.setStyleSheet("QLineEdit{background:#222240;border:1px solid #32325a;border-radius:5px;color:#f0e6d3;font-size:12px;padding:6px;}QLineEdit:focus{border-color:#d4a843;}"); nr.addWidget(self.ni)
        nb=Btn("Save","#d4a843","#0d0d1a","#f0d078",False); nb.clicked.connect(self._sn); nr.addWidget(nb); ncl.addLayout(nr); lay.addWidget(nc)
        tc=Card(); tcl=QVBoxLayout(tc); tcl.setContentsMargins(12,8,12,8); tcl.addWidget(L("Select Title",10,b=True))
        self.tcb=QComboBox()
        for t in TITLES:
            try: u=t["cond"](self.dm.data); self.tcb.addItem(f"{'✦' if u else '🔒'} {t['name']}", t["id"])
            except: self.tcb.addItem(f"🔒 {t['name']}", t["id"])
        self.tcb.setStyleSheet("QComboBox{background:#222240;border:1px solid #32325a;border-radius:5px;color:#f0e6d3;font-size:11px;padding:6px;}QComboBox::drop-down{border:none;}QComboBox QAbstractItemView{background:#1a1a2e;color:#f0e6d3;}")
        tcl.addWidget(self.tcb); lay.addWidget(tc); ec=Card(); ecl=QVBoxLayout(ec); ecl.setContentsMargins(12,8,12,8); ecl.addWidget(L("Data",10,b=True)); ebr=QHBoxLayout()
        eb=Btn("📁 Export","#222240","#f0e6d3","#222240",False); eb.clicked.connect(self._exp); ebr.addWidget(eb)
        ib=Btn("📂 Import","#222240","#f0e6d3","#222240",False); ib.clicked.connect(self._imp); ebr.addWidget(ib); ecl.addLayout(ebr); lay.addWidget(ec)
        rc=Card("#1a1515","#e74c3c"); rcl=QVBoxLayout(rc); rcl.setContentsMargins(12,8,12,8); rcl.addWidget(L("Danger Zone",10,b=True,C_RED))
        rb=Btn("🗑 Reset All","#2a1515","#e74c3c","#3a2020"); rb.clicked.connect(self._reset); rcl.addWidget(rb); lay.addWidget(rc); lay.addStretch()
        ab=Card("#12121e","#1e1e36"); abl=QVBoxLayout(ab); abl.setContentsMargins(12,8,12,8); abl.addWidget(L("Sacred Path v4.0 — Ultimate",10,b=True,C_GOLD)); abl.addWidget(L("25+ Systems: Practices, Meditation, Tasbih, Moods, Quests, Skills, Altar, Offices, Examen, Lectio, Fasting, Virtues, Blessings, Achievements, Calendar, Stats, Intentions, Journal, Wisdom, Figures",9,c=C_TEXT2)); lay.addWidget(ab)
    def _sn(self):
        n=self.ni.text().strip()
        if n: self.dm.data['name']=n; self.dm.save(); self.toast.show_t("Updated",n,C_GREEN)
    def _exp(self):
        p,_=QFileDialog.getSaveFileName(self,"Export","sacred_path_save.json","JSON (*.json)")
        if p: Path(p).write_text(json.dumps(self.dm.data,indent=2)); self.toast.show_t("Exported","",C_GREEN)
    def _imp(self):
        p,_=QFileDialog.getOpenFileName(self,"Import","","JSON (*.json)")
        if p:
            try:
                d=json.loads(Path(p).read_text())
                if "level" in d and "virtues" in d: self.dm.data=d; self.dm.save(); self.toast.show_t("Imported","Restart app",C_GREEN)
                else: self.toast.show_t("Invalid","Bad file",C_RED)
            except Exception as e: self.toast.show_t("Error",str(e),C_RED)
    def _reset(self):
        if QMessageBox.question(self,"Reset?","Delete ALL progress?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes: self.dm.reset(); self.toast.show_t("Reset","Cleared",C_RED)
    def refresh(self): self.ni.setText(self.dm.data['name'])

# ── Sidebar & Main Window ────────────────────────────────────────
class NavBtn(QPushButton):
    def __init__(self,ico,label): super().__init__(); self.ico=ico; self.label=label; self.setFixedHeight(32); self.setCursor(Qt.PointingHandCursor); self._a=False
    def setActive(self,a): self._a=a; self.update()
    def paintEvent(self,e):
        pt=QPainter(self); pt.setRenderHint(QPainter.Antialiasing); r=self.rect().adjusted(2,1,-2,-1)
        if self._a: pt.setPen(Qt.NoPen); pt.setBrush(QColor(212,168,67,20)); pt.drawRoundedRect(r,6,6); pt.setPen(QPen(C_GOLD,1.5)); pt.setBrush(Qt.NoBrush); pt.drawRoundedRect(r,6,6); tc=C_GOLD_L
        else: tc=C_TEXT2
        f=pt.font(); f.setPixelSize(13); pt.setFont(f); pt.setPen(tc); pt.drawText(QRectF(r.x()+6,r.y(),24,r.height()),Qt.AlignCenter,self.ico)
        f.setPixelSize(10); pt.setFont(f); pt.drawText(QRectF(r.x()+30,r.y(),r.width()-34,r.height()),Qt.AlignLeft|Qt.AlignVCenter,self.label)

STYLE = "QWidget{background:#0d0d1a;color:#f0e6d3;}QScrollBar:vertical{background:transparent;width:5px;}QScrollBar::handle:vertical{background:#32325a;border-radius:2px;min-height:20px;}QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("Sacred Path v4 — Ultimate Gamified Spiritual Practice"); self.setMinimumSize(1050,680); self.resize(1200,780); self.setStyleSheet(STYLE)
        self.dm=DM()
        if self.dm.data['total']==0 and self.dm.data['name']=='Pilgrim':
            n,ok=QInputDialog.getText(self,"Sacred Path","Enter the name for your spiritual journey:",text="Pilgrim")
            if ok and n.strip(): self.dm.data['name']=n.strip(); self.dm.save()
        central=QWidget(); self.setCentralWidget(central); ml=QHBoxLayout(central); ml.setContentsMargins(0,0,0,0); ml.setSpacing(0)
        self.particles=ParticleBg(central); self.particles.lower(); self.particles.resize(self.size())
        sb=QFrame(); sb.setFixedWidth(175); sb.setStyleSheet("QFrame{background:#0f0f22;border-right:1px solid #1a1a36;}")
        sl=QVBoxLayout(sb); sl.setContentsMargins(6,12,6,12); sl.setSpacing(1)
        logo=L("✦",26,b=True,C_GOLD); logo.setAlignment(Qt.AlignCenter); sl.addWidget(logo)
        ln=L("Sacred Path",11,b=True,C_GOLD); ln.setAlignment(Qt.AlignCenter); sl.addWidget(ln); sl.addSpacing(8)
        sections=[("JOURNEY",[("◈","Dashboard"),("✦","Practices"),("◎","Meditation"),("📿","Tasbih"),("😊","Moods")]),
                  ("PRAYER",[("🪷","Daily Office"),("🔍","Examen"),("📖","Lectio Divina"),("♡","Intentions"),("◈","Fasting")]),
                  ("GROWTH",[("❋","Virtues"),("✧","Blessings"),("★","Achievements"),("⚡","Quests"),("☯","Skill Tree")]),
                  ("INSIGHTS",[("🕯","Altar"),("▦","Calendar"),("📊","Statistics"),("✎","Journal"),("✿","Wisdom"),("🕊","Figures")]),
                  ("",[("⚙","Settings")])]
        self.nav_btns=[]
        for sec_name,items in sections:
            if sec_name: sl.addWidget(L(sec_name,7,b=True,QColor(60,60,90)))
            for ico,lbl in items: b=NavBtn(ico,lbl); b.clicked.connect(lambda _,i=len(self.nav_btns):self._nav(i)); sl.addWidget(b); self.nav_btns.append(b)
            if sec_name: sl.addSpacing(4)
        sl.addStretch(); self.side_lv=L("",9,c=C_TEXT2); self.side_lv.setAlignment(Qt.AlignCenter); sl.addWidget(self.side_lv)
        self.side_sk=L("",9,c=C_AMBER); self.side_sk.setAlignment(Qt.AlignCenter); sl.addWidget(self.side_sk); ml.addWidget(sb)
        self.toast=Toast(self); self.stack=QStackedWidget()
        self.pages=[DashboardPage(self.dm,self.toast), PracticesPage(self.dm,self.toast), MeditationPage(self.dm,self.toast),
                    TasbihPage(self.dm,self.toast), MoodPage(self.dm,self.toast), DailyOfficePage(self.dm,self.toast),
                    ExamenPage(self.dm,self.toast), LectioPage(self.dm,self.toast), IntentionsPage(self.dm,self.toast),
                    FastingPage(self.dm,self.toast), VirtuesPage(self.dm), BlessingsPage(self.dm),
                    AchievementsPage(self.dm), QuestsPage(self.dm,self.toast), SkillTreePage(self.dm,self.toast),
                    AltarPage(self.dm,self.toast), CalendarPage(self.dm), StatsPage(self.dm),
                    JournalPage(self.dm,self.toast), WisdomPage(self.dm), FiguresPage(self.dm),
                    SettingsPage(self.dm,self.toast)]
        # Replace heatmap in stats
        hm = HeatmapWidget(self.dm)
        stats_lay = self.pages[17].layout()
        stats_lay.replaceWidget(self.pages[17].heatmap, hm)
        self.pages[17].heatmap = hm
        
        for p in self.pages: self.stack.addWidget(p)
        self.pages[1].practice_done.connect(lambda *_: self._refresh_all())
        self._nav(0); self._refresh_all()
    def resizeEvent(self,e): self.particles.resize(self.size()); super().resizeEvent(e)
    def _nav(self,idx):
        self.stack.setCurrentIndex(idx)
        for i,b in enumerate(self.nav_btns): b.setActive(i==idx)
        self._refresh_all()
    def _refresh_all(self):
        for p in self.pages: p.refresh()
        d=self.dm.data; self.side_lv.setText(f"Lv.{d['level']} • {d['total']}p • {d.get('med_total',0)}m"); self.side_sk.setText(f"🔥 {d['streak']}d streak")

def main():
    app=QApplication(sys.argv); app.setStyle("Fusion")
    pal=QPalette(); pal.setColor(QPalette.Window,C_BG); pal.setColor(QPalette.WindowText,C_TEXT); pal.setColor(QPalette.Base,C_BG2); pal.setColor(QPalette.Text,C_TEXT); pal.setColor(QPalette.Button,C_BG2); pal.setColor(QPalette.ButtonText,C_TEXT); pal.setColor(QPalette.Highlight,C_GOLD); pal.setColor(QPalette.HighlightedText,C_BG); app.setPalette(pal)
    win=MainWindow(); win.show(); sys.exit(app.exec())

if __name__=="__main__": main()