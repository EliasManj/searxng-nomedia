from lxml import html

from searx.utils import (
    eval_xpath_getindex,
    eval_xpath_list,
    extract_text,
)

categories = ['general']  # optional


def request(query, params):
    '''pre-request callback
    params<dict>:
      method  : POST/GET
      headers : {}
      data    : {} # if method == POST
      url     : ''
      category: 'search category'
      pageno  : 1 # number of the requested page
    '''
    searchterm = query.replace(' ','+')
    params['url'] = f'https://wikispooks.com/w/index.php?search={searchterm}&title=Special%3ASearch&profile=advanced&fulltext=1&ns0=1'

    return params


def response(resp):
    '''post-response callback
    resp: requests response object
    '''
    results = []
    dom = html.fromstring(resp.text)
    for result in eval_xpath_list(dom, '//li[contains(@class,"mw-search-result")]'):
        href = eval_xpath_getindex(result, './/div[contains(@class,"mw-search-result-heading")]/a/@href', 0, default=None)
        title = extract_text(result.xpath('.//div[contains(@class,"mw-search-result-heading")]/a/@title'))
        content = extract_text(result.xpath('.//div[contains(@class,"searchresult")]'))
        # append result
        results.append({'url': f'https://wikispooks.com/{href}', 'title': title, 'content': content})
        
    
    return results
