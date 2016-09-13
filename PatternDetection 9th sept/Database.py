import MySQLdb, csv, sys
from classes import MeetingInfo,Position
def InitDatabase():
	conn = MySQLdb.connect (host = "localhost",user = "root", passwd = "",db = "AAMeetings",charset='utf8')
	return conn

def InsertMeeting(conn,OneMeeting):
	cur = conn.cursor()
	try:
	   cur.execute("""INSERT INTO meetinginformation(meetingday,meetingtime,meetingaddress,meetingurl,meetingcity,meetingX,meetingY,meetingwidth,meetingheight,meetingfulltext,meetingxpath) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(OneMeeting.mDay,OneMeeting.mTime,OneMeeting.mAddress,OneMeeting.mURL,OneMeeting.mCity,OneMeeting.mPosition.x,OneMeeting.mPosition.y,OneMeeting.mPosition.w,OneMeeting.mPosition.h,OneMeeting.mHTML,OneMeeting.mFirstTag))
	   conn.commit()
	except Exception as e:
		print "exception in db"+str(e)
		conn.rollback()