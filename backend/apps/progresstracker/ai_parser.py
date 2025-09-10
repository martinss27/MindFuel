import json
import re
import logging

logger = logging.getLogger(__name__)


def extract_json_from_text(s: str):
    if not isinstance(s, str): #type check
        return None
    
    #locate json bounds
    start = s.find('{') # find first {
    end = s.rfind('}') # find last }

    if start == -1 or end == -1 or end <= start:
        return None # if no valid json bounds found -> return None
    
    candidate = s[start:end+1] # slice the str to get text between the braces
    
    try: # tru to parse the candidate str with json.loads
        return json.loads(candidate) # if sucessfull, return a python dict
    except Exception:
        return None


def parse_plain_quiz_text(s: str):
    
    if not isinstance(s, str): #type check
        return None
    
    lines = [ln.rstrip() for ln in s.splitlines() if ln.strip()] #normalize input
    
    if not lines: # fallback if empty after cleanup
        return None

    text = '\n'.join(lines)
    
    mc_idx = text.find('Multiple-choice:') # search for MC sections
    block = text[mc_idx:] if mc_idx != -1 else text # if found, use from there to end, else whole text


    q_pattern = re.compile(r"^(\d+)\.\s*(.+?)(?=(?:\n\d+\.|\Z))", re.S | re.M) # match numbered questions like 1. Q/text
    opt_pattern = re.compile(r"^[A-Z][)\.]\s*(.+)$", re.M) #match options questions starting with A) or A.

    questions = []

    for qmatch in q_pattern.finditer(block): #loop through questions
        qtext = qmatch.group(2).strip() #extract question text
        
        opts = opt_pattern.findall(qtext) # finds mc options and removes them from question text
        qtext_clean = re.sub(r"\n[A-Z][)\.]\s*.+", '', qtext).strip()

        if opts: # if options found -> treat as MC
            questions.append({'text': qtext_clean, 'type': 'multiple_choice', 'choices': opts})
        else: # else -> True/False (assumption)
            questions.append({'text': qtext_clean, 'type': 'true_false'})

    if not questions:
        return None
    return {'questions': questions} # result structured


def parse_ai_response(ai_content): #function to accept various AI response formats and return structured obj (usually dict/list)

    if isinstance(ai_content, (dict, list)): # if already strcutured, just return it
        return ai_content

    if not isinstance(ai_content, str): # in case not str, dict or list -> reject = error
        raise ValueError(f"Unexpected AI response type: {type(ai_content)}")


    try: # trying to parse as json direcly
        return json.loads(ai_content)
    except Exception:
        pass

    # if IA put embedded json in text, the function bellow will try to extract it and parse
    extracted = extract_json_from_text(ai_content)
    if extracted is not None:
        return extracted

    # if not json, try to parse as plain text quiz format
    parsed = parse_plain_quiz_text(ai_content)
    if parsed is not None:
        return parsed

    # if nothing worked, raise error with raw content to help debugging
    logger.debug('AI raw content (unparseable): %s', ai_content)
    raise ValueError(f'Could not parse AI response; raw: {ai_content}')
