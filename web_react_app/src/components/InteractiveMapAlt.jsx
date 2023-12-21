import React, { useEffect } from 'react';
import { MapContainer, TileLayer, useMap , Map, FeatureGroup, Circle} from 'react-leaflet';
import Control from 'react-leaflet-custom-control';
import "leaflet/dist/leaflet.css";
import SearchOptions from './SearchOptions'; // Import your SearchOptions component
import FloatingMenu from './floatingMenu';
import MapDropdownButton from './MapDropdownButton';
import L from 'leaflet'
import 'leaflet-draw/dist/leaflet.draw.css'
import { useLeafletContext } from '@react-leaflet/core'
import { EditControl } from "react-leaflet-draw"



export function GetIntMap() {
  const map = useMap()
  
}


const InteractiveMap = () => {
  return (
    <div className="relative"> {/* Relative positioning for the wrapper */}
        {/* Search Options Button */}


        {/* Map Container */}
        <div className='z-20'>
            <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={true} className='map-container'>
              <GetIntMap/>
              <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
              <Control>
                <div className="-translate-x-full">
                  <FloatingMenu />
                </div>
              </Control>
            </MapContainer>

        </div>
    </div>
  );
};

export default InteractiveMap;
