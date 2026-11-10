// SPDX-License-Identifier: GPL-3.0-only
// Guru-600 editor: the interface in the language chosen (SETTINGS > EDITOR > LANGUAGE), and the tooltips.
// The editor's own words (tabs, boxes, buttons, hints) are translated; the FM-1's (the names on its screen: CUTOFF, LFO,
// MUTE, the menu...) stay in English, as on the device. Hovering an FM-1 word (or a knob, a key, a setting) shows a tooltip in
// the language chosen only: the word's translation (guru-gloss.js) and a summary of what it does (the guide's, guru-tips.js;
// its first sentence). The tooltips are switched on and off by the speech-bubble button left of the bulb (kept in this browser).
"use strict";

/* --------------------------------------------------------------------------- the editor's own words --- */
// [English, fr, de, es, it, zh, ja]; a page key first ("@song") limits the entry to that page (the word means something
// else elsewhere: ADD, INSERT, SAVE...)
const I18N_WORDS = [
  ["CONNECT FM-1", "CONNECTER LE FM-1", "FM-1 VERBINDEN", "CONECTAR EL FM-1", "COLLEGA L'FM-1", "连接 FM-1", "FM-1 に接続"],
  ["FM-1 CONNECTED", "FM-1 CONNECTÉ", "FM-1 VERBUNDEN", "FM-1 CONECTADO", "FM-1 COLLEGATO", "FM-1 已连接", "FM-1 接続中"],
  ["TRACK", "PISTE", "SPUR", "PISTA", "TRACCIA", "音轨", "トラック"],
  ["SOUND", "SON", "KLANG", "SONIDO", "SUONO", "音色", "サウンド"],
  ["SEQUENCER", "SÉQUENCEUR", "SEQUENZER", "SECUENCIADOR", "SEQUENCER", "音序器", "シーケンサー"],
  ["SONG", "MORCEAU", "SONG", "CANCIÓN", "BRANO", "乐曲", "ソング"],
  ["TRACKS", "PISTES", "SPUREN", "PISTAS", "TRACCE", "音轨", "トラック"],
  ["PROJECTS", "PROJETS", "PROJEKTE", "PROYECTOS", "PROGETTI", "项目", "プロジェクト"],
  ["SAMPLES", "SAMPLES", "SAMPLES", "MUESTRAS", "CAMPIONI", "采样", "サンプル"],
  ["BACKUP", "SAUVEGARDE", "SICHERUNG", "COPIA", "BACKUP", "备份", "バックアップ"],
  ["SETTINGS", "RÉGLAGES", "SETUP", "AJUSTES", "IMPOSTAZIONI", "设置", "設定"],
  ["SOUNDS", "SONS", "KLÄNGE", "SONIDOS", "SUONI", "音色", "サウンド"],
  ["@sound", "ALL", "TOUS", "ALLE", "TODOS", "TUTTI", "全部", "すべて"],
  ["SAVE TO THIS PLACE", "ENREGISTRER ICI", "HIER SPEICHERN", "GUARDAR AQUÍ", "SALVA QUI", "保存到此位置", "この位置に保存"],
  ["BACK TO ORIGINAL", "REVENIR À L'ORIGINAL", "ZUM ORIGINAL", "VOLVER AL ORIGINAL", "TORNA ALL'ORIGINALE", "恢复原始", "オリジナルに戻す"],
  ["EXPORT .SYX", "EXPORTER .SYX", "EXPORT .SYX", "EXPORTAR .SYX", "ESPORTA .SYX", "导出 .SYX", ".SYX 書き出し"],
  ["IMPORT .SYX", "IMPORTER .SYX", "IMPORT .SYX", "IMPORTAR .SYX", "IMPORTA .SYX", "导入 .SYX", ".SYX 読み込み"],
  ["RESET ALL SOUNDS", "RÉINITIALISER LES SONS", "ALLE SOUNDS ZURÜCK", "RESTABLECER SONIDOS", "RIPRISTINA I SUONI", "重置所有音色", "全サウンドをリセット"],
  ["SEQUENCE", "SÉQUENCE", "SEQUENZ", "SECUENCIA", "SEQUENZA", "音序", "シーケンス"],
  ["STEPS", "PAS", "SCHRITTE", "PASOS", "PASSI", "步", "ステップ"],
  ["TOOLS", "OUTILS", "WERKZEUGE", "HERRAMIENTAS", "STRUMENTI", "工具", "ツール"],
  ["DETAIL", "DÉTAIL", "DETAILS", "DETALLE", "DETTAGLIO", "细节", "詳細"],
  ["AUTOMATION", "AUTOMATION", "AUTOMATION", "AUTOMATIZACIÓN", "AUTOMAZIONE", "自动化", "自動化"],
  ["DELETE", "SUPPRIMER", "LÖSCHEN", "BORRAR", "ELIMINA", "删除", "削除"],
  ["CLEAR ALL", "TOUT EFFACER", "ALLES LÖSCHEN", "BORRAR TODO", "CANCELLA TUTTO", "全部清除", "すべて消去"],
  ["SECTIONS", "SECTIONS", "ABSCHNITTE", "SECCIONES", "SEZIONI", "段落", "セクション"],
  ["REPEAT", "RÉPÉT.", "WIEDERH.", "REPET.", "RIPET.", "重复", "リピート"],
  ["RESET GURU-600", "RÉINITIALISER LE GURU-600", "GURU-600 ZURÜCKSETZEN", "RESTABLECER GURU-600", "REIMPOSTA GURU-600", "重置 GURU-600", "GURU-600 をリセット"],
  ["FACTORY", "USINE", "WERKSEINST.", "FÁBRICA", "FABBRICA", "出厂", "初期化"],
  ["▶ PLAY SONG", "▶ JOUER", "▶ ABSPIELEN", "▶ REPRODUCIR", "▶ SUONA", "▶ 播放乐曲", "▶ ソング再生"],
  ["■ STOP", "■ ARRÊT", "■ STOPP", "■ PARAR", "■ STOP", "■ 停止", "■ 停止"],
  ["@song", "ADD", "AJOUTER", "HINZUFÜGEN", "AÑADIR", "AGGIUNGI", "添加", "追加"],
  ["@song", "INSERT", "INSÉRER", "EINFÜGEN", "INSERTAR", "INSERISCI", "插入", "挿入"],
  ["MOVE UP", "MONTER", "NACH OBEN", "SUBIR", "SU", "上移", "上へ"],
  ["MOVE DOWN", "DESCENDRE", "NACH UNTEN", "BAJAR", "GIÙ", "下移", "下へ"],
  ["CLEAR SONG", "EFFACER LE MORCEAU", "SONG LÖSCHEN", "BORRAR CANCIÓN", "CANCELLA BRANO", "清除乐曲", "ソング消去"],
  ["SLOTS", "EMPLACEMENTS", "PLÄTZE", "RANURAS", "SLOT", "槽位", "スロット"],
  ["SAVE THEM IN PROJECTS", "À ENREGISTRER DANS PROJETS", "IN PROJEKTEN SPEICHERN", "GUARDAR EN PROYECTOS", "SALVALI IN PROGETTI", "保存在项目中", "プロジェクトに保存"],
  ["@arp", "KEY", "TONALITÉ", "TONART", "TONALIDAD", "TONALITÀ", "调", "キー"],
  ["ALL TRACKS", "TOUTES LES PISTES", "ALLE SPUREN", "TODAS LAS PISTAS", "TUTTE LE TRACCE", "所有音轨", "全トラック"],
  ["TUNE: ALL TRACKS · GROOVE: THE SONG'S SWING", "TUNE : TOUTES LES PISTES · GROOVE : LE SWING DU MORCEAU", "TUNE: ALLE SPUREN · GROOVE: DER SWING DES SONGS",
    "TUNE: TODAS LAS PISTAS · GROOVE: EL SWING DE LA CANCIÓN", "TUNE: TUTTE LE TRACCE · GROOVE: LO SWING DEL BRANO", "TUNE：所有音轨 · GROOVE：乐曲的摇摆", "TUNE：全トラック · GROOVE：ソングのスウィング"],
  ["ACTIVE", "ACTIVES", "AKTIV", "ACTIVAS", "ATTIVE", "生效中", "有効"],
  ["@projects", "SAVE", "ENREGISTRER", "SPEICHERN", "GUARDAR", "SALVA", "保存", "保存"],
  ["LOAD", "CHARGER", "LADEN", "CARGAR", "CARICA", "载入", "読込"],
  ["EMPTY", "VIDE", "LEER", "VACÍO", "VUOTO", "空", "空"],
  ["SAVED", "ENREGISTRÉ", "GESPEICHERT", "GUARDADO", "SALVATO", "已保存", "保存済み"],
  ["A PROJECT HOLDS THE FOUR TRACKS: THEIR SOUNDS, STEPS AND AUTOMATION, THE MIX AND THE SONG.",
    "UN PROJET CONTIENT LES QUATRE PISTES : LEURS SONS, LEURS PAS ET LEUR AUTOMATION, LE MIXAGE ET LE MORCEAU.",
    "EIN PROJEKT ENTHÄLT DIE VIER SPUREN: IHRE SOUNDS, SCHRITTE UND AUTOMATION, DEN MIX UND DEN SONG.",
    "UN PROYECTO CONTIENE LAS CUATRO PISTAS: SUS SONIDOS, PASOS Y AUTOMATIZACIÓN, LA MEZCLA Y LA CANCIÓN.",
    "UN PROGETTO CONTIENE LE QUATTRO TRACCE: SUONI, PASSI E AUTOMAZIONE, IL MIX E IL BRANO.",
    "一个项目包含四个音轨：它们的音色、步进和自动化、混音以及乐曲。", "プロジェクトには 4 トラック（サウンド、ステップ、オートメーション）、ミックス、ソングが含まれます。"],
  ["THE SONG PLAYS ITS SECTIONS FROM THESE SLOTS.", "LE MORCEAU JOUE SES SECTIONS DEPUIS CES EMPLACEMENTS.", "DER SONG SPIELT SEINE ABSCHNITTE AUS DIESEN PLÄTZEN.",
    "LA CANCIÓN TOCA SUS SECCIONES DESDE ESTAS RANURAS.", "IL BRANO SUONA LE SUE SEZIONI DA QUESTI SLOT.", "乐曲从这些槽位播放其段落。", "ソングはこれらのスロットからセクションを再生します。"],
  ["USER SOUNDS", "SONS UTILISATEUR", "EIGENE SOUNDS", "SONIDOS DEL USUARIO", "SUONI UTENTE", "用户音色", "ユーザーサウンド"],
  ["STORE THE TRACK'S SOUND", "RANGER LE SON DE LA PISTE", "SOUND DER SPUR ABLEGEN", "GUARDAR EL SONIDO DE LA PISTA", "SALVA IL SUONO DELLA TRACCIA", "存储音轨的音色", "トラックの音色を保存"],
  ["ERASE", "EFFACER", "LÖSCHEN", "BORRAR", "CANCELLA", "清除", "消去"],
  ["NAME", "NOM", "NAME", "NOMBRE", "NOME", "名称", "名前"],
  ["DROP WAV FILES HERE", "DÉPOSEZ DES FICHIERS WAV ICI", "WAV-DATEIEN HIER ABLEGEN", "SUELTE AQUÍ ARCHIVOS WAV", "TRASCINA QUI I FILE WAV", "将 WAV 文件拖到此处", "WAV ファイルをここにドロップ"],
  ["OR", "OU", "ODER", "O", "O", "或", "または"],
  ["CHOOSE FILES", "CHOISIR DES FICHIERS", "DATEIEN WÄHLEN", "ELEGIR ARCHIVOS", "SCEGLI FILE", "选择文件", "ファイルを選択"],
  ["ON THE FM-1", "DANS LE FM-1", "IM FM-1", "EN EL FM-1", "NELL'FM-1", "FM-1 中", "FM-1 内"],
  ["SAVE A BACKUP TO THIS COMPUTER", "SAUVEGARDER SUR CET ORDINATEUR", "AUF DIESEM COMPUTER SICHERN", "GUARDAR UNA COPIA EN ESTE ORDENADOR", "SALVA UN BACKUP SU QUESTO COMPUTER", "备份到这台电脑", "このコンピューターにバックアップ"],
  ["FROM A FILE", "DEPUIS UN FICHIER", "AUS EINER DATEI", "DESDE UN ARCHIVO", "DA UN FILE", "从文件", "ファイルから"],
  ["DROP A BACKUP FILE HERE", "DÉPOSEZ UN FICHIER DE SAUVEGARDE ICI", "SICHERUNGSDATEI HIER ABLEGEN", "SUELTE AQUÍ UN ARCHIVO DE COPIA", "TRASCINA QUI UN FILE DI BACKUP", "将备份文件拖到此处", "バックアップファイルをここにドロップ"],
  ["CHOOSE A FILE", "CHOISIR UN FICHIER", "DATEI WÄHLEN", "ELEGIR UN ARCHIVO", "SCEGLI UN FILE", "选择文件", "ファイルを選択"],
  ["RESTORE IT ON THE FM-1", "LA RESTAURER SUR LE FM-1", "AUF DEM FM-1 WIEDERHERSTELLEN", "RESTAURARLA EN EL FM-1", "RIPRISTINALO SULL'FM-1", "恢复到 FM-1", "FM-1 に復元"],
  ["SAVED AS IT IS NOW, IN ONE FILE", "ENREGISTRÉ TEL QU'IL EST, EN UN SEUL FICHIER", "SO WIE ER JETZT IST, IN EINER DATEI", "GUARDADO TAL COMO ESTÁ, EN UN SOLO ARCHIVO",
    "SALVATO COM'È ORA, IN UN SOLO FILE", "按当前状态保存为一个文件", "現在の状態を 1 つのファイルに保存"],
  ["CONNECT THE FM-1 TO SAVE IT", "CONNECTEZ LE FM-1 POUR LE SAUVEGARDER", "FM-1 VERBINDEN, UM IHN ZU SICHERN", "CONECTE EL FM-1 PARA GUARDARLO", "COLLEGA L'FM-1 PER SALVARLO",
    "连接 FM-1 以进行备份", "保存するには FM-1 を接続"],
  ["THIS FIRMWARE CANNOT BE BACKED UP FROM HERE", "CE FIRMWARE NE PEUT PAS ÊTRE SAUVEGARDÉ D'ICI", "DIESE FIRMWARE KANN HIER NICHT GESICHERT WERDEN",
    "ESTE FIRMWARE NO SE PUEDE GUARDAR DESDE AQUÍ", "QUESTO FIRMWARE NON PUÒ ESSERE SALVATO DA QUI", "无法从此处备份此固件", "このファームウェアはここからバックアップできません"],
  ["A FILE SAVED HERE, BY THE MAC APPLICATION OR THE INSTALLER", "UN FICHIER ENREGISTRÉ ICI, PAR L'APPLICATION MAC OU PAR L'INSTALLEUR",
    "EINE HIER, VON DER MAC-ANWENDUNG ODER VOM INSTALLER GESPEICHERTE DATEI", "UN ARCHIVO GUARDADO AQUÍ, POR LA APLICACIÓN MAC O POR EL INSTALADOR",
    "UN FILE SALVATO QUI, DALL'APPLICAZIONE MAC O DALL'INSTALLER", "在此处、Mac 应用程序或安装程序保存的文件", "ここ、Mac アプリケーション、またはインストーラーで保存したファイル"],
  ["WHAT THE FILE HOLDS SHOWS HERE BEFORE IT IS RESTORED", "LE CONTENU DU FICHIER S'AFFICHE ICI AVANT LA RESTAURATION", "DER DATEIINHALT ERSCHEINT HIER VOR DER WIEDERHERSTELLUNG",
    "EL CONTENIDO DEL ARCHIVO SE MUESTRA AQUÍ ANTES DE RESTAURARLO", "IL CONTENUTO DEL FILE APPARE QUI PRIMA DEL RIPRISTINO", "恢复前，文件内容会显示在这里", "復元前にファイルの内容がここに表示されます"],
  ["MUSIC", "MUSIQUE", "MUSIK", "MÚSICA", "MUSICA", "音乐", "ミュージック"],
  ["CURRENT MUSIC", "MUSIQUE EN COURS", "AKTUELLE MUSIK", "MÚSICA ACTUAL", "MUSICA CORRENTE", "当前音乐", "現在のミュージック"],
  ["USER SOUNDS' FM6 PATCHES", "PATCHS FM6 UTILISATEUR", "EIGENE FM6-PATCHES", "PATCHES FM6 DEL USUARIO", "PATCH FM6 UTENTE", "用户 FM6 参数", "ユーザー FM6 パッチ"],
  ["P600 PLACES", "PLACES P600", "P600-PLÄTZE", "POSICIONES P600", "POSIZIONI P600", "P600 位置", "P600 プレイス"],
  ["FM6 VOICE BANK", "BANQUE DE VOIX FM6", "FM6-STIMMENBANK", "BANCO DE VOCES FM6", "BANCO VOCI FM6", "FM6 音色库", "FM6 ボイスバンク"],
  ["SLICE SLICES", "DÉCOUPES SLICE", "SLICE-SCHNITTE", "CORTES SLICE", "TAGLI SLICE", "SLICE 切片", "SLICE スライス"],
  ["FM6 PATCH BANK (OLD)", "BANQUE DE PATCHS FM6 (ANCIENNE)", "FM6-PATCHBANK (ALT)", "BANCO DE PATCHES FM6 (ANTIGUO)", "BANCO PATCH FM6 (VECCHIO)", "FM6 参数库（旧）", "FM6 パッチバンク（旧）"],
  // the FM-1's menu (SETTINGS): its rows' names translated; their values (ON, OFF, IDLE...) stay as on the FM-1
  ["@settings", "DISPLAY", "AFFICHAGE", "ANZEIGE", "PANTALLA", "SCHERMO", "显示", "表示"],
  ["@settings", "CONTROL", "COMMANDES", "BEDIENUNG", "CONTROLES", "CONTROLLI", "控制", "操作"],
  ["@settings", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "音频", "オーディオ"],
  ["@settings", "SYSTEM", "SYSTÈME", "SYSTEM", "SISTEMA", "SISTEMA", "系统", "システム"],
  ["@settings", "COLOR", "COULEURS", "FARBEN", "COLORES", "COLORI", "配色", "配色"],
  ["@settings", "STYLE", "STYLE", "STIL", "ESTILO", "STILE", "样式", "スタイル"],
  ["@settings", "LARGE", "GRAND TEXTE", "GROSSE SCHRIFT", "TEXTO GRANDE", "TESTO GRANDE", "大字", "大きな文字"],
  ["@settings", "ANIM", "ANIMATIONS", "ANIMATIONEN", "ANIMACIONES", "ANIMAZIONI", "动画", "アニメ"],
  ["@settings", "LEDS", "VOYANTS", "LEDS", "LEDS", "LED", "指示灯", "LED"],
  ["@settings", "SCREEN OFF", "VEILLE ÉCRAN", "BILDSCHIRM AUS", "APAGAR PANTALLA", "SPEGNI SCHERMO", "屏幕关闭", "画面オフ"],
  ["@settings", "SCOPE", "OSCILLOSCOPE", "OSZILLOSKOP", "OSCILOSCOPIO", "OSCILLOSCOPIO", "示波器", "スコープ"],
  ["@settings", "HOLD", "MAINTIEN", "HALTEN", "MANTENER", "TENUTA", "按住时长", "長押し"],
  ["@settings", "KNOB ACCEL", "ACCÉL. BOUTONS", "REGLER-BESCHL.", "ACEL. MANDOS", "ACCEL. MANOPOLE", "旋钮加速", "ノブ加速"],
  ["@settings", "FX LATCH", "VERROU EFFETS", "FX-HALTEN", "BLOQUEO FX", "BLOCCO FX", "效果锁定", "FX ラッチ"],
  ["@settings", "BPM LOCK", "VERROU TEMPO", "TEMPO-SPERRE", "BLOQUEO TEMPO", "BLOCCO TEMPO", "速度锁定", "テンポ固定"],
  ["@settings", "SCALE LEDS", "VOYANTS GAMME", "SKALEN-LEDS", "LEDS ESCALA", "LED SCALA", "音阶指示灯", "スケール LED"],
  ["@settings", "STEP PREVIEW", "ÉCOUTE DES PAS", "SCHRITT-VORHÖREN", "ESCUCHA PASOS", "ASCOLTO PASSI", "步进试听", "ステップ試聴"],
  ["@settings", "CHORD ENTRY", "SAISIE ACCORDS", "AKKORDEINGABE", "ENTRADA ACORDES", "INSERIM. ACCORDI", "和弦输入", "コード入力"],
  ["@settings", "SELECT", "BOUTON SELECT", "SELECT-REGLER", "MANDO SELECT", "MANOPOLA SELECT", "SELECT 旋钮", "SELECT ノブ"],
  ["@settings", "SPEAKER EQ", "ÉGALISEUR HP", "LAUTSPRECHER-EQ", "EQ ALTAVOZ", "EQ ALTOPARLANTE", "扬声器均衡", "スピーカー EQ"],
  ["@settings", "USB LEVEL", "NIVEAU USB", "USB-PEGEL", "NIVEL USB", "LIVELLO USB", "USB 电平", "USB レベル"],
  ["@settings", "CLICK", "MÉTRONOME", "METRONOM", "METRÓNOMO", "METRONOMO", "节拍器", "メトロノーム"],
  ["@settings", "CLICK LEVEL", "VOL. MÉTRONOME", "METRONOM-PEGEL", "VOL. METRÓNOMO", "VOL. METRONOMO", "节拍器音量", "メトロノーム音量"],
  ["@settings", "COUNT-IN", "DÉCOMPTE", "EINZÄHLER", "CUENTA PREVIA", "CONTEGGIO", "预备拍", "カウントイン"],
  ["@settings", "TUNE", "ACCORD", "STIMMUNG", "AFINACIÓN", "ACCORDATURA", "调音", "チューニング"],
  ["@settings", "MIDI IN", "ENTRÉE MIDI", "MIDI-EINGANG", "ENTRADA MIDI", "INGRESSO MIDI", "MIDI 输入", "MIDI 入力"],
  ["@settings", "AUTO SELECT", "SÉLECTION AUTO", "AUTO-AUSWAHL", "SELECCIÓN AUTO", "SELEZIONE AUTO", "自动选择", "自動選択"],
  ["@settings", "SCREEN WAKE", "RÉVEIL ÉCRAN", "BILDSCHIRM WECKEN", "DESPERTAR PANTALLA", "RIATTIVA SCHERMO", "屏幕唤醒", "画面復帰"],
  ["@settings", "RESTORE LAST", "REPRISE SESSION", "LETZTEN STAND", "RESTAURAR ÚLTIMO", "RIPRENDI ULTIMO", "恢复上次", "前回を復元"],
  ["@settings", "HELP", "AIDE", "HILFE", "AYUDA", "AIUTO", "帮助", "ヘルプ"],
  ["@settings", "2ND CORE", "2ᵉ CŒUR", "2. KERN", "2.º NÚCLEO", "2° CORE", "第二核心", "第 2 コア"],
  // ...and their values too (Marc, 10/11: the menu all in the language chosen; the tooltip gives the FM-1's word)
  ["@settings", "ON", "OUI", "AN", "SÍ", "SÌ", "开", "オン"],
  ["@settings", "OFF", "NON", "AUS", "NO", "NO", "关", "オフ"],
  ["@settings", "ON (BETA)", "OUI (BÊTA)", "AN (BETA)", "SÍ (BETA)", "SÌ (BETA)", "开 (测试版)", "オン (ベータ)"],
  ["@settings", "FLAT", "PLAT", "FLACH", "PLANO", "PIATTO", "平直", "フラット"],
  ["@settings", "LINE", "TRAITS", "LINIEN", "LÍNEAS", "LINEE", "线条", "ライン"],
  ["@settings", "LIT", "ÉCLAIRÉ", "LEUCHTEND", "ILUMINADO", "ILLUMINATO", "发光", "発光"],
  ["@settings", "IDLE", "AU REPOS", "LEERLAUF", "EN REPOSO", "A RIPOSO", "空闲时", "待機時"],
  ["@settings", "NEVER", "JAMAIS", "NIE", "NUNCA", "MAI", "从不", "しない"],
  ["@settings", "OUT", "SORTIE", "AUSGANG", "SALIDA", "USCITA", "输出", "出力"],
  ["@settings", "MIX", "MIXAGE", "MIX", "MEZCLA", "MIX", "混音", "ミックス"],
  ["@settings", "DIM LO", "TAMISÉ −", "GEDIMMT −", "TENUE −", "SOFFUSO −", "暗 −", "減光 −"],
  ["@settings", "DIM HI", "TAMISÉ +", "GEDIMMT +", "TENUE +", "SOFFUSO +", "暗 +", "減光 +"],
  ["@settings", "INV", "INVERSÉ", "INVERS", "INVERTIDO", "INVERTITO", "反相", "反転"],
  ["@settings", "DIM", "TAMISÉ", "GEDIMMT", "TENUE", "SOFFUSO", "暗", "減光"],
  ["@settings", "INV LO", "INVERSÉ −", "INVERS −", "INVERTIDO −", "INVERTITO −", "反相 −", "反転 −"],
  ["@settings", "INV HI", "INVERSÉ +", "INVERS +", "INVERTIDO +", "INVERTITO +", "反相 +", "反転 +"],
  ["@settings", "ADD", "AJOUT", "HINZU", "AÑADIR", "AGGIUNTA", "添加", "追加"],
  ["@settings", "PAGE", "PAGE", "SEITE", "PÁGINA", "PAGINA", "页面", "ページ"],
  ["@settings", "MODW", "MOLETTE", "MOD-RAD", "RUEDA MOD", "ROT. MOD", "调制轮", "MODW"],
  ["@settings", "VEL", "VÉLOCITÉ", "ANSCHLAG", "VELOCIDAD", "VELOCITÀ", "力度", "VEL"],
  ["@settings", "LOWCUT", "COUPE-BAS", "LOW-CUT", "CORTE GRAVES", "TAGLIO BASSI", "低切", "ローカット"],
  ["@settings", "BASS+", "GRAVES +", "BASS +", "GRAVES +", "BASSI +", "低音 +", "低音 +"],
  ["@settings", "MASTER", "GÉNÉRAL", "MASTER", "MAESTRO", "MASTER", "主音量", "マスター"],
  ["@settings", "FIXED", "FIXE", "FEST", "FIJO", "FISSO", "固定", "固定"],
  ["@settings", "REC", "ENREG.", "AUFN.", "GRAB.", "REG.", "录音时", "録音時"],
  ["@settings", "LOW", "FAIBLE", "LEISE", "BAJO", "BASSO", "低", "小"],
  ["@settings", "MID", "MOYEN", "MITTEL", "MEDIO", "MEDIO", "中", "中"],
  ["@settings", "HIGH", "FORT", "LAUT", "ALTO", "ALTO", "高", "大"],
  ["@settings", "1 BAR", "1 MESURE", "1 TAKT", "1 COMPÁS", "1 BATTUTA", "1 小节", "1 小節"],
  ["@settings", "2 BARS", "2 MESURES", "2 TAKTE", "2 COMPASES", "2 BATTUTE", "2 小节", "2 小節"],
  ["@settings", "SEL", "SÉL.", "AUSW.", "SEL.", "SEL.", "所选", "選択"],
  ["@settings", "TRACK", "PAR PISTE", "JE SPUR", "POR PISTA", "PER TRACCIA", "按音轨", "トラック別"],
  ["@settings", "PANEL", "FAÇADE", "BEDIENFELD", "PANEL", "PANNELLO", "面板", "パネル"],
  ["@settings", "GREY", "GRIS", "GRAU", "GRIS", "GRIGIO", "灰", "グレー"],
  ["@settings", "GREEN", "VERT", "GRÜN", "VERDE", "VERDE", "绿", "グリーン"],
  ["@settings", "AMBER", "AMBRE", "BERNSTEIN", "ÁMBAR", "AMBRA", "琥珀", "アンバー"],
  ["@settings", "ICE", "GLACE", "EIS", "HIELO", "GHIACCIO", "冰", "アイス"],
  ["@settings", "VIOLET", "VIOLET", "VIOLETT", "VIOLETA", "VIOLA", "紫", "バイオレット"],
  ["@settings", "ROSE", "ROSE", "ROSA", "ROSA", "ROSA", "玫瑰", "ローズ"],
  ["@settings", "PAPER", "PAPIER", "PAPIER", "PAPEL", "CARTA", "纸", "ペーパー"],
  ["@settings", "HI-CON", "CONTRASTÉ", "KONTRAST", "CONTRASTE", "CONTRASTO", "高对比", "ハイコントラスト"],
  ["@settings", "NIGHT", "NUIT", "NACHT", "NOCHE", "NOTTE", "夜", "ナイト"],
  ["@settings", "MONO", "MONO", "MONO", "MONO", "MONO", "单色", "モノ"],
  ["@settings", "CUSTOM", "PERSO", "EIGENE", "PERSONAL.", "PERSONAL.", "自定义", "カスタム"],
  ["EDITOR", "ÉDITEUR", "EDITOR", "EDITOR", "EDITOR", "编辑器", "エディター"],
  ["LIGHTING", "ÉCLAIRAGE", "BELEUCHTUNG", "ILUMINACIÓN", "ILLUMINAZIONE", "照明", "ライティング"],
  ["LANGUAGE", "LANGUE", "SPRACHE", "IDIOMA", "LINGUA", "语言", "言語"],
  ["THE EDITOR'S OWN, KEPT IN THIS BROWSER. THE OTHERS ARE THE FM-1'S MENU: SAVED IN IT AT ONCE.",
    "PROPRES À L'ÉDITEUR, GARDÉS DANS CE NAVIGATEUR. LES AUTRES SONT LE MENU DU FM-1 : ENREGISTRÉS AUSSITÔT DANS L'APPAREIL.",
    "NUR FÜR DEN EDITOR, IN DIESEM BROWSER GESPEICHERT. DIE ANDEREN SIND DAS MENÜ DES FM-1: SOFORT DARIN GESPEICHERT.",
    "PROPIOS DEL EDITOR, GUARDADOS EN ESTE NAVEGADOR. LOS DEMÁS SON EL MENÚ DEL FM-1: SE GUARDAN EN ÉL AL INSTANTE.",
    "PROPRI DELL'EDITOR, SALVATI IN QUESTO BROWSER. GLI ALTRI SONO IL MENU DELL'FM-1: SALVATI SUBITO NELL'APPARECCHIO.",
    "编辑器自身的设置，保存在此浏览器中。其他设置属于 FM-1 的菜单：会立即保存在设备中。",
    "エディター専用の設定で、このブラウザーに保存されます。その他は FM-1 のメニューで、すぐに本体に保存されます。"],
];
// patterns: the dynamic texts ($1, $2: the parts kept)
const I18N_RE = [
  [/^(\d)\.(\d) s$/, "$1,$2 s", "$1,$2 s", "$1,$2 s", "$1,$2 s", "$1.$2 秒", "$1.$2 秒"],
  [/^T(\d) CHANNEL$/, "CANAL PISTE $1", "KANAL SPUR $1", "CANAL PISTA $1", "CANALE TRACCIA $1", "音轨 $1 通道", "トラック $1 チャンネル"],
  [/^TRACK (\d)$/, "PISTE $1", "SPUR $1", "PISTA $1", "TRACCIA $1", "音轨 $1", "トラック $1"],
  [/^TRACK (\d) · SEND 0 %$/, "PISTE $1 · ENVOI 0 %", "SPUR $1 · SEND 0 %", "PISTA $1 · ENVÍO 0 %", "TRACCIA $1 · MANDATA 0 %", "音轨 $1 · 发送 0 %", "トラック $1 · センド 0 %"],
  [/^SECTION (\S+ \/ \S+)$/, "SECTION $1", "ABSCHNITT $1", "SECCIÓN $1", "SEZIONE $1", "段落 $1", "セクション $1"],
  [/^REPEAT (\S+ \/ \S+)$/, "RÉPÉTITION $1", "WIEDERHOLUNG $1", "REPETICIÓN $1", "RIPETIZIONE $1", "重复 $1", "リピート $1"],
  [/^SEND TO USR(\d)$/, "ENVOYER AU FM-1", "AN DEN FM-1 SENDEN", "ENVIAR AL FM-1", "INVIA ALL'FM-1", "发送到 FM-1", "FM-1 に送信"],
  [/^ONE ZONE PER FILE, PLAYED FROM ITS ROOT NOTE · (\d+) FILES AT MOST$/, "UNE ZONE PAR FICHIER, JOUÉE DEPUIS SA NOTE DE BASE · $1 FICHIERS AU PLUS",
    "EINE ZONE PRO DATEI, AB IHRER GRUNDNOTE GESPIELT · HÖCHSTENS $1 DATEIEN", "UNA ZONA POR ARCHIVO, TOCADA DESDE SU NOTA RAÍZ · $1 ARCHIVOS COMO MÁXIMO",
    "UNA ZONA PER FILE, SUONATA DALLA SUA NOTA BASE · AL MASSIMO $1 FILE", "每个文件一个区域，从其根音演奏 · 最多 $1 个文件", "1 ファイル 1 ゾーン、ルート音から再生 · 最大 $1 ファイル"],
  [/^TOTAL (.+)$/, "TOTAL $1", "GESAMT $1", "TOTAL $1", "TOTALE $1", "总计 $1", "合計 $1"],
  [/^PROJECT ([A-D])$/, "PROJET $1", "PROJEKT $1", "PROYECTO $1", "PROGETTO $1", "项目 $1", "プロジェクト $1"],
  [/^USER SOUNDS (\d+–\d+)$/, "SONS UTILISATEUR $1", "EIGENE SOUNDS $1", "SONIDOS DEL USUARIO $1", "SUONI UTENTE $1", "用户音色 $1", "ユーザーサウンド $1"],
  [/^SAMPLE USR(\d)$/, "SAMPLE, EMPL. $1", "SAMPLE, PLATZ $1", "MUESTRA, RANURA $1", "CAMPIONE, SLOT $1", "采样，槽位 $1", "サンプル スロット$1"],
  [/^(.*) · (\d+) ZONES?$/, "$1 · $2 ZONE(S)", "$1 · $2 ZONE(N)", "$1 · $2 ZONA(S)", "$1 · $2 ZONA/E", "$1 · $2 个区域", "$1 · $2 ゾーン"],
  [/^(.* KiB)( · TOO LONG FOR THE SLOT)?( · TWO FILES ON ONE ROOT NOTE)?$/, null],   // (handled below: two optional warnings)
];
const I18N_WARN = { " · TOO LONG FOR THE SLOT": [" · TROP LONG POUR L'EMPLACEMENT", " · ZU LANG FÜR DEN PLATZ", " · DEMASIADO LARGO PARA LA RANURA", " · TROPPO LUNGO PER LO SLOT", " · 超出槽位容量", " · スロットに対して長すぎます"],
  " · TWO FILES ON ONE ROOT NOTE": [" · DEUX FICHIERS SUR UNE MÊME NOTE", " · ZWEI DATEIEN AUF EINER GRUNDNOTE", " · DOS ARCHIVOS EN UNA MISMA NOTA", " · DUE FILE SULLA STESSA NOTA", " · 两个文件使用同一根音", " · 2 つのファイルが同じルート音"] };
const I18N_TITLES = { "FULL SCREEN": ["PLEIN ÉCRAN", "VOLLBILD", "PANTALLA COMPLETA", "SCHERMO INTERO", "全屏", "全画面"],
  "HELP": ["AIDE", "HILFE", "AYUDA", "AIUTO", "帮助", "ヘルプ"], "TOOLTIPS": ["INFOBULLES", "TOOLTIPS", "AYUDAS EMERGENTES", "SUGGERIMENTI", "提示", "ツールチップ"],
  "LIT / FLAT": ["ÉCLAIRÉ / UNI", "LEUCHTEND / FLACH", "ILUMINADO / PLANO", "ILLUMINATO / PIATTO", "发光 / 平面", "発光 / フラット"] };

// the boxes' titles (only there: CHORUS, FILTER... stay English as knobs' names): Marc, 10/11
const I18N_SEC = {
  "OSCILLATOR A": ["OSCILLATEUR A", "OSZILLATOR A", "OSCILADOR A", "OSCILLATORE A", "振荡器 A", "オシレーター A"],
  "OSCILLATOR B": ["OSCILLATEUR B", "OSZILLATOR B", "OSCILADOR B", "OSCILLATORE B", "振荡器 B", "オシレーター B"],
  "MIXER": ["MÉLANGE", "MISCHER", "MEZCLA", "MIXER", "混音器", "ミキサー"],
  "GLIDE": ["PORTA.", "PORTA.", "PORTA.", "PORTA.", "滑音", "グライド"],
  "UNISON": ["UNISSON", "UNISONO", "UNÍSONO", "UNISONO", "齐奏", "ユニゾン"],
  "FILTER": ["FILTRE", "FILTER", "FILTRO", "FILTRO", "滤波器", "フィルター"],
  "FILTER ENVELOPE": ["ENVELOPPE DU FILTRE", "FILTERHÜLLKURVE", "ENVOLVENTE DEL FILTRO", "INVILUPPO DEL FILTRO", "滤波器包络", "フィルター EG"],
  "AMPLIFIER": ["AMPLIFICATEUR", "VERSTÄRKER", "AMPLIFICADOR", "AMPLIFICATORE", "放大器", "アンプ"],
  "EXTRAS": ["EXTRAS", "EXTRAS", "EXTRAS", "EXTRA", "附加", "追加"],
  "VOICE": ["VOIX", "STIMME", "VOZ", "VOCE", "声部", "ボイス"],
  "SENDS": ["ENVOIS", "SENDS", "ENVÍOS", "MANDATE", "发送", "センド"],
  "ARPEGGIATOR": ["ARPÉGIATEUR", "ARPEGGIATOR", "ARPEGIADOR", "ARPEGGIATORE", "琶音器", "アルペジエーター"],
  "SCALE": ["GAMME", "TONLEITER", "ESCALA", "SCALA", "音阶", "スケール"],
  "CHORD": ["ACCORDS", "AKKORDE", "ACORDES", "ACCORDI", "和弦", "コード"],
  "INSERT": ["INSERTION", "INSERT", "INSERCIÓN", "INSERT", "插入效果", "インサート"],
  "SLICER": ["DÉCOUPEUR", "SLICER", "TROCEADOR", "SLICER", "切片器", "スライサー"],
  "DELAY": ["ÉCHO", "DELAY", "RETARDO", "DELAY", "延迟", "ディレイ"],
  "REVERB": ["RÉVERBÉRATION", "HALL", "REVERBERACIÓN", "RIVERBERO", "混响", "リバーブ"],
  "MASTER": ["GÉNÉRAL", "MASTER", "GENERAL", "GENERALE", "总输出", "マスター"],
  "MOD MATRIX": ["MATRICE DE MODULATION", "MODULATIONSMATRIX", "MATRIZ DE MODULACIÓN", "MATRICE DI MODULAZIONE", "调制矩阵", "モジュレーション・マトリクス"],
  "ENVELOPE": ["ENVELOPPE", "HÜLLKURVE", "ENVOLVENTE", "INVILUPPO", "包络", "エンベロープ"],
};
// Japanese, Chinese: the kana and punctuation set proportionally (palt), the nearest to a condensed face (Marc, 10/11)
document.documentElement.lang = lang;
document.head.insertAdjacentHTML("beforeend", "<style>html[lang=ja] body, html[lang=zh] body { font-feature-settings: 'palt' 1; } html[lang=ja] .chip, html[lang=ja] .btn, html[lang=ja] .tab { letter-spacing: -0.06em; }</style>");
const I18N_LI = ["fr", "de", "es", "it", "zh", "ja"].indexOf(lang);   // (-1: English, nothing translated)
const I18N_ALL = {}, I18N_PAGE = {};
for (const e of I18N_WORDS) {
  const [pg, w] = e[0][0] === "@" ? [e[0].slice(1), e.slice(1)] : [null, e];
  if (pg) (I18N_PAGE[pg] = I18N_PAGE[pg] || {})[w[0]] = w.slice(1); else I18N_ALL[w[0]] = w.slice(1);
}
const I18N_REV = new Set();                               // (the translations: never translated again)
function i18nText(en, page) {
  if (I18N_LI < 0) return null;
  const p = I18N_PAGE[page] && I18N_PAGE[page][en];
  if (p) return p[I18N_LI];
  if (I18N_ALL[en]) return I18N_ALL[en][I18N_LI];
  for (const r of I18N_RE) {
    const m = r[0].exec(en);
    if (!m) continue;
    if (!r[1]) {                                         // a size and its warnings (SAMPLES)
      if (!m[2] && !m[3]) return null;
      return m[1] + (m[2] ? I18N_WARN[m[2]][I18N_LI] : "") + (m[3] ? I18N_WARN[m[3]][I18N_LI] : "");
    }
    return r[1 + I18N_LI].replace(/\$(\d)/g, (_, k) => m[+k]);
  }
  return null;
}
const i18nEn = new WeakMap();                             // text node -> its English
function i18nNode(n) {
  const v = n.nodeValue, t = v.trim();
  if (!t || I18N_REV.has(t)) return;
  const page = n.parentElement && n.parentElement.closest("[data-page]") ? n.parentElement.closest("[data-page]").dataset.page : "";
  const pe = n.parentElement;
  if (pe && pe.matches(".v") && /^(?:[LR] \d+|C)$/.test(t)) {   // a pan value: left / centre / right letters of the language
    const P = [["G", "C", "D"], ["L", "M", "R"], ["I", "C", "D"], ["S", "C", "D"], ["L", "C", "R"], ["L", "C", "R"]][I18N_LI];
    const tr = t === "C" ? P[1] : (t[0] === "L" ? P[0] : P[2]) + t.slice(1);
    if (tr !== t) { i18nEn.set(n, t); n.nodeValue = v.replace(t, tr); }
    return;
  }
  const lab = typeof LABELS !== "undefined" && LABELS[page] && LABELS[page][t];   // (an FM-1 word that is not technical: translated)
  const tr = pe && pe.matches(".ttl, .pt") && I18N_SEC[t] ? I18N_SEC[t][I18N_LI]
    : lab && !(pe && pe.closest("#tabs, #list, #userlist, #autolist, #actlist")) ? lab[I18N_LI] : i18nText(t, page);
  if (tr == null) return;
  i18nEn.set(n, t); I18N_REV.add(tr);
  n.nodeValue = v.replace(t, tr);
  i18nFitSoon();                                     // (a text changed: the buttons fitted again)
}
function i18nBroken(root) {                               // a label on two lines (INITIAL<br>AMOUNT): read and translated whole
  if (!root.querySelectorAll || typeof LABELS === "undefined") return;
  for (const e of [root, ...root.querySelectorAll(".gt, .tl, .sl")]) {
    if (!e.matches || !e.matches(".gt, .tl, .sl") || !e.querySelector("br") || e.dataset.en) continue;
    const en = [...e.childNodes].filter((c) => c.nodeType === 3).map((c) => c.nodeValue.trim()).join(" ");
    const pg = e.closest("[data-page]"), lab = pg && LABELS[pg.dataset.page] && LABELS[pg.dataset.page][en];
    if (!lab) continue;
    e.dataset.en = en; e.textContent = lab[I18N_LI];
    i18nEn.set(e.firstChild, en); I18N_REV.add(lab[I18N_LI]);
  }
}
function i18nTree(root) {
  if (I18N_LI < 0) return;
  if (root.nodeType === 3) return i18nNode(root);
  i18nBroken(root);
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let n; while ((n = w.nextNode())) i18nNode(n);
  if (root.querySelectorAll) for (const e of root.querySelectorAll("[placeholder]")) { const tr = i18nText(e.getAttribute("placeholder"), ""); if (tr) e.setAttribute("placeholder", tr); }
}
function i18nTitles() {
  for (const e of document.querySelectorAll("[title]")) {
    const en = e.dataset.titleEn || e.title; e.dataset.titleEn = en;
    e.removeAttribute("title");                            // (the tooltips show it: no browser one on top)
    e.dataset.tipT = I18N_LI >= 0 && I18N_TITLES[en] ? I18N_TITLES[en][I18N_LI] : en;
  }
}

/* --------------------------------------------------------------------------------------- the tooltips --- */
const TIP_PAGE = { sound: "sound", seq: "seq", song: "song", arp: "arp", fx: "fx", mod: "mod", tracks: "tracks", projects: "projects",
  samples: "samples", backup: "backup", settings: "settings" };
let tipsOn = (() => { try { return localStorage.getItem("guru600-tips") !== "off"; } catch (e) { return true; } })();
const tipEl = document.createElement("div"); tipEl.id = "tip"; document.body.appendChild(tipEl);
document.head.insertAdjacentHTML("beforeend", "<style>" +
  "#tip { position: fixed; z-index: 1000; max-width: 330px; padding: 9px 12px 10px; background: #0d0d0d; border: 1.5px solid #8f8b80; border-radius: 6px;" +
  " box-shadow: 0 4px 16px rgba(0,0,0,.7); color: #EDEBE6; font: 500 15px/1.35 'Barlow C', sans-serif; text-transform: none; letter-spacing: 0; pointer-events: none; opacity: 0; transition: opacity .12s; }" +
  "#tip.on { opacity: 1; } #tip b { display: block; font-weight: 700; font-size: 17px; margin-bottom: 3px; color: #fff; } #tip b:only-child { margin: 0; }" +
  ".tp#t-tips { --c: var(--cream); } .tp#t-tips svg { fill: none; stroke: color-mix(in srgb, var(--c) 55%, #2a2a2a); }" +
  // (on: as the bulb beside it: the button stays dark, only its bubble glows, white, the i hollow)
  ".tp#t-tips.on { border-color: color-mix(in srgb, var(--cream) 30%, #333) !important; background: linear-gradient(color-mix(in srgb, var(--cream) 10%, #262626), #0b0b0b) !important;" +
  " box-shadow: inset 0 1px 0 rgba(255,255,255,.14), inset 0 -2px 3px rgba(0,0,0,.6), 0 2px 3px rgba(0,0,0,.7) !important; }" +
  ".tp#t-tips.on svg { stroke: #fffdf4; fill: #fbf7ea; filter: drop-shadow(0 0 3px rgba(255,252,240,.9)) drop-shadow(0 0 7px rgba(255,252,240,.5)); }" +
  ".tp#t-tips.on svg .i { stroke: #262626; }" +
  "body.flat .tp#t-tips.on svg { filter: none; } #t-tips { margin: 0; width: 40px; height: 40px; flex: none; }</style>");
function tipSummary(s, name) {                            // the description's first sentence (CJK: up to 。), two when it is short
  const pre = /^([A-Z0-9][A-Z0-9 >+\-·]*?)\s?[:：]\s*/.exec(s);       // (the notice's rows begin with the control's name:
  if (pre && name && pre[1].trim() === name.toUpperCase()) s = s.slice(pre[0].length);   //  only that one is taken off)
  s = s.charAt(0).toUpperCase() + s.slice(1);
  s = s.replace(/ \? (?=[a-zà-ÿ'’])/g, " " + ({ fr: "« ? »", de: "„?“", es: "«?»", it: "«?»" }[lang] || "“?”") + " ");   // (the ? button
                                                                     //  named in a sentence: not its end)
  const sent = s.match(/.+?(?:[.!?](?=\s+[A-ZÀ-ÖØ-Þ0-9"(<]|$)|[。！？])\s*|.+$/g) || [s];   // (a sentence ends before a capital)
  let t = sent[0].trim();
  if (t.length < 70 && sent[1]) t += " " + sent[1].trim();
  if (t.length > 190) t = t.slice(0, 180).replace(/[\s,;:]+\S*$/, "") + "…";
  return t;
}
// the description names the FM-1's words (the guide's, in English): the ones shown translated on this page are given as
// shown, so the text speaks of what is on the screen (Marc, 10/11: VOYANTS INVERSÉ, not LEDS INV)
const tipLocalCache = {};
function tipLocal(s, page) {
  if (I18N_LI < 0 || !s) return s;
  let L = tipLocalCache[page];
  if (!L) {
    const m = {};
    const add = (en, tr) => { if (tr && tr !== en && /^[A-Z0-9][A-Z0-9 .#+\-/>]*$/.test(en) && en.length > 1) m[en] = tr; };
    for (const en in I18N_ALL) add(en, I18N_ALL[en][I18N_LI]);
    const lb = typeof LABELS !== "undefined" && LABELS[page]; if (lb) for (const en in lb) add(en, lb[en][I18N_LI]);
    const pg = I18N_PAGE[page] || {}; for (const en in pg) add(en, pg[en][I18N_LI]);   // (the page's own last: they win)
    const keys = Object.keys(m).sort((a, b) => b.length - a.length);
    L = tipLocalCache[page] = keys.length ? { m, re: new RegExp("(?<![A-Za-zÀ-ÿ0-9])(" + keys.map((k) => k.replace(/[.*+?^${}()|[\]\\/-]/g, "\\$&")).join("|") + ")(?![A-Za-zÀ-ÿ0-9])", "g") } : { m, re: null };
  }
  return L.re ? s.replace(L.re, (k) => L.m[k]) : s;
}
function tipFind(page, word, sec) {                       // the guide's row for this word on this page, in this box
  const rows = (typeof TIPS !== "undefined" && TIPS[TIP_PAGE[page] || page]) || [];
  const S = (sec || "").toUpperCase(), W = word.toUpperCase();
  const cands = rows.filter((r) => { const n = r.n.toUpperCase();
    return n === W || n === S + " · " + W || n.startsWith(W + " (") || n.split(/\s*,\s*/).includes(W) ||
      (/ … /.test(n) && new RegExp("^" + n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\S+ … \S+/, ".+") + "$").test(W)); });
  if (!cands.length) return null;
  return cands.find((r) => r.n.toUpperCase() === S + " · " + W) || cands.find((r) => S && r.s.toUpperCase().includes(S)) || cands[0];
}
function tipLabel(t) {                                    // the label an element stands for: itself, or its knob's, its row's...
  const own = (e) => { const en = [...e.childNodes].filter((c) => c.nodeType === 3).map((c) => i18nEn.get(c) || c.nodeValue).join("").trim(); return en; };
  const item = t.closest(".item, .sk, .pan, .setr, .mxk, .wheel");
  if (item) { const l = item.querySelector(".tl, .nm, .gt"); if (l && own(l)) return [l, own(l)]; }
  for (let e = t; e && e !== document.body; e = e.parentElement) {
    if (e.matches(".tl, .gt, .ttl, .nm, .sl, .pt, .btn, .ch, .tab, .bkgt, .fxlab, .fxhint, .sethint, .hint, .chip, .field, #detlabels > div") && own(e)) return [e, own(e)];
    if (e.matches(".sec, #stage")) break;
  }
  return null;
}
let tipTimer = 0, tipFor = null, tipX = 0, tipY = 0;   // (tipX, tipY: the pointer)
function tipShow(ev) {
  if (!tipsOn) return;
  const t = ev.target instanceof Element ? ev.target : null; if (!t) return;
  const ttl = t.closest("[data-tip-t]");
  let html = "";
  if (ttl) html = `<b>${ttl.dataset.tipT}</b>`;
  else {
    const lab = tipLabel(t); if (!lab) return tipHide();
    const [el, en] = lab;
    if (el === tipFor) return;
    const pgEl = el.closest("[data-page]"), page = pgEl ? pgEl.dataset.page : "layout";
    const secEl = el.closest(".sec"), ttlEl = secEl && secEl.querySelector(":scope > .ttl");
    const sec = ttlEl ? [...ttlEl.childNodes].filter((c) => c.nodeType === 3).map((c) => i18nEn.get(c) || c.nodeValue).join("").trim() : "";
    const word = I18N_LI >= 0 && typeof GLOSS !== "undefined" && GLOSS[page] && GLOSS[page][en] ? GLOSS[page][en][["fr", "de", "es", "it", "zh", "ja"][I18N_LI]] : "";
    const shownTr = [...el.childNodes].some((c) => c.nodeType === 3 && i18nEn.has(c));   // (shown translated: SETTINGS)
    let row = tipFind(page, en, sec);
    const rowLab = el.matches(".ch, .btn.ch, .field") ? (el.closest(".setr") || el.closest(".grp.chg")) : null;   // a value: its row's text
    if (!row && rowLab) { const l = rowLab.querySelector(".nm, .gt"); if (l) row = tipFind(page, [...l.childNodes].filter((c) => c.nodeType === 3).map((c) => i18nEn.get(c) || c.nodeValue).join("").trim(), sec); }
    const desc = row ? tipLocal(tipSummary(row.d[lang] || row.d.en, row.n), page) : "";
    const shown = [...el.childNodes].filter((c) => c.nodeType === 3).map((c) => c.nodeValue).join("").trim();
    const head = shownTr && shown && shown !== en ? `${shown} (${en})`        // (Marc, 10/11: the word shown first, the FM-1's after:
      : word && word.toUpperCase() !== en.toUpperCase() ? `${word} (${en})` : word;   //  RÉPÉTITION (RATCH), Fréquence de coupure (CUTOFF))
    if (!head && !desc) return tipHide();
    html = (head ? `<b>${head}</b>` : "") + (desc ? `<span>${desc}</span>` : "");
    tipFor = el;
  }
  clearTimeout(tipTimer);
  tipTimer = setTimeout(() => {                         // (beside the pointer, never under it: below right, or flipped at an edge)
    tipEl.innerHTML = html;
    const w = tipEl.offsetWidth, hh = tipEl.offsetHeight;
    let x = tipX + 18, y = tipY + 24;
    if (x + w > innerWidth - 8) x = tipX - w - 14;
    if (y + hh > innerHeight - 8) y = tipY - hh - 14;
    tipEl.style.left = Math.max(8, x) + "px"; tipEl.style.top = Math.max(8, y) + "px"; tipEl.classList.add("on");
  }, 380);
}
document.addEventListener("pointermove", (ev) => { tipX = ev.clientX; tipY = ev.clientY; }, { passive: true });
function tipHide() { clearTimeout(tipTimer); tipEl.classList.remove("on"); tipFor = null; }
document.addEventListener("pointerover", tipShow);
document.addEventListener("pointerdown", tipHide, true);
document.addEventListener("pointerleave", tipHide);
document.addEventListener("pointerout", (ev) => { if (!ev.relatedTarget) tipHide(); });

/* ------------------------------------------- the speech-bubble button (left of the bulb), the LANGUAGE row --- */
(function () {
  const glow = document.getElementById("t-glow"); if (!glow) return;
  const b = document.createElement("div"); b.className = "tp" + (tipsOn ? " on" : ""); b.id = "t-tips"; b.title = "TOOLTIPS";
  b.innerHTML = `<svg viewBox="0 0 20 20"><path d="M3.5 4.5h13a1 1 0 0 1 1 1v7.5a1 1 0 0 1-1 1H9l-3.6 3v-3H3.5a1 1 0 0 1-1-1V5.5a1 1 0 0 1 1-1Z" stroke-width="1.6"/>` +
    `<path class="i" d="M10 7.2v.1M10 9.3v3" stroke-width="1.8" stroke-linecap="round"/></svg>`;
  glow.parentNode.insertBefore(b, glow);
  b.addEventListener("click", () => {
    tipsOn = !tipsOn; b.classList.toggle("on", tipsOn); tipHide();
    try { localStorage.setItem("guru600-tips", tipsOn ? "on" : "off"); } catch (e) {}
  });
})();

/* ------------------------------------------------- a translation longer than the English: abbreviated, never shrunk --- */
// (Marc, 10/11: the sizes stay as they are; a translation that does not fit is abbreviated in the lists above. ?checkfit:
// the texts that overflow their button or box are marked data-over, to find them: guide/check_fit.py)
document.head.insertAdjacentHTML("beforeend", "<style>.tab, .btn, .bkgt, .gt, .ttl, .pt, .chip { white-space: nowrap; }</style>");
const I18N_CHECK = new URLSearchParams(location.search).has("checkfit");
function i18nFit() {
  if (!I18N_CHECK) return;
  for (const e of document.querySelectorAll(".tab, .btn, .gt, .tl, .pt, .ttl, .nm, .chip")) {
    if (!e.offsetParent || !e.clientWidth) continue;
    const box = e.closest(".sec") || e.parentElement, r = e.getBoundingClientRect(), b = box.getBoundingClientRect();
    if (e.scrollWidth > e.clientWidth + 1 || (e.matches(".pt, .tl, .gt, .nm") && (r.left < b.left - 1 || r.right > b.right + 1))) e.dataset.over = "1";
  }
}
let i18nFitTimer = 0;
const i18nFitSoon = () => { clearTimeout(i18nFitTimer); i18nFitTimer = setTimeout(i18nFit, 60); };

/* --------------------------------------------------------- now, and whatever the pages write afterwards --- */
i18nTree(document.body); i18nTitles(); i18nFitSoon();
if (document.fonts) document.fonts.ready.then(i18nFitSoon);           // (measured with the panel's font, not a fallback)
addEventListener("load", i18nFitSoon);
document.querySelectorAll(".tab").forEach((t) => t.addEventListener("pointerdown", i18nFitSoon));   // (a page shown: its buttons fitted)
if (I18N_LI >= 0) new MutationObserver((ms) => {
  for (const m of ms) {
    if (m.type === "characterData") i18nNode(m.target);
    else for (const n of m.addedNodes) i18nTree(n);
  }
}).observe(document.body, { childList: true, characterData: true, subtree: true });

/* ------------------------------------------------ the notes' names in solfège, under the English letter (Marc, 10/11) --- */
// French, Spanish and Italian name the notes do, ré, mi: the letter stays (as on the FM-1), the solfège name shows under it
// or beside it, wherever a note is named: ARP's ROOT keys and KEY panel, the SEQUENCER's roll, the SAMPLES' zones.
const SOLF = { fr: ["DO", "DO#", "RÉ", "RÉ#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"],
  es: ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"],
  it: ["DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"] }[lang];
const SOLF_N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const solf = (nm) => { const m = /^([A-G]#?)(-?\d+)?$/.exec(nm || ""); return m && SOLF ? SOLF[SOLF_N.indexOf(m[1])] + (m[2] || "") : ""; };
if (SOLF) {
  document.head.insertAdjacentHTML("beforeend", "<style>" +
    ".chg.root .btn.ch { flex-direction: column; gap: 3px; }" +
    ".solf { display: block; font: inherit; opacity: .7; }" +
    ".ky i.solf { position: absolute; left: 7px; top: 50%; transform: translateY(-50%); font: 600 15px/1 'Barlow C'; font-style: normal; color: #000; }" +
    ".ky.b:not(.on) i.solf { color: #fff; }" +
    "#rollkeys { width: 112px; padding-left: 68px; }" +
    ".rk[data-s]::before { content: attr(data-s); position: absolute; right: calc(100% + 38px); top: 50%; transform: translateY(-50%); font: 600 15px/1 'Barlow C'; color: var(--cream); opacity: .7; white-space: nowrap; }" +
    "</style>");
  for (const b of document.querySelectorAll(".chg.root .btn.ch")) { const s = solf(b.textContent.trim()); if (s) b.insertAdjacentHTML("beforeend", `<span class="solf">${s}</span>`); }
  const drawKey0 = drawKey;
  drawKey = function () {
    drawKey0();
    keyV.querySelectorAll(".ky").forEach((k) => { const s = solf(k.textContent.trim()); if (s) k.insertAdjacentHTML("beforeend", `<i class="solf">${s}</i>`); });
    const kn = document.getElementById("keyname"), m = /^(\S+) /.exec(kn.textContent); if (m && solf(m[1])) kn.textContent = kn.textContent.replace(m[1], `${m[1]} (${solf(m[1])})`);
  };
  const drawRoll0 = drawRollFrame;
  drawRollFrame = function () { drawRoll0(); for (const k of rollKeys.children) if (k.dataset.c) k.dataset.s = solf(k.dataset.c); };   // (« C4  DO4 – », the column wider)
  // SAMPLES: each file's root note (the field keeps the letter: it is typed so) and its keys, the solfège beside them
  document.head.insertAdjacentHTML("beforeend", "<style>.frow { grid-template-columns: 1fr 58px 44px 150px 52px 30px 30px; } .frow .fs, .frow .fk i { opacity: .7; font-style: normal; }</style>");
  const solfZones = (root) => { for (const r of root.querySelectorAll ? root.querySelectorAll(".frow") : []) {
    if (r.querySelector(".fs")) continue;
    const inp = r.querySelector(".froot"), fk = r.querySelector(".fk"); if (!inp || !fk) continue;
    inp.insertAdjacentHTML("afterend", `<div class="fs">${solf(inp.value.toUpperCase())}</div>`);
    fk.innerHTML = fk.textContent + " <i>" + fk.textContent.split("–").map(solf).join("–") + "</i>";
    inp.addEventListener("input", () => { r.querySelector(".fs").textContent = solf(inp.value.trim().toUpperCase()); });
  } };
  new MutationObserver((ms) => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1) solfZones(n.parentElement || n); })
    .observe(document.body, { childList: true, subtree: true });
  if (page === "arp") drawKey();
  if (rollKeys.children.length) drawRollFrame();
}
