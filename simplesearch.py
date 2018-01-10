#!/usr/bin/env python
 
import sys
import xapian

def search(query_string, start = 0, end = 50, language = "de"):                                                                                          
    """
            Important values to be extracted:
            1. rank
            2. percent
            3. docid?
                *. FInd a method to map the docid to the <p> tag id??
            4. document.get_data()
        """
    try:
        if language == "de":
            database = xapian.Database('corpus/gesetze-de')
            stemmer = xapian.Stem("german")
        else:
            database = xapian.Database('corpus/gesetze-en')
            stemmer = xapian.Stem("english")
        enquire = xapian.Enquire(database)
        qp = xapian.QueryParser()
        qp.set_stemmer(stemmer)
        qp.set_database(database)
        qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        query = qp.parse_query(query_string)
     
        enquire.set_query(query)
        matches = enquire.get_mset(start, end)
        results = []
        
        for m in matches:
            data = m.document.get_data()
            relavence = m.percent
            data = data.decode("utf-8")
            url = ""
            sample = ""
            for i, d in enumerate(data.split("\n")):
                if i == 0:
                    url = d.split("url=")[1]
                if i == 1:
                    sample = d.split("sample=")[1]
                if i > 1:
                    break
            print("Sample is" + sample)
            results.append((url, relavence, sample))
        #~ print("%i results found." % matches.get_matches_estimated())
        #~ print("Results 1-%i:" % matches.size())
        
        #~ for m in matches:
        #~ print("%i: %i%% docid=%i [%s]" % (m.rank + 1, m.percent, m.docid,
        #~ m.document.get_data()))
        return results
    except Exception as error:
        print >> sys.stderr, "Exception: %s" % str(error)
        return None

if __name__ == '__main__':
    n_result= search(str.join(' ', sys.argv[1:]))
    for result in n_result:
        print(result)
    #~ print(result_tuple)
    
