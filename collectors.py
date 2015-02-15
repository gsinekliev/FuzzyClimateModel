import calendar
import json
import os
import re
import urllib2

from synop_parser import SynopParser, Synop, Normalizer, Attribute
import stations


MAX_RETRIES   = 5
SYNOP_HOUR    = '06'
RAW_FILE_NAME = os.getcwd() + '\\Data\\OgiMet-Raw\\{year}\\{month}\\{station}.txt'
FILE_NAME     = os.getcwd() + '\\Data\\OgiMet\\{year}\\{month}.json'
MONTH_NAMES   = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}


def get_synops( stations, month, year=2015 ):
    filename = FILE_NAME.format( year=year, month=month )
    if not os.access( filename, os.R_OK ):
        filedir  = os.path.dirname( filename )
        if not os.path.exists( filedir ):
            os.makedirs( filedir )

        result = { station: get_synop( station, month, year ) for station in stations }
        with open( filename, "w+" ) as f:
            file_result = { station: synop.to_dict() for station, synop in result.items() }
            json.dump( file_result, f, indent=4 )

    else:
        with open( filename, "r" ) as f:
            cached_result = { station: Synop.from_dict( synop_dict ) for station, synop_dict in json.load( f ).items() }

        cached_stations = cached_result.keys()
        changes_to_result = { station: get_synop( station, month, year ) for station in [ s for s in stations if s not in cached_stations ] }
        if changes_to_result:
            with open( filename, "w+") as f:
                cached_result.update( { station: get_synop( station, month, year ) for station in [ s for s in stations if s not in cached_stations ] } )
                json.dump( { station: synop.to_dict() for station, synop in cached_result.items() }, f, indent=4 )
        
        result = cached_result

    return result

def get_synop( station, month, year=2015, synop_hour=SYNOP_HOUR ):
    filename = RAW_FILE_NAME.format( year=str(year), month=MONTH_NAMES[ month ], station=station )
    if not os.access( filename, os.R_OK ):
        write_data_to_file( station, month, year )
    
    regex     = re.compile( r'^\d{5},\d{4},\d{2},\d{2},%s' % synop_hour )
    synops    = []
    full_list = []
    with open( filename, "r+" ) as f:
        for line in f.readlines():
            full_list.append( SynopParser.parse( line ) )
            if regex.match( line ):
                synops.append( SynopParser.parse( line ) )

    return Synop.aggregate( synops, full_list )

def write_data_to_file( station, month, year=2015, retry_num=0 ):
    """
        vars -> string, string (leading zero), int, int
        Function gets for each station monthly reports,
        converts them to Synop objects and aggregates
        them in one Synop object and write it in file.

        To get monthly reports calls:
        http://www.ogimet.com/cgi-bin/getsynop?block=<station_id>&begin=<year><month><start_day>0000&end=<year><month><end_day>2300
        returns reports for this station, each of them is on a new line.

        Report format:
        15614,      2015,01,08,06,00, AAXX   08061 15614 12970 50000 11132 21137 39629 40405 52001 60002 85030 333 11065 21144 47007 55053 70000 555 3/118 596//=
        15614,      2015,01,25,00,00, AAXX   25001 15614 11658 60000 10041 20024 39378 40084 54000 60001 71022 86800 333 10048 20036 555 589//=
        station_id, datetime,         separ, YYGGi IIiii iihVV Nddff 111 Group... and then other groups if available.
    """
    last_month_day = calendar.monthrange( year, int( month ) )[ 1 ]
    url_template = "http://www.ogimet.com/cgi-bin/getsynop?block={station}&begin={year}{month}010000&end={year}{month}{last_month_day}2300"
    filename = RAW_FILE_NAME.format( year=str(year), month=MONTH_NAMES[ month ], station=station )
    filedir  = os.path.dirname( filename )
    if not os.path.exists( filedir ):
        os.makedirs( filedir )

    with open( filename, "w+" ) as f:
        try:
            print 'CALLING for DATA'
            response = urllib2.urlopen( url_template.format( station=station, year=year, month=month, last_month_day=last_month_day ) )
            content  = response.read()
            f.write( content )
        except:
            if retry_num > MAX_RETRIES:
                raise

            print 'Retrying!!!'
            retry_num += 1
            write_data_to_file( station, month, retry_num )

if __name__ == '__main__':
    # get_data( stations.STATIONS_INFORMATION, 1 )
    
    # synop_data = '15614,2015,01,08,06,00,AAXX 08061 15614 12970 50000 11132 21137 39629 40405 52001 60002 85030 333 11065 21144 47007 55053 70000 555 3/118 596//='
    # synop_obj = SynopParser.parse( synop_data )
    # for k, v in vars( synop_obj ).items():
    #     print k, v

    # write_data_to_file( 15614, '01' )

    # synop_obj = get_synop( '15549', '01' )
    # for k, v in vars( synop_obj ).items():
    #     print k, v
    #     if isinstance( v, Attribute ):
    #         print 'Real value:', getattr( Normalizer, 'get_' + k , lambda *args, **kwargs: "BANICA S BOZA" )( v.value )

    # synop_obj = get_synop( '15549', '02' )
    # for k, v in vars( synop_obj ).items():
    #     print k, v
    #     if isinstance( v, Attribute ):
    #         print 'Real value:', getattr( Normalizer, 'get_' + k , lambda *args, **kwargs: "BANICA S BOZA" )( v.value )

    print get_synops( [ '15549', '15614' ], '01' )