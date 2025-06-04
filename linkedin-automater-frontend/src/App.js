import Tool from './pages/tool.jsx';
import Login from './pages/login.jsx';
import Confirm from './pages/confirm.jsx';
import NotFound from './pages/error.jsx';
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
