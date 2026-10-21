"""Insère le bouton PDF Dushow dans la barre gauche du viewer Speckle.

Échoue volontairement (code 1) si l'ancre n'est plus trouvée dans le code amont,
pour que le build casse plutôt que de publier une image sans bouton.
"""
import pathlib
import sys

left = pathlib.Path(sys.argv[1]) / "components/viewer/controls/Left.vue"
src = left.read_text(encoding="utf-8")

anchor = '''        <ViewerControlsButtonToggle
          v-if="isIntercomEnabled"'''
if src.count(anchor) != 1:
    sys.exit("Ancre introuvable dans Left.vue : le code amont a changé, adapter le patch.")

left.write_text(src.replace(anchor, "        <DushowPdfButton />\n" + anchor), encoding="utf-8")
print("Bouton PDF inséré dans Left.vue")
