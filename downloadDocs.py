import urllib
import urllib2
from bs4 import BeautifulSoup
import zipfile
import openpyxl
import os

def downloadDocs(baseUrl, meetingNumber):
    if meetingNumber[-1] == 'b':
        meetingNumber2 = meetingNumber[:-1] + '-BIS'
    else:
        meetingNumber2 = meetingNumber

    siteUrl = baseUrl + meetingNumber + '/Docs/'
    #siteUrl = 'http://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_AH/NR_AH_1706/Docs/'
    fileName_web = 'TDoc_List_Meeting_RAN1%23' + meetingNumber2 + '.xlsm'
    #fileName_web = 'TDoc_List_Meeting_RAN1-NR%232.xlsm'
    #fileName = 'TDoc_List_Meeting_RAN1-NR#2.xlsm'
    fileName = "TDoc_List_Meeting_RAN1#" + meetingNumber2 + '.xlsm'
    docURL = siteUrl + fileName_web
    if not os.path.exists(fileName):
        urllib.urlretrieve(docURL, fileName)

    wb = openpyxl.load_workbook(fileName)
    tDocList = wb.get_sheet_by_name('TDoc_List')
    nTdocs = 1
    while tDocList['A' + str(nTdocs)].value is not None:
        nTdocs += 1
    nTdocs -= 1

    name = [tDocList['A' + str(2)].value] * nTdocs
    agenda = [tDocList['L' + str(2)].value] * nTdocs
    agendaDes = [tDocList['M' + str(2)].value] * nTdocs
    agendaNameDes = [tDocList['M' + str(2)].value] * nTdocs

    for row in range(nTdocs):
        name[row] = tDocList['A' + str(row + 2)].value
        agenda[row] = tDocList['K' + str(row + 2)].value
        agendaDes[row] = tDocList['M' + str(row + 2)].value
        if tDocList['L' + str(row + 2)].value:
            agendaDes[row] = tDocList['L' + str(row + 2)].value.replace('>', 'GreaterThan').encode('ascii', 'ignore')
            agendaDes[row] = agendaDes[row].replace('<', 'LessThan').encode('ascii', 'ignore')
            agendaNameDes[row] = str(agenda[row]) + ' ' + str(agendaDes[row])
        else:
            #print agenda[row]
            if isinstance(agenda[row], basestring):
                agendaNameDes[row] = agenda[row].encode('utf8')
            else:
                agendaNameDes[row] = unicode(agenda[row]).encode('utf8')

            #agendaNameDes[row] = str(agenda[row])
    name_agenda = dict(zip(name, agenda))
    agendaDes = agenda + agendaDes
    name_agendaDes = dict(zip(name, agendaNameDes))

    agendaSet = set(agendaNameDes)
    for agendaItem in agendaSet:
        if agendaItem:
            if not os.path.exists(meetingNumber2 + '/' + agendaItem):
                os.makedirs(meetingNumber2 + '/' + agendaItem)

    try:
        webResponse = urllib2.urlopen(siteUrl, timeout=10)
    except urllib2.URLError, e:
        print "Oops, timed out?", e

    if webResponse is not None:
        docSoup = BeautifulSoup(webResponse, "lxml")
        docLinks = docSoup.findAll('a')
    for link in docLinks:
        if link.get('href') is not None:
            if (link['href'].find('/Docs/R1-') != -1) and (int(link['href'].split('-')[-1].split('.')[0]) > 1713404):
            #if (link['href'].find('/Docs/R1-') != -1):
                docURL = siteUrl + 'R1-' + str(link['href'].split('-')[-1].split('.')[0]) + '.zip'
                docName = 'R1-' + str(link['href'].split('-')[-1].split('.')[0])
                #if (str(name_agendaDes[docName])[:7] == '6.1.1.1'):
                if 1:
                    print docName
                    fileName = 'R1-' + str(link['href'].split('-')[-1].split('.')[0]) + '.zip'
                    fileNameLoc = './' + meetingNumber2 + '/zipFiles/' + fileName
                    if not os.path.exists('./' + meetingNumber2 + '/zipFiles'):
                        os.makedirs('./' + meetingNumber2 + '/zipFiles')
                    if not os.path.exists(fileNameLoc):
                        urllib.urlretrieve(docURL, fileNameLoc)
                    fh = open(fileNameLoc, 'rb')
                    z = zipfile.ZipFile(fh)
                    for zname in z.namelist():
                        if zname[-1] == '/':
                            if not os.path.exists('./' + meetingNumber2 + '/' + str(name_agendaDes[docName]) + '/' + zname):
                                os.makedirs('./' + meetingNumber2 + '/' + str(name_agendaDes[docName]) + '/' + zname)
                        else:
                            outfile = open('./' + meetingNumber2 + '/' + str(name_agendaDes[docName]) + '/' + zname, 'wb')
                            outfile.write(z.read(zname))
                            outfile.close()
                    fh.close()
    print "Main Thread Completed!!"
