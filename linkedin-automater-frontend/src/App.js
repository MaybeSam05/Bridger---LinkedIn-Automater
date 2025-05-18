import Tool from './pages/tool';
import Login from './pages/login';
import Confirm from './pages/confirm';
import NotFound from './pages/error';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { StrictMode } from 'react';

const router = createBrowserRouter([
  {path: "/", element: <Login />},
  {path: "/tool", element: <Tool />},
  {path: "/confirm", element: <Confirm />},
  {path: "*", element: <NotFound />}, 
]);

function App() {
  return (
    <StrictMode>
    <RouterProvider router={router} />
    </StrictMode>
  );
}

export default App;
