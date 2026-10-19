from pathlib import Path
import win32com.client
O=Path(__file__).resolve().parent
a=win32com.client.DispatchEx('PowerPoint.Application');p=None
try:
 p=a.Presentations.Open(str(O/'NCKH_Ensemble_IDS_Creative_Final.pptx'),False,False,False)
 for s in p.Slides:s.SlideShowTransition.Hidden=False
 p.SlideShowSettings.RangeType=1
 p.SaveAs(str(O/'NCKH_Ensemble_IDS_Static.pdf'),32)
finally:
 if p is not None:p.Saved=True;p.Close()
 a.Quit()
