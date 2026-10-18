#!/usr/bin/env python3
"""Opt-in tab offset placement preserves local swing and performed bar clocks; defaults stay byte-identical."""
import copy,json,os,pathlib,shutil,subprocess,sys,tempfile,types,unittest,warnings
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[2] if pathlib.Path(__file__).parent.name=='tests' else pathlib.Path.home()/'.config/chirp'
TOOLS=ROOT/'tools';sys.path.insert(0,str(TOOLS));IMPL=pathlib.Path(os.environ.get('T2S_TEST_IMPL',str(TOOLS/'tab2song.py')))
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(TOOLS/'tab2song.py');exec(compile(path.read_text(),str(path),'exec'),m.__dict__);return m
T=load(IMPL,'tested_offset');B=os.environ.get('CHIRP_TEST') or os.environ.get('CHIRP') or shutil.which('chirp')
class Placement(unittest.TestCase):
 def setUp(self):
  warnings.simplefilter('ignore', ResourceWarning)
  self.tmp=tempfile.TemporaryDirectory(prefix='offset-placement-');self.addCleanup(self.tmp.cleanup);self.d=pathlib.Path(self.tmp.name);c=self.d/'cache';c.mkdir();self.cache=c
  (c/'songsterr-meta.json').write_text(json.dumps({'tracks':[{'name':'line'}]}));self.write_track([[5,4],[5,4]])
 def write_track(self,sigs,bpms=None):
  measures=[]
  for sig in sigs:
   beats=[{'duration':[1,8],'notes':[{'string':0,'fret':0}]},{'duration':[1,8],'notes':[{'string':0,'fret':2}]},{'duration':[1,4],'notes':[{'string':0,'fret':4}]},{'duration':[(Fraction(sig[0],sig[1])-Fraction(1,2)).numerator,(Fraction(sig[0],sig[1])-Fraction(1,2)).denominator],'rest':True,'notes':[{'rest':True}]}]
   measures.append({'signature':sig,'voices':[{'beats':beats}]})
  track={'name':'line','tuning':[60],'instrumentId':27,'measures':measures,'automations':{'tempo':bpms or [{'measure':0,'bpm':170}]}};(self.cache/'songsterr-0.json').write_text(json.dumps(track))
 def mapping(self,**kw):
  m={'cache':str(self.cache),'meters':True,'offset':.1,'head':{'swing':2/3,'master':{'fx':[]}},'parts':[{'name':'line','track':0,'patch':'sine','bars':[[1,99]]}]};m.update(kw);return m
 def starts(self,song):
  if not B:self.skipTest('Set CHIRP_TEST to exercise native timing controls')
  song=copy.deepcopy(song);song.setdefault('patches',{})['sine']={'synth':{'layers':[{'wave':'sine'}]},'play':{'humanize':{'time':'0ms','vel':0}}}
  p=self.d/'song.json';p.write_text(json.dumps(song));r=subprocess.run([B,'plan','--json','--ir','-f',str(p)],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stdout+r.stderr);return [v['start']/48000 for v in json.loads(r.stdout)['data']['ir']['voices']]
 def test_swing_translation(self):
  zero=T.build(self.mapping(offset=0));placed=T.build(self.mapping(offset_mode='placement'));a,b=self.starts(zero),self.starts(placed);self.assertEqual(len(a),len(b));self.assertTrue(all(abs(y-x-.1)<=1/48000+1e-8 for x,y in zip(a,b)));self.assertEqual(placed['tempo'][0]['meter'],'5/4');self.assertEqual(placed['tracks'][0]['at'],'0.1s');self.assertNotIn('R/0.2833b',placed['tracks'][0]['score'])
 def test_default_rest_mode_unchanged(self):
  a=T.build(self.mapping());b=T.build(self.mapping(offset_mode='rest'));self.assertEqual(T.dump(a),T.dump(b));self.assertNotIn('at',a['tracks'][0]);self.assertIn('R/0.2833b',a['tracks'][0]['score'])
 def test_variable_tempo_mixed_meter_clock(self):
  self.write_track([[5,4],[7,8],[3,4]],[{'measure':0,'bpm':120},{'measure':1,'bpm':90},{'measure':2,'bpm':150}]);m=self.mapping(offset=.123456789,offset_mode='placement',head={'master':{'fx':[]}});song=T.build(m);got=self.starts(song);clock=T.performed_timeline(str(self.cache),m);self.assertEqual(len(got),9)
  for i,row in enumerate(clock):self.assertAlmostEqual(got[3*i],row['start'],delta=1/48000+1e-8)
  self.assertEqual([r['sig'] for r in clock],['5/4','7/8','3/4']);self.assertEqual(song['tempo'][0]['meter'],'5/4')
 def test_score_file_uses_placement(self):
  p=self.d/'notes.txt';p.write_text('bar 1 C4/0.5b D4/0.5b R/4b\nbar 2 E4/5b\n');m=self.mapping(offset_mode='placement');m['parts'][0].pop('track');m['parts'][0]['score_file']=str(p);song=T.build(m);self.assertEqual(song['tracks'][0]['at'],'0.1s');self.assertTrue(song['tracks'][0]['score'].startswith('C4/0.5b'));self.assertAlmostEqual(self.starts(song)[0],.1,delta=1/48000)
 def test_raw_is_not_offset_again(self):
  p=self.d/'raw.json';p.write_text(json.dumps({'x':{'score':'R/2b C4/1b'}}));m=self.mapping(offset_mode='placement');m['parts']=[{'name':'raw','patch':'sine','raw':str(p)+'#x','extra':{'at':'1b'}}];song=T.build(m);self.assertEqual(song['tracks'][0]['score'],'R/2b C4/1b');self.assertEqual(song['tracks'][0]['at'],'1b')
 def test_extra_at_conflict_refused(self):
  m=self.mapping(offset_mode='placement');m['parts'][0]['extra']={'at':'1b'}
  with self.assertRaises(SystemExit):T.build(m)
 def test_negative_or_invalid_mode_refused(self):
  for m in [self.mapping(offset=-.1,offset_mode='placement'),self.mapping(offset_mode='typo')]:
   with self.assertRaises(SystemExit):T.build(m)
 def test_tuplets_keep_relative_onsets(self):
  x=json.loads((self.cache/'songsterr-0.json').read_text());x['measures'][0]['voices'][0]['beats']=[{'duration':[1,12],'notes':[{'string':0,'fret':n}]} for n in [0,2,4]]+[{'duration':[1,1],'rest':True,'notes':[{'rest':True}]}];(self.cache/'songsterr-0.json').write_text(json.dumps(x));a=self.starts(T.build(self.mapping(offset=0)));b=self.starts(T.build(self.mapping(offset_mode='placement')));self.assertTrue(all(abs(y-x-.1)<=1/48000+1e-8 for x,y in zip(a,b)))
if __name__=='__main__':unittest.main()
