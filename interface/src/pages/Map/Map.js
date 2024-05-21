import React, { useState, useEffect } from 'react';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';
import './Map.scss';

const API_KEY = "AIzaSyA7HVl51-Q-QWMotQfWU87ZEdCADSkpGU0";
const containerStyle = {
  width: '100%',
  height: '800px',
  overflow: 'hidden',
};

const center = {
  lat: 0,
  lng: 0
};

function Map() {
  const [markers, setMarkers] = useState([]);
  const [selectedMarker, setSelectedMarker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedDomain, setSelectedDomain] = useState('');
  const [mapZoom, setMapZoom] = useState(5); 

  useEffect(() => {
    fetch('http://localhost:5000/api/geocode')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched data:', data);
        const newMarkers = data.map((item, index) => {
          const location = item.geocode_data.results[0]?.geometry.location;
          if (location) {
            return { id: index, lat: location.lat, lng: location.lng, address: item.address, domain: item.domain };
          } else {
            console.warn('Invalid location data:', item);
            return null;
          }
        }).filter(marker => marker !== null);
        setMarkers(newMarkers);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching geocode data:', error);
        setLoading(false);
      });
  }, []);

  const handleDomainChange = (event) => {
    const selectedDomain = event.target.value;
    setSelectedDomain(selectedDomain);

    const markerForDomain = markers.find(marker => marker.domain === selectedDomain);
    if (markerForDomain) {
      setSelectedMarker(markerForDomain);
      setMapZoom(10); 
    }
  };

  return (
    <LoadScript googleMapsApiKey={API_KEY}>
      <div style={{ filter: loading ? 'grayscale(100%)' : 'none', overflow: 'auto' }}>
        <div className = "dropdownContainer">
  
          <select id="domain-select" className='dropdown' onChange={handleDomainChange} value={selectedDomain}>
            <option value="">Select a domain</option>
            {markers.map(marker => (
              <option key={marker.id} value={marker.domain}>{marker.domain}</option>
            ))}
          </select>
        </div>
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={markers.length > 0 ? markers[0] : center}
          zoom={mapZoom} // Utilizează starea mapZoom pentru a seta nivelul de zoom al hărții
        >
          {loading && (
            <div class="loading loading01">
              <span>L</span>
              <span>O</span>
              <span>A</span>
              <span>D</span>
              <span>I</span>
              <span>N</span>
              <span>G</span>
            </div>
          )}

          {markers.map((marker) => (
            <Marker
              key={marker.id}
              position={{ lat: marker.lat, lng: marker.lng }}
              onClick={() => setSelectedMarker(marker)}
              icon={
                loading
                  ? {
                    url: 'https://maps.google.com/mapfiles/ms/icons/grey-dot.png',
                    scaledSize: new window.google.maps.Size(20, 20),
                  }
                  : null
              }
            />
          ))}

          {selectedMarker && (
            <InfoWindow
              position={{ lat: selectedMarker.lat, lng: selectedMarker.lng }}
              onCloseClick={() => setSelectedMarker(null)}
            >
              <div>
                <h2>Location Details</h2>
                <p>Address: {selectedMarker.address}</p>
                <a href={selectedMarker.domain}>Check Out Their Website</a>
              </div>
            </InfoWindow>
          )}
        </GoogleMap>
      </div>
    </LoadScript>
  );
}

export default Map;
