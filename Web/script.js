function disableMapInteraction(m){
  m.dragging.disable();
  m.touchZoom.disable();
  m.doubleClickZoom.disable();
  m.scrollWheelZoom.disable();
  m.boxZoom.disable();
  m.keyboard.disable();
  if (m.tap) m.tap.disable();
 // document.getElementsByClassName('map').style.cursor='default';
  m.removeControl(drawControl)
  m.zoomControl.remove();

}


function getGoogleSatelliteTiles(){
  var googleSateliteBasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains:['mt0','mt1','mt2','mt3']
})

return googleSateliteBasemap
}

function getOSMTiles(){
  var osmTiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})



return osmTiles
}




var map = L.map('IndMap').setView([51.505, -0.09], 13);

var settingsMap = L.map('settingsMap').setView([51.505, -0.09], 13);
var resultsMap = L.map('resultsMap').setView([51.505, -0.09], 13);

var indBase = getGoogleSatelliteTiles().addTo(map)
var settingsBase = getGoogleSatelliteTiles().addTo(settingsMap)
var resultsBase = getGoogleSatelliteTiles().addTo(resultsMap)


//map.addLayer(googleSateliteBasemap)
var drawnItems = new L.FeatureGroup();
var drawnItemsSettings = new L.FeatureGroup();
var drawnItemsResults = new L.FeatureGroup();

map.addLayer(drawnItems);
settingsMap.addLayer(drawnItemsSettings);
resultsMap.addLayer(drawnItemsResults);


var PolygonString = ''

var drawPluginOptions = {
    draw: {
      polygon: {
        allowIntersection: false, // Restricts shapes to simple polygons
        drawError: {
          color: '#e1e100', // Color the shape will turn when intersects
          message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
        },
        shapeOptions: {
          color: '#97009c'
        }
      },
      // disable toolbar item by setting it to false
      polyline: false,
      circle: false, // Turns off this drawing tool
      rectangle: false,
      marker: false,
      circlemarker: false
      },
  };
  

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);


map.on('draw:created', function (e) {
    var type = e.layerType,
        layer = e.layer;

    if (type === 'polygon') {
        layer.options.maxZoom = map.getZoom();
        layer.options.minZoom = map.getZoom();
        drawnItems.addLayer(layer);
        drawnItemsSettings.addLayer($.extend( true, {}, layer ));
        drawnItemsResults.addLayer($.extend( true, {}, layer ));
        //settingsMap.fitBounds(e.getBounds())
        //resultsMap.fitBounds(layer.getBounds())
    }
});

map.on('draw:drawstop' , function() {
    var points = String(drawnItems.toGeoJSON().features[0].geometry.coordinates[0]) ;
    console.log(points);
    PolygonString = points;
    document.getElementById("indexNext").style.visibility = 'visible'

}

)
  


map.on('draw:drawstart ', function (e) {
    drawnItems.clearLayers();
    drawnItemsSettings.clearLayers();
    drawnItemsResults.clearLayers();
    PolygonString = '';
    document.getElementById("indexNext").style.visibility = 'hidden'
})




function makeApiQuery() {
    // Get references to the form inputs
    const startDateInput = document.querySelector('#start-date');
    const endDateInput = document.querySelector('#end-date');
    const imageryTypeInput = document.querySelector( 'input[name="imagery-type"]:checked')
    const aggregationLengthInput = document.querySelector( 'input[name="aggregation-length"]:checked')
    const aggregationTypeInput = document.querySelector( 'input[name="aggregation-type"]:checked')
    
    // Get the values of the form inputs
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    const imageryType = imageryTypeInput.value;
    const aggregationLength = aggregationLengthInput.value;
    const aggregationType = aggregationTypeInput.value;
    
    // Format the input values as a string for the API query
    const apiQueryString = `start-date=${startDate}&end-date=${endDate}&imagery-type=${imageryType}&aggregation-length=${aggregationLength}&aggregation-type=${aggregationType}`;
    console.log(apiQueryString)
    /// Make query
    // Go to loading screen
    // Wait for results
    // Add results to html and show


}

document.getElementById('draw-polygon-btn').addEventListener('click', function() {
  polylineDrawHandler = new L.Draw.Polygon(map, drawControl.options.polygon);
  polylineDrawHandler.enable();
});


//document.getElementById("query-button").addEventListener("click",makeApiQuery)

