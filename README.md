# Crawl3r
Crawl3r is a web crawler that is designed to index all request/response headers, defined tags, comments, and links recursively.

Example of crawling python.org:
```
$ crawl3r python.org
[.] Initialize 10 redis client(s).
[ 23:50:37 ] CRAWLING python.org
[ 23:50:40 ] CRAWLING https://www.python.org/static/humans.txt
[ 23:50:40 ] CRAWLING https://www.python.org/dev/peps/peps.rss/
[ 23:50:40 ] CRAWLING https://www.python.org/jobs/feed/rss/
[ 23:50:40 ] CRAWLING https://www.python.org/psf-landing/
[ 23:50:40 ] CRAWLING https://docs.python.org
[ 23:50:40 ] CRAWLING https://www.python.org/jobs/
[ 23:50:40 ] CRAWLING https://www.python.org/community-landing/
[ 23:50:40 ] CRAWLING https://www.python.org/search/
[ 23:50:40 ] CRAWLING https://www.python.org/community/irc/
[ 23:50:40 ] CRAWLING https://www.python.org/about/
[ 23:50:42 ] CRAWLING https://www.python.org/about/apps/
[ 23:50:42 ] CRAWLING https://www.python.org/about/quotes/
[ 23:50:42 ] CRAWLING https://www.python.org/about/gettingstarted/
[ 23:50:42 ] CRAWLING https://www.python.org/about/help/
[ 23:50:42 ] CRAWLING https://www.python.org/downloads/
[ 23:50:42 ] CRAWLING https://www.python.org/downloads/source/
[ 23:50:42 ] CRAWLING https://www.python.org/downloads/windows/
[ 23:50:42 ] CRAWLING https://www.python.org/downloads/mac-osx/
[ 23:50:42 ] CRAWLING https://www.python.org/download/other/
[ 23:50:42 ] CRAWLING https://docs.python.org/3/license.html
[ 23:50:45 ] CRAWLING https://www.python.org/download/alternatives
[ 23:50:45 ] CRAWLING https://www.python.org/doc/
[ 23:50:45 ] CRAWLING https://www.python.org/doc/av
[ 23:50:45 ] CRAWLING https://wiki.python.org/moin/BeginnersGuide
[ 23:50:45 ] CRAWLING https://devguide.python.org/
[ 23:50:45 ] CRAWLING https://docs.python.org/faq/
[ 23:50:45 ] CRAWLING http://wiki.python.org/moin/Languages
[ 23:50:45 ] CRAWLING http://python.org/dev/peps/
[ 23:50:45 ] CRAWLING https://wiki.python.org/moin/PythonBooks
[ 23:50:45 ] CRAWLING https://www.python.org/doc/essays/
[ 23:50:50 ] CRAWLING https://www.python.org/community/
[ 23:50:50 ] CRAWLING https://www.python.org/community/survey
[ 23:50:50 ] CRAWLING https://www.python.org/community/diversity/
[ 23:50:50 ] CRAWLING https://www.python.org/community/lists/
[ 23:50:50 ] CRAWLING https://www.python.org/community/forums/
[ 23:50:50 ] CRAWLING https://www.python.org/psf/annual-report/2020/
[ 23:50:50 ] CRAWLING https://www.python.org/community/workshops/
[ 23:50:50 ] CRAWLING https://www.python.org/community/sigs/
[ 23:50:50 ] CRAWLING https://www.python.org/community/logos/
[ 23:50:50 ] CRAWLING https://wiki.python.org/moin/
[ 23:50:52 ] CRAWLING https://www.python.org/community/merchandise/
[ 23:50:52 ] CRAWLING https://www.python.org/community/awards
[ 23:50:52 ] CRAWLING https://www.python.org/psf/conduct/
[ 23:50:52 ] CRAWLING https://www.python.org/psf/get-involved/
[ 23:50:52 ] CRAWLING https://www.python.org/psf/community-stories/
[ 23:50:52 ] CRAWLING https://www.python.org/success-stories/
[ 23:50:52 ] CRAWLING https://www.python.org/success-stories/category/arts/
[ 23:50:52 ] CRAWLING https://www.python.org/success-stories/category/business/
[ 23:50:52 ] CRAWLING https://www.python.org/success-stories/category/education/
[ 23:50:52 ] CRAWLING https://www.python.org/success-stories/category/engineering/
[ 23:50:55 ] CRAWLING https://www.python.org/success-stories/category/government/
[ 23:50:55 ] CRAWLING https://www.python.org/success-stories/category/scientific/
[ 23:50:55 ] CRAWLING https://www.python.org/success-stories/category/software-development/
[ 23:50:55 ] CRAWLING https://www.python.org/blogs/
[ 23:50:55 ] CRAWLING https://www.python.org/psf/newsletter/
[ 23:50:55 ] CRAWLING https://www.python.org/events/
[ 23:50:55 ] CRAWLING https://www.python.org/events/python-events
[ 23:50:55 ] CRAWLING https://www.python.org/events/python-user-group/
[ 23:50:55 ] CRAWLING https://www.python.org/events/python-events/past/
[ 23:50:55 ] CRAWLING https://www.python.org/events/python-user-group/past/
[ 23:50:56 ] CRAWLING https://wiki.python.org/moin/PythonEventsCalendar
[ 23:50:56 ] CRAWLING https://www.python.org/shell/
[ 23:50:56 ] CRAWLING http://docs.python.org/3/tutorial/controlflow.html
[ 23:50:56 ] CRAWLING http://docs.python.org/3/tutorial/introduction.html
[ 23:50:56 ] CRAWLING http://docs.python.org/3/tutorial/
[ 23:50:56 ] CRAWLING https://www.python.org/downloads/release/python-394/
[ 23:50:56 ] CRAWLING http://jobs.python.org
[ 23:50:56 ] CRAWLING https://blog.python.org
[ 23:50:56 ] CRAWLING https://www.python.org/events/calendars/
[ 23:50:56 ] CRAWLING https://www.python.org/events/python-events/893/
[ 23:51:03 ] CRAWLING https://www.python.org/events/python-user-group/1090/
[ 23:51:03 ] CRAWLING https://www.python.org/events/python-events/1088/
[ 23:51:03 ] CRAWLING https://www.python.org/events/python-events/1048/
[ 23:51:03 ] CRAWLING https://www.python.org/events/python-events/1036/
[ 23:51:03 ] CRAWLING https://www.python.org/success-stories/python-provides-convenience-and-flexibility-for-scalable-mlai/
[ 23:51:03 ] CRAWLING https://www.python.org/about/apps
[ 23:51:03 ] CRAWLING http://wiki.python.org/moin/TkInter
[ 23:51:03 ] CRAWLING https://www.python.org/dev/peps/
[ 23:51:03 ] CRAWLING https://www.python.org/dev/peps/peps.rss
[ 23:51:03 ] CRAWLING https://www.python.org/psf/
[ 23:51:06 ] CRAWLING https://www.python.org/users/membership/
[ 23:51:06 ] CRAWLING https://www.python.org/psf/donations/
[ 23:51:06 ] CRAWLING https://www.python.org/dev/
[ 23:51:06 ] CRAWLING https://bugs.python.org/
[ 23:51:06 ] CRAWLING https://mail.python.org/mailman/listinfo/python-dev
[ 23:51:06 ] CRAWLING https://www.python.org/dev/core-mentorship/
[ 23:51:06 ] CRAWLING https://www.python.org/dev/security/
[ 23:51:06 ] CRAWLING https://status.python.org/
[ 23:51:06 ] CRAWLING https://www.python.org/about/legal/
[ 23:51:06 ] CRAWLING https://www.python.org/privacy/
[ 23:51:08 ] CRAWLING https://www.python.org/psf/sponsorship/sponsors/
$
$ ls -1 
all-paths.python.org.21-04-29.json
been-crawled.python.org.21-04-29.json
logger.python.org.21-04-29.log
reqer-result.python.org.21-04-29.json
static-files.python.org.21-04-29.json
```

## Setup
Due to connecting to "postgres" database it is necessary to run with sudo
```
sudo bash setup.sh
```

## Usage
```
```


## config\.py

**DEPTH**: Define depth of crawling.  
E.g: If it was set to 2, passed URL and all found links in it will be crawled. Assigning 0 to it, causing crawling the entire domain.

**PROCESSES**: Number of processes that will run in parallel mode.

**RESULT_PATH**: Path to save results.

**REQUEST_HEADERS**: Headers which used for requests. Use specified user agents in lib/user_agents.py file.

**RESPONSE_HEADERS**: Headers which will be indexed.

**HTML_ATTRIBUTES**: Attributes which contain links.

**HTML_TAGS**: Desired tags for indexing.  
E.g: form, input, meta, etc.
