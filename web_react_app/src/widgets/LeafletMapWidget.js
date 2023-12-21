import 'leaflet/dist/leaflet.css';
import * as L from 'leaflet';

export class MapWidget {
  constructor(domNode) {
    this.points = ''
    this.map = L.map(domNode, {
      zoomControl: true,
      doubleClickZoom: true,
      boxZoom: false,
      keyboard: false,
      scrollWheelZoom: true,
      zoomAnimation: true,
      touchZoom: false,
      zoomSnap: 0.1
    });
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(this.map);
    this.map.setView([0, 0], 0);

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
          }
        }
    
    this.drawControl = new L.Draw.Polygon(this.map, drawPluginOptions);
    //this.map.addControl(drawControl);
    console.log(this)



    }
  setZoom(level) {
    this.map.setZoom(level);
  }
  stopDraw(){
    this.drawControl.disable();
  }
  startDraw(){
    return new Promise((resolve, reject) => {
        var drawnItems = new L.FeatureGroup();
        this.map.addLayer(drawnItems);

        this.drawControl.enable();
    
        this.map.on('draw:created', (e) => {
            var type = e.layerType,
                layer = e.layer;
    
            if (type === 'polygon') {
                //console.log("layer", layer);
                drawnItems.addLayer(layer);
            }
        });
        
        this.map.on('draw:drawstop', () => {
            let points;
            try {
                points = String(drawnItems.toGeoJSON().features[0].geometry.coordinates[0]);
                console.log(points);
                this.stopDraw();
                resolve(points); // Resolve the promise with the points
            } catch (error) {
                reject(error); // Reject the promise in case of an error
            }
        });
    
        this.map.on('draw:drawstart', (e) => {
            drawnItems.clearLayers();
        });
    });
}


    disableInteraction(){
        this.map.dragging.disable();
        this.map.touchZoom.disable();
        this.map.doubleClickZoom.disable();
        this.map.scrollWheelZoom.disable();
        this.map.boxZoom.disable();
        this.map.keyboard.disable();
        if (this.map.tap) this.map.tap.disable();
        // document.getElementsByClassName('map').style.cursor='default';
        this.map.zoomControl.remove();
          


    }
}