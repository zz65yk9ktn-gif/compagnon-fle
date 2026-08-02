from __future__ import annotations
from collections.abc import Mapping, Sequence

LEVELS=("A0","A1","A2","B1","B2")
SUPPORTED_QUESTION_TYPES={"single_choice","multiple_choice","ordering","manual_response"}
RESULT_THRESHOLDS=((0,29,"too_difficult","Niveau probablement trop difficile"),(30,59,"fragile","Compétences fragiles : nouvelle série au même niveau avec plus d’aide"),(60,79,"partial","Acquisition partielle : nouvelle série au même niveau"),(80,94,"mastered","Niveau globalement maîtrisé : consolidation ou niveau suivant"),(95,100,"excellent","Très bonne maîtrise : réévaluation possible au niveau supérieur"))

def normalize_text(value:object)->str:return " ".join(str(value or "").strip().lower().split())
def recommendation_for_percentage(percentage:int)->dict[str,object]:
    p=max(0,min(100,int(percentage)))
    for lo,hi,code,label in RESULT_THRESHOLDS:
        if lo<=p<=hi:return {"code":code,"label":label,"percentage":p}
    raise ValueError("Pourcentage hors seuils")
def _keys(q):
    c=q.get("choices",{})
    if not isinstance(c,Mapping):raise ValueError("Les choix doivent être un dictionnaire")
    return [str(k) for k in c]
def evaluate_answer(q:Mapping[str,object],data:Mapping[str,str])->dict[str,object]:
    t=str(q.get("type","")); expected=str(q.get("correct_answer",""))
    if t not in SUPPORTED_QUESTION_TYPES:raise ValueError(f"Type de question non pris en charge : {t or 'vide'}")
    if t=="manual_response":
        a=str(data.get("answer_text","")).strip()
        if not a:raise ValueError("Une réponse ou une note de réalisation est nécessaire")
        return {"answer_text":a,"is_correct":None,"score":None,"requires_manual_review":True}
    keys=_keys(q)
    if t=="multiple_choice":
        sel=sorted(k for k in keys if data.get(f"answer_{k}")==k)
        if not sel:raise ValueError("Choisissez au moins une réponse")
        a="+".join(sel); exp="+".join(sorted(x.strip() for x in expected.replace(",","+").split("+") if x.strip())); ok=a==exp
    elif t=="ordering":
        pos={}
        for k in keys:
            v=str(data.get(f"position_{k}",""))
            if not v.isdigit():raise ValueError("Attribuez une position à chaque élément")
            pos[k]=int(v)
        if sorted(pos.values())!=list(range(1,len(pos)+1)):raise ValueError("Chaque position doit être utilisée une seule fois")
        a="-".join(k for k,_ in sorted(pos.items(),key=lambda i:i[1])); ok=normalize_text(a)==normalize_text(expected)
    else:
        a=str(data.get("answer","")).strip()
        if not a:raise ValueError("Choisissez une réponse")
        if a not in keys:raise ValueError("Réponse inconnue pour cette question")
        ok=normalize_text(a)==normalize_text(expected)
    return {"answer_text":a,"is_correct":ok,"score":1.0 if ok else 0.0,"requires_manual_review":False}
def validate_question_bank(sequence:Mapping[str,object])->None:
    levels=sequence.get("levels",{}); ids=[]; seqno=None
    if not str(sequence.get("slug","")).strip() or not str(sequence.get("title","")).strip() or not isinstance(levels,Mapping):raise ValueError("Séquence incomplète")
    required={"id","sequence","level","type","instruction","support","choices","correct_answer","feedback_success","feedback_error","competency","difficulty","help","source_group"}
    for level in LEVELS:
        questions=levels.get(level,[])
        if not isinstance(questions,Sequence) or isinstance(questions,(str,bytes)) or not questions:raise ValueError(f"Banque invalide ou vide pour {level}")
        for q in questions:
            if not isinstance(q,Mapping):raise ValueError(f"Question invalide dans {level}")
            missing=required-set(q)
            if missing:raise ValueError(f"Champs manquants pour {q.get('id')}: {sorted(missing)}")
            current=int(q["sequence"]); seqno=current if seqno is None else seqno
            if current!=seqno or q["level"]!=level:raise ValueError(f"Métadonnées incohérentes pour {q['id']}")
            if str(q["type"]) not in SUPPORTED_QUESTION_TYPES:raise ValueError(f"Type non pris en charge pour {q['id']}")
            if not isinstance(q["difficulty"],int) or not 1<=q["difficulty"]<=5:raise ValueError(f"Difficulté invalide pour {q['id']}")
            keys=_keys(q); expected=str(q["correct_answer"])
            if q["type"]!="manual_response" and len(keys)<2:raise ValueError(f"Choix insuffisants pour {q['id']}")
            if q["type"]=="single_choice" and expected not in keys:raise ValueError(f"Bonne réponse absente pour {q['id']}")
            qid=str(q["id"])
            if not qid.startswith(f"S{seqno}-{level}-"):raise ValueError(f"Identifiant incohérent pour {qid}")
            ids.append(qid)
    if len(ids)!=len(set(ids)):raise ValueError("Identifiants dupliqués")
