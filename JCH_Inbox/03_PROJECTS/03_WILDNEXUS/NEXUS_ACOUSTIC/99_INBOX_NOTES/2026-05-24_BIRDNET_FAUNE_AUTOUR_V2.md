# BIRDNET / FAUNE AUTOUR V2

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-05-24 20:43

�%�%�BIRDNET / FAUNE AUTOUR V2

IP du RPi : 192.168.1.48
connexion : ssh jchavaux@192.168.1.48

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILv07xvUqBwxNgRItmby/BnK/3aHblAVza9rbAphYcPt jchavaux

Accès interface :   http://100.84.45.93  ATTENTION TAILSCALE ACTIF



BIRDNET-PI Si jamais tu vois à nouveau "Database is busy" ou que l'interface Safari ne répond pas, ouvre ton Terminal sur Mac et lance
  cette commande magique :

 ssh jchavaux@100.84.45.93 "/home/jchavaux/BirdNET-Pi/scripts/birdnet_check.sh --repair"

  Ce que fait cet outil en 5 secondes :
   1. Il vérifie l'espace disque.
   2. Il redémarre les services BirdNET (analysis, stats, recording, chart_viewer) pour purger les processus fantômes.
   3. Il force l'optimisation de la base de données (VACUUM).
   4. Il s'assure que le mode WAL (concurrence accélérée) est actif.

Xeno-canto
f174275c7e3d21af9b305102d0a1512f0f93f518
(
�
(
(
((
)Q (
�	R(
�	(
�	(
�	(	
�	(

�	 (
�	(
�	 (
�(
� (
� (
�	 (
�	 (
�	 (
�	 (
�	 (
�	 (
�	 (
�	 (
�	 (
�	 (
�� (
* (
+Y(
�S (
�T(
�	( 
�	!(!
�	"("
�	#(#
�	$($
�	%(%
�	&(&
�	'('
�	(((
�	)()
�	*(*
�	+(+
�	,(,
�	-(-
�	.(.
�	/(/
�	0(0
�	1(1
�	2(2
�	3(3
�	4(4
�	5(5
�	6(6
�	7(7
�	8(8
�	A (9
�	(:
�	E (;
�	D (<
�	C (=
�	B (>
�	(?
�	F(@
�
U (A
�
U (B
�
U (C
�	G (D
�
)U (E
�
V(F
�L(G
�
(H
�
�L(I
�(J
�P (K
�O (L
�N (M
�M (N
��(O
�(P
�X(Q
�(W(R
��������"

`L�NL���ї{�Y*J}jh���No�]d�jh����*J}jh���No�]d�jh����*J}jh���No�]d�jh����*J}jh���No�]d�jh����*J}jh���No�]d�jhߖ��*J}jh���No�]d�jh����*J}jh���No�]d�jh���*J}jh���No�]d�jh���*J}jh���No�]d�jh���*J}jh���No�]d�jh���*J:��xT�E!�wy��ph�h���* J�|y@�hD��C<Hh���* J�|y@�hD��C<Hh����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����*:Jp��R7LԆ@�����Jmailto:jchavaux@192.168.1.48h����*:Jp��R7LԆ@�����Jmailto:jchavaux@192.168.1.48h����*:Jp��R7LԆ@�����Jmailto:jchavaux@192.168.1.48h����*:Jp��R7LԆ@�����Jmailto:jchavaux@192.168.1.48h����*:Jp��R7LԆ@�����Jmailto:jchavaux@192.168.1.48h����*:Jp��R7LԆ@�����Jmailto:jchavaux@192.168.1.48h����*Jp��R7LԆ@�����h����*Jp��R7LԆ@�����h����* YJ��<�Dx�)��)�mh���*J��<�Dx�)��)�m*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*1J�b�d��@Ϩu�GTJhttp://100.84.45.93h����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�b�d��@Ϩu�GTh����*J�ͽ�=B(��B5A4�h����*J�ͽ�=B(��B5A4�h����*J�ͽ�=B(��B5A4�h����*J�ͽ�=B(��B5A4�h����*J�ͽ�=B(��B5A4�h����*�J�ͽ�=B(��B5A4�h����*!�J�ͽ�=B(��B5A4�h����* J�ͽ�=B(��B5A4�h����*JEh��<;MR����_ە9h����*JEh��<;MR����_ە9(h����*(JEh��<;MR����_ە9h����
