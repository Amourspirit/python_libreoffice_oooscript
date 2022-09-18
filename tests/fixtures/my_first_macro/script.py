import uno
def my_1st_macro():
    # Won't run directly in Anaconda, Geany, KDevelop, PyCharm or else
    doc = XSCRIPTCONTEXT.getDocument()
    doc.getText().setString("Hello World!")

g_exportedScripts = (my_1st_macro,)