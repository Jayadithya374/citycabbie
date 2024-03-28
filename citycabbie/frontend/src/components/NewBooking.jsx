// NewBooking.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {BACKEND_URL} from '../App';
import '../index.css';

function NewBooking() {
  const [cities, setCities] = useState([]);
  const [selectedSource, setSelectedSource] = useState('');
  const [selectedDestination, setSelectedDestination] = useState('');
  const [duration, setDuration] = useState('');
  const [cabs, setCabs] = useState([]);
  const [selectedCab, setSelectedCab] = useState('');
  const [fare, setFare] = useState('');
  const [availability, setAvailability] = useState(false);
  const [reason, setReason] = useState(''); 
  const [pickUpTime, setPickUpTime] = useState('');
  const [email, setEmail] = useState('');
  const [possible, setPossible] = useState(false);
  const [itinerary, setitinerary] = useState([]);

  useEffect(() => {
    // Fetch cities
    axios.get(BACKEND_URL + 'cities')
      .then(response => {
        setCities(response.data);
      })
      .catch(error => {
        console.error('Error fetching cities:', error);
      });
  }, []);

  const fetchDuration = () => {
    setDuration('Calculating...');
    setPossible(false);
    if (!selectedSource || !selectedDestination || selectedSource === selectedDestination || selectedSource == '' || selectedDestination == '') {
      setDuration('Invalid!');
      return;
    }
    // Fetch duration based on source and destination
    axios.get(BACKEND_URL + `duration?src=${selectedSource}&dest=${selectedDestination}`)
      .then(response => {
        if (response.data.status == 'error') {
            // alert(response.data.error);
            setPossible(false);
            setDuration('');
            return;
        }
        setPossible(true);
        setDuration(response.data.duration);
        setitinerary(response.data.path);
      })
      .catch(error => {
        console.error('Error fetching duration:', error);
        alert(error);
      });
  };

  useEffect(() => {
    fetchDuration();
  }, [selectedSource, selectedDestination]);
  useEffect(() => {
    checkAvailability();
  }, [selectedCab, pickUpTime]);

  const handleSourceChange = (event) => {
    setSelectedSource(event.target.value);
    // Calculate duration based on source and destination (you'll need to implement this logic)
  };

  const handleDestinationChange = (event) => {
    setSelectedDestination(event.target.value);
    // Calculate duration based on source and destination (you'll need to implement this logic)
    // fetchDuration();
  };

  const handleCabChange = (event) => {
    setSelectedCab(event.target.value);
    checkAvailability();
  };

  const handlePickUpTimeChange = (event) => {
    setPickUpTime(event.target.value);
    checkAvailability();
    // Check availability based on pick up time (you'll need to implement this logic)
  };

  const [loading, setLoading] = useState(true); // Add loading state

  useEffect(() => {
    axios.get(BACKEND_URL + 'cities')
      .then(response => {
        console.log('Fetched cities:', response.data.cities);
        setCities(response.data.cities);
        setLoading(false); // Set loading to false after fetching cities
      })
      .catch(error => {
        console.error('Error fetching cities:', error);
        setCities([]); // Set cities to an empty array in case of error
        // setLoading(false); // Set loading to false in case of error
      });
  }, []);

  const checkAvailability = () => {
    if (!selectedSource || !selectedDestination || selectedSource === selectedDestination || selectedSource == '' || selectedDestination == '' ) {
      setDuration('Invalid!');
      return;
    }
    if (!pickUpTime || selectedCab == '') {
      setAvailability(false);
      return;
    }
    // Check availability based on pick up time, source, destination, and selected cab
    axios.get(BACKEND_URL + `availability?cab=${cabs[selectedCab].name}&duration=${duration}&pickup_time=${pickUpTime}&src=${selectedSource}&dest=${selectedDestination}`)
      .then(response => {
        setAvailability(true);
        // console.log(cabs);
        // console.log(event.target.key);
        setFare(duration*cabs[selectedCab].price_per_minute);
      })
      .catch(error => {
        console.error('Error fetching fare:', error);
        if (response.data.status == 'error') {
          // alert(response.data.error);
          setAvailability(false);
          setReason(response.data.error);
          return;
        }
        alert(error);
      });
  };


  const [loadingCabs, setLoadingCabs] = useState(true); // Add loading state for cabs

  useEffect(() => {
    axios.get(BACKEND_URL + 'cabs')
      .then(response => {
        console.log('Fetched cabs:', response.data.cabs);
        setCabs(response.data.cabs);
        setLoadingCabs(false); // Set loading to false after fetching cabs
      })
      .catch(error => {
        console.error('Error fetching cabs:', error);
        setCabs([]); // Set cabs to an empty array in case of error
        // setLoadingCabs(false); // Set loading to false in case of error
      });
  }, []);

  

  const handleBook = () => {
    console.log("dsafjnnjd")
    // Perform booking by sending data to the backend
    if (!selectedSource || !selectedDestination || selectedSource === selectedDestination || selectedSource == '' || selectedDestination == '' ) {
      setDuration('Invalid!');
      return;
    }
    if (!pickUpTime || selectedCab == '' || !possible || !availability || email == '') {
      return;
    }
    // Calculate fare based on selected cab (you'll need to implement this logic)
    axios.get(BACKEND_URL + `book?cab=${cabs[selectedCab].name}&duration=${duration}&pickup_time=${pickUpTime}&src=${selectedSource}&dest=${selectedDestination}&email=${email}`)
      .then(response => {
        // setAvailability(true);
        alert(response.data.status);
        // console.log(cabs);
        // console.log(event.target.key);
        // setFare(duration*cabs[event.target.value].price_per_minute);
      })
      .catch(error => {
        console.error('Error booking:', error);
        if (response.data.status == 'error') {
          // alert(response.data.error);
          // setAvailability(false);
          setReason(response.data.error);
          return;
        } 
        alert(error);
      });
    
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}>
      <h1>New Booking</h1>
      <div>
      <select value={selectedSource} onChange={handleSourceChange}>
      {loading ? (
          <option>Loading...</option> // Show loading option while fetching cities
        ) : (
          <>
          <option id="src" value="">Select Source</option>
          {Array.isArray(cities) && cities.map((city, index) => (
            <option key={index} value={city}>{city}</option>
          ))}
          </>
        )}
      </select>
      <select value={selectedDestination} onChange={handleDestinationChange}>
        {loading ? (
          <option>Loading...</option> // Show loading option while fetching cities
        ) : (
          <>
          <option value="">Select Destination</option>
          
          {Array.isArray(cities) && cities.map((city, index) => (
            <option key={index} value={city}>{city}</option>
          ))}
          </>
        )}
      </select>
      </div>
      <h2>Estimated time: {duration} </h2>
      { possible?
        (<>
        <h2 style={{marginTop: "0"}}>itinerary: {itinerary.join(' -> ')} </h2>
        </>):<>
        </>
      }
      {possible && !loadingCabs?<>
      <label for="dt">Pickup Time:</label>
      <input id="dt" type="datetime-local" value={pickUpTime} onChange={handlePickUpTimeChange} />
      <br/>
      <select value={selectedCab} onChange={handleCabChange}>
        <option value="">Select Cab</option>
        {Array.isArray(cabs) && cabs.map((cab, index) => (
            <option key={index} value={index}>{cab.name}</option>
            ))}
      </select>
      <br/>
      
      {availability?<><h2>Fare: {fare}</h2></>:<h2>Unavailibility Reason: {reason}</h2>}
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Enter your email" />


      </>:<></>}
      {/* Other input fields for duration, cab selection, pick up time, email */}
      <br/>
      <button onClick={handleBook}>Book</button>
    </div>
  );
}

export default NewBooking;
