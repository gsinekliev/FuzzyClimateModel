from collections import namedtuple
from datetime import datetime, time, date
from numpy import array
from math import sqrt

Attribute = namedtuple( 'Attribute', [ 'name', 'value', 'weight' ] )


class Synop( object ):
    """
        Class to contain one synop report,
        will have only used fields for clusterization
        for now, could be extended later.
    """
    MISSING_ATTRIBUTE = lambda x: Attribute( x, None, 0.0 )

    # TODO: add fields which will be used for clusterization.
    def __init__( self, date_of_measurement,
                        time_of_measurement,
                        wmo_index,
                        cloud_base_of_lowest_cloud_seen=MISSING_ATTRIBUTE( 'Cloud base of lowest cloud seen' ),
                        visibility=MISSING_ATTRIBUTE( 'Visibility' ),
                        temperature=MISSING_ATTRIBUTE( 'Temperature' ),
                        dew_point=MISSING_ATTRIBUTE( 'Dew Point' ),
                        station_pressure=MISSING_ATTRIBUTE( 'Station Pressure' ),
                        precipitation=MISSING_ATTRIBUTE( 'Precipitation' ) ):
        """ Each attribute used for clusterization has weight. """
        self.date_of_measurement = date_of_measurement
        self.time_of_measurement = time_of_measurement
        self.wmo_index           = wmo_index

        self.cloud_base_of_lowest_cloud_seen = cloud_base_of_lowest_cloud_seen
        self.visibility                      = visibility
        self.temperature                     = temperature
        self.dew_point                       = dew_point
        self.station_pressure                = station_pressure
        self.precipitation                   = precipitation

    def to_dict( self ):
        result = {}
        for key in self.keys():
            value = getattr( self, key )
            if isinstance( value, Attribute ):
                result[ key ] = value.__dict__
            elif isinstance( value, date ):
                result[ key ] = [ 'date', value.year, value.month, value.day ]
            elif isinstance( value, time ):
                result[ key ] = [ 'time', value.hour ]
            else: 
                result[ key ] = value

        return result

    @staticmethod
    def from_dict( loaded_dict ):
        formated_data = {}
        for k, v in loaded_dict.items():
            if isinstance( v, dict ):
                formated_data[ k ] = Attribute( **v )
            elif isinstance( v, list ):
                formated_data[ k ] = date( *v[ 1: ] ) if v[ 0 ] == 'date' else time( *v[ 1: ] )
            else:
                formated_data[ k ] = v
        return Synop( **formated_data )

    def keys( self ):
        return [ 'date_of_measurement', 'time_of_measurement', 'wmo_index', 'cloud_base_of_lowest_cloud_seen',
                 'visibility', 'temperature', 'dew_point', 'station_pressure', 'precipitation' ]

    def real_vector( self ):
        return Normalizer.get_unnormed_vector( self.vector() )

    def normalized_vector( self ):
        unnormalized_vector = self.vector()
        denom = sqrt( sum( map( lambda x: x * x, unnormalized_vector ) ) )
        return array( [ item / denom for item in unnormalized_vector ] )

    def vector( self ):
        return [ getattr( self, attribute ).value for attribute in Synop.attributes() ]

    @staticmethod
    def attributes():
        return [ 'cloud_base_of_lowest_cloud_seen', 'visibility', 'temperature', 'dew_point', 'station_pressure', 'precipitation' ]

    def attributes_dict(self):
        return {attribute: getattr( self, attribute ).value for attribute in Synop.attributes()}

    @staticmethod
    def aggregate( synops, full_list_synops ):
        """ 
            Passing multiple Synop objects to aggregate them in one synop,
            so that it could be used for clusterization.
            Using this for the same time_of_measurement and wmo_index!
        """
        result_synop = Synop( date_of_measurement=None,
                              time_of_measurement=synops[ 0 ].time_of_measurement,
                              wmo_index=synops[ 0 ].wmo_index )

        filt_synops_by_cloud_base = [ s for s in synops if s.cloud_base_of_lowest_cloud_seen.weight != 0.0 ]
        result_synop.cloud_base_of_lowest_cloud_seen = Attribute( 'Cloud base of lowest cloud seen',
                                                                  sum( s.cloud_base_of_lowest_cloud_seen.value for s in filt_synops_by_cloud_base ) / len( filt_synops_by_cloud_base ),
                                                                  sum( s.cloud_base_of_lowest_cloud_seen.weight for s in filt_synops_by_cloud_base ) / len( filt_synops_by_cloud_base ) )

        filt_synops_by_visibility = [ s for s in synops if s.visibility.weight != 0.0 ]
        result_synop.visibility                      = Attribute( 'Visibility',
                                                                  sum( s.visibility.value for s in filt_synops_by_visibility ) / len( filt_synops_by_visibility ),
                                                                  sum( s.visibility.weight for s in filt_synops_by_visibility ) / len( filt_synops_by_visibility ) )

        filt_synops_by_temperature = [ s for s in synops if s.temperature.weight != 0.0 ]
        result_synop.temperature                     = Attribute( 'Temperature',
                                                                  sum( s.temperature.value for s in filt_synops_by_temperature ) / len( filt_synops_by_temperature ),
                                                                  sum( s.temperature.weight for s in filt_synops_by_temperature ) / len( filt_synops_by_temperature ) )

        filt_synops_by_dew_point = [ s for s in synops if s.dew_point.weight != 0.0 ]
        result_synop.dew_point                       = Attribute( 'Dew Point',
                                                                  sum( s.dew_point.value for s in filt_synops_by_dew_point ) / len( filt_synops_by_dew_point ),
                                                                  sum( s.dew_point.weight for s in filt_synops_by_dew_point ) / len( filt_synops_by_dew_point ) )

        filt_synops_by_station_pressure = [ s for s in synops if s.station_pressure.weight != 0.0 ]
        result_synop.station_pressure                = Attribute( 'Station Pressure',
                                                                  sum( s.station_pressure.value for s in filt_synops_by_station_pressure ) / len( filt_synops_by_station_pressure ),
                                                                  sum( s.station_pressure.weight for s in filt_synops_by_station_pressure ) / len( filt_synops_by_station_pressure ) )

        filt_synops_by_precipitation = [ s for s in full_list_synops or synops if s.precipitation.weight != 0.0 ]
        result_synop.precipitation                   = Attribute( 'Precipitation',
                                                                  sum( s.precipitation.value for s in filt_synops_by_precipitation ),
                                                                  sum( s.precipitation.weight for s in filt_synops_by_precipitation ) / len( filt_synops_by_precipitation ) )
        print "__________________LEWTF____________________________"
        print result_synop.wmo_index
        print result_synop.cloud_base_of_lowest_cloud_seen
        print result_synop.visibility
        return result_synop

    def to_JSON( self ):
        return json.dumps( self, default=lambda o: o.__dict__, sort_keys=True, indent=4 )

MAX_CLOUD_BASE_OF_LOWEST_CLOUD_SEEN = 2750.0
MAX_VISIBILITY = 75.0
MIN_TEMPERATURE = -40.0
MAX_TEMPERATURE = 40.0
MIN_DEW_POINT = -40.0
MAX_DEW_POINT = 40.0
MAX_STATION_PRESSURE = 1000.0
MAX_PRECIPITATION = 1000.0


class Normalizer( object ):
    @staticmethod
    def get_unnormed_vector( vector ):
        attributes = [ 'cloud_base_of_lowest_cloud_seen', 'visibility', 'temperature', 'dew_point', 'station_pressure', 'precipitation' ]
        return [ getattr( Normalizer, 'get_' + attributes[ ind ] )( item ) for ind, item in enumerate( vector ) ]        

    @staticmethod
    def get_cloud_base_of_lowest_cloud_seen( norm_cloud_base ):
        return norm_cloud_base * MAX_CLOUD_BASE_OF_LOWEST_CLOUD_SEEN

    @staticmethod
    def get_visibility( norm_visibility ):
        return norm_visibility * MAX_VISIBILITY

    @staticmethod
    def get_temperature( norm_temp ):
        delta_temperature = MAX_TEMPERATURE - MIN_TEMPERATURE
        return norm_temp * delta_temperature + MIN_TEMPERATURE

    @staticmethod
    def get_dew_point( norm_dew_point ):
        delta_dew_point = MAX_DEW_POINT - MIN_DEW_POINT
        return norm_dew_point * delta_dew_point + MIN_DEW_POINT

    @staticmethod
    def get_station_pressure( norm_station_pressure ):
        return norm_station_pressure * MAX_STATION_PRESSURE

    @staticmethod
    def get_precipitation( norm_precipitation ):
        return norm_precipitation * MAX_PRECIPITATION


class SynopParser( object ):
    """
        Parser for SYNOP Data Format (FM-12)

        Only part of '111 Group - Land Observations' implemented.
        Raises KeyError for missing data.

        IIiii or IIIII YYGGi 99LLL QLLLL
        iihVV Nddff 00fff 1sTTT 2sTTT 3PPPP 4PPPP 5appp 6RRRt 7wwWW 8NCCC 9GGgg -> 111 Group
        222Dv 0sTTT 1PPHH 2PPHH 3dddd 4PPHH 5PPHH 6IEER 70HHH 8aTTT             -> 222 Group
        333 0.... 1sTTT 2sTTT 3Ejjj 4Esss 5jjjj jjjjj 6RRRt 7RRRR 8Nchh 9SSss   -> 333 Group

        Example data:
        201502100900 -> datetime
        AAXX
        10094   YYGGi
        07146   The WMO number of the station
        24556   iihVV
        80204   Nddff
                00fff (optional) -> wind speed if value greater than 100
        10030   1sTTT Temperature
        20012   2sTTT Dew Point
        30125   3PPPP Station pressure in 0.1 mb (thousandths digit omitted, last digit can be slash, then pressure in full mb) 
        40328   4PPPP Sea level pressure in 0.1 mb (thousandths digit omitted, last digit can be slash, then pressure in full mb) or \
                      Geopotential of nearest mandatory pressure level (use for high altitude stations where sea level pressure reduction is not accurate)
        51006   5appp Pressure tendency over 3 hours
                6RRRt Liquid precipitation
        700//   7wwWW Present and past weather
                8NCCC Cloud type information
                9GGgg Time of observation in hours and minutes

                222 Group - Sea Surface Observations

        333     333 Group - Special / Climatological Data
        4/000   4Esss -- Snow depth missing value /
        60007   6RRRt Liquid precipitation
        90710   9SSss -- Supplementary information 
        91107   9SSss -- Supplementary information 

        555     not documented in FM-12
        60005   not documented in FM-12
        =     end symbol of data
    """

    @classmethod
    def parse( cls, data ):
        """ Parsing 15614,2015,01,08,06,00,AAXX 08061 15614 12970 50000 11132 21137 39629 40405 52001 60002 85030 333 11065 21144 47007 55053 70000 555 3/118 596//= to Synop object """
        splitted_data = data.split( ',' )
        result_synop  = Synop( date_of_measurement=date( *map( int, splitted_data[ 1:4 ] ) ), 
                               time_of_measurement=time( *map( int, splitted_data[ 4:6 ] ) ),
                               wmo_index=int( splitted_data[ 0 ] ) )
        observation   = splitted_data[ 6 ].split( ' ' )

        if observation[ 3 ].startswith( "NIL" ) or observation[ 3 ].startswith( "AAXX" ):
            return result_synop

        result_synop.cloud_base_of_lowest_cloud_seen = Attribute( 'Cloud base of lowest cloud seen', *cls.get_normalized_cloud_base_of_lowest_cloud_seen( observation[ 3 ] ) )
        result_synop.visibility                      = Attribute( 'Visibility', *cls.get_normalized_visibility( observation[ 4 ] ) )
        for ind, element in enumerate( observation[ 5: ] ):
            if element.startswith( '222' ) or element.startswith( '333' ) or element.startswith( 'AAXX' ) or element in [ '333', '444', '555' ]:
                break

            if '=' in element:
                element = element.split( '=' )[0]

            if element.startswith( '1' ):
                result_synop.temperature = Attribute( 'Temperature', *cls.get_normalized_temperature( element ) )

            if element.startswith( '2' ):
                result_synop.dew_point = Attribute( 'Dew Point', *cls.get_normalized_dew_point( element ) )

            if element.startswith( '3' ):
                result_synop.station_pressure = Attribute( 'Station Pressure', *cls.get_normalized_station_pressure( element ) )

            if element.startswith( '6' ):
                result_synop.precipitation = Attribute( 'Precipitation', *cls.get_normalized_first_group_liquid_precipitation( element ) )
 
        return result_synop

    # WARNING NOT ALL ATTRIBUTES BELOW ARE MADE TO RETURN THE ATTRIBUTE_WEIGHT
    @classmethod
    def get_wind_type_indicator( cls, YYGGi ):
        """ i from YYGGi -> iw -- Wind type indicator """
        WIND_TYPE_INDICATORS = {
            '0': 'm/s',   # (estimated)
            '1': 'm/s',   # (from anemometer)
            '2': 'knots', # (estimated)
            '3': 'knots', # (from anemometer) 
        }
        return WIND_TYPE_INDICATORS[ YYGGi[ 4 ] ] # if key error "Invalid wind type indicator."

    @classmethod
    def get_precipation_indicator( cls, iihVV ):
        """ first i from iihVV -> iR -- Precipitation indicator """
        PRECIPATION_INDICATOR = {
            '0': "Precipitation in groups 1 and 3",
            '1': "Precipitation reported in group 1 only",
            '2': "Precipitation reported in group 3 only",
            '3': "Precipitation omitted, no precipitation",
            '4': "Precipitation omitted, no observation",
        }
        return PRECIPATION_INDICATOR[ iihVV[ 0 ] ] # if key error "Invalid precipitation indicator."

    @classmethod
    def get_station_type( cls, iihVV ):
        """ second i from iihVV -> ix -- Station type and present and past weather indicator """
        STATION_TYPE = {
            '1': "manned station -- weather group included",
            '2': "manned station -- omitted, no significant weather",
            '3': "manned station -- omitted, no weather observation",
            '4': "automated station -- weather group included (see automated weather codes 4677 and 4561)",
            '5': "automated station -- omitted, no significant weather",
            '6': "automated station -- omitted, no weather observation",
            '7': "automated station -- weather group included (see automated weather codes 4680 and 4531)",
        }
        return STATION_TYPE[ iihVV[ 1 ] ] # if key error "Invalid station type."

    @classmethod
    def get_normalized_cloud_base_of_lowest_cloud_seen( cls, iihVV ):
        result = cls.get_cloud_base_of_lowest_cloud_seen( iihVV )
        if result[ 1 ] == 0.0:
            return result

        return result[ 0 ] / MAX_CLOUD_BASE_OF_LOWEST_CLOUD_SEEN, 1.0

    @classmethod
    def get_cloud_base_of_lowest_cloud_seen( cls, iihVV ):
        """ h from iihVV -> h -- Cloud base of lowest cloud seen (meters above ground) in meters """
        ATTRIBUTE_WEIGHT = 1.0
        CLOUD_BASE_OF_LOWEST_CLOUD_SEEN = {
            '0': 25.0, # "0 to 50 m" ),
            '1': 75.0, # "50 to 100 m" ),
            '2': 150.0, # "100 to 200 m" ),
            '3': 250.0, # "200 to 300 m" ),
            '4': 450.0, # "300 to 600 m" ),
            '5': 800.0, # "600 to 1000 m" ),
            '6': 1250.0, # "1000 to 1500 m" ),
            '7': 1750.0, # "1500 to 2000 m" ),
            '8': 2250.0, # "2000 to 2500 m" ),
            '9': 2750.0, # "above 2500 m" ),
            # '/': None, # "unknown" ),
        }

        # if key error "Invalid cloud base of lowest cloud seen."
        return ( None, 0.0 ) if iihVV[ 2 ] == '/' else ( CLOUD_BASE_OF_LOWEST_CLOUD_SEEN[ iihVV[ 2 ] ], ATTRIBUTE_WEIGHT )

    VISIBILITY = {
        '91': 0.05,
        '92': 0.2,
        '93': 0.5,
        '94': 1.0,
        '95': 2.0,
        '96': 4.0,
        '97': 10.0,
        '98': 20.0,
    }

    @classmethod
    def get_normalized_visibility( cls, iihVV ):
        result = cls.get_visibility( iihVV )
        if result[ 1 ] == 0.0:
            return result

        return result[ 0 ] / MAX_VISIBILITY, result[ 1 ]

    @classmethod
    def get_visibility( cls, iihVV ):
        """ vv from iihVV -> VV -- Visibility in km """
        ATTRIBUTE_WEIGHT = 1.0
        vv = iihVV[ 3: ]
        if vv == '00' or vv == '90':
            return 0.025, ATTRIBUTE_WEIGHT # less than 0.1 km / less than 0.05 km
        if '01' <= vv and vv <= '50':
            return float( vv ) / 10, ATTRIBUTE_WEIGHT

        if '56' <= vv and vv <= '80':
            return float( vv ) - 50, ATTRIBUTE_WEIGHT

        if '81' <= vv and vv <= '88':
            return ( float( vv ) - 80 ) * 5 + 30, ATTRIBUTE_WEIGHT

        if vv == '89' or vv == '99':
            return 75.0, ATTRIBUTE_WEIGHT # greater than 70 km / greater than 50 km

        if cls.VISIBILITY.has_key( vv ):
            return cls.VISIBILITY[ vv ], ATTRIBUTE_WEIGHT

        # if vv == '//':
        return None, 0.0 # missing

        # raise KeyError( "Invalid visibility" )

    @classmethod
    def get_total_cloud_cover( cls, Nddff ):
        """ N from Nddff -> N -- Total cloud cover in percentage """
        TOTAL_CLOUD_COVER = {
            '0': 0.0,  # clear
            '1': 0.125,
            '2': 0.25,
            '3': 0.375,
            '4': 0.5,
            '5': 0.625,
            '6': 0.75,
            '7': 0.875,
            '8': 1.0,  # overcast
            '9': None, # sky obscured
            '/': None, # no observation 
        }
        return TOTAL_CLOUD_COVER[ Nddff[ 0 ] ] # if key error "Invalid total cloud cover"

    @classmethod
    def get_wind_direction( cls, Nddff ):
        """ dd from Nddff -> dd -- wind direction in 10s of degrees """
        return float( Nddff[ 1:3 ] ) * 10

    @classmethod
    def get_wind_speed( cls, Nddff, zzfff=None ):
        """ ff  from Nddff -> ff -- wind speed in units determined by wind type indicator (see above) or
            fff from 00fff -> fff -- wind speed if value greater than 100 """
        if zzfff is not None: # optional in synop data
            return float( zzfff[ 2: ] )

        return float( Nddff[ 3: ] )

    @classmethod
    def get_normalized_temperature( cls, osTTT ):
        result = cls.get_temperature( osTTT )
        if result[ 1 ] == 0.0:
            return result

        delta_temperature = MAX_TEMPERATURE - MIN_TEMPERATURE
        return ( result[ 0 ] - MIN_TEMPERATURE ) / delta_temperature, result[ 1 ]

    @classmethod
    def get_temperature( cls, osTTT ):
        """ TTT from 1sTTT -> s -- sign of temperature (0=positive, 1=negative)
                              TTT -- Temperature in .1 C """
        if '/' in osTTT:
            return None, 0.0

        return ( 0.1 if osTTT[ 1 ] == '0' else -0.1 ) * float( osTTT[ 2: ] ), 1.0

    @classmethod
    def get_normalized_dew_point( cls, tsTTT ):
        result = cls.get_dew_point( tsTTT )
        if result[ 1 ] == 0.0:
            return result

        delta_dew_point = MAX_DEW_POINT - MIN_DEW_POINT
        return ( result[ 0 ] - MIN_DEW_POINT ) / delta_dew_point, result[ 1 ]

    @classmethod
    def get_dew_point( cls, tsTTT ):
        """ TTT from 2sTTT -> s -- sign of temperature (0=positive, 1=negative, 9 = RH)
                              TTT -- Dewpoint temperature in .1 C (if sign is 9, TTT is relative humidity) """
        ATTRIBUTE_WEIGHT = 1.0
        if '/' in tsTTT:
            return None, 0.0

        if tsTTT[ 1 ] == '9':
            return float( tsTTT[ 2: ] ), 0.0 # relative humidity

        return ( 0.1 if tsTTT[ 1 ] == '0' else -0.1 ) * float( tsTTT[ 2: ] ), 1.0 # dewpoint temperature

    @classmethod
    def get_normalized_station_pressure( cls, tPPPP ):
        result = cls.get_station_pressure( tPPPP )
        if result[ 1 ] == 0.0:
            return result

        return result[ 0 ] / MAX_STATION_PRESSURE, result[ 1 ]

    @classmethod
    def get_station_pressure( cls, tPPPP ):
        """ PPPP from 3PPPP -> 3PPPP -- Station pressure in 0.1 mb (thousandths digit omitted, last digit can be slash, then pressure in full mb) """
        ATTRIBUTE_WEIGHT = 1.0
        if '/' in tPPPP[ 2:4 ]:
            return None, 0.0

        if tPPPP[ 4 ] == '/':
            return float( tPPPP[ 1:4 ] ), ATTRIBUTE_WEIGHT

        if tPPPP[ 1 ] == '/':
            return float( tPPPP[ 2:5 ] ), ATTRIBUTE_WEIGHT

        return float( tPPPP[ 1: ] ) * 0.1, ATTRIBUTE_WEIGHT

    @classmethod
    def _get_liquid_precipitation_amount( cls, RRR ):
        if '000' <= RRR and RRR <= '989':
            return float( RRR ), 1.0
        elif '991' <= RRR and RRR <= '999':
            return ( float( RRR ) - 990 ) * 0.1, 1.0
        else:
            return None, 0.0

    @classmethod
    def _get_liquid_precipitation_duration( cls, t ):
        LIQUID_PRECIPITATION_DURATION = {
            '1': 6,
            '2': 12,
            '3': 18,
            '4': 24,
            '5': 1,
            '6': 2,
            '7': 3,
            '8': 9,
            '9': 15,
            '/': 24,
        }
        return LIQUID_PRECIPITATION_DURATION[ t ]

    @classmethod 
    def get_liquid_precipitation( cls, sRRRt, sRRRt_third_group, precipation_indicator ):
        """ RRRt from 6RRRt of Group 111 or 333 -> RRR -- Precipitation amount in mm 
                                                   t -- Duration over which precipitation amount measured 
            note: weight of attribute is in amount.
        """
        if precipation_indicator not in [ 0, 1, 2 ]:
            return None

        used_sRRRt          = sRRRt if precipation_indicator in [ 0, 1 ] else sRRRt_third_group
        LiquidPrecipitation = namedtuple( 'LiquidPrecipitation', [ 'amount', 'duration' ] )
        return LiquidPrecipitation( cls._get_liquid_precipitation_amount( used_sRRRt[ 1:4 ] ),
                                    cls._get_liquid_precipitation_duration( used_sRRRt[ 4 ] ) )

    @classmethod
    def get_normalized_first_group_liquid_precipitation( cls, sRRRt ):
        result = cls.get_first_group_liquid_precipitation( sRRRt )
        if result[ 1 ] == 0.0:
            return result

        return result[ 0 ] / MAX_PRECIPITATION, result[ 1 ]


    @classmethod
    def get_first_group_liquid_precipitation( cls, sRRRt ):
        """ RRRt from 6RRRt of Group 111 -> RRR -- Precipitation amount in mm 
                                            t -- Duration over which precipitation amount measured 
        """
        return cls._get_liquid_precipitation_amount( sRRRt[ 1:4 ] )
