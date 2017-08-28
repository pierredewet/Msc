function drawmaps() {
trainMap();
dentistMap();
gpMap();
initMap();
}

function trainMap() {
var start = new google.maps.LatLng({{ core_dets.lat }},{{ core_dets.lng }});
var end = new google.maps.LatLng({{ transport.lat }},{{ transport.lng }});
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  var map = new google.maps.Map(document.getElementById('rail-directions'), {
    zoom: 10,
    center: {lat: {{ core_dets.lat }}, lng: {{ core_dets.lng }}}
  });

  var latlngbounds = new google.maps.LatLngBounds();
  latlngbounds.extend(start);
  latlngbounds.extend(end);
  map.fitBounds(latlngbounds);

  directionsDisplay.setMap(map);

  calculateAndDisplayRoute(directionsService, directionsDisplay, start, end);
}

function dentistMap() {
var start = new google.maps.LatLng({{ core_dets.lat }},{{ core_dets.lng }});
var end = new google.maps.LatLng({{ dentist.lat }},{{ dentist.lng }});
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  var map = new google.maps.Map(document.getElementById('dentist-directions'), {
    zoom: 10,
    center: {lat: {{ core_dets.lat }}, lng: {{ core_dets.lng }}}
  });

  var latlngbounds = new google.maps.LatLngBounds();
  latlngbounds.extend(start);
  latlngbounds.extend(end);
  map.fitBounds(latlngbounds);

  directionsDisplay.setMap(map);

  calculateAndDisplayRoute(directionsService, directionsDisplay, start, end);
}


function gpMap() {
var start = new google.maps.LatLng({{ core_dets.lat }},{{ core_dets.lng }});
var end = new google.maps.LatLng({{ gpdata.lat }},{{ gpdata.lng }});
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  var map = new google.maps.Map(document.getElementById('gp-directions'), {
    zoom: 10,
    center: {lat: {{ core_dets.lat }}, lng: {{ core_dets.lng }}}
  });

  var latlngbounds = new google.maps.LatLngBounds();
  latlngbounds.extend(start);
  latlngbounds.extend(end);
  map.fitBounds(latlngbounds);

  directionsDisplay.setMap(map);

  calculateAndDisplayRoute(directionsService, directionsDisplay, start, end);
}

function calculateAndDisplayRoute(directionsService, directionsDisplay, start, end) {
  directionsService.route({
    origin: start,
    destination: end,
    travelMode: 'WALKING'
  }, function(response, status) {
    if (status === 'OK') {
      directionsDisplay.setDirections(response);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}


function initMap() {
  var pcode = {lat: {{ core_dets.lat }}, lng: {{ core_dets.lng }}};
  var map = new google.maps.Map(document.getElementById('pcode-map'), {
    zoom: 14,
    center: pcode,
    disableDefaultUI: true,
    gestureHandling: 'none',
    scrollwheel: false,
    disableDoubleClickZoom: true,
    zoomControl: false
  });
  var marker = new google.maps.Marker({
    position: pcode,
    animation: google.maps.Animation.DROP,
    map: map,
    title: {{ core_dets.lat }}
  });

// map legend etc
  var iconBase = '../static/images/';
        var icons = {
          gp: {
            name: 'GP',
            icon: iconBase + 'medicine.png'
          },
          school: {
            name: 'Schools',
            icon: iconBase + 'university.png'
          },
          transport: {
            name: 'Transport',
            icon: iconBase + 'train.png'
          }
        };

  var features = [
    {
      position: new google.maps.LatLng({{ nurserydata.lat }}, {{ nurserydata.lng }}),
      type: 'school'
    }, {
      position: new google.maps.LatLng({{ secondarydata.lat }}, {{ secondarydata.lng }}),
      type: 'school'
    }, {
      position: new google.maps.LatLng({{ primarydata.lat }}, {{ primarydata.lng }}),
      type: 'school'
    }, {
      position: new google.maps.LatLng({{ gpdata.lat }}, {{ gpdata.lng }}),
      type: 'gp'
    }, {
      position: new google.maps.LatLng({{ transport.lat }}, {{ transport.lng }}),
      type: 'transport'
    }
  ];

  // Create markers.
  var poi = [
  [{{ nurserydata.establishment_name }}],
  [{{ primarydata.establishment_name }}],
  [{{ secondarydata.establishment_name }}],
  [{{ gpdata.name }}]
  [{{ transport.station_name }}]
];
  features.forEach(function(feature) {
    var marker = new google.maps.Marker({
      position: feature.position,
      icon: icons[feature.type].icon,
      map: map,
      html: poi[4]
    });
  });

  infowindow = new google.maps.InfoWindow({
                content: "loading..."
            });

  google.maps.event.addListener(marker, "click", function () {
                alert(this.html);
                infowindow.setContent(this.html);
                infowindow.open(map, this);
            });

  var legend = document.getElementById('map-legend');
  for (var key in icons) {
    var type = icons[key];
    var name = type.name;
    var icon = type.icon;
    var div = document.createElement('div');
    div.innerHTML = '<img src="' + icon + '"> ' + name;
    legend.appendChild(div);
  }
  document.body.appendChild(legend);

  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(legend);

// end map legend
}


// CHARTS
var ring_data1 = {{pop.working_pop}};
var ring_data2 = {{pop.tot_pop}};
var ringctx = document.getElementById("ringChart");
var donutChart = new Chart(ringctx, {
  type: 'doughnut',
  data: {
    labels: ["Working population", "Total population"],
    datasets: [{
      backgroundColor: [
        "#0000CD",
        "#DCDCDC"
      ],
      borderColor: [
        "#000080",
        "#CBCBCB"
      ],
      data: [ring_data1,ring_data2],
      borderWidth: [1, 1]
    }]
  },
  options: {
    cutoutPercentage: [70],
    // rotation: [60],
    // circumference: [ring_data]
  }
});

var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Children", "Adults", "Older people"],
    datasets: [{
      backgroundColor: [
        "#2ecc71",
        "#3498db",
        "#95a5a6"
      ],
      data: [{{ pop.children_0_15 }}, {{ pop.gen_pop_16_59 }}, {{ pop.old_pop_60_plus }}]
    }]
  }
});

var bar_ctx = document.getElementById("CrimeChart").getContext('2d');
var BarChart = new Chart(bar_ctx, {
  type: 'bar',
  data: {
    labels: ["Theft", "ASBO", "Serious crime"],
    datasets: [
    {
      label: 'Local',
      data: [{{ crimedata.theft_tot }}, {{ crimedata.asb_tot }}, {{ crimedata.serious_tot }}],
      backgroundColor: 'rgba(0, 204, 0, 0.2)',
      borderColor: 'rgba(0, 204, 0,1)',
      borderWidth: 1
    },
    {
      label: 'Surrounding area',
      // data: [{{ crimedata.theft_average }}, {{ crimedata.asb_average }}, {{ crimedata.serious_crime_average }}],
      data: [{{ crimedata.theft_average }}, {{ crimedata.asb_average }}, {{ crimedata.serious_crime_average }}],
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  },
  options: {
    scales: {
        yAxes: [{
          id:"y-axis-1",
          position:'left',
          type: 'linear',
            ticks: {
              beginAtZero:true
            },
            scaleLabel: {
                display: true,
                labelString: 'Number of incidents'
              }
          }],
        xAxes : [{
          gridLines : {
                display : false
            },
            scaleLabel: {
                display: true,
                labelString: 'Crime by type'
              }
        }]
    }

  }
});

new Chart(document.getElementById("deprivation-radar"), {
    type: 'radar',
    data: {
      labels: ["Income", "Employment", "Education", "Health", "Crime", "Barriers to services", "Environment"],
      datasets: [
        {
          label: "Domains of deprivation",
          fill: true,
          backgroundColor: "rgba(179,181,198,0.2)",
          borderColor: "#8e5ea2",
          // borderColor: "rgba(179,181,198,1)",
          pointBorderColor: "#fff",
          // pointBackgroundColor: "rgba(179,181,198,1)",
          pointBackgroundColor: "rgb(255,102,204)",
          data: [{{ deprivation.income_decile }},{{ deprivation.employment_decile }},{{ deprivation.education_decile }},{{ deprivation.health_decile }},
          {{ deprivation.crime_decile }}, {{ deprivation.barriers_decile }}, {{ deprivation.environment_decile }}]
        }
      ]
    }
});

var p_year = [];
var tot_avg = [];
var pcode_avg = [];
var outcode_avg = [];
      {% for line in propertydata %}
        p_year.push({{ line.year| int }});
        tot_avg.push({{ line.total_avg }});
        pcode_avg.push({{ line.postcode_avg | int}});
        outcode_avg.push({{ line.outcode_avg}});
      {% endfor %}
var line_ctx = document.getElementById("property-price-chart").getContext('2d');
var LineChart = new Chart(line_ctx, {
  type: 'line',
  data: {
    labels: p_year.reverse(),
    datasets: [{
        data: tot_avg.reverse(),
        label: "UK Average",
        borderColor: "#3e95cd",
        fill: false
      }, {
        data: pcode_avg.reverse(),
        label: "Postcode Average",
        borderColor: "#8e5ea2",
        fill: false
      }, {
        data: outcode_avg.reverse(),
        label: "Outcode Average",
        borderColor: "#3cba9f",
        fill: false
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Property price values'
    },
    scales: {
        yAxes: [{
          id:"y-axis-1",
          position:'left',
          type: 'linear',
            ticks: {
              beginAtZero:true
            },
            scaleLabel: {
                display: true,
                labelString: 'Price in £'
              }
          }],
        xAxes : [{
          gridLines : {
                display : false
            },
            scaleLabel: {
                display: true,
                labelString: 'Year'
              }
        }]
    }
  }
});
