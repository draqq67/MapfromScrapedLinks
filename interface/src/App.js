import {React} from 'react';
import {
  createBrowserRouter,
  RouterProvider,BrowserRouter
} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';

import Home from './pages/Home/Home';
import Map from './pages/Map/Map';
import Statistics from './pages/Statistics/Statistics';

import PageNavbar from "./Components/Navbar"
import Footer from "./Components/Footer"

function App() {

  const router = createBrowserRouter([
      {
      path : "/",
      element : <Home />,
      loader: async () => { return null; },
      },
      {
        path : "/map",
        element : <Map />,
        loader: async () => { return null; },
      },
      {
        path : "/statistics",
        element : <Statistics />,
        loader: async () => { return null; },
        },
      {
      
      },
    
  ])
  return (
    
    <> 
      <PageNavbar />
      <RouterProvider router={router} />
      <Footer />
    </>

  );
}

export default App;