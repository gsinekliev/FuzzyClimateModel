from collections import namedtuple


class Synop( object ):
    """
        Class to contain one synop report,
        will have only used fields for clusterization
        for now, could be extended later.
    """
    # TODO: add fields which will be used for clusterization.
    def __init__( self ):
        pass

    @staticmethod
    def aggregate( synops ):
        """ 
            Passing multiple Synop objects to aggregate them in one synop,
            so that it could be used for clusterization.
        """
        pass

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
        20012   2sTTT Dewpoint
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
        # TODO: write parser of one data line
        pass

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
    def get_cloud_base_of_lowest_cloud_seen( cls, iihVV ):
        """ h from iihVV -> h -- Cloud base of lowest cloud seen (meters above ground) in meters """
        CLOUD_BASE_OF_LOWEST_CLOUD_SEEN = {
            '0': ( 25.0, "0 to 50 m" ),
            '1': ( 75.0, "50 to 100 m" ),
            '2': ( 150.0, "100 to 200 m" ),
            '3': ( 250.0, "200 to 300 m" ),
            '4': ( 450.0, "300 to 600 m" ),
            '5': ( 800.0, "600 to 1000 m" ),
            '6': ( 1250.0, "1000 to 1500 m" ),
            '7': ( 1750.0, "1500 to 2000 m" ),
            '8': ( 2250.0, "2000 to 2500 m" ),
            '9': ( 2750.0, "above 2500 m" ),
            '/': ( None, "unknown " ),
        }
        return CLOUD_BASE_OF_LOWEST_CLOUD_SEEN[ iihVV[ 2 ] ] # if key error "Invalid cloud base of lowest cloud seen."

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
    def get_visibility( cls, iihVV ):
        """ vv from iihVV -> VV -- Visibility in km """
        vv = iihVV[ 3: ]
        if vv == '00' or vv == '90':
            return 0.025 # less than 0.1 km / less than 0.05 km
        if '01' <= vv and vv <= '50':
            return float( vv ) / 10

        if '56' <= vv and vv <= '80':
            return float( vv ) - 50

        if '81' <= vv and vv <= '88':
            return ( float( vv ) - 80 ) * 5 + 30

        if vv == '89' or vv == '99':
            return 100.0 # greater than 70 km / greater than 50 km

        if cls.VISIBILITY.has_key( vv ):
            return cls.VISIBILITY[ vv ]

        if vv == '//':
            return None # missing

        raise KeyError( "Invalid visibility" )

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
    def get_temperature( cls, osTTT ):
        """ TTT from 1sTTT -> s -- sign of temperature (0=positive, 1=negative)
                              TTT -- Temperature in .1 C """
        return ( 0.1 if osTTT[ 1 ] == '0' else -0.1 ) * float( osTTT[ 2: ] )

    @classmethod
    def get_dew_point( cls, tsTTT ):
        """ TTT from 2sTTT -> s -- sign of temperature (0=positive, 1=negative, 9 = RH)
                              TTT -- Dewpoint temperature in .1 C (if sign is 9, TTT is relative humidity) """
        if tsTTT[ 1 ] == '9':
            return float( tsTTT[ 2: ] ) # relative humidity

        return 0.1 * float( tsTTT[ 2: ] ) # dewpoint temperature

    @classmethod
    def get_station_pressure( cls, tPPPP ):
        """ PPPP from 3PPPP -> 3PPPP -- Station pressure in 0.1 mb (thousandths digit omitted, last digit can be slash, then pressure in full mb) """
        if tPPPP[ 4 ] == '/'
            return float( tPPPP[ 1:4 ] )

        return float( tPPPP[ 1: ] ) * 0.1

    @classmethod
    def _get_liquid_precipitation_amount( cls, RRR ):
        if '001' <= RRR and RRR <= '989':
            return float( RRR )
        elif '991' <= RRR and RRR <= '999':
            return ( float( RRR ) - 990 ) * 0.1
        else:
            return None

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
        """
        if precipation_indicator not in [ 0, 1, 2 ]:
            return None

        used_sRRRt          = sRRRt if precipation_indicator in [ 0, 1 ] else sRRRt_third_group
        LiquidPrecipitation = namedtuple( 'LiquidPrecipitation', [ 'amount', 'duration' ] )
        return LiquidPrecipitation( cls._get_liquid_precipitation_amount( used_sRRRt[ 1:4 ] ),
                                    cls._get_liquid_precipitation_duration( used_sRRRt[ 4 ] ) )
