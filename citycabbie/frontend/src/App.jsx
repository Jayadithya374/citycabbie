// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NewBooking from './components/NewBooking';
import { useState, useEffect } from 'react';

function LoadingScreen() {
  return (
    <div
    style={{
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      justifyContent: 'center',
    }}
    >
      <h2>Loading...</h2>
      {/* You can add a spinner or any other loading animation here */}
    </div>
  );
}

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate a loading delay of 5 seconds
    const timer = setTimeout(() => {
      setLoading(false); // Hide loading screen after 5 seconds
    }, 3000);

    // Clear the timer if the component unmounts or if the loading state changes
    return () => clearTimeout(timer);
  }, []);

  return (
    <div
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}
    >
      {loading ? <LoadingScreen /> : (
        /* Your main content goes here */
        <>
        <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<NewBooking />} />
            {/* Add other routes here */}
          </Routes>
        </div>
        </Router>
        </>
      )}
    </div>
  );
}


// import ViewBookings from './components/ViewBookings';
// import EditBooking from './components/EditBooking';

export const BACKEND_URL = 'http://localhost:8000/';

// function App() {
//   return (
//     <Router>
//       <div className="App">
//         <Routes>
//           <Route path="/" element={<NewBooking />} />
//           {/* Add other routes here */}
//         </Routes>
//       </div>
//     </Router>
//   );
// }

export default App;
