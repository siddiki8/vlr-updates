from bs4 import BeautifulSoup as bs
import requests
import itertools
import time


class Match:

  def __init__(self, link):
    match = requester(link)
    self.match = match

  def map(self):
    map = self.match.find_all('div', class_='map')
    maps = []
    mapsf = []
    for i in map:
      maps.append(i.span.text.strip())
    for i in maps:
      i = i.replace('\n', '')
      i = i.replace('\t', '')
      i = i.replace('PICK', '')
      mapsf.append(i)
    return mapsf

  def event(self):
    event = self.match.find('div', style='font-weight: 700;').text.strip()
    return event

  def round(self):
    round = self.match.find('div',
                            class_='match-header-event-series').text.strip()
    round = round.replace('\n', '')
    round = round.replace('\t', '')
    return round

  def scores(self):
    scores = self.match.find_all('div', class_='score')
    scorel = []
    for i in scores:
      scorel.append(i.text.strip())
    return scorel

  def leftteam(self):
    leftteamname = ''
    lefttlink = self.match.find('a',
                                class_="match-header-link wf-link-hover mod-1")
    lefttlink = lefttlink['href']
    lefttlink = ('https://www.vlr.gg' + lefttlink)
    lefttlink = requester(lefttlink)
    leftteamname = lefttlink.find('h1', class_='wf-title').text
    return leftteamname.strip()

  def lefttwitter(self):
    lefttlink = self.match.find('a',
                                class_="match-header-link wf-link-hover mod-1")
    lefttlink = lefttlink['href']
    lefttlink = ('https://www.vlr.gg' + lefttlink)
    lefttlink = requester(lefttlink)
    try:
      ltwitter = lefttlink.find('div',
                                class_='team-header-links').text.lstrip()
      ltwitter = ltwitter.replace('\n', '')
      ltwitter = ltwitter.replace('\t', '')
      ltwitter = '@' + ltwitter.split('@')[1]
      ltwitter = ltwitter.split(' ')[0]
    except:
      ltwitter = None
    return ltwitter

  def righttwitter(self):
    righttlink = self.match.find(
      'a', class_="match-header-link wf-link-hover mod-2")
    righttlink = righttlink['href']
    righttlink = ('https://www.vlr.gg' + righttlink)
    righttlink = requester(righttlink)
    try:
      rtwitter = righttlink.find('div',
                                 class_='team-header-links').text.lstrip()
      rtwitter = rtwitter.replace('\n', '')
      rtwitter = rtwitter.replace('\t', '')
      rtwitter = '@' + rtwitter.split('@')[1]
      rtwitter = rtwitter.split(' ')[0]
    except:
      rtwitter = None
    return rtwitter

  def rightteam(self):
    rightteamname = ''
    righttlink = self.match.find(
      'a', class_="match-header-link wf-link-hover mod-2")
    righttlink = righttlink['href']
    righttlink = ('https://www.vlr.gg' + righttlink)
    righttlink = requester(righttlink)
    rightteamname = righttlink.find('h1', class_='wf-title').text
    return rightteamname.strip()

  def mapscore(self):
    mapscore = []
    maps = self.map()
    score = self.scores()
    x = 0
    y = 2
    if len(maps) == 1:
      slist = []
      mlist = []
      mlist.append(maps[0])
      slist.append(score[0:2])
      mlist.extend(slist)
      mapscore.append(tuple(mlist))
      return mapscore
    else:
      for i in maps:
        mlist = []
        slist = []
        mlist.append(i)
        slist.append(score[x:y])
        mlist.extend(slist)
        mapscore.append(tuple(mlist))
        x += 2
        y += 2
      return mapscore

  def __str__(self):
    winner = ''
    lwinner = 0
    rwinner = 0
    output = ""
    s = self.mapscore()
    rightteam = self.rightteam()
    leftteam = self.leftteam()
    map = self.map()
    ltwitter = self.lefttwitter()
    rtwitter = self.righttwitter()
    if len(self.mapscore()) == 1:
      if int(s[0][1][0]) > int(s[0][1][1]):
        output = (str(leftteam) + ' defeat ' + str(rightteam) + ' ' +
                  str(s[0][1][0]) + ' to ' + str(s[0][1][1]) + ' on' +
                  str(map[0]) + '.')
        lwinner += 1
      else:
        output = (str(rightteam) + ' defeat ' + str(leftteam) + ' ' +
                  str(s[0][1][1]) + ' to ' + str(s[0][1][0]) + ' on ' +
                  str(map[0]) + '.')
        rwinner += 1
    else:
      mbuff = 0
      sbuff = 0
      for i in s:
        if int(s[sbuff][1][0]) > int(s[sbuff][1][1]):
          output += (leftteam + ' defeat ' + rightteam + ' ' +
                     str(s[sbuff][1][0]) + ' to ' + str(s[sbuff][1][1]) +
                     ' on ' + str(map[mbuff]) + '.' + '\n')
          mbuff += 1
          sbuff += 1
          lwinner += 1
        else:
          output += (rightteam + ' defeat ' + leftteam + ' ' +
                     str(s[sbuff][1][1]) + ' to ' + str(s[sbuff][1][0]) +
                     ' on ' + str(map[mbuff]) + '.' + '\n')
          mbuff += 1
          sbuff += 1
          rwinner += 1
    mbuff = 0
    sbuff = 0

    if lwinner > rwinner:
      if ltwitter != None and rtwitter != None:
        winner = ltwitter + ' ' + str(lwinner) + '-' + str(
          rwinner) + ' ' + rtwitter
      elif ltwitter == None and rtwitter != None:
        winner = leftteam + ' ' + str(lwinner) + '-' + str(
          rwinner) + ' ' + rtwitter
      elif ltwitter != None and rtwitter == None:
        winner = ltwitter + ' ' + str(lwinner) + '-' + str(
          rwinner) + ' ' + rightteam
      else:
        winner = leftteam + ' ' + str(lwinner) + '-' + str(
          rwinner) + ' ' + rightteam
    else:
      if ltwitter != None and rtwitter != None:
        winner = rtwitter + ' ' + str(rwinner) + '-' + str(
          lwinner) + ' ' + ltwitter
      elif ltwitter == None and rtwitter != None:
        winner = rtwitter + ' ' + str(rwinner) + '-' + str(
          lwinner) + ' ' + leftteam
      elif ltwitter != None and rtwitter == None:
        winner = rightteam + ' ' + str(rwinner) + '-' + str(
          lwinner) + ' ' + ltwitter
      else:
        winner = rightteam + ' ' + str(rwinner) + '-' + str(
          lwinner) + ' ' + leftteam

    final_score = self.event() + ' ' + self.round() + '\n' + winner.lstrip(
    ) + '\n' + output

    if len(final_score) > 280:
      output = ''
      for i in s:
        if int(s[sbuff][1][0]) > int(s[sbuff][1][1]):
          output += (str(s[sbuff][1][0]) + ' to ' + str(s[sbuff][1][1]) + ' ' +
                     leftteam + ' on ' + str(map[mbuff]) + '.' + '\n')
          mbuff += 1
          sbuff += 1
        else:
          output += (str(s[sbuff][1][1]) + ' to ' + str(s[sbuff][1][0]) + ' ' +
                     rightteam + ' on ' + str(map[mbuff]) + '.' + '\n')
          mbuff += 1
          sbuff += 1
      final_score = str(self.event()) + ' ' + str(
        self.round()) + '\n\n' + winner.lstrip() + '\n\n' + str(output)

    return f"{final_score}"


def live_matches():
  match = requester('https://www.vlr.gg/matches')
  m1 = match.find_all('div', class_='wf-card')
  matchlist = []
  for i in m1:
    m1link = i.find_all('a')
    for s in m1link:
      matchlist.append(s['href'])
  matchlist.pop(0)
  matchlist.pop(0)
  livelist = []

  # loop until you find 1 game that isnt live then break
  # all live games are going to be at the top so no point in looping through 32 games if only 1 is live
  for i in matchlist:
    game = requester('https://www.vlr.gg' + i)
    final = game.find('div', class_='match-header-vs-note').text.strip()
    if final == 'live':
      livelist.append('https://www.vlr.gg' + i)
    else:
      break
      # pass
  return livelist


def is_completed(matchurl):
  game = requester(matchurl)
  final = game.find('div', class_='match-header-vs-note').text.strip()
  if final == 'final':
    return True
  else:
    return False


def requester(url):
  htmlText = requests.get(url)
  return bs(htmlText.content, "lxml")
