import Home from './pages/Home.jsx'
import Scores from './pages/Scores.jsx'
import Add from './pages/Add.jsx'
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
// import './index.css'

function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route
        path="/"
      >
        <Route index element={<Home />} />
        <Route path='Scores' element={<Scores />} />
        <Route path='Add' element={<Add />} />
      </Route>,
    ),
  );

  return (
    <>
      <RouterProvider router={router} />
    </> 
  );
}

export default App
