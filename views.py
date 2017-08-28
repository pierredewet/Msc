from app import app, session
from models import *
from flask import render_template, flash, redirect, url_for, request, jsonify
import json
import requests


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/deprivationmap', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        querydata = request.form
        lookup_sql = text(" SELECT "
                          " p.code, "
                          " p.lat, "
                          " p.lng "
                          " FROM pcode p "
                          " WHERE crime_lvl < :crime "
                          " AND ( "
                          " nearest_primary <= :school OR "
                          " nearest_nursery <= :school OR "
                          " nearest_secondary <= :school "
                          " ) "
                          " AND nearest_gp <= :gp "
                          " AND nearest_tube_train < :transport "
                          " AND green_space_pc > :green "
                          " ORDER BY imd_rank DESC "
                          " LIMIT 20"
                          )

    # Query Nursery schools
        try:
            rp = session.execute(lookup_sql, {'crime': querydata['crime'], 'school': querydata['school'], 'gp': querydata['doctor'], 'transport': querydata['transport'], 'green': querydata['greenspace']})
            lookup_rp = rp.fetchall()
            postcodes = lookup_rp
        except NoResultFound:
            flash('No postcode matches found')
            return redirect(url_for('index'))

        return render_template('map.html', postcodes=postcodes)
    else:
        return redirect(url_for('index'))


@app.route('/myhood/', methods=['GET', 'POST'])
def myhood():
        postcode = request.form['postcode']
        try:
            core_details = session.query(Pcode).filter_by(code=postcode).one()
        except NoResultFound:
            flash('No postcode records found for that search')
            return redirect(url_for('index'))

        # Deprivation data
        try:
            deprivation = session.query(DeprivationByLsoa).filter_by(LSOA_code=core_details.lsoa).first()
        except NoResultFound:
            flash('No deprivation records found for that search')

        # Poverty data
        try:
            poverty = session.query(HouseholdPoverty).filter_by(msoa_code=core_details.msoa).first()
        except NoResultFound:
            flash('No Poverty records found for that search')

        # Population data extract
        try:
            population = session.query(PopulationByLsoa).filter_by(lsoa=core_details.lsoa).one()
        except NoResultFound:
            flash('No population records found for that search')
        avg_pop = session.query(func.avg(PopulationByLsoa.tot_pop).label('avg_pop')).scalar()

        # Crime data extract
        try:
            crime_data = session.query(CrimeStat).filter_by(lsoa=core_details.lsoa).first()
        except NoResultFound:
            crime_data = 0
            flash('No crime records found for that search')

        school_sql = text("SELECT "
                          " s.establishment_name,"
                          " s.street,"
                          " s.town,"
                          " s.postcode,"
                          " s.website,"
                          " s.tel,"
                          " s.head_teacher,"
                          " s.type,"
                          " s.gender,"
                          " s.religious,"
                          " s.phase,"
                          " so.url,"
                          " s.lat, "
                          " s.lng, "
                          " so.\"Overall effectiveness\" AS ranking, "
                          " ST_DISTANCE_SPHERE(st_point(:x, :y),st_point(s.lng, s.lat)) AS \"Distance\""
                          " FROM school s"
                          " JOIN school_ofsted so"
                          " ON so.urn = s.urn"
                          " WHERE phase IN (:phase, 'Not applicable')"
                          " ORDER BY \"Distance\" asc"
                          " LIMIT 1"
                          )
        # Query for GP surgeries
        gp_sql = text("SELECT "
                      " name, "
                      " addr1, "
                      " addr2, "
                      " addr3, "
                      " postcode, "
                      " telno,"
                      " lat,"
                      " lng,"
                      " tot_patients,"
                      " ST_DISTANCE_SPHERE(st_point(:x, :y),st_point(gp.lng, gp.lat)) AS \"Distance\""
                      " FROM gp_surgeries gp "
                      " ORDER BY \"Distance\" asc"
                      " LIMIT 1"
                      )
        avg_patients = session.query(func.avg(GpSurgery.tot_patients).label('avg_patients')).scalar()

        # Query for Stations near postcode
        stations_sql = ("SELECT "
                        "   ls.station_name,"
                        "   ls.postcode,"
                        "   ls.lat,"
                        "   ls.lng,"
                        "   ls.zones,"
                        "   ST_DISTANCE_SPHERE(st_point(:x, :y),st_point(ls.lng, ls.lat)) AS \"Distance\""
                        " FROM lon_stations ls"
                        " ORDER BY \"Distance\" asc"
                        " LIMIT 1"
                        )

        # Query Property prices
        property_sql = (" SELECT"
                        "    mapp.year AS year"
                        "   ,mapp.annual_avg AS total_avg"
                        "   ,A.avg_price AS postcode_avg"
                        "   ,maop.annual_avg AS outcode_avg"
                        "   FROM mv_annual_property_price_avg mapp"
                        " LEFT OUTER"
                        "   JOIN mv_annual_outcode_property_price maop"
                        "     ON maop.year = mapp.year"
                        " LEFT OUTER"
                        "   JOIN ("
                        "          SELECT"
                        "             CAST(extract(year FROM date_sold) AS INTEGER) AS year"
                        "            ,AVG(price) AS avg_price"
                        "            FROM property_price p"
                        "            WHERE p.postcode = :postcode"
                        "            GROUP BY year"
                        "        ) A"
                        "     ON A.year = mapp.year"
                        "   WHERE maop.outcode = :outcode"
                        " ORDER BY mapp.year DESC"
                        " LIMIT 10"
                        )

        # Query for local dentists
        dental_sql = (" SELECT  "
                      "  name,  "
                      "  addr2,  "
                      "  postcode, "
                      "  lat, "
                      "  lng, "
                      "  subtype, "
                      "  ST_DISTANCE_SPHERE(st_point(:x, :y),st_point(dp.lng, dp.lat)) AS \"Distance\" "
                      "  FROM dental_prac dp "
                      "  ORDER BY \"Distance\"  asc "
                      " LIMIT 1 "
                      )

        # Get outcode and do property search
        out_code = core_details.code.split(" ")
        try:
            rp = session.execute(property_sql, {'postcode': core_details.code, 'outcode': out_code[0]})
            property_rp = rp.fetchall()
            property_result = property_rp
        except NoResultFound:
            flash('No property prices found for that search')

        # Query Nursery schools
        try:
            rp = session.execute(school_sql, {'x': core_details.lng, 'y': core_details.lat, 'phase': "Nursery"})
            nursery_rp = rp.fetchall()
            nursery_result = nursery_rp[0]
        except NoResultFound:
            flash('No school records found for that search')
        # Query primary schools
        try:
            prp = session.execute(school_sql, {'x': core_details.lng, 'y': core_details.lat, 'phase': "Primary"})
            primary_rp = prp.fetchall()
            primary_result = primary_rp[0]
        except NoResultFound:
            flash('No school records found for that search')
        # Query secondary schools
        try:
            srp = session.execute(school_sql, {'x': core_details.lng, 'y': core_details.lat, 'phase': "Secondary"})
            secondary_rp = srp.fetchall()
            secondary_result = secondary_rp[0]
        except NoResultFound:
            flash('No school records found for that search')
        # GP Surgeries
        try:
            gprp = session.execute(gp_sql, {'x': core_details.lng, 'y': core_details.lat})
            gp_rp = gprp.fetchall()
            gp_result = gp_rp[0]
        except NoResultFound:
            flash('No surgeries found for that search')

        # Transport
        try:
            trp = session.execute(stations_sql, {'x': core_details.lng, 'y': core_details.lat})
            t_rp = trp.fetchall()
            t_result = t_rp[0]
        except NoResultFound:
            flash('No station records found for that search')

        # Dentists
        try:
            dentalrp = session.execute(dental_sql, {'x': core_details.lng, 'y': core_details.lat})
            dental_rp = dentalrp.fetchall()
            dental_result = dental_rp[0]
        except NoResultFound:
            flash('No dentists found for that search')

        # Air pollution
        air_qual_url = "http://api.erg.kcl.ac.uk/AirQuality/Data/Nowcast/lat={0}/lon={1}/JSon".format(core_details.lat, core_details.lng)

        try:
            uResponse = requests.get(air_qual_url)
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        pollutiondata = json.loads(Jresponse)

        # Return results
        return render_template('myhood.html', core_dets=core_details, pop=population, avgpop=avg_pop, crimedata=crime_data, nurserydata=nursery_result, primarydata=primary_result, secondarydata=secondary_result, gpdata=gp_result, avgpatients=avg_patients, transport=t_result, pollution=pollutiondata, propertydata=property_result, deprivation=deprivation, dentist=dental_result, poverty=poverty)
        # air quality data


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
