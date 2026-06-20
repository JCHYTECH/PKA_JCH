# Pour utiliser votre clé API NVIDIA gratuitement dans VS Code, la méthode…

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-06-03 08:50

�!� �Pour utiliser votre clé API NVIDIA gratuitement dans VS Code, la méthode la plus simple et la plus puissante consiste à l'intégrer dans une extension d'assistant de code comme Continue ou Cline.
Voici comment configurer l'extension gratuite Continue (l'alternative open-source la plus populaire) :
Étape 1 : Installer l'extension

Ouvrez VS Code.
Cliquez sur l'icône Extensions dans la barre latérale gauche (ou faites Ctrl+Shift+X / Cmd+Shift+X).
Cherchez Continue et cliquez sur Installer.
Étape 2 : Configurer la clé API NVIDIA
Une fois installée, l'extension ajoute une nouvelle icône Continue dans votre barre latérale.

Cliquez sur l'icône de Continue.
Cliquez sur l'icône d'engrenage (Settings) en bas à droite du panneau Continue. Cela ouvre un fichier de configuration nommé config.json.
Remplacez le contenu ou ajoutez NVIDIA dans la section models. L'API NVIDIA étant compatible avec le format OpenAI, copiez-collez ce bloc :
{
  "models": [
    {
      "title": "NVIDIA Llama 3",
      "provider": "openai",
      "model": "meta/llama3-70b-instruct",
      "apiKey": "VOTRE_CLE_API_NVIDIA_ICI",
      "apiBase": "https://nvidia.com"
    }
  ]
}
(Remplacez meta/llama3-70b-instruct par le nom exact du modèle choisi sur le site NVIDIA build si vous préférez un autre modèle comme DeepSeek ou Nemotron, et collez votre clé).
Étape 3 : Utiliser le LLM

Enregistrez le fichier config.json (Ctrl+S).
Sélectionnez NVIDIA Llama 3 dans le menu déroulant des modèles en bas de l'extension.
Vous pouvez maintenant :
Poser des questions dans le chat de gauche.
Sélectionner du code dans votre éditeur et faire Ctrl+I (ou Cmd+I) pour demander des modifications ou générer du code directement.

Pourriez-vous me dire quel modèle spécifique vous avez choisi sur le catalogue NVIDIA, ou souhaitez-vous des exemples de code pour utiliser cette clé directement dans un script Python / JavaScript au lieu d'une extension ?




(
5(
5�(
�!(
�	 (
�(
�	 (
�e(
�	 (	
��(

�	 (
�!(
�	 (
��(
�	 (
��(
��(
�	(
�	�(
�
(
�
	 (
�
-(
�	 (
�V(
�	 (
�(
�	 (
�,(
�	 (
�1(
�R(
�	 ( 
�(!
��("
��������"

`L�NL���ї{�
*5J��&�NJT�^��2�*J��&�NJT�^��2�(*J��&�NJT�^��2�*�J��&�NJT�^��2�(*0J��&�NJT�^��2�*J�M��eCF���s�7�(*1J�M��eCF���s�7�* J�pQ�e�D�*b4��(*J��U�J����T*fJg\���Ox���3�T*fJn�yԽCMf�����]�U*
fJn�yԽCMf�����]�U(*GfJn�yԽCMf�����]�U*	fJ��;~gH����E��%5*fJ��;~gH����E��%5(*fJ��;~gH����E��%5*	fJ��;~gH����E��%5(*fJ��;~gH����E��%5*'J�G��@TC���'Uz�(*_J~xK0��I��H��Dxg2*fJ����^NҤ`��Ғ5V*fJ����^NҤ`��Ғ5V(*fJ����^NҤ`��Ғ5V*fJ�ױ^@���|S*fJ�ױ^@���|S(*`fJ�ױ^@���|S*�fJ�����=B�;r``���*�J͏��K��}�@<Q}*&J�ҩ��N;�<�����*J͏��K��}�@<Q}* J�mt�CA�,�gVi�|*J͏��K��}�@<Q}*J�벑��H/��Qi�"�(*OJ�벑��H/��Qi�"�3
*.AppleSystemUIFontMonospaced-RegularItalic@A(*�J�벑��H/��Qi�"�(*J�벑��H/��Qi�"�*Ji�gd�BÛ�TQt��u(*J#��FwM(��3̈́�;*-fJ.VQ��D�b\�л�*fJ8��0O�� uo[v�*fJ8��0O�� uo[v�(*;fJ8��0O�� uo[v�*fJF��͘KG�{�%^w�*,d J��Ѕ~J̀iF���c*�d JH��ن�F衄��w��*fJ�CR��A��K��F*J��ZW'C�k�)��*J��ZW'C�k�)��(*�J��ZW'C�k�)��*J��ZW'C�k�)��(*J��ZW'C�k�)��
