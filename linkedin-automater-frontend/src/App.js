import Tool from './components/tool.jsx';
import Login from './components/login.jsx';
import Confirm from './components/confirm.jsx';
import NotFound from './components/error.jsx';
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
