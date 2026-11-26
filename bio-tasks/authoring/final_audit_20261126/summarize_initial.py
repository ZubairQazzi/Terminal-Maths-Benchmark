"""Summarize measured initial trajectories; do not infer scientific errors from infrastructure."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,os,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
OUT=ROOT/'authoring/trajectories/initial-gemini35lite-high-20261126'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def main():
    data=read(OUT/'results.json');rows=data['attempts']
    for row in rows:
        events_path=OUT/(row['run_id']+'-transport.jsonl')
        events=[json.loads(s) for s in events_path.read_text().splitlines()] if events_path.exists() else []
        good=[e for e in events if e.get('event')=='request_succeeded'];bad=[e for e in events if e.get('event')=='request_failed']
        row['provider_successful_calls']=len(good);row['provider_errors']=bad
        row['provider_error_status_counts']={str(code):sum(e.get('status')==code for e in bad) for code in sorted({e.get('status') for e in bad},key=str)}
        row['provider_reported_prompt_tokens']=sum((e.get('usage') or {}).get('prompt_tokens',0) for e in good)
        row['provider_reported_completion_tokens']=sum((e.get('usage') or {}).get('completion_tokens',0) for e in good)
        row['provider_reported_total_tokens']=sum((e.get('usage') or {}).get('total_tokens',0) for e in good)
        row['provider_reported_cache_read_tokens']=sum((e.get('usage') or {}).get('cache_read_input_tokens') or ((e.get('usage') or {}).get('prompt_tokens_details') or {}).get('cached_tokens') or 0 for e in good)
        reasoning=[((e.get('usage') or {}).get('completion_tokens_details') or {}).get('reasoning_tokens') for e in good]
        row['provider_reported_reasoning_tokens']=sum(v for v in reasoning if v is not None) if any(v is not None for v in reasoning) else None
        row['successful_calls_reporting_reasoning_tokens']=sum(v is not None for v in reasoning)
        row['reasoning_token_note']='Sum of reported reasoning-token fields only; incomplete if not all successful calls report them. Included in completion usage where the provider reports them; do not add to output totals.'
        if row.get('trajectory_path'):
            t=read(row['trajectory_path']);commands=[]
            for s in t.get('steps',[]):
                for call in s.get('tool_calls',[]):
                    arg=call.get('arguments',{})
                    if isinstance(arg,str):
                        try:arg=json.loads(arg)
                        except json.JSONDecodeError:arg={'unparsed':arg}
                    commands.append({'step_id':s.get('step_id'),'timestamp':s.get('timestamp'),'arguments':arg})
            dump(OUT/(row['run_id']+'-commands.json'),commands)
            text='\n'.join(str(x['arguments']) for x in commands)
            patterns={
              'private_path_probe':r'/(?:tests|solution|app/authoring)(?:/|\b)',
              'seed_replay_terms':r'default_rng|RandomState|manual_seed|seed\s*\(\s*273600|seed\s*=\s*273600',
              'network_fetch_commands':r'\b(?:curl|wget|git\s+clone)\b',
            }
            row['trajectory_command_screen']={label:[m.group(0) for m in re.finditer(pattern,text,re.I)][:20] for label,pattern in patterns.items()}
            row['command_screen_scope']='Text screening only; direct command/source/output review is required. A match is not automatically misconduct; no match is not proof of no shortcut.'
            errors=[]
            for s in t.get('steps',[]):
                chunks=[x.get('content','') for x in ((s.get('observation') or {}).get('results') or [])]
                if s.get('source') not in ('agent','user'):chunks.append(s.get('message',''))
                for chunk in chunks:
                    for line in chunk.splitlines():
                        if re.search(r'error:|permission denied|cannot open|can.t open|no such file|traceback|syntaxerror',line,re.I):
                            errors.append({'step':s.get('step_id'),'message':line[:350]})
            row['terminal_or_parser_error_excerpts']=errors
            row['xml_parser_error_observations']=sum('No <response> tag found' in x['message'] for x in errors)
        if row.get('individual_verifier_results'):
            row['failed_verifier_names']=[x['name'] for x in row['individual_verifier_results'] if x.get('status')!='passed']
            if row['status']=='PASS':row['scientific_failure_reason']='None observed: all 11 verifier requirements passed. This is contract success, not new biological validation or difficulty calibration.'
    reviews=read(OUT/'scientific_review.json') if (OUT/'scientific_review.json').exists() else {}
    for row in rows:
        if row['run_id'] in reviews.get('by_run',{}):row['scientific_failure_reason']=reviews['by_run'][row['run_id']]
    summary={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'One initial diagnostic trajectory per task; all attempts retained. Not a statistically reliable estimate of success probability or eight-trial calibration.','model':data['manifest']['model'],'agent':'terminus-2','settings_manifest':str(OUT/'manifest.json'),'attempts':rows,'source_report':str(OUT/'results.json'),'cost_note':'Token counts are native SDK/provider-reported consumption; cache reads may be a subset of input tokens. Do not add them to input totals. Null reasoning token count means not reported. SDK cost is an estimate, not a billing receipt; actual invoice is unverified.'}
    dump(OUT/'initial_comparison.json',summary)
    fields=['task','run_id','status','reward','wall_seconds','agent_execution_seconds','steps','tool_calls','input_tokens','output_tokens','cached_tokens','provider_reported_prompt_tokens','provider_reported_completion_tokens','provider_reported_cache_read_tokens','cost_usd_estimate','scientific_failure_reason','trajectory_path']
    with (OUT/'initial_comparison.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    with (OUT/'individual_verifier_results.csv').open('w',newline='',encoding='utf-8') as f:
        fields=['task','run_id','attempt_status','binary_reward','check','status','duration_seconds'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for row in rows:
            for test in row.get('individual_verifier_results') or []:
                writer.writerow({'task':row['task'],'run_id':row['run_id'],'attempt_status':row['status'],'binary_reward':row['reward'],'check':test['name'],'status':test['status'],'duration_seconds':test.get('duration')})
    print(json.dumps([{k:r.get(k) for k in ('task','run_id','status','reward','wall_seconds','steps','input_tokens','output_tokens','provider_successful_calls')} for r in rows],indent=2))
if __name__=='__main__':main()
