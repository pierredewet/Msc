from app import db

# coding: utf-8
from sqlalchemy import ARRAY, Boolean, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata


class CrimeStat(Base):
    __tablename__ = 'crime_stat'

    lsoa = Column(String(9), primary_key=True, unique=True)
    asb = Column(Integer, server_default=text("0"))
    bicycle_theft = Column(Integer, server_default=text("0"))
    burglary = Column(Integer, server_default=text("0"))
    damage_arson = Column(Integer, server_default=text("0"))
    drugs = Column(Integer, server_default=text("0"))
    other_crime = Column(Integer, server_default=text("0"))
    other_theft = Column(Integer, server_default=text("0"))
    weapon_possession = Column(Integer, server_default=text("0"))
    public_order = Column(Integer, server_default=text("0"))
    robbery = Column(Integer, server_default=text("0"))
    shoplifting = Column(Integer, server_default=text("0"))
    theft_from_person = Column(Integer, server_default=text("0"))
    vehicle_crime = Column(Integer, server_default=text("0"))
    sex_offense = Column(Integer, server_default=text("0"))
    total = Column(Integer)
    serious_tot = Column(Integer)
    asb_tot = Column(Integer)
    theft_tot = Column(Integer)
    totale_average = Column(Integer)
    serious_crime_average = Column(Integer)
    asb_average = Column(Integer)
    theft_average = Column(Integer)


class DentalPrac(Base):
    __tablename__ = 'dental_prac'

    _org_code = Column('\ufefforg_code', Text, primary_key=True)
    name = Column(Text)
    addr1 = Column(Text)
    addr2 = Column(Text)
    addr3 = Column(Text)
    addr4 = Column(Text)
    addr5 = Column(Text)
    postcode = Column(ForeignKey('pcode.code'), index=True)
    status = Column(Text)
    subtype = Column(Text)
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))

    pcode = relationship('Pcode')


class DeprivationByLsoa(Base):
    __tablename__ = 'deprivation_by_lsoa'

    LSOA_code = Column('LSOA code', String(9), primary_key=True)
    LSOA_Name = Column('LSOA Name', Text)
    Index_of_Multiple_Deprivation_Rank = Column('Index of Multiple Deprivation Rank', Integer)
    Index_of_Multiple_Deprivation_Decile = Column('Index of Multiple Deprivation Decile', Integer)
    income_rank = Column(Integer)
    income_decile = Column(Integer)
    income_score = Column(Numeric)
    employment_rank = Column(Integer)
    employment_decile = Column(Integer)
    employment_score = Column(Numeric)
    education_rank = Column(Integer)
    education_decile = Column(Integer)
    health_rank = Column(Integer)
    health_decile = Column(Integer)
    crime_rank = Column(Integer)
    crime_decile = Column(Integer)
    barriers_rank = Column(Integer)
    barriers_decile = Column(Integer)
    environment_rank = Column(Integer)
    environment_decile = Column(Integer)


t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)


t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


class GpSurgery(Base):
    __tablename__ = 'gp_surgeries'

    org_code = Column(String(10), primary_key=True, unique=True)
    name = Column(Text)
    addr1 = Column(Text)
    addr2 = Column(Text)
    addr3 = Column(Text)
    addr4 = Column(Text)
    addr5 = Column(Text)
    postcode = Column(ForeignKey('pcode.code'), nullable=False, unique=True)
    opendate = Column(Date)
    telno = Column(Text)
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))
    tot_patients = Column(Integer)
    tot_female = Column(Integer)
    tot_male = Column(Integer)

    pcode = relationship('Pcode')


class HouseholdPoverty(Base):
    __tablename__ = 'household_poverty'

    msoa_code = Column(String(9), primary_key=True, unique=True)
    msoa_name = Column(Text)
    la_code = Column(Text)
    la_name = Column(Text)
    region_code = Column(Text)
    region_name = Column(Text)
    household_pov = Column(Numeric(3, 1))
    household_pov_95_lower = Column(Numeric(3, 1))
    household_pov_95_upper = Column(Numeric(3, 1))


class LonStation(Base):
    __tablename__ = 'lon_stations'

    station_name = Column(String(50), primary_key=True, unique=True)
    lat = Column(Numeric(9, 6), nullable=False)
    lng = Column(Numeric(9, 6), nullable=False)
    zones = Column(String(25))
    postcode = Column(String(9), nullable=False, unique=True)


t_mv_annual_outcode_property_price = Table(
    'mv_annual_outcode_property_price', metadata,
    Column('year', Integer),
    Column('outcode', Text),
    Column('annual_avg', Integer)
)


t_mv_annual_property_price_avg = Table(
    'mv_annual_property_price_avg', metadata,
    Column('year', Integer),
    Column('annual_avg', Integer)
)


class Pcode(Base):
    __tablename__ = 'pcode'

    code = Column(String(9), primary_key=True, unique=True)
    lat = Column(Numeric(9, 6), nullable=False)
    lng = Column(Numeric(9, 6), nullable=False)
    county = Column(Text)
    district = Column(Text)
    ward = Column(Text)
    dist_code = Column(String(9))
    ward_code = Column(String(9))
    county_code = Column(String(9))
    lsoa = Column(ForeignKey('population_by_lsoa.lsoa'), index=True)
    msoa = Column(ForeignKey('household_poverty.msoa_code'))
    msoa_description = Column(Text)
    old_ward_code = Column(String(9))
    green_space_pc = Column(Numeric(4, 2))
    nearest_gp = Column(Numeric)
    nearest_nursery = Column(Numeric(7, 5))
    nursery_religious = Column(Text)
    nearest_primary = Column(Numeric(7, 5))
    primary_religious = Column(Text)
    nearest_secondary = Column(Numeric(7, 5))
    secondary_religious = Column(Text)
    crime_lvl = Column(Integer)
    imd_rank = Column(Integer)
    imd_decile = Column(Integer)
    nearest_tube_train = Column(Numeric(7, 5))

    population_by_lsoa = relationship('PopulationByLsoa', primaryjoin='Pcode.lsoa == PopulationByLsoa.lsoa')
    household_poverty = relationship('HouseholdPoverty', primaryjoin='Pcode.msoa == HouseholdPoverty.msoa_code')


class PopulationByLsoa(Base):
    __tablename__ = 'population_by_lsoa'

    lsoa = Column(String(9), primary_key=True, unique=True)
    tot_pop = Column(Integer)
    children_0_15 = Column(Integer)
    gen_pop_16_59 = Column(Integer)
    old_pop_60_plus = Column(Integer)
    working_pop = Column(Numeric)


class PropertyPrice(Base):
    __tablename__ = 'property_price'

    guid = Column(String(40), primary_key=True, unique=True)
    price = Column(Integer, index=True)
    date_sold = Column(DateTime, index=True)
    postcode = Column(ForeignKey('pcode.code'), index=True)
    f1 = Column(String(5))
    f2 = Column(String(5))
    f3 = Column(String(5))
    house_name_no = Column(String(50))
    addr2 = Column(String(50))
    addr3 = Column(String(50))
    addr4 = Column(String(50))
    addr5 = Column(String(50))
    town = Column(String(50))
    county = Column(String(50))
    a1 = Column(String(10))
    a2 = Column(String(10))

    pcode = relationship('Pcode')


class SchoolOfsted(Base):
    __tablename__ = 'school_ofsted'

    url = Column(Text)
    urn = Column(Integer, primary_key=True)
    Total_pupils = Column('Total pupils', Integer)
    Overall_effectiveness = Column('Overall effectiveness', Integer)


class School(SchoolOfsted):
    __tablename__ = 'school'

    urn = Column(ForeignKey('school_ofsted.urn'), primary_key=True, unique=True)
    local_authority_name = Column(String, nullable=False)
    local_authority_code = Column(String, nullable=False)
    establishment_no = Column(String, nullable=False)
    establishment_name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    locality = Column(String, nullable=False)
    addr3 = Column(String, nullable=False)
    town = Column(String, nullable=False)
    county = Column(String, nullable=False)
    postcode = Column(ForeignKey('pcode.code'), nullable=False, index=True)
    type = Column(String, nullable=False)
    statutory_highest_age = Column(String, nullable=False)
    statutory_lowest_age = Column(String, nullable=False)
    has_boarders = Column(String, nullable=False)
    has_sixth_form = Column(String, nullable=False)
    ukprn = Column(String, nullable=False)
    phase = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    religious = Column(String, nullable=False)
    religious_ethos = Column(String, nullable=False)
    admin_policy = Column(String, nullable=False)
    website = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    head_teacher = Column(String, nullable=False)
    status = Column(String, nullable=False)
    open_date = Column(String, nullable=False)
    constituency_code = Column(String, nullable=False)
    constituency_name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))

    pcode = relationship('Pcode')
