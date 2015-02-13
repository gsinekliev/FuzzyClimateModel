import stations


def get_data( stations, month ):
	"""
		Function gets for each station monthly reports,
		converts them to Synop objects and aggregates
		them in one Synop object and write it in file.

		To get monthly reports calls:
		http://www.ogimet.com/cgi-bin/getsynop?block=<station_id>&begin=<year><month><start_day>0000&end=<year><month><end_day>2300
		returns reports for this station, each of them is on a new line.

		Report format:
		15614,		2015,01,25,00,00, AAXX   25001 15614 11658 60000 10041 20024 39378 40084 54000 60001 71022 86800 333 10048 20036 555 589//=
		station_id, datetime, 		  separ, YYGGi IIiii iihVV Nddff 111 Group... and then other groups if available.
	"""
	pass


if __name__ == '__main__':
    get_data( stations.STATIONS_INFORMATION, 1 )