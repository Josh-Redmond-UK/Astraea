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




var map = L.map('IndMap').setView([23.6345, -102.5528], 5);

var settingsMap = L.map('settingsMap').setView([23.6345, -102.5528], 5);
var resultsMap = L.map('resultsMap').setView([23.6345, -102.5528], 5);

var indBase = getGoogleSatelliteTiles().addTo(map)
var settingsBase = getGoogleSatelliteTiles().addTo(settingsMap)
var resultsBase = getGoogleSatelliteTiles().addTo(resultsMap)


//map.addLayer(googleSateliteBasemap)
var drawnItems = new L.FeatureGroup();
var drawnItemsSettings = new L.FeatureGroup();
var drawnItemsResults = new L.FeatureGroup();

map.addLayer(drawnItems);
settingsMap.addLayer(drawnItemsSettings);
//resultsMap.addLayer(drawnItemsResults);


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


var searchButton = document.getElementById('search-button');

// Attach an event listener to the search button
searchButton.addEventListener('click', function() {
  var searchInput = document.getElementById('search-input').value;
  searchLocation(searchInput);
});

// Function to search for a location
async function searchLocation(query) {

  var apiResponse = await fetch(`https://geocode.maps.co/search?q=${query}`);
  var data = await apiResponse.json()
  console.log(data)

  resultLat = data[0]['lat']
  resultLon = data[0]['lon']
  console.log(resultLat)
  console.log(resultLon)

  map.setView([resultLat, resultLon], 8)

}

function createImageCarousel(imageUrls) {
  var carouselContainer = document.createElement('div');
  carouselContainer.id = 'carouselExampleIndicators';
  carouselContainer.className = 'carousel slide';
  carouselContainer.setAttribute('data-ride', 'carousel');

  var indicatorsList = document.createElement('ol');
  indicatorsList.className = 'carousel-indicators';

  var carouselInner = document.createElement('div');
  carouselInner.className = 'carousel-inner';

  var prevControl = document.createElement('a');
  prevControl.className = 'carousel-control-prev';
  prevControl.href = '#carouselExampleIndicators';
  prevControl.role = 'button';
  prevControl.setAttribute('data-slide', 'prev');

  var prevIcon = document.createElement('span');
  prevIcon.className = 'carousel-control-prev-icon';
  prevIcon.setAttribute('aria-hidden', 'true');

  var prevText = document.createElement('span');
  prevText.className = 'sr-only';
  prevText.textContent = 'Previous';

  prevControl.appendChild(prevIcon);
  prevControl.appendChild(prevText);

  var nextControl = document.createElement('a');
  nextControl.className = 'carousel-control-next';
  nextControl.href = '#carouselExampleIndicators';
  nextControl.role = 'button';
  nextControl.setAttribute('data-slide', 'next');

  var nextIcon = document.createElement('span');
  nextIcon.className = 'carousel-control-next-icon';
  nextIcon.setAttribute('aria-hidden', 'true');

  var nextText = document.createElement('span');
  nextText.className = 'sr-only';
  nextText.textContent = 'Next';

  nextControl.appendChild(nextIcon);
  nextControl.appendChild(nextText);

  for (var i = 0; i < imageUrls.length; i++) {
    var indicatorItem = document.createElement('li');
    indicatorItem.setAttribute('data-target', '#carouselExampleIndicators');
    indicatorItem.setAttribute('data-slide-to', i.toString());
    if (i === 0) {
      indicatorItem.className = 'active';
    }

    var carouselItem = document.createElement('div');
    carouselItem.className = 'carousel-item';
    if (i === 0) {
      carouselItem.classList.add('active');
    }

    var image = document.createElement('img');
    image.className = 'd-block w-100';
    image.src = imageUrls[i];
    image.alt = 'Slide ' + (i + 1).toString();

    carouselItem.appendChild(image);
    carouselInner.appendChild(carouselItem);
    indicatorsList.appendChild(indicatorItem);
  }

  carouselContainer.appendChild(indicatorsList);
  carouselContainer.appendChild(carouselInner);
  carouselContainer.appendChild(prevControl);
  carouselContainer.appendChild(nextControl);

  return carouselContainer.outerHTML;
}





async function makeApiQuery() {
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

    //var londonBounds = L.latLngBounds(L.latLng(51.507222, -0.127758), L.latLng(51.515419, -0.109863));
  
  
    
    // Format the input values as a string for the API query
    const apiQueryString = `http://127.0.0.1:5000/api/mapping?coords=${PolygonString}&start-date=${startDate}&end-date=${endDate}&imagery-type=${imageryType}&aggregation-length=${aggregationLength}&aggregation-type=${aggregationType}`;
    console.log(apiQueryString)
    /// Make query
    var response = await fetch(apiQueryString);

    if (response.ok) {


    var data = await response.json();



    console.log(response);
    console.log(data);
    var gifUrl = data.gifUrl;
    var zipUrl = data.zipUrl;
    var dates = data.dates
    var jgpUrls = data.jpgUrls

    // Get the latitude and longitude of the GIF from the response data
    const n =  data.n;
    const e = data.e;
    const s = data.s;
    const w = data.w;

    var latLngBounds = drawnItemsResults.getBounds()// L.latLngBounds(L.latLng(s, w), L.latLng(n, e))
    // Create an image overlay with the URL of the image and the bounds of the spatial extent
    var imageOverlay = L.imageOverlay(gifUrl, latLngBounds);
  
    // Add the image overlay to the resultsMap
    imageOverlay.addTo(resultsMap);

    var downloadButton = document.getElementById('downloadZipButton')
    var gifButton = document.getElementById('downloadGifButton')

    const onclicktext = 'window.location.href${test}';
    console.log(zipUrl)
    downloadButton.onclick = function() {
      window.open(zipUrl);
    };
    gifButton.onclick = function() {
      window.open(gifUrl);
    };
    //var carouselHTML = createImageCarousel(jpegUrls);

    // Append the generated HTML to an element in your page
    //var carouselContainer = document.getElementById('carouselContainer');
    //carouselContainer.innerHTML = carouselHTML;


    showPage('results')
    }
    else{
      const loaderText = document.querySelector('.loader-text');
      loaderText.textContent = 'Error, por favor intentalo de nuevo';
      setTimeout(location.reload(), 2000);



    }


    // Go to loading screen
    // Wait for results
    // Add results to html and show


}

document.getElementById('query-button').addEventListener('click', makeApiQuery)

document.getElementById('draw-polygon-btn').addEventListener('click', function() {
  polylineDrawHandler = new L.Draw.Polygon(map, drawControl.options.polygon);
  polylineDrawHandler.enable();
});

document.getElementById('indexNext').addEventListener('click', function() {
  bounds = map.getCenter()
  zoom = map.getZoom()


  settingsMap.setView(bounds, zoom)
  resultsMap.setView(bounds, zoom)

})

function showPage(pageId) {
  $('.page').removeClass('active');
  $('#' + pageId).addClass('active');
  map.invalidateSize();
  settingsMap.invalidateSize();
  resultsMap.invalidateSize();
  disableMapInteraction(settingsMap)
  disableMapInteraction(resultsMap)

  }
//document.getElementById("query-button").addEventListener("click",makeApiQuery)

