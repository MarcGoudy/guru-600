#!/bin/zsh
# Guru-600 Editor (16/11/2026, Marc): opens the editor kept INSIDE this application (Resources/editor), so it works
# without Internet and whatever the browser has kept or cleared, in a window of its own (--app: no address bar, no tabs).
# The browser: one with MIDI (Chromium's family), the default one if it is one, else the first one installed.
R=${0:A:h:h}/Resources
P="$R/editor/index.html"
B=$(osascript -l JavaScript - <<'JS'
ObjC.import("AppKit");
const ws = $.NSWorkspace.sharedWorkspace;
const ids = ["com.google.Chrome", "com.microsoft.edgemac", "ai.perplexity.comet", "com.brave.Browser", "com.operasoftware.Opera",
  "com.vivaldi.Vivaldi", "org.chromium.Chromium", "com.google.Chrome.beta", "com.microsoft.edgemac.beta", "com.google.Chrome.canary"];
let def = "";
try { const u = ws.URLForApplicationToOpenURL($.NSURL.URLWithString("https://guru-600.com")); def = ObjC.unwrap($.NSBundle.bundleWithURL(u).bundleIdentifier) || ""; } catch (e) {}
const has = (id) => !ws.URLForApplicationWithBundleIdentifier(id).isNil();
ids.includes(def) && has(def) ? def : (ids.find(has) || "");
JS
)
if [[ -z $B ]]; then
  case $(defaults read -g AppleLocale 2>/dev/null | cut -c1-2) in
    fr) M="L'éditeur Guru-600 a besoin d'un navigateur avec le MIDI : Chrome, Edge, Brave, Opera ou Comet. Installez-en un, puis rouvrez l'éditeur.";;
    de) M="Der Guru-600 Editor braucht einen Browser mit MIDI: Chrome, Edge, Brave, Opera oder Comet. Installieren Sie einen und öffnen Sie den Editor erneut.";;
    es) M="El editor Guru-600 necesita un navegador con MIDI: Chrome, Edge, Brave, Opera o Comet. Instale uno y vuelva a abrir el editor.";;
    it) M="L'editor Guru-600 ha bisogno di un browser con il MIDI: Chrome, Edge, Brave, Opera o Comet. Installatene uno, poi riaprite l'editor.";;
    zh) M="Guru-600 编辑器需要支持 MIDI 的浏览器：Chrome、Edge、Brave、Opera 或 Comet。请安装其中之一，然后重新打开编辑器。";;
    ja) M="Guru-600 エディターには MIDI 対応のブラウザーが必要です（Chrome、Edge、Brave、Opera、Comet）。いずれかをインストールして、エディターを開き直してください。";;
    *)  M="The Guru-600 editor needs a browser with MIDI: Chrome, Edge, Brave, Opera or Comet. Install one, then open the editor again.";;
  esac
  osascript -e 'on run a' -e 'display dialog (item 1 of a) buttons {"OK"} default button 1 with title "Guru-600 Editor" with icon caution' -e 'end run' "$M" >/dev/null
  exit 0
fi
U=$(osascript -l JavaScript -e 'function run(a) { return "file://" + encodeURI(a[0]); }' "$P")
open -nb "$B" --args --app="$U"
