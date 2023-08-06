import requests

#settings = {"q_per_page":1,"accepted":True,"sort":3,"default_tags":["python"]}
def whatIsSettings():
    return "settings = {\"q_per_page\":1,\"accepted\":True,\"sort\":3,\"default_tags\":[\"python\"]}\noh and sort order is activity, votes, creation, relevance\nalso tags should be an array :)"


def getQuestionByTags(tags=["python"],settings={"q_per_page":1,"accepted":True,"sort":3,"default_tags":["python"]}): #tags is array
    formattedtags = ";".join(tags)
    url = "https://api.stackexchange.com/2.2/questions?pagesize={0}&order=desc&sort=votes&tagged={1}&site=stackoverflow&filter=withbody".format(str(settings["q_per_page"]),formattedtags)
    return requests.get(url).json() #returns question object(s)


def getQuestionBySearch(query,tags=["python"],settings={"q_per_page":1,"accepted":True,"sort":3,"default_tags":["python"]}):
    formattedtags = ";".join(tags)
    url = "https://api.stackexchange.com/2.3/search/advanced?pagesize={0}&order=desc&sort={1}&q={2}&accepted={3}&tagged={4}&site=stackoverflow&filter=withbody".format(settings["q_per_page"],["activity","votes","creation","relevance"][settings["sort"]],query,settings["accepted"],formattedtags)
    return requests.get(url).json()

def getAnswerByQuestion(question_id):
    url = "https://api.stackexchange.com/2.3/questions/{0}/answers?order=desc&site=stackoverflow&filter=withbody".format(question_id)
    return requests.get(url).json()


def getAnswerById(answer_id):
    url = "https://api.stackexchange.com/2.3/answers/{0}?order=desc&site=stackoverflow&filter=withbody".format(answer_id)
    return requests.get(url).json()

