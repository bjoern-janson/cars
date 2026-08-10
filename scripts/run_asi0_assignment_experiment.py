#!/usr/bin/env python3
"""ASI-0 assignment harness. --smoke is plumbing evidence only; no model API is called."""
import argparse, hashlib, json, math, random, statistics
from collections import defaultdict
from pathlib import Path

PH = "MUST_FREEZE_BEFORE_SCIENTIFIC_RUN"
PRIMARY = ("aligned", "misaligned")
SECONDARY = ("static", "random_edit")


def jload(path):
    with open(path, encoding="utf-8") as f: return json.load(f)


def jl_load(path):
    out=[]
    with open(path, encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            if line.strip():
                try: out.append(json.loads(line))
                except json.JSONDecodeError as e: raise ValueError(f"invalid JSONL line {n}: {e}") from e
    return out


def jwrite(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,"w",encoding="utf-8") as f: json.dump(obj,f,indent=2,sort_keys=True); f.write("\n")


def jl_write(path,rows):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,"w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,sort_keys=True)+"\n")


def chash(obj):
    s=json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return hashlib.sha256(s.encode()).hexdigest()


def has_ph(x):
    if isinstance(x,dict): return any(has_ph(v) for v in x.values())
    if isinstance(x,list): return any(has_ph(v) for v in x)
    return x==PH


def validate_cfg(c,scientific):
    if c.get("schema_version")!=1: raise ValueError("unsupported schema_version")
    if c["treatment"]["primary_arms"]!=list(PRIMARY): raise ValueError("primary arms changed")
    if scientific and has_ph(c): raise ValueError("scientific preparation refused: config still contains MUST_FREEZE_BEFORE_SCIENTIFIC_RUN")


def skey(r,c):
    fs=c["matching"]["stratum_fields"]; miss=[f for f in fs if f not in r]
    if miss: raise ValueError(f"target {r.get('target_id')} missing stratum fields {miss}")
    return tuple(r[f] for f in fs)


def pool_hash(r,c):
    cs=r["candidates"]
    if len(cs)!=int(r["candidate_count"]): raise ValueError(f"candidate_count mismatch for {r['target_id']}")
    seen=set(); norm=[]; cap=int(c["agent"]["max_patch_utf8_bytes"])
    for x in cs:
        if not all(k in x for k in c["manifest"]["candidate_fields"]): raise ValueError(f"malformed candidate for {r['target_id']}")
        cid=str(x["candidate_id"]); text=str(x["text"])
        if cid in seen: raise ValueError(f"duplicate candidate {cid}")
        if len(text.encode())>cap: raise ValueError(f"candidate {cid} exceeds patch cap")
        seen.add(cid); norm.append({"candidate_id":cid,"text":text})
    return chash(norm)


def manifest(rows,c):
    req=c["manifest"]["required_target_fields"]; ids=set(); strata=defaultdict(list); out=[]
    for x in rows:
        miss=[f for f in req if f not in x]
        if miss: raise ValueError(f"manifest row missing {miss}")
        r=dict(x); r["target_id"]=str(r["target_id"])
        if r["target_id"] in ids: raise ValueError(f"duplicate target {r['target_id']}")
        ids.add(r["target_id"])
        if r["evidence_hash"]!=hashlib.sha256(str(r["evidence_text"]).encode()).hexdigest(): raise ValueError(f"evidence hash mismatch {r['target_id']}")
        r["candidate_pool_hash"]=pool_hash(r,c); r["match_stratum_hash"]=chash(list(skey(r,c)))
        strata[skey(r,c)].append(r); out.append(r)
    n=int(c["matching"]["minimum_targets_per_stratum"])
    bad=[(k,len(v)) for k,v in strata.items() if len(v)<n]
    if bad: raise ValueError(f"strata too small for derangement: {bad}")
    return out,strata


def prompt(target,evidence,cs):
    opts="\n".join(f"- {x['candidate_id']}: {x['text']}" for x in cs)
    return "You are selecting exactly one bounded modification for a frozen base agent.\nUse the assigned development evidence only as evidence; do not invent concealed outcomes.\nReturn exactly one candidate_id and no other text.\n\nTARGET CONTEXT:\n"+target+"\n\nASSIGNED DEVELOPMENT EVIDENCE:\n"+evidence+"\n\nFROZEN CANDIDATE POOL:\n"+opts+"\n"


def prepare(rows,c):
    rs,strata=manifest(rows,c); byid={r["target_id"]:r for r in rs}; src={}; rng=random.Random(int(c["treatment"]["assignment_seed"]))
    for key in sorted(strata,key=repr):
        g=sorted(strata[key],key=lambda r:r["target_id"]); off=rng.randrange(1,len(g))
        p=g[off:]+g[:off]
        for t,s in zip(g,p):
            if t["target_id"]==s["target_id"]: raise AssertionError("misaligned fixed point")
            src[t["target_id"]]=s["target_id"]
    out=[]; rr=random.Random(int(c["secondary_controls"]["random_edit_seed"])); sec=bool(c["secondary_controls"].get("enabled"))
    for t in sorted(rs,key=lambda r:r["target_id"]):
        common={k:t[k] for k in ("target_id","target_context","candidate_pool_hash","candidate_count","resource_budget_units","base_agent_hash","evaluator_id","concealed_suite_id","match_stratum_hash","candidates")}
        common.update({"canonical_evidence_id":t["evidence_id"],"replicate_id":t.get("replicate_id","r0")})
        for arm,e in (("aligned",t),("misaligned",byid[src[t["target_id"]]])):
            out.append({**common,"arm":arm,"assigned_evidence_source_target_id":e["target_id"],"assigned_evidence_id":e["evidence_id"],"assigned_evidence_hash":e["evidence_hash"],"assigned_evidence_text":e["evidence_text"],"selection_prompt":prompt(t["target_context"],e["evidence_text"],t["candidates"]),"selected_candidate_id":None,"control_action":"model_select_one_candidate"})
        if sec:
            base={**common,"assigned_evidence_source_target_id":t["target_id"],"assigned_evidence_id":t["evidence_id"],"assigned_evidence_hash":t["evidence_hash"],"assigned_evidence_text":t["evidence_text"],"selection_prompt":None}
            out.append({**base,"arm":"static","selected_candidate_id":None,"control_action":"no_op"})
            out.append({**base,"arm":"random_edit","selected_candidate_id":rr.choice(t["candidates"])["candidate_id"],"control_action":"uniform_random_candidate"})
    return out


def pct(xs,q):
    y=sorted(xs); p=q*(len(y)-1); lo=int(math.floor(p)); hi=int(math.ceil(p))
    return y[lo] if lo==hi else y[lo]*(hi-p)+y[hi]*(p-lo)


def analyze(rows,c):
    req=("target_id","replicate_id","arm","canonical_evidence_id","assigned_evidence_id","candidate_pool_hash","candidate_count","resource_budget_units","base_agent_hash","evaluator_id","concealed_suite_id","match_stratum_hash","base_concealed_score","concealed_score","protected_regression_pass")
    groups=defaultdict(dict)
    for r in rows:
        miss=[f for f in req if f not in r]
        if miss: raise ValueError(f"result row missing {miss}")
        key=(str(r["target_id"]),str(r["replicate_id"])); arm=r["arm"]
        if arm in groups[key]: raise ValueError(f"duplicate arm {arm} for {key}")
        groups[key][arm]=r
    pairs=[]; gains=defaultdict(list); gates=defaultdict(list)
    exact=("target_id","replicate_id","candidate_pool_hash","candidate_count","resource_budget_units","base_agent_hash","evaluator_id","concealed_suite_id","match_stratum_hash")
    for key,a in sorted(groups.items()):
        if not all(x in a for x in PRIMARY): raise ValueError(f"missing primary arm for {key}")
        x,y=a["aligned"],a["misaligned"]
        bad=[f for f in exact if x.get(f)!=y.get(f)]
        if bad: raise ValueError(f"primary pair {key} mismatched {bad}")
        if x["assigned_evidence_id"]!=x["canonical_evidence_id"]: raise ValueError(f"aligned evidence mismatch {key}")
        if y["assigned_evidence_id"]==y["canonical_evidence_id"]: raise ValueError(f"misaligned fixed point {key}")
        gx=float(x["concealed_score"])-float(x["base_concealed_score"]); gy=float(y["concealed_score"])-float(y["base_concealed_score"])
        pairs.append({"target_id":key[0],"replicate_id":key[1],"aligned_gain":gx,"misaligned_gain":gy,"pair_delta_align":gx-gy})
        gains["aligned"].append(gx); gains["misaligned"].append(gy); gates["aligned"].append(bool(x["protected_regression_pass"])); gates["misaligned"].append(bool(y["protected_regression_pass"]))
        for arm in SECONDARY:
            if arm in a: gains[arm].append(float(a[arm]["concealed_score"])-float(a[arm]["base_concealed_score"]))
    delta=statistics.fmean(p["pair_delta_align"] for p in pairs); by=defaultdict(list)
    for p in pairs: by[p["target_id"]].append(p["pair_delta_align"])
    tm={k:statistics.fmean(v) for k,v in by.items()}; tids=sorted(tm); rng=random.Random(int(c["evaluation"]["bootstrap_seed"])); draws=[]
    for _ in range(int(c["evaluation"]["bootstrap_target_resamples"])): draws.append(statistics.fmean(tm[rng.choice(tids)] for _ in tids))
    return {"study":c["study"],"estimand":c["treatment"]["primary_estimand"],"n_target_replicate_pairs":len(pairs),"n_targets":len(tids),"delta_align":delta,"bootstrap_target_ci95":[pct(draws,.025),pct(draws,.975)],"bootstrap_target_resamples":len(draws),"mean_gain_by_arm":{k:statistics.fmean(v) for k,v in gains.items() if v},"protected_regression_pass_rate":{k:sum(v)/len(v) for k,v in gates.items() if v},"pair_rows":pairs,"interpretation_ceiling":c["interpretation"]["positive_maximum"],"nonclaims":c["interpretation"]["nonclaims"]}


def smoke_manifest(c):
    s=c["smoke"]; rng=random.Random(int(s["seed"])); out=[]
    for i in range(int(s["strata"])):
        for j in range(int(s["targets_per_stratum"])):
            tid=f"s{i:02d}-t{j:02d}"; ev=f"Development failure trace for {tid}: verifier mismatch class {i}."; cs=[{"candidate_id":f"{tid}-c{k}","text":f"Bounded policy patch {k} for target {tid}; synthetic smoke only."} for k in range(4)]
            out.append({"target_id":tid,"target_context":f"Synthetic target {tid}","evidence_id":f"e-{tid}","evidence_text":ev,"evidence_hash":hashlib.sha256(ev.encode()).hexdigest(),"task_family":f"synthetic_family_{i%2}","evidence_type":"verifier_trace","trace_length_bucket":"short","difficulty_bucket":f"d{i%3}","candidate_count":4,"resource_budget_units":1,"candidates":cs,"base_agent_hash":"synthetic-base","evaluator_id":"synthetic-evaluator","concealed_suite_id":"synthetic-concealed-suite","_latent":rng.uniform(-.08,.08)})
    return out


def smoke(c):
    m=smoke_manifest(c); a=prepare(m,c); latent={r["target_id"]:r["_latent"] for r in m}; rng=random.Random(int(c["smoke"]["seed"])+1); inj=float(c["smoke"]["injected_delta_align"]); sd=float(c["smoke"]["noise_sd"]); rows=[]
    for r in a:
        base=.5+latent[r["target_id"]]; arm=r["arm"]
        gain=inj+rng.gauss(0,sd) if arm=="aligned" else (rng.gauss(0,sd) if arm=="misaligned" else (.02+rng.gauss(0,sd) if arm=="random_edit" else 0.0))
        rows.append({**r,"base_concealed_score":base,"concealed_score":base+gain,"protected_regression_pass":True})
    z=analyze(rows,c); fixed=sum(r["arm"]=="misaligned" and r["assigned_evidence_id"]==r["canonical_evidence_id"] for r in a); grouped=defaultdict(dict)
    for r in a: grouped[(r["target_id"],r["replicate_id"])][r["arm"]]=r
    poolbad=sum(x["aligned"]["candidate_pool_hash"]!=x["misaligned"]["candidate_pool_hash"] for x in grouped.values()); tol=max(.04,4*sd/math.sqrt(len(m))); ok=abs(z["delta_align"]-inj)<=tol and not fixed and not poolbad
    return {"status":"PASS" if ok else "FAIL","scientific_result":False,"note":"synthetic smoke validates plumbing only; it is not ASI-0 evidence","manifest_targets":len(m),"assignment_rows":len(a),"misaligned_fixed_points":fixed,"candidate_pool_match_failures":poolbad,"injected_delta_align":inj,"estimated_delta_align":z["delta_align"],"recovery_tolerance":tol,"analysis":z}


def main():
    p=argparse.ArgumentParser(); p.add_argument("config"); g=p.add_mutually_exclusive_group(required=True); g.add_argument("--smoke",action="store_true"); g.add_argument("--prepare-manifest"); g.add_argument("--analyze-results"); p.add_argument("--assignments-out"); p.add_argument("--json-out"); a=p.parse_args(); c=jload(a.config); validate_cfg(c,not a.smoke)
    if a.smoke:
        out=smoke(c); print(json.dumps(out,indent=2,sort_keys=True));
        if a.json_out: jwrite(a.json_out,out)
        if out["status"]!="PASS": raise SystemExit(1)
    elif a.prepare_manifest:
        if not a.assignments_out: raise SystemExit("--assignments-out required")
        rows=prepare(jl_load(a.prepare_manifest),c); jl_write(a.assignments_out,rows); out={"status":"PASS","mode":"prepare","targets":len({r['target_id'] for r in rows}),"assignment_rows":len(rows),"assignments_out":a.assignments_out,"scientific_result":False}; print(json.dumps(out,indent=2));
        if a.json_out: jwrite(a.json_out,out)
    else:
        out=analyze(jl_load(a.analyze_results),c); print(json.dumps(out,indent=2,sort_keys=True));
        if a.json_out: jwrite(a.json_out,out)

if __name__=="__main__": main()
