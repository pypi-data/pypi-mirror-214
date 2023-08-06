import requests
import re
from bs4 import BeautifulSoup

#settings = {"q_per_page":1,"accepted":True,"sort":3,"default_tags":["python"]}
def whatIsSettings():
    return "settings = {\"q_per_page\":1,\"accepted\":True,\"sort\":3,\"default_tags\":[\"python\"]}\noh and sorts are activity, votes, creation, relevance (for questions)\nfor answers sorts are activity, votes, creation\nalso tags should be an array :)"


def getQuestionByTags(tags=["python"],q_per_page=1,page=1,accepted=True,sort="relevance"): #tags is array
    formattedtags = ";".join(tags)
    url = "https://api.stackexchange.com/2.2/questions?page={0}&pagesize={1}&order=desc&sort=votes&tagged={2}&site=stackoverflow&filter=withbody".format(str(page),str(q_per_page),formattedtags)
    return requests.get(url).json() #returns question object(s)


def getQuestionBySearch(query,tags=["python"],q_per_page=1,page=1,accepted=True,sort="relevance"):
    formattedtags = ";".join(tags)
    url = "https://api.stackexchange.com/2.3/search/advanced?page={0}&pagesize={1}&order=desc&sort={2}&q={3}&accepted={4}&tagged={5}&site=stackoverflow&filter=withbody".format(str(page),str(q_per_page),sort,query,accepted,formattedtags)
    return requests.get(url).json()


def getAnswerByQuestion(question_id,sort="votes"):
    url = "https://api.stackexchange.com/2.3/questions/{0}/answers?order=desc&sort={1}&site=stackoverflow&filter=withbody".format(question_id,sort)
    return requests.get(url).json()


def getAnswerById(answer_id,sort="votes"):
    url = "https://api.stackexchange.com/2.3/answers/{0}?order=desc&sort={1}&site=stackoverflow&filter=withbody".format(answer_id,sort)
    return requests.get(url).json()


def formatResponse(response, isQuestion=True):  #False if it is an answer
    try:
        title = ""
        if isQuestion:
            title = response['items'][0]['title']

        raw = response['items'][0]['body']
        soup = BeautifulSoup(raw, 'html.parser')

        for link in soup.find_all('a'):
            new_tag = soup.new_tag("p")
            new_tag.string = link.text + " ("+link.get('href').strip()+")"
            link.replace_with(new_tag)

        return soup.get_text()
    except:
        raise ValueError("Invalid response passed")

    
def getQandA(query,preformat=True,tags=["python"],q_per_page=1,page=1,accepted=True,sort="relevance"):
    question = getQuestionBySearch(query,tags,q_per_page,page,accepted,sort)
    try:
        answer = getAnswerById(question['items'][0]['accepted_answer_id'])
    except:
        try:
            answer = getAnswerByQuestion(question['items'][0]['question_id'])
        except:
            raise ValueError("No accepted answer")
    
    if preformat:
        return [formatResponse(question),formatResponse(answer,False)]
    else:
        return [question,answer]

                                         
