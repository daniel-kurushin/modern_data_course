def _filter_term(term):
    wrong_grammemes = {'ADJF', 'LATN', 'UNKN', 'NUMB', 'NUMR' }
    
    word = term.words[0].parsed
    
    return len(term.words) > 1 and \
           len(word.tag.grammemes & wrong_grammemes) == 0 

def _normalize_terms_weights(kw):
    import numpy as np
    res = []

    max_weight, min_weight = kw[0][1], kw[-1][1]
    a, b = np.polyfit([max_weight, min_weight], [1, 0.1], 1)
    for term, weight in kw:
        normalized_weight = max(0, a * weight + b)
        res += [[str(term), normalized_weight]]
        
    return res
    
def get_text_keywords(a_text):
    from rutermextract import TermExtractor
    te = TermExtractor()
    kw = [ (term, term.count) for term in te(a_text) if _filter_term(term) ]
    
    return _normalize_terms_weights(kw)

def compare_keywords(kw_a, kw_b):
    set_of_kw_a = set([ x[0] for x in kw_a ])
    set_of_kw_b = set([ x[0] for x in kw_b ])
    
    return len(set_of_kw_a & set_of_kw_b) / min(len(set_of_kw_a), len(set_of_kw_b))

def compare_freq(kw_a, kw_b):
    import numpy as np
    from scipy.stats import chi2_contingency
    l = min(len(kw_a), len(kw_b))
    table = np.array([[x[1] for x in kw_a][:l],[x[1] for x in kw_b][:l]])
    stat, p, dof, _ = chi2_contingency(table)

    return stat, p, dof

