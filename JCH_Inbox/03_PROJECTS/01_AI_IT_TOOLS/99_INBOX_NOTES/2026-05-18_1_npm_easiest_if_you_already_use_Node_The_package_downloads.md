# # 1. npm — easiest if you already use Node. The package downloads…

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-05-18 09:43

� ��# 1. npm — easiest if you already use Node. The package downloads the
#    matching prebuilt Rust binaries from GitHub Releases.
npm install -g deepseek-tui

# 2. Cargo — no Node needed. Requires Rust 1.88+ (the crates use the
#    2024 edition; older toolchains fail with "feature `edition2024` is
#    required"). Run `rustup update` first, or use a non-Cargo path below.
cargo install deepseek-tui-cli --locked   # `deepseek` (entry point)
cargo install deepseek-tui     --locked   # `deepseek-tui` (TUI binary)

# 3. Homebrew — macOS package manager.
brew tap Hmbown/deepseek-tui
brew install deepseek-tui

# 4. Direct download — no package manager or toolchain.
#    https://github.com/Hmbown/DeepSeek-TUI/releases
#    Prebuilt for Linux x64/ARM64, macOS x64/ARM64, Windows x64.

# 5. Docker — prebuilt release image.
docker volume create deepseek-tui-home
docker run --rm -it \
  -e DEEPSEEK_API_KEY="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" \
  -v deepseek-tui-home:/home/deepseek/.deepseek \
  -v "$PWD:/workspace" \
  -w /workspace \
  ghcr.io/hmbown/deepseek-tui:latest




Les deux modèles sont confirmés sur NIM (vérifiés il y a 2 minutes via l'API).

────────────────────────────────────────────────────────────

Pour l'utiliser

Une fois le fichier sauvegardé, relance DeepSeek TUI. Tu devrais pouvoir basculer sur
deepseek-ai/deepseek-v4-pro (probablement via /model ou le sélecteur de modèles dans l'UI). Le
default_text_model actuel (deepseek-v4-pro) pointe vers l'API DeepSeek native — si tu veux que le
modèle NVIDIA devienne le défaut, il faudra le référencer en nvidia/deepseek-ai/deepseek-v4-pro ou
le format que DeepSeek TUI utilise pour les modèles de providers customs.

Tu veux que je t'aide à déterminer la syntaxe exacte de référencement ?

ok

thinking done · 10.8s
Full reasoning in Ctrl+O

Voici le bloc final prêt à coller, avec les deux modèles + le défaut mis à jour si tu veux que
NVIDIA soit ton moteur principal :

    default_text_model = "nvidia/deepseek-ai/deepseek-v4-pro"
    reasoning_effort = "auto"
    
    [projects."/Users/jchavauxm5/PKA_JCH"]
    trust_level = "trusted"
    
    [providers.nvidia]
    base_url = "https://integrate.api.nvidia.com/v1"
    api_key = "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"
    models = [
        "deepseek-ai/deepseek-v4-pro",
        "deepseek-ai/deepseek-v4-flash",
    ]

Une fois DeepSeek TUI relancé, /model te permettra de basculer entre les deux.

⚠️ Rappel sécurité : ta clé API est en clair dans ce chat. Fais-la tourner sur build.nvidia.com
(https://build.nvidia.com) après.comment on sauvegarde un fichier dans vscode je vois pas de save
(
�((
��(
�F(
�F (
�F (
��
 (
�$ (
�c(	
�"%(

�(
�&(
�'(
��(
�"((
�?(
��������":

`L�NL���ї{�)

��NSQ�O���!d[���)*�J.L[QsL
�K�gC�R*�J.L[QsL
�K�gC�R* FJ.L[QsL
�K�gC�Rh����*cJ.L[QsL
�K�gC�R*E"J.L[QsL
�K�gC�RJ)http://ghcr.io/hmbown/deepseek-tui:latest* J.L[QsL
�K�gC�Rh����*J/���bEВ���(�&h����*!�J�:a��A4��j�u�2h����*!J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����*J�:a��A4��j�u�2h����
