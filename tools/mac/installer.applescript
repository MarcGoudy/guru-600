--  GURU-600  ·  INSTALLATION
--
--  ▶  Cliquez sur le triangle ▶, en haut de cette fenêtre.
--  ▶  Click the ▶ triangle, at the top of this window.
--     DE: oben auf ▶ klicken · ES: haga clic en ▶ · IT: fate clic su ▶ · 中文：点击 ▶ · 日本語：▶ をクリック
--
--  Le Guru-600 est gratuit et n'est pas signé par Apple : téléchargé par le navigateur, macOS
--  le bloquerait. Ce script le télécharge depuis guru-600.com, l'installe dans Applications
--  et l'ouvre. Rien d'autre : chaque ligne est lisible ci-dessous.
--  The Guru-600 is free and not signed by Apple. This script downloads it from guru-600.com,
--  installs it in Applications and opens it. Nothing else: every line is readable below.
--
-- ------------------------------------------------------------------------------------------

property appURL : "https://guru-600.com/telecharger/Guru-600-Mac.zip"

on run argv
	set lang to text 1 thru 2 of (user locale of (system info))
	if lang is "fr" then
		set t to {"Installer le Guru-600 ?" & return & return & "L'application va être téléchargée depuis guru-600.com, placée dans votre dossier Applications, puis ouverte.", "Annuler", "Installer", "Téléchargement impossible. Vérifiez votre connexion à Internet, puis recommencez.", "Le Guru-600 est installé dans Applications.", "OK", "Téléchargement…", "Installation…"}
	else if lang is "de" then
		set t to {"Guru-600 installieren?" & return & return & "Die App wird von guru-600.com geladen, in Ihren Ordner Programme gelegt und dann geöffnet.", "Abbrechen", "Installieren", "Download nicht möglich. Prüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.", "Der Guru-600 ist im Ordner Programme installiert.", "OK", "Download…", "Installation…"}
	else if lang is "es" then
		set t to {"¿Instalar el Guru-600?" & return & return & "La aplicación se descargará de guru-600.com, se colocará en su carpeta Aplicaciones y se abrirá.", "Cancelar", "Instalar", "No se pudo descargar. Compruebe su conexión a Internet e inténtelo de nuevo.", "El Guru-600 está instalado en Aplicaciones.", "OK", "Descargando…", "Instalando…"}
	else if lang is "it" then
		set t to {"Installare il Guru-600?" & return & return & "L'app verrà scaricata da guru-600.com, messa nella cartella Applicazioni e aperta.", "Annulla", "Installa", "Download non riuscito. Controllate la connessione a Internet e riprovate.", "Il Guru-600 è installato in Applicazioni.", "OK", "Download…", "Installazione…"}
	else if lang is "zh" then
		set t to {"安装 Guru-600？" & return & return & "将从 guru-600.com 下载此应用，放入“应用程序”文件夹并打开。", "取消", "安装", "无法下载。请检查网络连接后重试。", "Guru-600 已安装到“应用程序”。", "好", "正在下载…", "正在安装…"}
	else if lang is "ja" then
		set t to {"Guru-600 をインストールしますか？" & return & return & "guru-600.com からダウンロードし、「アプリケーション」フォルダに入れて開きます。", "キャンセル", "インストール", "ダウンロードできませんでした。インターネット接続を確認して、もう一度お試しください。", "Guru-600 を「アプリケーション」にインストールしました。", "OK", "ダウンロード中…", "インストール中…"}
	else
		set t to {"Install the Guru-600?" & return & return & "The app will be downloaded from guru-600.com, placed in your Applications folder, then opened.", "Cancel", "Install", "The download failed. Check your Internet connection and try again.", "The Guru-600 is installed in Applications.", "OK", "Downloading…", "Installing…"}
	end if

	-- the Guru-600's icon, in this installer's bundle (else macOS's own)
	try
		set ico to (item 1 of argv) as alias -- (the Guru-600's icon, given by the launcher)
	on error
		set ico to note
	end try

	-- (the Script Editor's window out of the way: only the Guru-600's own windows are seen)
	try
		tell application "Script Editor" to set miniaturized of every window to true
	end try
	display dialog (item 1 of t) buttons {item 2 of t, item 3 of t} default button 2 cancel button 1 with title "Guru-600" with icon ico

	set progress total steps to 3
	set progress description to "Guru-600"
	set progress additional description to (item 7 of t)
	set progress completed steps to 1

	set tmp to do shell script "mktemp -d /tmp/guru600.XXXXXX"
	try
		do shell script "curl -fsSL --retry 2 " & quoted form of appURL & " -o " & quoted form of (tmp & "/g.zip") & " && ditto -x -k " & quoted form of (tmp & "/g.zip") & " " & quoted form of tmp
	on error
		do shell script "rm -rf " & quoted form of tmp
		display dialog (item 4 of t) buttons {item 6 of t} default button 1 with title "Guru-600" with icon stop
		return
	end try

	set progress additional description to (item 8 of t)
	set progress completed steps to 2
	set src to quoted form of (tmp & "/Guru-600.app")
	set cmd to "pkill -f 'Guru-600.app/Contents/MacOS/' ; rm -rf /Applications/Guru-600.app && ditto " & src & " /Applications/Guru-600.app && xattr -dr com.apple.quarantine /Applications/Guru-600.app"
	try
		do shell script cmd
	on error
		-- (an account without the right to write in Applications: macOS asks for an administrator's password)
		do shell script cmd with administrator privileges
	end try
	do shell script "rm -rf " & quoted form of tmp
	set progress completed steps to 3

	do shell script "open /Applications/Guru-600.app"
	display dialog (item 5 of t) buttons {item 6 of t} default button 1 with title "Guru-600" with icon ico giving up after 8
	try
		tell application "Script Editor" to quit saving no
	end try
end run
